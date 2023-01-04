import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
from collections import Counter
from io import BytesIO
import base64
from bioseq.fqanalyze.htmlgen import gen_html
def max_q (list_data):
    arr_value = np.array(list_data)
    max_value = np.max(arr_value)
    return max_value

def mean_q (list_data):   
    arr_value = np.array(list_data)
    max_value = np.mean(arr_value)
    return max_value

def min_q (list_data):   
    arr_value = np.array(list_data)
    max_value = np.min(arr_value)
    return max_value
def sum_q (list_data):   
    arr_value = np.array(list_data)
    max_value = np.sum(arr_value)
    return max_value
def group_list(lst):      
    return list(zip(Counter(lst).keys(), Counter(lst).values()))

def show_alldata(data):
    avg_score_data = []
    length_data = []
    for x in data:
        aList = json.loads(x)
        avg_score_data.append(aList["Average_Qscore"])
        length_data.append(aList["Read_length"])
        #df = pd.DataFrame(aList, columns=list("ABCD"))
       # print(aList["Average_Qscore"])
    maxQscore_str = str(max_q(avg_score_data))
    minQscore_str = str(min_q(avg_score_data))
    meanQscore_str = str(round(mean_q(avg_score_data),2))
    print("Average_Qscore : Max " + maxQscore_str)
    print("Average_Qscore : Min " + minQscore_str)
    print("Average_Qscore : Mean " + meanQscore_str)
    print("///////////")
    
    maxlength = max_q(length_data)
    maxLength_str = str(f'{maxlength:,.0f}')
 
    minLength_str = str(min_q(length_data))
    meanLength = round(mean_q(length_data),0)
    meanLength_str = str(f'{meanLength:,.0f}')
    print("Average_length : Max " + maxLength_str)
    print("Average_length : Min " + minLength_str)
    print("Average_length : Mean " + meanLength_str)
    
    len_data = len(data)
    total_reads = str(f'{len_data:,.0f}')
    print("Reads : " + total_reads)
    print("Bases : " + str(sum_q(length_data)))

    plt.scatter(avg_score_data, length_data)
    plt.title("Distribution of read quality scores")
    plt.xlabel("Read quality scores")
    plt.ylabel("Read density")      


    img = BytesIO()      
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img1_base = base64.b64encode(img.getvalue()).decode('utf8')
  

 

    
    
    
    out_array = np.log10(length_data)
    length_log = []
    for v in out_array :    
        length_log.append(round(v,1))


    
  

      
 
    avg_score_data_list = group_list(avg_score_data)
    lst = avg_score_data_list
    lst.sort(key=lambda x:x[0]) 
    x = []
    y = []
    for v in lst:    
        x.append(v[0])
        y.append(v[1])

    plt.plot(x, y)
    plt.title("Distribution of read quality scores")
    plt.xlabel("Read quality scores")
    plt.ylabel("Read density")    
    img = BytesIO()      
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img2_base = base64.b64encode(img.getvalue()).decode('utf8')
    
    length_data_list = group_list(length_log)
    lst = length_data_list
    lst.sort(key=lambda x:x[0])    
    x = []
    y = []

    for v in lst: 
        x.append(v[0])
        y.append(v[1])
    plt.plot(x, y)
    plt.title("Distribution of read length")
    plt.xlabel("Read length (log scale)")
    plt.ylabel("Read density")
    img = BytesIO()      
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img3_base = base64.b64encode(img.getvalue()).decode('utf8')
    
    html = gen_html(maxQscore_str,minQscore_str               ,meanQscore_str,total_reads,maxLength_str,minLength_str,meanLength_str,img1_base,img2_base,img3_base)
    with open('test.html','w') as f:
        f.write(html)