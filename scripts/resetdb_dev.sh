#!/bin/bash

CONFIG_KEY=${FLASK_CONFIG:-development}
PROJECT=crabsnack
curdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOTDIR=$(dirname ${curdir})

python ${ROOTDIR}/manage.py dbreset --configkey=${CONFIG_KEY}
#python ${ROOTDIR}/manage.py dbupgrade --configkey=${CONFIG_KEY}
