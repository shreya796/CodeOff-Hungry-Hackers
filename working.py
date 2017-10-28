from flask import Flask, render_template, request
import requests
# import pro





from math import log
#import operator
#from .models import Personaldetails
#from django.core import serializers
#from django.http import HttpResponse



def createDataSet():
    #response = []
    #response['proposal_list'] = serializers.serialize("json", Personaldetails.objects.all())
    #return HttpResponse(response, content_type="application/json")
   # qs = Personaldetails.objects.all()


    #qs=Personaldetails.objects.values_list('Gender','RelationshipStatus','Occupation','Student','City','Age','Score','Resultp')
    #dataSet = list(qs)
    dataSet = [['apple', 'low','Scab'],
               ['Potato', 'medium','Leaf Blights'],
               ['Wheat', 'high','Yel0 dwarf (virus)'],
              ['Rice', 'medium','Foliage diseases'],
               ]
    labels = ['crop','temp','disease']
    #change to discrete values

    #vlqs = qs.values_list()
    #dataSet = list(vlqs)
    #dataSet = [['boy', 'college','married', 'yes'],
              # ['girl', 'school', 'single', 'yes'],
             #  ['boy', 'school', 'relation', 'no'],
             #  ['girl', 'college', 'single', 'yes'],
              # ]
    #labels = ['gender', 'study', 'relationshipstatus','ans']
    # change to discrete values
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:  # the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)  # log base 2
    return shannonEnt


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec1=list(reducedFeatVec)  # chop out axis used for splitting
            reducedFeatVec1.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec1)
            #reducedFeatVec=tuple(reducedFeatVec1)
    return retDataSet



def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # the last column is used for the labels
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0;
    bestFeature = -1
    for i in range(numFeatures):  # iterate over all the features
        featList = [example[i] for example in dataSet]  # create a list of all the examples of this feature
        uniqueVals = set(featList)  # get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)


        infoGain = baseEntropy - newEntropy  # calculate the info gain; ie reduction in entropy
        """
        print("feature : " + str(i))
        print("baseEntropy : "+str(baseEntropy))
        print("newEntropy : " + str(newEntropy))
        print("infoGain : " + str(infoGain))
        """
        if (infoGain > bestInfoGain):  # compare this to the best gain so far
            bestInfoGain = infoGain  # if better than current best, set to best
            bestFeature = i
    return bestFeature  # returns an integer


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    # extracting data
    print("dataSet",dataSet)
    classList = [example[-1] for example in dataSet]
    print("classlist:",classList)
    if classList.count(classList[0]) == len(classList):
        return classList[0]  # stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1:  # stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    # use Information Gain
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]

    #build a tree recursively
    myTree = {bestFeatLabel: {}}
    #print("myTree : "+labels[bestFeat])
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    #print("featValues: "+str(featValues))
    uniqueVals = set(featValues)
    #print("uniqueVals: " + str(uniqueVals))
    for value in uniqueVals:
        subLabels = labels[:]  # copy all of labels, so trees don't mess up existing labels
        #print("subLabels"+str(subLabels))
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
        #print("myTree : " + str(myTree))
    return myTree


def classify(inputTree, featLabels, testVec):
    print("inputTree :", list(inputTree.keys()))
    firstStr = list(inputTree.keys())[0]
    print("fistStr : "+firstStr)
    secondDict = inputTree[firstStr]
    print("secondDict : " + str(secondDict))
    featIndex = featLabels.index(firstStr)
    print("featIndex : " + str(featIndex))
    key = testVec[featIndex]
    print("key : " + str(key))
    valueOfFeat = secondDict[key]
    print("valueOfFeat : " + str(valueOfFeat))
    if isinstance(valueOfFeat, dict):
        #print("is instance: "+str(valueOfFeat))
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        #print("is Not instance: " + valueOfFeat)
        classLabel = valueOfFeat
    return classLabel


def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

# collect data



def decision(data):
    # data=['Wheat','high', 'high', 'low']
    myData, labels = createDataSet()

#build a tree
    mytree = createTree(myData, labels)
    print(mytree)

   # print("Thanks, now I can recognize winter family photo, give me any photo")

#run test

# test with winter family photo
   # answer = classify(mytree,['gender', 'study', 'relationshipstatus'], ['boy', 'college', 'married'])
   # print("Hi, the answer is "+ answer + ", depressed")

# test with cartoon characters winter pictures
   # answer = classify(mytree, ['gender', 'study', 'relationshipstatus'], ['girl', 'school', 'relation'])
    #print("Hi, the answer is "+ answer + ", depressed")
#
    #answer = classify(mytree,['id','name', 'gender','relationshipstatus','occupation','student','city','age','Email_id','score'], [5 ,'ananya','male','Married','Professional','NA','mm' ,4,'abc@gmail.com'])
    answer = classify(mytree,['crop','temp'], data)
    print(answer)





















app = Flask(__name__)
data=[]
s1=""
s2=""
s3=""
@app.route('/temperature', methods=['GET'])
def temperature():
    #zipcode = input("enter zip")
    zipcode = "01234"
    r = requests.get('http://samples.openweathermap.org/data/2.5/weather?zip=zipcode,us&appid=b1b15e88fa797225412429c1c50c122a1')
    json_object = r.json()
    # print(json_object)
    main = json_object['main']

    temp_k = main['temp']
    temp_f = (temp_k - 273.15) * 1.8 + 32
    # print(temp_f)
    # humid = float(json_object['humidity'])
    if temp_f <80:
    	s1="low"
    elif temp_f>=80 & temp_f<100:
    	s1="medium"
    elif temp_f>=100:
    	s1="high"
    data.append("Rice")
    data.append(s1)
    """
    pressure = (float['pressure'])
    if pressure<500:
    	s2="low" 
    elif pressure>=500 & pressure<750:
    	s2="medium"
    elif pressure>=750 :
    	s2="high"
    print(s2)
    data.append(s2)
    humid = float(json_object['humidity'])
    if humid<50 :
    	s3="low"
    elif humid>=50 & temp_f<75:
    	s3="medium"
    elif humid>=75:
    	s3="high"
        print(s3)
    data.append(s3)
    """
  
    print(data)
    decision(data)
    return render_template('temperature.html')



 

if __name__ == '__main__':
    app.run(debug=True)


temperature()


















