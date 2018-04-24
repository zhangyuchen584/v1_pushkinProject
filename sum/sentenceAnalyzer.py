
__aim__ = """same with Java code: sentenceAnalyzer
             analyze same noun percentage"""
from parser import parserWords
# print (parserWords.posTag("you are person"))

class sentneceAnalyzer(object):

    def ComputeNunSim(sentA,sentB):
        anumcount = 0
        bnumcount = 0
        sameNum = 0
        posTagA =  parserWords.posTag(sentA)
        for word in set(posTagA):
            if word[1] == 'NN':
                anumcount +=1

        posTagB = parserWords.posTag(sentB)
        for word in set(posTagB):
            if word[1] == 'NN':
                bnumcount += 1

        for wordA in posTagA:
            if wordA[1] == 'NN':
                for wordB in posTagB:
                    if wordB[1] == 'NN':
                        # print (wordA[0],wordB[0])
                        if wordA[0].lower() == wordB[0].lower():
                            sameNum += 1
                            break
        if anumcount+bnumcount>0:
            return sameNum/(anumcount+bnumcount)
        else:
            return 0

if __name__ == '__main__':
    senta = 'you are the best student i have ever seen'
    sentb = 'student can join in our school music festival'
    a = sentneceAnalyzer()
    print (sentneceAnalyzer.ComputeNunSim(senta,sentb))
