
# We want a data handler class that will take in data that will be comming from different data sources (on different threads)
# and will be able to handle the data in a thread safe way.  The data will be stored in a dictionary with the key being the data source



import threading
import time
import csv

class DataHandler:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def addDataType(self, dataType: str):
        self.lock.acquire()
        self.data[dataType] = 0
        self.lock.release()

    def updateData(self, dataType: str, data):
        self.lock.acquire()
        self.data[dataType] = data
        self.lock.release()

    def getData(self, dataType: str):
        self.lock.acquire()
        data = self.data[dataType]
        self.lock.release()
        return data

    
    def getDataTypes(self):
        self.lock.acquire()
        dataTypes = self.data.keys()
        self.lock.release()
        return dataTypes

    def getDataValues(self):
        self.lock.acquire()
        dataValues = self.data.values()
        self.lock.release()
        return dataValues
    
    def getFrame(self):
        # This functions get the current timestamp at the index 0 of the array followed by the data values
        self.lock.acquire()
        dataValues = self.data.values()
        self.lock.release()
        return [time.time()] + list(dataValues)
        
    



if __name__=='__main__':
    #little test
    dataHandler = DataHandler()
    dataHandler.addDataType('test')
    dataHandler.addDataType('test2')

    dataHandler.updateData('test2', 15)
    dataHandler.updateData('test', 5)
    print(dataHandler.getData('test'))
    dataHandler.updateData('test', 10)
    print(dataHandler.getData('test'))
    

    print(dataHandler.getDataTypes())
    print(dataHandler.getDataValues())


