from definition import ROOT
from parser.process import process
import pickle

def returnProcessedData():
    dataDic = pickle.load(open(ROOT.DATA_ROOT + '/newData/groupofData.pk', 'rb'))
    for key in dataDic:
        for i,item in enumerate(dataDic[key]):
            dataDic[key][i] = process.line(dataDic[key][i])
    return dataDic

if __name__ == '__main__':
    ProcessedData = returnProcessedData()
    pickle.dump(ProcessedData,open(ROOT.DATA_ROOT+'/newData/ProcessedData.pk','wb'))