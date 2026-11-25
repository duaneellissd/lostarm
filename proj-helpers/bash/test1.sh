#! /bin/bash

#
# We set this so can simplify the unit test.
export BASH_HELPERS_FILENAME_ONLY=true

rm ./actual_output/*
rmdir ./actual_output
mkdir ./actual_output

for test1_id in 0 1 2 3 4
do

    good_file=$(printf "./good_output/test1_%d_good.txt" $test1_id)
    out_file=$(printf "./actual_output/test1_%d_actual.txt" $test1_id)

    bash ./do_test_1.sh $test1_id > $out_file
    # ALL of these cases call fatal, which exits with 1
    if [ $? -ne 1 ]
    then
        printf "Test1-0, case %s fails exit case\n" "${test1_id}"
        exit 1
    fi
    diff $good_file $out_file
    if [ $? -ne 0 ]
    then
        printf "Test1-ID=%d - fails.\n" $test1_id
        printf "Expected file: %s\n" $good_file
        printf "  Actual file: %s\n" $out_file
        exit 1
    fi
done
printf "TEST1: Pass\n"
exit 0
