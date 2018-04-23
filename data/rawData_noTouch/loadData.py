import sys
import numpy as np
sys.path.append(r"../..")
from definition import ROOT
import pickle

DataRoot = ROOT.DATA_ROOT+"/rawData_noTouch"
filesWithTarget = {'/Twitter':["/dev_target.txt","/test_target.txt","/train_tag.txt"],'/YouTube':["/dev_target.txt","/test_target.txt","/train_targ_(new).txt"]}
filesWithoutTarget = {'/YouTube':["/train_target.txt"]}

def loadalldata(threshold):
	alldata = []
	for folder in filesWithTarget:
		for file in filesWithTarget[folder]:
			fileRoot = DataRoot+folder+file
			with open(fileRoot) as fi:
				for line in fi:
					# if  (len(line.strip('\n').split("\t"))) !=3:
					# 	alldata.append([' '.join(line.strip('\n').split('\t')[0].split(' ')[:-1]),line.strip('\n').\
					# 		split('\t')[0].split(' ')[-1],line.strip('\n').split("\t")[-1],folder+file])

					# else:
					# 	alldata.append([line.strip('\n').split('\t')[0],line.strip('\n').split('\t')[1],line.strip('\n').\
					# 		split('\t')[2],folder+file])
					if  (len(line.strip('\n').split("\t"))) !=3:
						alldata.append([' '.join(line.strip('\n').split('\t')[0].split(' ')[:-1]),line.strip('\n').\
							split('\t')[0].split(' ')[-1],line.strip('\n').split("\t")[-1]])
						
					else:
						alldata.append(line.strip('\n').split('\t'))
	#remove duplicated sentences
	uniqueList = []
	for item in alldata:		
		if item not in uniqueList:
			uniqueList.append(item)

	#remove neutral sentences
	removeNeutral = []
	removeNeutral= removeNeutral+ ([item for item in uniqueList if item[1]!='1'])

	#combine multiple target
	resetData = {}
	for item in removeNeutral:
		try:
			resetData[item[2]].extend(item[:2])
		except:
			resetData[item[2]] = item[:2]
	print ("raw data: {}\nremove duplicated sentences: {}\nremove neutral sentences: {}\ncombine multiple targets: {}\n".format(len(alldata),len(uniqueList),len(removeNeutral),len(resetData)))

	calculateGroup = {}
	for item in removeNeutral:
		try:
			
			calculateGroup[item[0]+'_Positive' if item[1] =='2' else item[0]+'_Negtive'].append(item[2])
			
		except:
			calculateGroup[item[0]+'_Positive' if item[1] =='2' else item[0]+'_Negtive'] = []
			calculateGroup[item[0]+'_Positive' if item[1] =='2' else item[0]+'_Negtive'].append(item[2])
	

	print ("total groups: ",len(calculateGroup))
	#rank targetPolarity according to number of sentences
	for ti in threshold:
		count = 0
		for k in sorted(calculateGroup, key=lambda k: len(calculateGroup[k]), reverse=True):
			# print (k,len(calculateGroup[k]))
			if len(calculateGroup[k])>=ti:
				count +=1

		print ("senteces > %s: %s" %(ti,count))

	return resetData,calculateGroup

	
	
if __name__ == '__main__':
	newData,groups = loadalldata(threshold = [20,30,50,70])
	pickle.dump(newData,open(ROOT.DATA_ROOT+'/newData/allData.pk','wb'))
	pickle.dump(groups, open(ROOT.DATA_ROOT + '/newData/groupofData.pk', 'wb'))


