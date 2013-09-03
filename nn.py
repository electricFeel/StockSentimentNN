import time
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import RecurrentNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from multiprocessing import Process

def buildDataSet():
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
    ds = ClassificationDataSet(4, 1, nb_classes=2)

    #create the dataset
    for k in timestamps:
        ds.addSample((float(sentiment[k]), float(snp5002012[k]), float(cci[k]),
                      float(new_housing[k])), (int(output[k]),))

    return ds


def buildNetwork(hidden_layer = 3):
    #build the network
    #create the layers
    input_layer = LinearLayer(4)
    hidden_layer = SigmoidLayer(hidden_layer, name='hidden')
    output_layer = LinearLayer(2)
    net = RecurrentNetwork()

    net.addInputModule(input_layer)
    net.addModule(hidden_layer)
    net.addOutputModule(output_layer)

    in_to_hidden = FullConnection(input_layer, hidden_layer)
    hidden_to_out = FullConnection(hidden_layer, output_layer)
    net.addRecurrentConnection(FullConnection(net['hidden'], net['hidden']))

    net.addConnection(in_to_hidden)
    net.addConnection(hidden_to_out)

    net.sortModules()
    return net

def runTest(hidden_layer = 3, learning_rate = 0.1, momentum = 0.5, epochs = 5000, filename='RCNetwork2.xml'):
    ds = buildDataSet()
    tstdata, trndata = ds.splitWithProportion(0.25)
    trndata._convertToOneOfMany()
    tstdata._convertToOneOfMany()
    net = buildNetwork(hidden_layer)
    #define the connections
    trainer = BackpropTrainer(net, dataset=trndata, momentum=momentum, verbose=False, weightdecay=learning_rate)
    #trainer = BackpropTrainer(net, learningrate = 0.01, dataset = ds, momentum = 0.99, verbose = True)
    trainer.trainEpochs(epochs)
    trnresult = percentError( trainer.testOnClassData(),
                              trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )
    print filename
    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult
    #trainer.train()
    print 'Final weights:', net.params

    NetworkWriter.writeToFile(net, filename)

if __name__ == "__main__":
    print buildDataSet()
    p1 = Process(target=runTest, args=(6, 0.05, 0.35, 500000, 'RCNetwork.xml'))
    p2 = Process(target=runTest, args=(6, 0.15, 0.5, 500000, 'RCNetwork2.xml'))
    p3 = Process(target=runTest, args=(6, 0.05, 0.5, 500000, 'RCNetwork3.xml'))
    p4 = Process(target=runTest, args=(6, 0.5, 0.15, 500000, 'RCNetwork4.xml'))
    p5 = Process(target=runTest, args=(6, 0.1, 0.23, 500000, 'RCNetwork5.xml'))
    #runTest(hidden_layer = 3, learning_rate = 0.05, momentum = 0.5, epochs = 5000, filename = 'RCNetwork1.xml')
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()



