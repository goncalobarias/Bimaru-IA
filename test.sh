#!/bin/sh

# get all files ending with .txt from ./tests/
# and run them, comparing them with their respective .out
# if the output is the same, print "Test _ SUCCESS" in green,
# otherwise print "Test _ FAILED" in red

files=$(ls ./tests/ | grep ".txt")

for file in $files
do
  echo -e "Testing $file..."
  python ./src/bimaru.py < ./tests/$file > /tmp/bimaru.out
  output=$(cat /tmp/bimaru.out)
  output_file=$(echo $file | sed 's/txt/out/')
  expected_output=$(cat ./tests/$output_file)
  if [ "$output" = "$expected_output" ]
  then
    echo -e "\e[32mTest $file SUCCESS\e[0m"
  else
    echo -e "\e[31mTest $file FAILED\e[0m"
    # diff between /tmp/bimaru.out and ./$output_file
    colordiff -u ./tests/$output_file /tmp/bimaru.out
  fi
done
