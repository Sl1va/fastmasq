#!/bin/bash

if [ "${FASTMASQ_SERVER}" == "" ]; then
    echo "FASTMASQ_SERVER variable is not set: no server to connect"
    exit 1
fi

domain="$1"
if [ "$domain" == "" ]; then
    echo "No domain provided"
    exit 1
fi

curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"domain\":\"${domain}\"}" \
  http://${FASTMASQ_SERVER}/del >/dev/null
