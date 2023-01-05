import gzip
import shutil
from pathlib import Path
from datetime import datetime
import re, csv
import json
from bioseq.fqanalyze.display import show_alldata

def QScore_Cal(ASCII):
    list_Qscore = []
    list_ASCII = []
    Dict_Qscore = {}
    length_ASCII = len(ASCII)
    for each_ASCII in ASCII:
        each_Qscore = ord(each_ASCII)-33
        list_Qscore.append(each_Qscore)
        list_ASCII.append(each_ASCII)       
    sum_Qscore = sum(list_Qscore)
    average_Qscore = sum_Qscore/length_ASCII
    return round(average_Qscore,0) 

def ReadLength(gzfile):  
    print("Please waiting ....")
    rowss = 0   
    str_json = ""
    j_data = []
    with gzip.open(gzfile, 'rb') as filein:
        with open('processfile.fastq', 'wb') as fileout:
            shutil.copyfileobj(filein, fileout)
            path = Path('processfile.fastq')          
            with open(path, 'r') as readfile:
                lines = readfile.read()
                for data in re.finditer (r'@(?P<Read_ID>\w*).*barcode=(?P<Read_barcode>\w*).*\n.*\n\+\n(?P<Read_Qscore>.*)', lines):                    
                    rowss += 1 
                    readID = data.group('Read_ID') 
                    readBarcode = data.group('Read_barcode') 
                    readQscore = data.group('Read_Qscore') 
                    readlength = str(len(readQscore))                    
                    Q_score = str(QScore_Cal(readQscore))                   
                    str_json = "{\"Read_ID\":\"" + readID + "\",\"Read_barcode\":\"" + readBarcode + "\",\"Read_length\":" + readlength + ",\"Average_Qscore\":" + Q_score + ",\"No\":" + str(rowss) + "}"
                    j_data.append(str_json)
                    
    path.unlink()     
    write_list(j_data)    
    print ("Read length analysis complete")
    

def write_list(a_list):
    print("Started writing list data into a json file")
    with open("results.json", "w") as fp:
        json.dump(a_list, fp)
        print("Done writing JSON data into .json file")
              
              
def GetJsonData(json_name,filterQ,filterL):   
    # load data using Python JSON module
    with open(json_name,'r') as f:
        data = json.loads(f.read())       
    barcodeList = []
    for x in data:
            aList = json.loads(x)
            if aList["Read_barcode"] not in barcodeList:
                  barcodeList.append(aList["Read_barcode"])          
    print("Data : " , len(data))
    print(barcodeList)
    show_alldata(data,barcodeList,filterQ,filterL)
    
