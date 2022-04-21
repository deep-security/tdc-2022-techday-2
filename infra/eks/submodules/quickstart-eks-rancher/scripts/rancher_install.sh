#!/bin/bash

if [ $# -lt 5 ]; then
    echo "I need a minimum of 5 arguments to proceed. REGION, QSS3BucketName, QSS3KeyPrefix, QSS3BucketRegion, EKSCLUSTERNAME, (optional - domain name)" && exit 1
fi

REGION=$1
QSS3BucketName=$2
QSS3KeyPrefix=$3
QSS3BucketRegion=$4
EKSCLUSTERNAME=$5
[ -z "$6" ] && HostedZone="aws.private" || HostedZone="$6"
RancherURL="rancher.$HostedZone"

KeyPrefix=${QSS3KeyPrefix%?}

#Install jq for easier JSON object parsing
sudo yum -y install jq

#Update kube config to point to the cluster of our choice
aws eks update-kubeconfig --name ${EKSCLUSTERNAME} --region $REGION

#Install kubectl
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.19.0/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
kubectl get svc

# Install helm
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

# Start by creating the mandatory resources for NGINX Ingress in your cluster:
# Parameterize version 0.40.2
if [ $QSS3BucketName == 'aws-quickstart' ]
then
  kubectl apply -f https://$QSS3BucketName-$REGION.s3.$REGION.amazonaws.com/$KeyPrefix/scripts/deploy.yaml
else
  kubectl apply -f https://$QSS3BucketName.s3.$QSS3BucketRegion.amazonaws.com/$KeyPrefix/scripts/deploy.yaml
fi

#Download latest Rancher repository
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
helm fetch rancher-stable/rancher

# Create NameSpace:
kubectl create namespace cattle-system

# The Rancher management server is designed to be secure by default and requires SSL/TLS configuration.
# Defining the Ingress resource (with SSL termination) to route traffic to the services created above
# Example ${RancherURL} is like ranchereksqs.awscloudbuilder.com
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=${RancherURL}/O=${RancherURL}"

#Create the secret in the cluster:
kubectl create secret tls tls-secret --key tls.key --cert tls.crt

sleep 300

helm upgrade --install rancher rancher-stable/rancher --namespace cattle-system --set hostname=$RancherURL --set ingress.tls.source=secret

#Create Route53 Hosted Zone
CALLER_REF=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13 ; echo '')
MYMAC=`curl http://169.254.169.254/latest/meta-data/mac`
VPCID=`curl http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MYMAC/vpc-id`
aws route53 create-hosted-zone --name $HostedZone --caller-reference $CALLER_REF --hosted-zone-config Comment="Rancher Domain,PrivateZone=True" --vpc VPCRegion=$REGION,VPCId=$VPCID

#Extract Hosted Zone ID:
ZONE_ID=`aws route53 list-hosted-zones-by-name |  jq --arg name "${HostedZone}." -r '.HostedZones | .[] | select(.Name=="\($name)") | .Id' | cut -d"/" -f3`

#Create Resource Record Set
NLB=`kubectl get svc -n ingress-nginx -o json | jq -r ".items[0].status.loadBalancer.ingress[0].hostname"`
NLB_NAME=`echo $NLB | cut -d"-" -f1`

#Create Resource Record Set
NLB_HOSTEDZONE=`aws elbv2 describe-load-balancers --region $REGION --names $NLB_NAME | jq -r ".LoadBalancers[0].CanonicalHostedZoneId"`

cat > rancher-record-set.json <<EOF
{
        "Comment": "CREATE/DELETE/UPSERT a record ",
        "Changes": [{
                "Action": "UPSERT",
                "ResourceRecordSet": {
                        "Name": "${RancherURL}.",
            "SetIdentifier": "RancherEKS",
            "Region": "$REGION",
                        "Type": "A",
                        "AliasTarget": {
                                "HostedZoneId": "$NLB_HOSTEDZONE",
                                "DNSName": "dualstack.$NLB",
                                "EvaluateTargetHealth": false
                        }
                }
        }]
}
EOF

aws route53 change-resource-record-sets --region $REGION --hosted-zone-id $ZONE_ID --change-batch file://rancher-record-set.json