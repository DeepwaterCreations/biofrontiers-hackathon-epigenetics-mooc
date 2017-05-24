# -*- coding: utf-8 -*-
import re
import json
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import unicodedata
import urllib,urllib2
#import requests
#from bs4 import BeautifulSoup
from tools import usefulResources
import jpype
import time
import sys,getopt
stopSet=stopwords.words('english')
wordSet=set(nltk.corpus.words.words());
porterStemmer=PorterStemmer();

lemmatizer=nltk.stem.wordnet.WordNetLemmatizer();
#The address will be represented in a more appropriate way
modelAnswerAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/processed_answer.json"
strRawDataAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/raw_json_data2.json"

strProcessedDataAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/processed_bow.json"
strProcessedTotalDictAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/processed_total.json"
strProcessedDataAddr2=r"/Users/ksun/Desktop/syd/syd/FInal_project/processed_bow2.json"
strProcessedTotalDictAddr2=r"/Users/ksun/Desktop/syd/syd/FInal_project/processed_total2.json"

strProcessedDataBigramAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/processed_bow_bi.json"
strProcessedTotalDictBigramAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/processed_total_bi.json"

statisticsAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/statistics.json"
modifiedWordAddr=r"/Users/ksun/Desktop/syd/syd/FInal_project/manuallyModification.json"
class JsonRW(object):
    pass
    def __init__(self):
        pass
    def readFromJson(self,addr):
        with open(addr,'r')as jsonFile:
            jsonData=json.loads(jsonFile.read());
        return jsonData
    def writeToJson(self,addr,dictObj):
        with open(addr,'w')as jsonFile:
            json.dump(dictObj,jsonFile);
        return

#return a string wiout the useless words and tags
def removeUnicodeSign(string):
    '''
    reg=re.compile('(\xa0)|(\x0c)');
    tempString=re.sub(reg," ",string)
    return unicodedata.normalize("NFKD",unicode(tempString)).encode('ascii','ignore');'''
    return re.sub(r'[^\x00-\x7f]',r'', string) 
def unicodeToString(uniString):
    return unicodedata.normalize('NFKD', uniString).encode('ascii','ignore')
def removeTag(string):
    stringTag="<.*?>"
    reg=re.compile(stringTag)
    return re.sub(reg," ",string)
#useless when the removeSinglechar function runs after removing all the non-char characters
def removeQuesitonSign(string):
    reg=re.compile("([Qq]\s?\d)")
    return re.sub(reg," ",string)
#this function will merged to getBOW function
def removeSingleChar(word):
    if len(word)<=1:
        pass
def cleanData(string):
    #first step is to remove '\xa0' and unicode signs
    string=removeUnicodeSign(string);
    #the tag will be replaced as " "
    stringTag1='(<\/i>)|(<i>)|(\/strong)|(<strong>)|(<a.*?>)|(\/a)|(<span.*?>)|(<\/span>)|'
    stringTag2='(<ol>)|(<li>)|(<\/ol>)|(<\/li>)|(<u>)|(<\/u>)|<em>|<pre>|'
    #stringTag="<.*?>";
    #the other form will be replaced as ""
    stringOtherForm='(\n)|(\[\d+\]\.)|'
    #the string Others will be replaced as " "
    stringOthers='[^a-zA-Z]'
    stringHttp="((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?"
    regexHttp=re.compile(stringHttp);
    string=re.sub(regexHttp," ",string);
    #regexString=stringTag1+stringTag2+stringOtherForm+stringOthers;
    regexString=stringTag1+stringTag2+stringOtherForm+stringOthers;
    #don't forget to deal with http address
    regex=re.compile(regexString);
    rs=re.sub(regex," ",string);
    return rs    
#it seems the adj and adv cannot be parsed as the same word root
def myLemmatizer(word,pos=None):
    lemma=lemmatizer.lemmatize(word,'v')
    if lemma==word:
        lemma=lemmatizer.lemmatize(word,'n')
    return lemma
