from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import time

#dataset lists
sentiment = {}
snp5002012 = {}
cci = {}
new_housing = {}
output = {}
#load datasets
#first load the sentiment index
for line in open('SNP500Sentiment2012.txt'):
    row = line.rstrip().split(',')
    sentiment[row[1]] = row[2]
#next load the SNP500 values
for line in open('SNP5002012.txt'):
    row = line.rstrip().split(',')
    snp5002012[row[0]] = row[2]
#load the CCI numbers
for line in open('CCI2012.txt'):
    row = line.rstrip().split(',')
    cci[row[0]] = row[1]
#load the New Housing starts
for line in open('NewHousing2012.txt'):
    row = line.rstrip().split(',')
    new_housing[row[0]] = row[1]
#load the yes/no output
for line in open('SNP5002012Close.txt'):
    row = line.rstrip().split(',')
    output[row[0]] = row[1]

print len(sentiment), len(snp5002012), len(cci), len(new_housing), len(output)

#create timestamps
timestamps = output.keys()
timestamps.sort(key=lambda x: time.mktime(time.strptime(x, "%m/%d/%Y")))

#build the dataset
ds = SupervisedDataSet(4, 1)

for k in timestamps:
    ds.addSample((float(sentiment[k]), float(snp5002012[k]), float(cci[k]),
                  float(new_housing[k])), float((output[k],)))



