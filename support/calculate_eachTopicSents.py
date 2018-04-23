import sys
sys.path.append(r"../..")
from pushkin_gs.definition import ROOT
import argparse

origDataRoot = ROOT.DATA_ROOT+'/corpus/'
# with open(ROOT.DATA_ROOT+'/corpus', "r") as fi:
# files = os.listdir(ROOT.DATA_ROOT+'/corpus')
# # print ('files',files)
# def calculate_eachTopicSents(folder):
#     for ifl in folder:
#         dir = ROOT.DATA_ROOT + '/corpus/'+ifl
#         pattern = re.compile(r'.txt')
#         print (pattern)
#         files = os.listdir(dir)
#         print (files)
#         for i in files:
#             print (i)
#             match = pattern.match(i)
#             print (match)
#
#
#
#
#     # files = os.listdir(ROOT.DATA_ROOT + '/corpus/'+)
#
# if __name__ == '__main__':
#     """
#
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--dataFolder', default='', help="Tw",action='store', nargs='+')
#
#
#     args = parser.parse_args()
#     data = calculate_eachTopicSents(args.dataFolder)
#
#     # print (data)
#     # pass

import os


alldata = {}

def topicSents(folders,threshold):
    count = 1
    for ifold in folders:
        dir = origDataRoot+ifold

        files = os.listdir(dir)  # 得到文件夹下的所有文件名称
        for file in files:

            if file.find('swp') == -1:
                if file.find('txt') != -1:
                    # print(file)
                    with open (origDataRoot+'/'+ifold+'/'+file,'r') as fi:
                        icount = 1
                        for line in fi:
                            # print (line)
                            count = count + 1
                            icount = icount +1
                            # print(re.split('1|2|0', line, 1))
                            # print (line.split('\t')[0]+'_'+line.split('\t')[1])
                            try:
                                alldata[line.split('\t')[0]+'_'+line.split('\t')[1]] = alldata[line.split('\t')[0]+'_'+line.split('\t')[1]] + line.split('\t')[2]
                            except:
                                alldata[line.split('\t')[0] + '_' + line.split('\t')[1]] = line.split('\t')[2]
                    # print (icount)
    print ("total number of sentence: ",count)
    # print(alldata)
    for ith in threshold:
        neg = 0
        pos = 0
        print ("\nnumber of sents > ", ith)
        for i in alldata:
            if i[-1] == str(1):
                continue

            if len(alldata[i].split('\n')) > int(ith):
                if i[-1] == str(0):
                    neg = neg+1
                if i[-1] == str(2):
                    pos = pos+1
                print ("target: ",i, ",  number: ",len(alldata[i].split('\n')))
        print ("\npolarity_0:", neg,"polarity_1:", pos,"\n")

    return alldata

def SenWithMoreTargets(folders):
    count = {}
    sents = []
    alldata = []
    alldataPolarity = {}
    for ifold in folders:
        dir = origDataRoot+ifold
        files = os.listdir(dir)  # 得到文件夹下的所有文件名称
        for file in files:
            if file.find('swp') == -1:
                if file.find('txt') != -1:
                    with open (origDataRoot+'/'+ifold+'/'+file,'r') as fi:

                        for line in fi:
                            sents.append(line.split('\t')[2].strip('\n'))
                            alldata.append(line.strip('\n')+'\t'+ifold+'_'+file)
    print ("alldata",alldata)



    sents.sort()
    myset = set(sents)
    multiTarget = []
    for item in myset:
        try:
            count[sents.count(item)]+=1
        except:
            count[sents.count(item)]=1
        if sents.count(item) !=1:
            multiTarget.append(item)

    for sent in alldata:

        if sent.split('\t')[-2].strip('\n') in multiTarget:
            try:
                alldataPolarity[sent.split('\t')[-2].strip('\n')].append(sent.split('\t')[0].strip('\n'))
                alldataPolarity[sent.split('\t')[-2].strip('\n')].append(sent.split('\t')[1].strip('\n'))
            except:
                alldataPolarity[sent.split('\t')[-2].strip('\n')] = [sent.split('\t')[0].strip('\n'),sent.split('\t')[1].strip('\n')]


    duplicate = 0
    differentTarget = 0
    differentPolarity = 0
    differentTarPol = 0
    print ("sentence with more than 1 target: ",len(alldataPolarity))

    folderFile = {}
    for key in alldataPolarity:
        if ((len(set(alldataPolarity[key][::2]))) ==1) & ((len(set(alldataPolarity[key][1::2])))==1):
            duplicate+=1
            folder = []
            for line in alldata:
                if line.split('\t')[-2] == key:
                    folder.extend((line.split('\t')[-1],line.split('\t')[-2]))
                    # folder.append(line.split('\t')[-1])
            # print (folder)
            try:
                folderFile[str(set(folder[::2]))].append(folder[1])
            except:
                folderFile[str(set(folder[::2]))] = [folder[1]]

        elif (len(set(alldataPolarity[key][::2]))) ==1:
            differentPolarity+=1
        elif ((len(set(alldataPolarity[key][1::2]))) ==1):

            differentTarget+=1
        else:
            differentTarPol+=1

    print ("%s sentences are duplicated\n%s sentences have different targets\n%s sentences have different polarity\n%s sentences have different targets and polarity\n" % (duplicate,differentTarget,differentPolarity,differentTarPol))
    for key in folderFile:
        print ("%s %s\n"%([key],len(folderFile[key])))
        if len(key.split(',')) == 2:
            with open('question'+key+'.txt', 'a') as the_file:
                the_file.write(str(folderFile[key]))

    for key in count:
        print ("%s sentences have %s target" %(count[key],key))

from termcolor import colored




if __name__ == "__main__":
    """
    python calculate_eachTopicSents.py --dataFolder Twitter YouTube --threshold 40
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataFolder', default='', help="Tw",action='store', nargs='+')
    parser.add_argument('--threshold', default='', help="Tw", action='store', nargs='+')
    args = parser.parse_args()
    # data = topicSents(args.dataFolder,args.threshold)
    a = SenWithMoreTargets(args.dataFolder)


    """
    sentence with more than 1 target:  789
    422 sentences are duplicated
    363 sentences have different targets
    3 sentences have different polarity
    1 sentences have different targets and polarity
    
    ["{'YouTube_dev_111.txt', 'Twitter_dev_111.txt'}"] 49
    
    ["{'Twitter_train_111.txt', 'YouTube_train_111.txt'}"] 362
    
    ["{'Twitter_train_111.txt'}"] 10
    
    ["{'YouTube_train_111.txt'}"] 1
    
    2241 sentences have 1 target
    781 sentences have 2 target
    8 sentences have 4 target
    """
    import re