#The improvemet shoul be made here: by adding the specialist lexicon as another wordset tesing with the wordSet
def maxMatch(string,wordsSet=wordSet):
    ur=usefulResources()
    ansWordList=set(ur.getModelAnswerWordList(modelAnswerAddr))
    if not len(string):
        return [];
    for i in range(1,len(string)+1)[::-1]:
        firstword=myLemmatizer(string[:i]);
        remainder=string[i:];
        if (firstword in ansWordList) or (firstword in wordsSet):
            return [string[:i],maxMatch(remainder,wordsSet)]
    #firstword=string[0];
    #remainder=string[1:];
    #return [firstword,maxMatch(remainder,wordsSet)];
def minMatch(string, wordsSet=wordSet):
    ur=usefulResources()
    ansWordList=set(ur.getModelAnswerWordList(modelAnswerAddr))
    if not len(string):
        return [];
    for i in range(2,len(string)):
        firstword=myLemmatizer(string[:i]);
        remainder=string[i:];
        if (firstword in ansWordList) or (firstword in wordsSet):
            return [string[:i],maxMatch(remainder,wordsSet)]

def get_word_from_MMlist(l):
    li=[];
    temp=l;
    while(len(temp)!=0):
        li.append(temp[0])
        if len(temp)==2:
            temp=temp[1];
        else:
            break; 
    return li;

def getModelAnswList(modelAnswerAddress):
    ur=usefulResources()
    l=ur.getModelAnswerWordList(modelAnswerAddress)
    return l
#solve the problme caused by maxMatch by this method, or manually make or import a biomedical corpus
#like: tansfer [u'i', u'm', u'mun', u'ode', u'fi', u'c', u'ie', u'n', u'c', u'y']to[immunodeficiency]
def combineWronglySplittedWord(strList):
    pass
def writeManuallyWordModification(addr,li):
    strLi=str(li)+","
    with open(addr,'a+')as txtFile:
        txtFile.write(strLi)
    
#return a list of strings
#the maxMatch algorithm will be acted here for splitting the wrong word group without spaces

def convertToList(string,nLen=15,ifPOSTag=False):
    #put remove the question sign here 
    result=[]
    taggers=[]
    manTupDict={}
    words=string.lower().split();
    #if pos:
        #rawTaggers=nltk.pos_tag(words);
    for w in words:
        tempList=[]
        ansList=getModelAnswList(modelAnswerAddr);
        if len(w)>nLen and (w not in ansList):
            #print w
            #the problem would happened at here,since there is the case like this "hypomethlyationhappens"
            #the solution should add the necessary lexicon in the maxMatch process
            tempList=get_word_from_MMlist(maxMatch(w));
        if len(tempList)>2:
            #print tempList
            manTupDict[tuple(tempList)]=1
            #writeManuallyWordModification(modifiedWordAddr,tempList)
            result.extend(tempList)
        else:
            result.append(w)
    if ifPOSTag:
        taggers=nltk.pos_tag(result)
    return (result,taggers,manTupDict)


#main guide for deeper process the data:
#(1)POS with raw, get List of taggers
#(2)
#lightCleanWord use bioLemmetizer by jpype
jvmPth=jpype.getDefaultJVMPath()
externalJarPath=r"/Users/ksun/Desktop/syd/syd/FInal_project/corpus/biolemmatizer-core-1.2-jar-with-dependencies.jar"
if not jpype.isJVMStarted():
    jpype.startJVM(jvmPth,"-ea","-Djava.class.path=%s"%(externalJarPath),"-Xms1g", "-Xmx1g");

#word and pos are both strings
def bioLemmatizer(word,pos):
    jPackage="edu.ucdenver.ccp.nlp.biolemmatizer"
    javaBioLemmClass=jpype.JClass(jPackage+".BioLemmatizer")
    jInstance=javaBioLemmClass()
    lemmedWord=jInstance.lemmatizeByLexiconAndRules(word,pos).lemmasToString()
    return unicodeToString(lemmedWord)

