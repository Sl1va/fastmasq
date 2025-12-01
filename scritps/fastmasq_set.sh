#!/bin/bash

if [ "${FASTMASQ_SERVER}" == "" ]; then
    echo "FASTMASQ_SERVER variable is not set: no server to connect"
    exit 1
fi

domain="$1"
record="$2"
if [ "$domain" == "" -o "$record" == "" ]; then
    echo "No domain or record provided"
    exit 1
fi

curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"domain\":\"${domain}\", \"record\": \"${record}\"}" \
  http://${FASTMASQ_SERVER}/set | jq
