
# Will use a DataHandler object to save data to a csv file on its own thread


import threading
import time
import csv
from DataHandler import DataHandler
import os

class DataSaver:

    dataFilePrefix = "data_"

    def __init__(self, dataHandler: DataHandler, dataPath: str="./", frequency: int=1):
        self.dataHandler = dataHandler
        self.dataPath = dataPath
        self.frequency = frequency
        self.delay = 1 / frequency
        self.fileName = f"{DataSaver.dataFilePrefix}{self.getLatestCount(dataPath)}.csv"
        self.path = os.path.join(self.dataPath, self.fileName)


        self.dataThread = threading.Thread(target=self.dataThread)
        self.dataThread.start()




    def getLatestCount(self, dataPath: str):

        count = 0
        for file in os.listdir(dataPath):
            if file.startswith(DataSaver.dataFilePrefix):
                fileCount = int(file.split('_')[1].split('.')[0])
                if fileCount > count:
                    count = fileCount
        
        return count + 1

    def dataThread(self):
        with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp'] + list(self.dataHandler.getDataTypes()))
            print(self.formatFrame(['timestamp'] + list(self.dataHandler.getDataTypes()), delimiter="\t"))
            while True:

                print(self.formatFrame(self.dataHandler.getFrame(), delimiter="\t"))
                writer.writerow(self.dataHandler.getFrame())
                file.flush()
                time.sleep(self.delay)
            
    def formatFrame(self, frame: list, delimiter: str=","): #return a string of all the values in the frame separated by commas
        frameString = ""
        for value in frame:
            frameString += f"{value}{delimiter}"

        # remove last delimiter
        frameString = frameString[:-1]

        return frameString    
    
    

if __name__=='__main__':
    # little test
    dataHandler = DataHandler()
    dataSaver = DataSaver(dataHandler, frequency=10)


    dataHandler.addDataType('test')
    dataHandler.addDataType('test2')

    dataHandler.updateData('test2', 15)
    dataHandler.updateData('test', 5)

    time.sleep(5)

    dataHandler.updateData('test2', 20)
    dataHandler.updateData('test', 10)

    time.sleep(5)

    dataHandler.updateData('test2', 25)
    dataHandler.updateData('test', 15)
