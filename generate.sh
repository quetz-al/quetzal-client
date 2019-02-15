#!/bin/bash

set -e

QUETZAL_URL="https://local.quetz.al/api/v1/openapi.json"
WORK_DIR=$(mktemp -d /tmp/quetzal-client-generator.XXXXXX)
DOCKER_IMAGE="openapitools/openapi-generator-cli:latest"

echo "Downloading API specification"
curl --insecure -o ${WORK_DIR}/openapi.json ${QUETZAL_URL}

# Fix the $refs, which generate incorrect code as shown in
# https://github.com/OpenAPITools/openapi-generator/issues/1991
echo "Dereferencing..."
python deref.py ${WORK_DIR}/openapi.json ${WORK_DIR}/openapi-noref.json
cp openapi-generator-config.json ${WORK_DIR}


echo "Running openapi-generator-cli..."
docker image pull ${DOCKER_IMAGE}
docker run --rm \
       -v ${PWD}:/local \
       -v ${WORK_DIR}:/tmp/input:ro \
       ${DOCKER_IMAGE} \
       generate \
       -i /tmp/input/openapi-noref.json \
       -g python \
       -c /tmp/input/openapi-generator-config.json \
       -o /local/

# Let's fix the disaster created by
# https://github.com/OpenAPITools/openapi-generator/issues/1658
# Not needed since around Feb 15th
#echo "Fixing openapi-generator-cli issue #1658..."
#for file_or_dir in $(find quetzal._auto_client)
#do
#    fixed_name="quetzal/_auto_client/${file_or_dir:21}"
#    echo "Fixing ${file_or_dir} -> ${fixed_name}"
#
#    if [[ -d "${file_or_dir}" ]]
#    then
#        mkdir -p ${fixed_name}
#    else
#        mv ${file_or_dir} ${fixed_name}
#    fi
#done
#
## Add a __init__.py to make quetzal.client.autogen a module
##touch quetzal/client/autogen/__init__.py
#
#echo "Cleaning files..."
#rm -r quetzal._auto_client
#rm -r quetzal._auto_client_README.md
