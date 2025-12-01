#!/bin/bash

if [ "${FASTMASQ_SERVER}" == "" ]; then
    echo "FASTMASQ_SERVER variable is not set: no server to connect"
    exit 1
fi

curl -s -X POST http://${FASTMASQ_SERVER}/list | jq
