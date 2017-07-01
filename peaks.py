import datetime as dt
import math
import csv

#This will store date <-> Future+PE value mapping
realTimeData = [];

#This constructs our data from file
def readFileAndParseValues(fileName):
    with open(fileName,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row[1]) > 1:
                realTimeData.append(float(row[1]));
    
    
#This will get value at index - we will use to simulate real time data
def getValue(i):
    return realTimeData[i]

def stdDeviation(data):
    if len(data) > 1:
        mean = sum(data)/len(data)
        meanSq = 0
        for i in range(0, len(data), 1):
            meanSq += math.pow((data[i] - mean), 2)
        meanSq = math.sqrt(meanSq/(len(data)-1))
        return meanSq

def updateStdv(stdDev, data):
    if len(data) > 1:
        stdDeviationForNewData = stdDeviation(data)
        updatedStdDev = stdDev*0.5 + stdDeviationForNewData*0.5
        return updatedStdDev
    else:
        return stdDev
 
readFileAndParseValues('nifty.csv')

#Setting values - please experiment with them in order to optimize the alogorithm
window = 20;  #how many datapoints to consider before calculating 
threshold = 10 #how many std deviations away from mean should the data point be before it is considered a peak
peaks = [];


historicalMean = sum(realTimeData)/len(realTimeData)
histroricalStdv = stdDeviation(realTimeData)

updatedMean = historicalMean
updatedStdv = histroricalStdv

dataPoint = 20; #starting with 20th entry

for i in range(0, 19, 1):
    peaks.append(0)

count = 0;
realTimeValues = []



for i in range(0, len(realTimeData), 1):
    timeSeriesValue = getValue(dataPoint)
    realTimeValues.append(timeSeriesValue)
    delta = abs(historicalMean - timeSeriesValue)
    if(delta > threshold*updatedStdv):
        peaks.append(1)
    else:
        peaks.append(0)
    updatedStdv = updateStdv(updatedStdv, realTimeValues)
    count+=1;

print peaks