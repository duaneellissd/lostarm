#! /bin/bash

GENMAKE_SH_ROOT=false

if [ "${TARGET}" == "unix" ]
then
    SOURCES=`ls *.c`
    python ${GENMAKE_PY} --staticlibrary ll_hal --source "${SOURCES}"
fi
