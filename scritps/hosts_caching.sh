#!/bin/bash

[ "${FASTMASQ_SERVER}" == "" ] && exit
[ "${HOSTFILE}" == "" ] && exit

LOCK_FILE="/tmp/fastmasq.lock"

exec 200>${LOCK_FILE}
flock -n 200 || exit
trap "rm -f ${LOCK_FILE}" EXIT

fastmasq_monitor() {
    while true; do
        [ -f "${HOSTFILE}" ] && sed -i '/# fastmasq$/d' ${HOSTFILE}
        for host in $(curl -s -X POST http://${FASTMASQ_SERVER}/list | jq -r '.[].domain'); do
            echo "${host} # fastmasq" >>${HOSTFILE}
        done
        sleep 60
    done
}

fastmasq_monitor
