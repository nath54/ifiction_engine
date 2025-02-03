#
python test1_command_parsing.py tests/test1_in.txt > tmp_out.txt

#
diff -q tmp_out.txt tests/test1_out.txt > /dev/null 2>&1  # Redirect output to null

# Check the exit status of diff
if [ $? -eq 0 ]; then
  echo "TEST 1 PASSED"
else
  echo "TEST 1 FAILED"
fi

#
rm tmp_out.txt