#input is a list of tuples.
def tupleListToString(tupList):
    res=[]
    for t in tupList:
        res.append(str(t))
    return res
def tupleStringReader():
    pass
    
def bigramFeatureGenerator(sentList,ifTransferKeyToStr=False):
    nonStopList=[]
    for w in sentList:
        if w not in stopSet and len(w)>1:
            nonStopList.append(w)
    res=zip(nonStopList, nonStopList[1:])
    if ifTransferKeyToStr:
        res=tupleListToString(res)
    return res

def lemmBigram(tup,lemmer):
    return (lemmer(tup[0]),lemmer(tup[1]))


#wordList is a list of strings
#return a dict contains words for an answer without stopwords
#in getBOW, all the last step for removing word will be acted: remove the word whose len=1s
#para:lemmetizer is the lemmatizer method used in this function: myLemmatizer, bioLemmatizer
#integrated with best performed lemmatizer?
def getBOW(wordList,lem=bioLemmatizer,tagList=None):
    result={}
    for wi in range(len(wordList)):
        word=wordList[wi]
        #print word
        if tagList:
            posTag=tagList[wi][1]
        else:
            posTag=None
        #print posTag
        if type(word)==tuple:
            word=lemmBigram(word,lem)
            result[word]=result.get(word,0)
        elif word not in stopSet and len(word)>1:
            word=lem(word,posTag);#speed of biolemmatizer is too slow
            result[word]=result.get(word,0)+1;
    #print "overXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    return result;
#dict 2 is a small dictionary for the sake of efficiency
def mergeDict(dict1,dict2):
    for key in dict2:
        if key in dict1:
            dict1[key]=int(dict1[key])+int(dict2[key]);
        else:
            dict1[key]=int(dict2[key]);
    return dict1
    
def avg(dictionary,size):
    for k,v in dictionary.items():
        dictionary[k]=float(dictionary[k])/size;
    return dictionary
    
#TODO(KeSun):get a total word dict that includes every key word and its occurrence by:
#{Q1:{word1:occ1,word2:occ2,...},Q2:...}
def getTotalWordDict():
    pass

#get words that only occur n times for basic coarse dimension deduction
def removeRareWord(BOW,totalBowDict,n=0):
    if n>0:
        for i in range(1,5):
            deleteKeySet=set()
            for k,v in totalBowDict["Q"+str(i)].items():
                if v<n:
                    deleteKeySet.add(k)
            for everyBow in BOW["Q"+str(i)]:
                for deleteKey in everyBow.keys():
                    if deleteKey in deleteKeySet:
                        #print deleteKey
                        del everyBow[deleteKey];
            print "finished Q",i,": on ",time.strftime('%X %x %Z')            
    return BOW               
    
def countAverageScore(labelDict):
    avgScoreDict={}
    for i in range(1,5):
        totalScores=sum(labelDict["Q"+str(i)])
        numberOfAnswers=len(labelDict["Q"+str(i)]);
        avgScoreDict["Q"+str(i)]=float(totalScores)/float(numberOfAnswers);
    return avgScoreDict;
        
#the function below is to convert a list of strings(first 17 items) to an integer array 
def convertListToArray(stringList):
    intList=[];
    for w in stringList[:17]:
        intList.append(int(w));
    return intList
def ifQAnswered(response):
    if response:
        return True
    return False

#TODO(KeSun):To remove the referrence after the whole answer or response
def removeReferrence():
    pass

