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
    result_value = np.max(arr_value)
    return result_value

def mean_q (list_data):   
    arr_value = np.array(list_data)
    result_value = np.mean(arr_value)
    return result_value

def min_q (list_data):   
    arr_value = np.array(list_data)
    result_value = np.min(arr_value)
    return result_value

def sum_q (list_data):   
    arr_value = np.array(list_data)
    result_value = np.sum(arr_value)
    return result_value

def group_list(lst):      
    return list(zip(Counter(lst).keys(), Counter(lst).values()))

def get_barcodeinfo(data,filterQ,filterL):
    avg_score_data = []
    length_data = []
    barcodeName = ""
    for x in data:
        aList = x
        if filterQ == 0 and filterL == 0  :
                avg_score_data.append(aList["Average_Qscore"])
                length_data.append(aList["Read_length"])
                barcodeName = str(aList["Read_barcode"]) 
                
        if int(aList["Average_Qscore"]) >= filterQ  :
               if filterL == 0  :
                        avg_score_data.append(aList["Average_Qscore"])
                        length_data.append(aList["Read_length"])
                        barcodeName = str(aList["Read_barcode"])
                    
               if aList["Read_length"] >= filterL :
                        avg_score_data.append(aList["Average_Qscore"])
                        length_data.append(aList["Read_length"])
                        barcodeName = str(aList["Read_barcode"])

    if len(avg_score_data) == 0  |  len(length_data) == 0 :
        return

    maxQscore_str = str(max_q(avg_score_data))
    minQscore_str = str(min_q(avg_score_data))
    meanQscore_str = str(round(mean_q(avg_score_data),2))
    maxQscore_str = str(max_q(avg_score_data))
    minQscore_str = str(min_q(avg_score_data))
    meanQscore_str = str(round(mean_q(avg_score_data),2))
    print("Average_Qscore : Max " + maxQscore_str)
    print("Average_Qscore : Min " + minQscore_str)
    print("Average_Qscore : Mean " + meanQscore_str)
    print("///////////" +barcodeName)
    
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
    Bases = str(sum_q(length_data))
    print("Reads : " + total_reads)
    print("Bases : " + Bases)
    
    
    plt.scatter(avg_score_data, length_data)
    plt.title("Distribution of read quality scores")
    plt.xlabel("Read quality scores")
    plt.ylabel("Read Length")     
    img = BytesIO()      
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img1_base = base64.b64encode(img.getvalue()).decode('utf8')
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
    out_array = np.log10(length_data)
    length_log = []
    for v in out_array :    
        length_log.append(round(v,1))
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
    ############################ barcode json return  
    # barcode_info = {
    #                   "Average_Qscore_Max": maxQscore_str,
    #                   "Average_Qscore_Min": minQscore_str,
    #                   "Average_Qscore_Mean": meanQscore_str,
    #                   "Average_length_Max": maxLength_str,
    #                   "Average_length_Min": minLength_str,
    #                   "Average_length_Mean": meanLength_str,
    #                   "BarcodeName": barcodeName,
    #                   "Reads": total_reads,
    #                   "Bases": Bases
    #                 }
    ############################
    html = ' 		<tr>'
    html += ' 		  <td>' + '<a href="'+barcodeName+'.html" target="_blank">' + barcodeName+'</a></td>'
    html += ' 		  <td>'+total_reads+'</td>'
    html += ' 		  <td>'+maxQscore_str+'</td>'
    html += ' 		  <td>'+minQscore_str+'</td>'
    html += ' 		  <td>'+meanQscore_str+'</td>'
    html += ' 		  <td>'+maxLength_str+'</td>'
    html += ' 		  <td>'+minLength_str+'</td>'
    html += ' 		  <td>'+meanLength_str+'</td>'
    html += ' 		</tr>'
    
    
    with open(barcodeName+'.html','w') as f:
        f.write(gen_html(barcodeName,maxQscore_str,minQscore_str,meanQscore_str,total_reads,maxLength_str,minLength_str,meanLength_str,img1_base,img2_base,img3_base,""))
    return html
    
def show_alldata(data,barcodeList,filterQ,filterL):
    avg_score_data = []
    length_data = []
    for x in data:
        aList = json.loads(x)
        if filterQ == 0 and filterL == 0  :
                avg_score_data.append(aList["Average_Qscore"])
                length_data.append(aList["Read_length"])   
        if int(aList["Average_Qscore"]) >= filterQ  :
               if filterL == 0  :
                    avg_score_data.append(aList["Average_Qscore"])
                    length_data.append(aList["Read_length"])
                    
               if aList["Read_length"] >= filterL :
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
    print("Reads : " , len_data)
    print("Bases : " + str(sum_q(length_data)))

    plt.scatter(avg_score_data, length_data)
    plt.title("Distribution of read quality scores")
    plt.xlabel("Read quality scores")
    plt.ylabel("Read Length")      


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
    
    bcdata = []
    html2 = ""
    for x in barcodeList :
        bcdata = []
        for i in data:
            aaList = json.loads(i)
            if aaList["Read_barcode"] == x :
                   bcdata.append(aaList) 
        print("\\bc//:" + x , len(bcdata))        
        html2 += get_barcodeinfo(bcdata,filterQ,filterL)
    
    
    html = gen_html("ALL",maxQscore_str,minQscore_str,meanQscore_str,total_reads,maxLength_str,minLength_str,meanLength_str,img1_base,img2_base,img3_base,html2)
    with open('report.html','w') as f:
        f.write(html)