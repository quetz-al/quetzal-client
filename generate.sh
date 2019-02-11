#!/bin/bash

set -e

QUETZAL_URL="http://10.4.33.236:5000/api/v1/openapi.json"

echo "Running openapi-generator-cli..."
docker run --rm \
       -v ${PWD}:/local \
       openapitools/openapi-generator-cli:latest \
       generate \
       -i ${QUETZAL_URL} \
       -g python \
       -c /local/openapi-generator-config.json \
       -o /local/quetzal/client/autogen

echo "Cleaning files..."
#rm quetzal/client/generated/openapi_client_README.md
