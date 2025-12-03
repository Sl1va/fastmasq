#!/bin/bash

[ "${FASTMASQ_SERVER}" == "" ] && exit
[ "${HOSTFILE}" == "" ] && exit

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
