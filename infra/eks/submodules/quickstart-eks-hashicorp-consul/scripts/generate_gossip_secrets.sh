#!/bin/bash
RELEASE=consul_${VERSION}_linux_amd64.zip
# Fetch Consul binaries & prerequisites
yum install -y unzip

curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/linux/amd64/kubectl
chmod +x ./kubectl
curl -q https://releases.hashicorp.com/consul/${VERSION}/${RELEASE} -o ${RELEASE}
unzip ${RELEASE} -d .
chmod +x ./consul

# Cleanup secrets
./kubectl -n $NS delete secret consul-gossip-encryption-key
./kubectl -n $NS delete secret consul-ca-cert
./kubectl -n $NS delete secret consul-ca-key

# Create Gossip Secret
./kubectl -n $NS create secret generic consul-gossip-encryption-key --from-literal=key=$(./consul keygen)

# Create TLS Requirements
./consul tls ca create
./kubectl -n $NS create secret generic consul-ca-cert --from-file='tls.crt=./consul-agent-ca.pem'
./kubectl -n $NS create secret generic consul-ca-key --from-file='tls.key=./consul-agent-ca-key.pem'