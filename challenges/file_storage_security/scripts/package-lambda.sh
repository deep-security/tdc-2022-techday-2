#!/usr/bin/env bash

LAMBDA_NAME=$(basename "$(pwd)")

#install dependencies
mkdir -p ./dependencies
pip install --target ./dependencies/ -r ./requirements.txt

#packaage dependencies into initial zip file
cd dependencies || exit
zip -r ../"$LAMBDA_NAME" .
cd ..
rm -rf dependencies

# add function to zip archive
zip -g "$LAMBDA_NAME".zip index.py
