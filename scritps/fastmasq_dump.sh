#!/bin/bash

if [ "${FASTMASQ_SERVER}" == "" ]; then
    echo "FASTMASQ_SERVER variable is not set: no server to connect"
    exit 1
fi

config_file="$1"
if [ "$config_file" == "" ]; then
    echo "No output filename provided"
    exit 1
fi

curl -s -X POST http://${FASTMASQ_SERVER}/config >${config_file}
