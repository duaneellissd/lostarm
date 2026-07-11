if [ ! -f ./venv/bin/activate ]
then
    bash ./create_venv.sh
fi

. ./venv/bin/activate
for x in `find . -type f -name 'test_*.py'`
do
    cmd="python3 -m unittest $x"
    echo "========================================"
    echo $cmd
    echo "========================================"
    $cmd
    if [ $? -ne 0 ]
    then
	echo "========================================"
	echo "FAIL: $x"
	echo "========================================"
	exit 1
    fi
done

