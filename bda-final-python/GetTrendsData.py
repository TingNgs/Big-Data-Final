from pytrends.request import TrendReq
import pandas as pd
import statistics
import time
import json

def GetKeywordsTrend(keywordsList,timeFrame,location,pytrend):
    pytrend.build_payload(keywordsList, cat=47, timeframe=timeFrame ,geo=location)
    interest_over_time_df = pytrend.interest_over_time()
    return interest_over_time_df

def FindTarget(pList,start):
    for i in range(start,len(pList)):
        for j in range(len(pList[i]['data'])):
            if(pList[i]['data'][j] == 100):
                return {"x":i,"y":j}
    print("error")

def mean_sort(t):
    return t['mean']

def GetTrendsData(carNames,timeFrame,location):
    pytrend = TrendReq()
    keywordList = []
    pList=[]
    targetXY = {"x":0,"y":0}
    dateTimeList = []
    endWord = carNames[len(carNames)-1]
    for keyword in carNames:
        keywordList.append(keyword)
        if(len(keywordList) == 5 or keyword==endWord):
            newTarget = False
            tempDF = GetKeywordsTrend(keywordList,timeFrame,location,pytrend)
            if(len(pList) == 0):
                newTarget = True
                dateTimeList = tempDF.index.strftime("%d/%m/%Y, %H:%M:%S").tolist()
                try:
                    dataList = tempDF[keywordList[0]].tolist()
                except:
                    dataList = [0 for n in range(len(dateTimeList))]
                    print(keywordList[0])
                pList.append({"name":keywordList[0],"data":dataList,"mean":0})
                
            else:
                tempList = tempDF[keywordList[0]].tolist()
                if(tempList[targetXY['y']] != 100): # check if 100 is still 100, if not change all pList
                    newTarget = True
                    if(100 in tempList):
                        print("err",keywordList[0])
                        #pList[targetXY['x']]['data'] = tempList
                    else:
                        tempP = tempList[targetXY['y']]/100
                        for i in range(len(pList)):
                            for j in range(len(pList[i]['data'])):
                                pList[i]['data'][j] *= tempP
            
            for i in range (1,len(keywordList)): # Push all data into pList
                dataList = []
                try:
                    dataList = tempDF[keywordList[i]].tolist()
                except:
                    dataList = [0 for n in range(len(dateTimeList))]
                pList.append({"name":keywordList[i],"data":dataList,"mean":0})
                
            if(newTarget):
                targetXY = FindTarget(pList,targetXY['x'])# Find the position of 100
            # Clean up keywordList, append the top of pList to keywordList
            keywordList = []
            keywordList.append(pList[targetXY['x']]['name'])
    for i in range (len(pList)): # Cal the new mean of all pList
        pList[i]['mean'] = statistics.mean(pList[i]['data'])
    pList.sort(key = mean_sort,reverse = True)# Sort pList by mean
    return [dateTimeList,pList]

#print(GetTrendsData(['Aixam AIXAM COMPACT','Aixam AIXAM COUPE','Arcfox GT','Arcfox GT RACEEDITION','Artega Scalo'],"today 12-m",""))

