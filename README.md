To the Moon Project  
This program can analyze gzipped .fastq files' read length and average Qscore data, plot the data into graphs and report in HTML format.

How to use the program

1. Analyze Read Length: ./myseq ReadLength  
Arguments: -r or --readgz: Provide your .gz file  
Example: ./myseq ReadLength -r input.fastq.gz  
This command will run read length and average Qscore analysis of input.fastq.gz

2. Filter Read: ./myseq GetJsonData  
Arguments:  
-r or --jsonname: Provide results.json file  
           -q or --filterQ: Filter Qscore option (type=integer)  
           -l or --filterL: Filter Length option (type=integer)  
Example: ./myseq GetJsonData -r results.json -q 10 -l 1000  
  This command will filter out reads with average Qscore below 10 and reads with less than 1000 bp length out of results.json file.  
  The results will be displayed in an HTML format.
