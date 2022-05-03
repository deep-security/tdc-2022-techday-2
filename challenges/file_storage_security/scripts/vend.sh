#!/usr/bin/env bash
read -p "Are you sure? " -n 1 -r
echo 
if [[ $REPLY =~ ^[Yy]$ ]]
then
    gh workflow -R deep-security/tdc-2022-techday-2 run build-dev-environment.yaml -f name="$(git rev-parse '@{u}')"
fi