#preprocess to get the final BOW data representation
#the input is a list of dictionaries, every dict is the BOW of a certain answer 
#for a particular question.
#every questions have a bunch of standards for evaluations (n criterions)
#so there supposed to be 
def preprocess(addr,ifBigram=False):
    BOW={"Q1":[],"Q2":[],"Q3":[],"Q4":[]};#BOW is dict: {"Q1":[every answer bag of words dict...],"Q2":...}
    label={"Q1":[],"Q2":[],"Q3":[],"Q4":[]};#label is a dict:{"Q1":[every evaluation average for Q1]}
    totalBOW={"Q1":{},"Q2":{},"Q3":{},"Q4":{}}#every key word and its occurrence By:{Q1:{word1:occ1,word2:occ2,...},Q2:...}
    #the average for a answer is avg of (first i citerionsfor Qj) /5
    modi={}
    with open(addr)as rawFile:
        data=json.loads(rawFile.read());
        for k,v in data.items():#for everyone's submission, k is submitter's id
            answeredQuestions=[];
            try:
                for ka,va in v["answers"].items():#ka is in {Q1,Q2,Q3,Q4},va is the string of answer
                    #tempAnswer=convertToList(cleanData(va),16);
                    #another problem may occur here: the wrongly spelled long word could not be cleaned,should be clean again
                    (tempAnswer,tempTaggers,tempManTupDict)=convertToList(cleanData(va));
                    modi=mergeDict(modi,tempManTupDict)
                    #generate bigram bow by temAnswer list
                    if ifBigram:
                        #if want to json.dump the tuple key, you have to turn it to string
                        #so if you turns these keys of bigramList to string, you have to make a parser
                        #wen you want to read this file next time to turn string back to tuple
                        #If you don't want to turn back, it can still used as feature "(w1,w2)"
                        bigramList=bigramFeatureGenerator(tempAnswer,True);
                        tempAnswer.extend(bigramList)
                    #if ifBigram:
                        tempBOW=getBOW(tempAnswer,lem=myLemmatizer)
                        #make the tuple key to string.
                    else:
                        tempBOW=getBOW(tempAnswer,lem=myLemmatizer,tagList=tempTaggers);
                    #newList=[];
                    #different ka, different length, since someone only answer 2-3 questions
                    if ifQAnswered(va):
                        BOW.get(ka).append(tempBOW);
                        #print tempBOW
                        #print BOW
                        
                        totalBOW[ka]=mergeDict(totalBOW[ka],tempBOW);
                        answeredQuestions.append(ka);
                tempLabel={}
                tempAvgEvaluationQ=[];
                size=float(len(v["evaluations"]));
                for ke,ve in v["evaluations"].items():#ke is every evaluator's id
                    intVe=convertListToArray(ve);
                    tempAvgEvaluationQ.append(float('%.2f'%(float(sum(intVe[:6]))/6)));
                    tempAvgEvaluationQ.append(float('%.2f'%(float(sum(intVe[6:10]))/4)));
                    tempAvgEvaluationQ.append(float('%.2f'%(float(sum(intVe[10:13]))/3)));
                    tempAvgEvaluationQ.append(float('%.2f'%(float(sum(intVe[13:]))/4)));
                    for i in range(1,5):
                        q="Q"+str(i);
                        if q in answeredQuestions:
                            tempLabel[q]=tempLabel.get(q,0.0)+tempAvgEvaluationQ[i-1];
                tempLabel=avg(tempLabel,size);
                for qId,vMark in tempLabel.items():
                    label.get(qId).append(vMark);
            except KeyError:
                continue;
        #write the parsed data set into a json file.
    return BOW,label,totalBOW,modi
def remap_keys(mapping):
    return [{'key':k, 'value': v} for k, v in mapping.iteritems()]
#bigram feature should not include stopwords? "the Mythlation" is meaningless.

#main method for command line running this script
#parameters: 1. rawData: string address/rawData obj: dict; 2. ifBigram: bool
#3.n in removeRareWord(),(the occurrence number int set for the threshold for deleting rarely occurred word);
#4. write to addresses:strProcessedDataBigramAddr,strProcessedTotalDictBigramAddr or 
#strProcessedDataAddr,strProcessedTotalDictAddr

