
## Preparing the program to run
 
from datetime import datetime , timedelta ## We need these to count time correctly
startTime = datetime.now()
import csv ## Avoid Pandas for big data 
path= "./input/log.csv" ## Given the file structure that is where the log file is
file = open(path, newline='') ## Opening the log file to read data
reader = csv.reader(file) ## Reading the file in csv format
header = next(reader) ## Header of the file 
f = open('./input/inactivity_period.txt','r') ## Reading inactivity time
InActive=int(f.read())
count =0
## Data collection
data=[]   ## define varible data
for row in reader:
    time = row[1] + " " + row[2]  ## Combining Time and date 
    My_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S') ## Changing string to date 
    FileCount=1  ## Default for file visit for each session
    Flag=0 ## Flag data to make sure we don't double count them

    data.append([row[0] , My_time, My_time,FileCount, row[4] , row[5] , row[6]])  ## Creating our data set

DataLength=len(data)
DataLength

InActive=InActive+1                        ## to use smaller sign
f= open("./output/sessionization.txt","w+") ## Open an output file
for i in range (DataLength):
    Flag=0
    for j in range (i+1,DataLength):     ## don't compare element to itself
        
        if int((data[j][2] - data[i][2]).seconds ) < InActive:## elements within given time limit
            if data[j][0] == data[i][0]:                      ## compare their IP
                data[j][1] = data[i][1]                       ## transfer the start time
                data[j][3] = data[i][3]+1                     ## add 1 to file counts
                Flag=1                                       ## this element repeats to write down
                break                                        ## if you found a repeating IP go to next entry
        elif int((data[j][2] - data[i][2]).seconds ) > InActive:
            break                                ## don't compare when time difference has reached

    
    if Flag == 0:       ## if the inactivity time reached with no repeat print it
     
        count = count + data[i][3]
        dt=int((data[i][2]-data[i][1]).seconds )+1  ## Find time spend in each session for a given IP
        print(data[i][0],data[i][1].strftime("%Y-%m-%d %H:%M:%S"),data[i][2].strftime("%Y-%m-%d %H:%M:%S"),dt,data[i][3],sep=",", file=f)


f.close()                           ## Print the result and close the file
print(datetime.now() - startTime)    
        
lostFile = (DataLength-count)
if lostFile == 0:
    print ("no files lost")
else:
    print ("Worning", lostFile, "'s lost")
