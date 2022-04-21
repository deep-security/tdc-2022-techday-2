#!/bin/bash

#Rancher Uninstall Script
REGION="$1"
[ -z "$2" ] && HostedZone="aws.private" || HostedZone="$2"
RancherURL="rancher.$HostedZone"

yum -y install jq

# Delete NameSpace:
helm uninstall rancher --namespace cattle-system
kubectl delete namespaces cattle-system

#Delete the secret in the cluster:
kubectl delete secret tls-secret

#Uninstall Rancher

#Delete Resource Record Set
#Extract Hosted Zone ID:
ZONE_ID=`aws route53 list-hosted-zones-by-name |  jq --arg name "${HostedZone}." -r '.HostedZones | .[] | select(.Name=="\($name)") | .Id' | cut -d"/" -f3`

#Delete Resource Record Set
NLB=`kubectl get svc -n ingress-nginx -o json | jq -r ".items[0].status.loadBalancer.ingress[0].hostname"`
NLB_NAME=`echo $NLB | cut -d"-" -f1`

#Delete Resource Record Set
NLB_HOSTEDZONE=`aws elbv2 describe-load-balancers --region $REGION --names $NLB_NAME | jq -r ".LoadBalancers[0].CanonicalHostedZoneId"`

cat > rancher-record-set.json <<EOF
{
        "Comment": "CREATE/DELETE/UPSERT a record ",
        "Changes": [{
                "Action": "DELETE",
                "ResourceRecordSet": {
                        "Name": "$RancherURL.",
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

aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID --change-batch file://rancher-record-set.json

#Delete Route53 HostedZone
aws route53 delete-hosted-zone --id $ZONE_ID

#Delete the record file
rm -f rancher-record-set.json

# Delete resources for NGINX Ingress in your cluster:
kubectl delete -f https://github.com/aws-quickstart/quickstart-eks-rancher/blob/main/functions/source/kubernetes/ingress-nginx/controller-v0.40.2/deploy/static/provider/aws/deploy.yaml