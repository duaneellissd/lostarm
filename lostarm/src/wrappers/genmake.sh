#! /bin/bash

GENMAKE_SH_ROOT=false

SOURCES=`ls *.c`
python ${GENMAKE_PY} --static-library --source "${SOURCES}"
