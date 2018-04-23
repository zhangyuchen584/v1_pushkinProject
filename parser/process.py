# -*- coding: utf-8 -*-
__author__ = "Yuchen"

import sys
import re
from nltk.stem import SnowballStemmer
import unidecode
from string import punctuation
from nltk.corpus import wordnet as wn
sys.path.append(r"../..")
from definition import ROOT
# from support import stopwordsNoNegWords


class process(object):
    # def __init__(self,fun1=1,fun2=2):
    #
    #     self.fun1 = fun1
    #     self.fun2 = fun2

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # # read abbraviation dic
    # with open(ROOT.ROOT_DIR + "/support/slangDic.txt", "r") as f1:
    #     slangDic = f1.read()
    #
    # slang = {}
    # slangKey = []
    #
    # for index in slangDic.split("\n"):
    #     try:
    #         slang[index.split(":")[0]] = index.split(":")[1]
    #         slangKey.append(index.split(":")[0])
    #     except:
    #         pass

    ##stemmer words##
    snowball_stemmer = SnowballStemmer("english")


    @classmethod
    def test(cls,line='345', toLower =True, removeURL =True,removeHashtag=True,removePunctuations=True,\
             modifyAccent = True,removeEmoticons=True,removeAbbreviation=True,removeStopWords=True, \
             removeStemmer = True):
        print (line)

        if toLower==True:
            line = line.replace("\t", " ").lower()
        if removeURL ==True:
            line = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', line)
        if removeHashtag == True:
            line = re.sub(r'[@#][ ]?([A-Za-z0-9_-]+)', '', line)
        if removePunctuations == True:
            # line = ' '.join(word for word in line.split() if word not in punctuation)+' . '
            line = ' '.join(''.join(word for word in line if word not in punctuation).split())
        if modifyAccent ==True:
            line = unidecode.unidecode(line)
        if removeEmoticons ==True:
            # pass
            line = cls.emoji_pattern.sub(r'', line)
        if removeAbbreviation == True:
            abbre = [x for x in slangKey if x in line.split(" ")]

            line = line.split(" ")

            if abbre:
                for item in abbre:
                    line = [x if (x not in abbre) else slang[item] for x in line]
            line = ' '.join(line)

        if removeStopWords == True:
            line = ' '.join([word for word in line.split() if word not in stopwordsNoNegWords.stop_words])
        if removeStemmer == True:
            line = ' '.join([cls.snowball_stemmer.stem(word) for word in line.split()]) + '.'

        print(line)
        return line


    @classmethod
    ##find the synonyms words
    def synonyms(cls,word):
        """

        :param words: str(word)
        :return: synonyms list['word1','word2','word3'...]
        """
        synonyms = []
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                synonyms.append(' '.join(l.name().split('_')))

        print(set(synonyms))
        # print (synonyms)
        return synonyms



if __name__ == '__main__':
    line = 'you  didn\'t 🙏 gonna ()..)thinking "improvement" http://www.df.df i home @lichao .'
    process.test(line,removeAbbreviation=False,removeStopWords=False)
    # word = 'me'
    process.synonyms('me')