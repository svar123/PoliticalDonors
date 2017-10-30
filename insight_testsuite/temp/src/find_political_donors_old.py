import sys
import numpy as np
import csv
import re
import statistics

def main(argv):
    in_data_lst = []
    try:
         in_data_lst = read_infile(argv[1]) 
         preprocess_data(in_data_lst,argv[2],argv[3]) 
    except:
         print("Need input filename, and 2 output file names")

def read_infile(filename):
    '''
    input is the csv filename
    output is a list with all the fields
    '''
    in_data_lst = []
    with open(filename,'r') as csvfile:
        input_val = csv.reader(csvfile, delimiter='|')
        for row in input_val:
            in_data_lst.append(row)
    return (in_data_lst)

def preprocess_data(data,file1,file2):
    '''
    input is the data list, and the two files to write the output
    output is the two written files after processing info
    '''
    id_zip_dict = {}  # dictionary with (id,zipcode) as keys that stores freq and amt
    id_date_dict = {} # dictionary with (id,date) as keys that stores freq and amt
    id_zip_amt_dict = {} # dictionary with zipcode as key that stores a list of amt to calculate median
    id_date_amt_dict = {} #dictionary with date as key that stores a list of amt to calculate median

    with open(file1,'w') as fw1:
    
     year = r"(^[0-9]{4}(2015|2016|2017)$)" #match year of format xxxxy where x is a digit(0-9) and y is 2015/2016/2017
     zipcode=r"(^[0-9]{5}$)"  #match zipcode of format xxxxx where x is a digit(0-9)
     for i in range(len(data)):
        if ((data[i][0] == '')   # CMTE_ID is blank
            or (data[i][14] == '') #TRANSACTION_AMT is blank
               or (data[i][15] != '')): #OTHER_ID is not blank
                    continue
        zip_flag = False
        year_flag = False
        if len(data[i][10]) > 5: #if zipcode greater than 5 digits then get the first five digits
            zipc = data[i][10][0:5]       
        if re.match(zipcode,zipc):
            zip_flag = True   #zipcode is valid
        date = data[i][13]
        if re.match(year,date):
            year_flag = True  #year is valid and between 2015-2017
        
        #process the zip dict
        id_zip_dict,id_zip_amt_dict = process_id_zip(zip_flag,year_flag,data[i][0],zipc,data[i][14],id_zip_dict,id_zip_amt_dict)
        med = round(statistics.median(id_zip_amt_dict[(data[i][0],zipc)]))
        fw1.write(data[i][0]+"|"+zipc+"|"+str(med)+"|"+str(id_zip_dict[(data[i][0],zipc)][1])+"|"+str(id_zip_dict[(data[i][0],zipc)][0])+"\n")
        #process the date dict
        id_date_dict,id_date_amt_dict = process_id_date(year_flag,data[i][0],date,data[i][14],id_date_dict,id_date_amt_dict)
    
    #sort date dictionary    
    with open(file2,'w') as fw2:
      for keys in sorted(id_date_dict.items()):
        med_date = round(statistics.median(id_date_amt_dict[keys[0]]))
        fw2.write(keys[0][0]+"|"+keys[0][1]+"|"+str(med_date)+"|"+str(keys[1][1])+"|"+str(keys[1][0])+"\n")

    
def process_id_zip(zip_flag,year_flag,custid,zipc,amt,id_zip_dict,id_zip_amt_dict):
    '''
    inputs are flags,CMTE_ID,ZIP_CODE,TRANSACTION_AMT,and the two zipcode dictionaries
    outputs are the updated two zipcode dictionaries
    '''
    if zip_flag:
        if ((custid,zipc) not in id_zip_dict):
            fr = 1
            am = int(amt)
            id_zip_dict[(custid,zipc)]=[am,fr]
            id_zip_amt_dict[custid,zipc] = [am]
        else:
            fr = id_zip_dict[(custid,zipc)][1] + 1
            am = id_zip_dict[(custid,zipc)][0] + int(amt)           
            id_zip_dict[(custid,zipc)]=[am,fr]
            id_zip_amt_dict[(custid,zipc)].append(int(amt))
            #sort the amt list
            id_zip_amt_dict = {x:sorted(id_zip_amt_dict[x]) for x in id_zip_amt_dict.keys()}
    return (id_zip_dict,id_zip_amt_dict)       
            


def process_id_date(year_flag,custid,date,amt,id_date_dict,id_date_amt_dict):
    '''
    inputs are the year_flag,CMTE_ID,TRANSACTION_DATE,TRANSACTION_AMT and the two date dictionaries
    outputs are the updated two date dictionaries
    '''
    if year_flag:
       if ((custid,date) not in id_date_dict):
         fr = 1
         am = int(amt)
         id_date_dict[(custid,date)]=[am,fr]
         id_date_amt_dict[custid,date] = [am]
       else:
         fr = id_date_dict[(custid,date)][1] + 1
         am = id_date_dict[(custid,date)][0] + int(amt)
         id_date_dict[(custid,date)]=[am,fr]
         id_date_amt_dict[(custid,date)].append(int(amt))
        #sort the amt list
         id_date_amt_dict = {x:sorted(id_date_amt_dict[x]) for x in id_date_amt_dict.keys()}
    return (id_date_dict,id_date_amt_dict)


if __name__ == "__main__":
    main(sys.argv)
