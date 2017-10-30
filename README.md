
# Political Donors Challenge Report


## Challenge

For this challenge, we're asked to take an input file that lists campaign contributions by individual donors and distill it into two output files:
  
1. median_vals_by_zip.txt: contains a calculated running median, total dollar amount and total number of contributions by recipient and zipcode.
  
2. median_vals_by_date.txt: has the calculated median, total dollar amount, and total number of contributions by recipient and date.
  
For the first output file (medianvals_by_zip.txt) the code should process  each line of the input file as if that record was sequentially streaming into the program. For each input file line, it should calculate the running median of contributions, total number of transactions and total amount of contributions streaming in so far for that recipient and zip code.
  
For the second output file (medianvals_by_date.txt) the code should list every unique combination of date and recipient from the input file and then the calculated total contributions and median contribution for that combination of date and recipient. The lines are represented by unique combination of date and recipient, sorted alphabetically by recipient and then chronologically by date.


## Design

I used Python code (version 3.6.1) for this challenge. The key to solving a  challenge of this type is to come up with the right data structure.

For the first output file, I used the dict structure of Python (id_zip_dict) that takes in a tuple (CMTE_ID,ZIP_CODE) as keys and values as median, number of transactions, and total transaction amt. For each transaction, I incremented the number of transactions, added the transaction amt, calculated the median and wrote each line to the output. To calculate the median, I used a second dict structure (id_zip_amt_dict) with  (CMTE_ID,ZIP_CODE) as keys and a sorted list of TRANSACTION_AMT as values.
  
For the second output file, I used the dict structure of Python (id_date_dict) that takes in a tuple (CMTE_ID,TRANSACTION_DT) as keys and values as median, number of transactions, and total transaction amt. For each transaction, I incremented the number of transactions, added the transaction amt, calculated the median and wrote each line to the output. To calculate the median, I used a second dict structure (id_date_amt_dict) with  (CMTE_ID,TRANSACTION_DT) as keys and a sorted list of TRANSACTION_AMT as values. To order the recipients alphabetically and sort chronologically, I used the Python 'sorted' function just before writing to the output file which sorted the dictionary based on the first value (CMTE_ID) and then the second value (TRANSACTION_DT) of the keys tuple.

I assumed the valid years in TRANSACTION_DT is 2015-2017. 
  

## Testing

For unit testing, I created 4 test cases which are described below.

* test_1 (given)

  Passed the given testcase
  
  
* test_2 

  Checked for empty fields CMTE_ID and TRANSACTION_AMT.
  If these fields are empty the records are ignored. 
  1. CMTE_ID field is set to empty (in record 2).
  2. TRANSACTION_AMT filed is set to empty (in record 3).
  3. CMTE_ID and TRANSACTION_AMT fields are set to empty (in record 4).
  
  
* test_3

  Checked for empty/malformed TRANSACTION_DT field.
  If this field is empty/malformed then this record is ignored for second      output file(medianvals_by_date.txt) but included in first output   file(medianvals_by_zip.txt).
  1. TRANSACTION_DT is set to empty (set to '' in record 2).
  2. TRANSACTION_DT is malformed (set to '012017' in record 3).
  3. TRANSACTION_DT is malformed (set to 'a1312017' in record 4).
  4. TRANSACTION_DT is not in 2015-2017 (set to '01312018' in record 5).
  

* test_4

  Checked for empty/malformed ZIP_CODE field.
  If this field is empty/malformed then this record is ignored for first  output file(medianvals_by_zip.txt) but included in second output  file(medianvals_by_date.txt).
  1. ZIP_CODE is set to empty (set to '' in record 2).
  2. ZIP_CODE is malformed (set to '0289' in record 3).
  3. ZIP_CODE is malformed (set to '30ab50' in record 4).
  
  
* test_5

  Added 5 records to check if the second output file   (medianvals_by_date.txt) is sorted alphabetically by recipient and then chronologically by date.
  
insight_testsuite/run_tests.sh

[PASS]: test_1 medianvals_by_zip.txt

[PASS]: test_1 medianvals_by_date.txt

[PASS]: test_2 medianvals_by_zip.txt

[PASS]: test_2 medianvals_by_date.txt

[PASS]: test_3 medianvals_by_zip.txt

[PASS]: test_3 medianvals_by_date.txt

[PASS]: test_4 medianvals_by_zip.txt

[PASS]: test_4 medianvals_by_date.txt

[PASS]: test_5 medianvals_by_zip.txt

[PASS]: test_5 medianvals_by_date.txt

[Mon, Oct 30, 2017 10:12:20 AM] 5 of 5 tests passed


