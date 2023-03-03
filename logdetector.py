# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:04:01 2023

@author: ss250217
"""
import psutil
import os
import time
import re
import pandas as pd
#from tabulate import tabulate

file_name = "dcs.log.2023-02-10"

print(f'File Size is {os.stat(file_name).st_size / (1024 * 1024 * 1024)} GsB')
print(psutil.Process().memory_info().rss / (1024 * 1024))
print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

error_substring = "ERROR"

starttime = time.time()
#get error line - DOne
#fetch error stack trace matching timestamp _DONE
#split the error line with collectorname / system name/ error details/ timestamp
#match the error similarity and system name and collector name - calculate frequency
#then append the list to a tabular form
#o/p in a file all the details
#convert to script
#check
#check to make it work for all kind of log files

flagToStop=0
errorLine=[]
outputContents=[]
lastCausedByException=[]
finaleList=[]
errorFromSystemName=[]
errorFromCollectorName=[]

causedByStringSearch="caused by:"
'''
Error message in short
System Name | Error Type (Collector/other)| Collector name | Error message | Frequency and time stamp
'''

def fetchedSystemName(line):
    firstLine=line.split("System=")
    #print(firstLine)
    fetchSystemName = firstLine[1].split("}") if len(firstLine)>=2 else ""
    #print(fetchSystemName)
    fetchSystemName = fetchSystemName[0] if len(fetchSystemName)>=1 else "" 
    print(fetchSystemName)##got system name
    return(fetchSystemName)
        
def fetchedCollectorName(line):
    firstLine=line.split("Collector=")
    #print(firstLine)
    fetchCollectorName = firstLine[1].split(",") if len(firstLine)>=2 else ""
    #print(fetchSystemName)
    fetchCollectorName = fetchCollectorName[0] if len(fetchCollectorName)>=1 else "" 
    print(fetchCollectorName)##got system name
    return(fetchCollectorName)
    
with open(file_name) as f:
    for line in f.readlines():
        if flagToStop==0 and error_substring in line:
            print("-------------------")
            print(line)
            if not len(outputContents)==0:
                dataList=[]
                dataList.append(errorFromSystemName[-1])
                dataList.append(errorFromCollectorName[-1])                
                dataList.append(lastCausedByException[-1])
                print(dataList)
                finaleList.append(dataList)
            
            errorLine.append(line)
            outputContents.append(line)
            lastCausedByException.append(line)
            errorFromSystemName.append(fetchedSystemName(line))
            errorFromCollectorName.append(fetchedCollectorName(line))
                       
            flagToStop=1
        elif flagToStop==1:
            pattern = r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"            
            matches = re.findall(pattern, line)
            #print(matches)
            if not matches or "Error".lower() in line.lower() or "exception".lower() in line.lower()  :
                print(line)
                if causedByStringSearch in line.lower():
                    lastCausedByException[-1]=line
                outputContents[-1] += line
            else:
                #print(line)
                flagToStop=0
#Trace log location- for all system in same error file -location
#like all socket timeout in a /b file
#cause by last one <calculate freq based on this>
#Error codes -TBD
#calculate frequency

headers = ["SystemName", "CollectorName", "Error Type"]
df = pd.DataFrame(finaleList, columns=headers)

pd.set_option('display.max_colwidth', 35)

#table = tabulate(finaleList, headers=["SystemName", "CollectorName", "Error Type"], tablefmt="grid")

#print(table)

df.to_csv('output.csv', index=False)

'''
with open('output_file.txt', 'w') as f:
    for item in outputContents:
        f.write(pd)
'''
'''    
with open(file_name, 'r') as file:

    # Read the contents of the file into a string
    contents = file.read()

    # Use a regular expression to search for stack traces
    pattern = r'\n((?:.*\n)*)(.*ERROR.*)$'
    match = re.search(pattern, contents, re.MULTILINE)

    # If a stack trace was found, print it
    if match:
        print(match.group(0))
'''            

endtime = time.time()
print("Time taken to execute this program",endtime-starttime)
