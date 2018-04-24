# -*- coding: utf-8 -*-
__author__ = "Yuchen"
__aim__ = 'calculate TFIDF value for each topic in all documents(6k tweets) and return content words'

import math
from textblob import TextBlob as tb
from definition import ROOT
import pickle


class ContentWords(object):
    def __init__(self,contentWordNumber,database,targetList):
        self.allData = database
        # self.targetData = targetData
        self.contentWordNumber = contentWordNumber
        self.targetList = targetList

    def tfidf(self):

        print("func: tfidf")
        keywordsDic = {}
        for key in self.allData:
            if key in self.targetList:
                temdic = {key:self.allData[key]}
                dictMerged = dict(temdic,**self.allData)
                bloblist = []
                for sent in dictMerged:
                    bloblist.append(tb(dictMerged[sent]))

                def tf(word, blob):
                    return blob.words.count(word) / len(blob.words)

                def n_containing(word, bloblist):
                    return sum(1 for blob in bloblist if word in blob.words)

                def idf(word, bloblist):
                    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

                def tfidf(word, blob, bloblist):
                    return tf(word, blob) * idf(word, bloblist)

                scores = {word: tfidf(word, bloblist[0], bloblist) for word in bloblist[0].words}
                sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

                contentWordList = []

                for word, score in sorted_words[:int(self.contentWordNumber)]:
                    # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
                    # remove single letter
                    if len(word)>1 and word != key.split("_")[0]:
                        contentWordList.append(word)
                print ('top',self.contentWordNumber,'content words for',key,'\n',contentWordList,'\n',100*'**')
                keywordsDic[key] = contentWordList
        print (keywordsDic)
        return keywordsDic



def main():
    dataDic = pickle.load(open(ROOT.DATA_ROOT + '/newData/ProcessedData.pk', 'rb'))
    targetList = ["ns_Negtive","ns_Positive","ord_Positive","enlistment_Positive","bmt_Positive","ippt_Negtive",\
                  "bookout_Positive","tekong_Negtive","ord_Negtive","ippt_Positive","platoon_Positive"]

    for key in dataDic:
        dataDic[key] = " ".join(dataDic[key])


    instance = ContentWords(14, dataDic, targetList)
    keywordDic = ContentWords.tfidf(instance)
    pickle.dump(keywordDic, open(ROOT.ROOT_DIR + '/support/keywordDic.kp', 'wb'))

if __name__ == '__main__':
    #top 14 key words
    main()
