#! /bin/bash

GENMAKE_SH_ROOT=false

if [ "${TARGET}" == "stm32h743zit" ]
then
    SOURCES=`ls *.c`
    python ${GENMAKE_PY} --staticlibrary ll_hal --source "${SOURCES}"
fi
