#!/bin/bash

set -e

QUETZAL_URL="https://local.quetz.al/api/v1/openapi.json"
WORK_DIR=$(mktemp -d /tmp/quetzal-client-generator.XXXXXX)

# Generate with a docker image of the openapi-generator-cli project, or with a
# local clone of this repo. Until recently, we were using the former, but some
# particular regressions impact us and there has not been a release yet. The
# regression is documented here:
# https://github.com/OpenAPITools/openapi-generator/issues/2209
#
# For this case, set this variable:
OPENAPI_GENERATOR_CLI_DIR=${HOME}/apps/openapi-generator


# For an official openapi-generator-cli Docker image, use this variable instead:
# DOCKER_IMAGE="openapitools/openapi-generator-cli:v4.0.0-beta2"

if [[ -z ${DOCKER_IMAGE} ]]
then
   # When DOCKER_IMAGE is not defined or is empty
   if [[ -d ${OPENAPI_GENERATOR_CLI_DIR} ]]
   then
       pushd ${OPENAPI_GENERATOR_CLI_DIR}
       REFERENCE="git-$(git rev-parse --short HEAD)"
       popd
       echo "Using local openapi-generator-cli in ${OPENAPI_GENERATOR_CLI_DIR}."
       echo "Generator reference is ${REFERENCE}..."
   else
       echo "${OPENAPI_GENERATOR_CLI_DIR} not defined."
       exit -1
   fi
   GENERATE_CMD="java -jar ${OPENAPI_GENERATOR_CLI_DIR}/modules/openapi-generator-cli/target/openapi-generator-cli.jar generate"

else
    echo "Pulling docker image..."
    docker image pull ${DOCKER_IMAGE}
    REFERENCE="docker-$(docker image inspect --format "{{.Id}}" ${DOCKER_IMAGE})"
    GENERATE_CMD="docker run --rm -v ${PWD}:${PWD} -v ${WORK_DIR}:${WORK_DIR}:ro ${DOCKER_IMAGE} generate"
fi
echo "Generator reference is ${REFERENCE}."

echo "Downloading API specification..."
curl --insecure -o ${WORK_DIR}/openapi.json ${QUETZAL_URL}

# Fix the $refs, which generate incorrect code as shown in
# https://github.com/OpenAPITools/openapi-generator/issues/1991
echo "Dereferencing..."
python deref.py ${WORK_DIR}/openapi.json ${WORK_DIR}/openapi-noref.json
cp openapi-generator-config.json ${WORK_DIR}


echo "Running openapi-generator-cli..."
${GENERATE_CMD} \
    -i ${WORK_DIR}/openapi-noref.json \
    -g python \
    -c ${WORK_DIR}/openapi-generator-config.json \
    -o ${PWD}

# # Let's fix the disaster created by
# # https://github.com/OpenAPITools/openapi-generator/issues/1658
# # Not needed since around Feb 15th, but then needed again due to regression
# echo "Fixing openapi-generator-cli issue #1658..."
# for file_or_dir in $(find quetzal._auto_client)
# do
#    fixed_name="quetzal/_auto_client/${file_or_dir:21}"
#    echo "Fixing ${file_or_dir} -> ${fixed_name}"

#    if [[ -d "${file_or_dir}" ]]
#    then
#        mkdir -p ${fixed_name}
#    else
#        mv ${file_or_dir} ${fixed_name}
#    fi
# done

# echo "Cleaning files..."
# rm -r quetzal._auto_client
# rm -r quetzal._auto_client_README.md

echo "Saving reference..."
sed -i '' \
    -e "s/__version__[[:space:]]*=[[:space:]]*\(.*\)/\# __version__ = \1  \# Commented by generate.sh/g" \
    quetzal/_auto_client/__init__.py

cat >> quetzal/_auto_client/__init__.py <<EOF

# Added by generate.sh:
# Add a complete reference to the generator version:
# a git commit or Docker image ID used to generate this code with openapi-generator-cli
__openapi_generator_cli_version__ = "${REFERENCE}"
EOF
