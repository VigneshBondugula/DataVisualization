import pickle
import pandas as pd
import glob
from functools import reduce
from tqdm import tqdm

class DataGenerator:
    def __init__(self, paths, lineSkip, pickleName):
        self.paths = paths
        self.lineSkip = lineSkip
        self.pickleName = pickleName
        self.fileNames = self.getFileNames(paths[0])
        self.data = {}

    def getFileNames(self, path):
        filePaths = glob.glob(f'data/{path}/*.txt')
        fileNames = []
        for path in filePaths:
            fileNames.append(path.split("/")[-1])
        fileNames.sort()
        return fileNames
    
    def extractDate(self, filename):
        filename = filename.split(".")[0]
        return "".join(filename)
    
    def generatePickle(self):  
        with open(self.pickleName + ".pkl", 'wb') as f:
            pickle.dump(self.data, f)
        
    def mergeDataFrames(self, dataFrames):
        dfMerged = reduce(lambda  left,right: pd.merge(left,right,on=['LON', 'LAT'],
                                            how='left', suffixes=('', '_y')), dataFrames)
        dfMerged.drop(dfMerged.filter(regex='_y$').columns, axis=1, inplace=True)
        return dfMerged

    def generateData(self):
        print("Extracting " + self.pickleName)
        for file in tqdm(self.fileNames):
            date = self.extractDate(file)
            dataFrames = []
            for path in self.paths:
                df = pd.read_csv(f'data/{path}/{file}', skiprows=self.lineSkip)
                dataFrames.append(df)
            dfMerged = self.mergeDataFrames(dataFrames)
            self.data[date] = dfMerged
        self.generatePickle()
            
    
if __name__ == '__main__':
    scalarDataGenerator = DataGenerator(paths = ['ssha', 'sss', 'sst'], 
                                        lineSkip = 9,
                                        pickleName = "scalarData")

    vectorDataGenerator = DataGenerator(paths = ['meridional-current', 'zonal-current'], 
                                        lineSkip = 10,
                                        pickleName = "vectorData")
    
    #Extracting and saving data as pickles
    scalarDataGenerator.generateData()
    vectorDataGenerator.generateData()
