#! /bin/bash

thisdir=`realpath ${BASH_SOURCE[0]}`

tmp=${thisdir}/.venv
if [ -d $tmp ]
then
    echo "Removing venv dir"
    rm -rf $tmp
fi

EMACS_BACKUP_FILES=`find $thisdir -type f -name '*~' -print`

for fn in $EMACS_BACKUP_FILES
do
    echo "Remove Emacs backup file: $fn"
    rm $fn
done

# Python compiled files.
for dn in `find . -type d -name '__pycache__' -print`
do
    echo "Remove python cache directory: $dn"
    rm -rf $dn
done