def helperInfor():
    print 'Usage: preprocess.py -a <string_address> -o <string_address> -t <string_address> [-b <True or False> -r <int>]'
    print 'The specification of every parameter:\n'
    print '\t-a:\t\tthe JSON file address of raw data extracted from submissions'
    print '\t-o:\t\tthe output JSON file address of preprocessed data'
    print '\t-t:\t\ttthe output JSON file address of total BOW for every questions'
    print '\t(option)-b:\t\tif need bigram feature'
    print '\t(option)-r:\t\tthe number of threshold(< this para) for removing all the features that rarely happen in the input data'
    print '\n'
    print '''The Example of Usage: python preprocess.py -a '/Users/ksun/Desktop/syd/syd/FInal_project/raw_json_data2.json' -o '/Users/ksun/Desktop/syd/syd/FInal_project/processed_bow_bi2.json' -t '/Users/ksun/Desktop/syd/syd/FInal_project/processed_total_bi2.json' -b True -r 5'''
def main(argv):
    rawJSONAddr=''
    writeToPreprocessedDataAddr=''
    writeToPreTotalDataAddr=''
    ifBigram=False
    rareWordThreshold=0
    try:
        opts,args=getopt.getopt(argv,'ha:o:t:b:r:')
    except getopt.GetoptError:
        helperInfor()
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-h':
            helperInfor();
            sys.exit(0)
        elif opt=='-a':
            rawJSONAddr=arg
        elif opt=='-o':
            writeToPreprocessedDataAddr=arg
        elif opt=='-t':
            writeToPreTotalDataAddr=arg
        elif opt=='-b':
            ifBigram=bool(arg)
        elif opt=='-r':
            rareWordThreshold=int(arg)
    if not (rawJSONAddr and writeToPreprocessedDataAddr and writeToPreTotalDataAddr):
        print 'The -a, -o, -t parameters are needed.'
        helperInfor()
        sys.exit(1)
    print "start preprocessing at: ",time.strftime('%X %x %Z')
    BOW,label,totalBOW,modi=preprocess(rawJSONAddr,ifBigram);
    print "basic preprocess done!"
    print "start to remove rare word at: ",time.strftime('%X %x %Z')
    BOW=removeRareWord(BOW,totalBOW,rareWordThreshold)
    data={}
    data["BOW"]=BOW
    data["label"]=label
    jsRW=JsonRW()
    jsRW.writeToJson(writeToPreprocessedDataAddr,data)
    jsRW=JsonRW()
    jsRW.writeToJson(writeToPreTotalDataAddr,totalBOW)
    print "done"
      
if __name__=='__main__':
    main(sys.argv[1:])
    #print "start preprocessing at: ",time.strftime('%X %x %Z')
    #BOW,label,totalBOW,modi=preprocess(strRawDataAddr,False);
    #print "preprocess done!"
    #print "start to remove rare word: ",time.strftime('%X %x %Z') 
    #BOW=removeRareWord(BOW,totalBOW,0)
    '''
    data={}
    data["BOW"]=BOW;
    data["label"]=label'''
    
    '''
    statistics={}
    statistics["average_score"]=countAverageScore(label);
    for i in range(1,5):
        print "Q",i," infor:"
        #print len(BOW["Q"+str(i)])
        #print len(label["Q"+str(i)])
        for j in range(3):
            print BOW["Q"+str(i)][j]
            print label["Q"+str(i)][j]
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"'''
    
    #with open(strProcessedDataAddr2,'w') as jsonFile1:
    #    json.dump(data,jsonFile1);
    #with open(strProcessedTotalDictAddr2,'w') as jsonFile2:
    #    json.dump(totalBOW,jsonFile2);
    
    #reMapModi=remap_keys(modi)
    #jsRW=jsonRW()
    #jsRW.writeToJson(modifiedWordAddr,reMapModi)
    '''
    jsRW=JsonRW()
    jsRW.writeToJson(strProcessedDataAddr2,data)
    
    jsRW=JsonRW()
    jsRW.writeToJson(strProcessedTotalDictAddr2,totalBOW)
    '''
    #when the file will be writen next time, you have to read it first,
    #then add the element into the statistics dictionary
    #finally,re-write it to file with "w"
    '''
    with open(statisticsAddr,'w') as jsonFile:
        json.dump(statistics,jsonFile);'''
    #print "\nDone."
    