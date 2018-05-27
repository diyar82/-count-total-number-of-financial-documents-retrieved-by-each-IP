Data Engineering challenge:
Insight Data Engineering Fellows Program 
The coding challenge /Electronic Data Gathering, Analysis and Retrieval (EDGAR) 
Solution approach

Contents
Introduction	
Loading components and Getting the data from log and txt files
Basic approach	
Advanced approach	
Comparison and big–O	
Conclusion

Introduction
The challenge basically asks to count total number of financial documents retrieved by each IP during single visit. 
The program is written in Python3. Please make sure Python3 is installed for the program to run properly
For the purpose of testing our code we downloaded the log file for Dec/10th/2004. Which has a size of 41 MB. From https://www.sec.gov/dera/data/edgar-log-file-data-set.html . 
Loading components and Getting the data from log and txt files
First datetime and csv components are called. We avoid using Pandas to make sure the programs scale up efficiently. The code gets a file called “log.csv” where the data is stored and a file called “inactivity_period.txt” where the time for inactivity in seconds are given. 

#####################################################################
from datetime import datetime , timedelta ## We need these to count time correctly
startTime = datetime.now()
import csv ## Avoid Pandas for big data 
path= "./input/log.csv" ## Given the file structure that is where the log file is
file = open(path, newline='') ## Opening the log file to read data
reader = csv.reader(file) ## Reading the file in csv format
header = next(reader) ## Header of the file 
f = open('./input/inactivity_period.txt','r') ## Reading inactivity time
InActive=int(f.read())
################################################################
Basic approach
In basic approach we are dealing with each data entry separately and compare it to the subsequent entries. 
##############################################################################
Data collection
data=[]   ## define varible data
for row in reader:
    time = row[1] + " " + row[2]  ## Combining Time and date 
    My_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S') ## Changing string to date 
    FileCount=1  ## Default for file visit for each session
    data.append([row[0] , My_time, My_time,FileCount, row[4] , row[5] , row[6]])  ## Creating 										##our data set
DataLength=len(data)
InActive=InActive+1		## we add one to use smaller comparison 
f= open("../output/Long_Ver_Out.txt","w+") ## Open an output file
for i in range (DataLength): 
    Flag=0  			## a flag to recognized data ready to print
    for j in range (i+1,DataLength):  
        if int((data[j][2] - data[i][2]).seconds ) < InActive: ## Checking expiry time
            if data[j][0] == data[i][0]:			## compare ip addresses
                data[j][1] = data[i][1]			## advance start time to next entry
                data[j][3] = data[i][3]+1		## add file count by 1
                Flag=1					## flag to show the file was updated
                Break
        elif int((data[j][2] - data[i][2]).seconds ) > InActive:
            break                                ## don't compare when time difference has reached


    if Flag == 0:
        dt=int((data[i][2]-data[i][1]).seconds )+1	 ## time difference inclusive
        print(data[i][0],data[i][1].strftime("%Y-%m-%d %H:%M:%S"),data[i][2].strftime("%Y-%m-%d %H:%M:%S"),dt,data[i][3],sep=",", file=f)	 ## write file with no correspondence ahead
f.close()                           ## Print the result and close the file
print(datetime.now() - startTime)   
############################################################################

Advanced approach 
This approach is better when we have data bigger than 1k and more than 1 access for each second. This approach is different that the basic approach through the way data compared and function called. In this approach the time for each entry is read first and the number of entries having same time are recorded in an array. Then elements of the array is called for comparison purpose. 
#########################################################################
## Data collection
data=[]   ## define varible data
for row in reader:
    time = row[1] + " " + row[2]  ## Combining Time and date 
    My_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S') ## Changing string to date 
    FileCount=1  ## Default for file visit for each session
    Flag=0 ## Flag data to make sure we don't double count them
    data.append([row[0] , My_time, My_time,FileCount,Flag , row[4] , row[5] , row[6]])  ## Creating our data set
## Time counter 
m=0 ## The very first entry is located in row 0
n=len(data) ## Length of the data is the total number of entries
My_array=[] ## Define an array to hold number of entries for each second
for i in range (n): ## Loop over the entire data
    K=data[m][1]    ## The time for the first entry
    for j in range(m, n): 
        if (data[j][1]-K).seconds > 0:  ## Compare the time to detect time change
            My_array.append(j-m)        ## Add a number sum of all enteries at the same second 
            m=j                         ## Passing on to next second
            break                       ## At time change break the loop
Start=0                                 ## The first entry is located at row 0
TimeArrayLength=len(My_array)           ## Lenth of time array which is equal or smaller than number of seconds                     
for k in range (TimeArrayLength):       ## For each element of the time array "each second"
    ArrayEnd=Start+My_array[k]          ## elemnts having same second of time
    for i in range (Start,ArrayEnd):    ## Iterate over the elemnts of that second
        CompareLength=sum(My_array[k:k+InActive])+Start+1  ## Define last element before inactive timereached
        for j in range (i+1,CompareLength): ##Look at elements until inactivity time reachs
            if data[j][0] == data[i][0]: ## Find if an IP is repeated within acceptable time fram
                data[j][1]=data[i][1]    ## if so copy first contact time to the other entity
                data[j][3] = data[i][3]+1 ## Add one to number of files accessed
                data[i][4] = 1           ## mark the data as repeated so we dont double counted
                break
    Start=ArrayEnd
ToWrite=[] 
f= open("../output/sessionization.txt","w+") ## Open an output file
count =0
for i in range (n):                  ## Itterate over the entire document
    if data[i][4] == 0:              ## find last repeating data within given time frame
        dt=int((data[i][2]-data[i][1]).seconds )+1     ## Find time spend in each session for a given IP
        count = count + data[i][3]
        print(data[i][0],data[i][1].strftime("%Y-%m-%d %H:%M:%S"),data[i][2].strftime("%Y-%m-%d %H:%M:%S"),dt,data[i][3],sep=",", file=f)
f.close()                           ## Print the result and close the file
print(datetime.now() - startTime)
lostFile = (n-count)
if lostFile == 0:
    print ("no files lost")
else:
    print ("Worning", lostFile, "'s lost")
###########################################################################

Comparison and big – O
The advanced approach decreases the time required for the program run extensively. When both programs run on same input. While the basic code took 3:26:06.811366 (12366.8 seconds) the advanced code needed only 0:00:19.351307 (19.4 seconds). In other words the efficiency increase about 600 times!. However 
The reason is the first method is comparing the time of each entry with following times to make sure if it repeats in future. This approach if not stopped through “break” command has n!  calls while looking up in index is a linear function. Another break function added to the basic approach at “elif” which decreased the required time from 3:26:06.811366 (12366.8 seconds)to 0:00:20.868073 (20.9 seconds).
The same two code ran on Linux environment the advanced method required 7 seconds while the basic method required 8 seconds on average. In other words Linux proved 2-3 times more efficient running this specific code.

Conclusion
For bigger data it is important to find ways to decrease the computational cost to increase the efficiency. Here we showed one way of increasing efficiency. 



