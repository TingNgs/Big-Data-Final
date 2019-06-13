from pytrends.request import TrendReq
import pandas as pd
import json
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

import warnings
warnings.filterwarnings('ignore')


def GetKeywordsTrend(keywordsList, timeFrame, location, pytrend):
    pytrend.build_payload(keywordsList, cat=47,
                          timeframe=timeFrame, geo=location)
    interest_over_time_df = pytrend.interest_over_time()
    return interest_over_time_df


preResult = []


def test(data, p, d, q):
    X = data
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    try:
        model = ARIMA(history, order=(p, d, q))
        model_fit = model.fit(disp=0)
        step = (len(X)-size)
        predictions = model_fit.forecast(steps=step)[0]
        error = mean_squared_error(test, predictions)
        print({'aic': model_fit.aic, 'error': error, 'p': p, 'd': d, 'q': q})
        return {'aic': model_fit.aic, 'error': error, 'p': p, 'd': d, 'q': q}
    except:
        return 0


def Draw(data, p, d, q, step):
    predictions = [0]
    try:
        model = ARIMA(data, order=(p, d, q))
        model_fit = model.fit(disp=0)
        predictions = model_fit.forecast(steps=step)[0]
        error = mean_squared_error(test, predictions)
    except:
        print()
    # plot
    return predictions
    '''pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    print(predictions)
    pyplot.show()'''


def mean_sort(t):
    return t['error']


def GetMax(data):
    DataError = []
    maxData = {'error': 9999999999, 'p': 0, 'd': 0, 'q': 0}
    aicData = {'aic': 9999999999, 'p': 0, 'd': 0, 'q': 0}
    for i in range(6):
        for j in range(3):
            for k in range(3):
                tempData = test(data, i, j, k)
                if(tempData != 0):
                    DataError.append(tempData)
    for datae in DataError:

        if(maxData['error'] > datae['error']):
            maxData = datae
        if(aicData['aic'] > datae['aic']):
            aicData = datae
    return {'aic': aicData, 'error': maxData}


def GetPD(name, data, timeFrame):
    tempData = GetMax(data)
    step = 0
    if(timeFrame == "now 1-d"):
        step = int(len(data)/2)
    if(timeFrame == "now 7-d"):
        step = int((len(data)/7)*3)
    if(timeFrame == "today 1-m" or timeFrame == "today 3-m"):
        step = int(len(data)/3)
    if(timeFrame == "today 12-m"):
        step = int(len(data)/3)
    if(timeFrame == "today 5-y"):
        step = int(len(data)/5)
    print(step)
    tempAns = Draw(data, tempData['aic']['p'],
                   tempData['aic']['d'], tempData['aic']['q'], step)
    if(len(tempAns) == 1 and tempAns[0] == 0):
        tempAns = Draw(data, tempData['error']['p'],
                   tempData['error']['d'], tempData['error']['q'], step)
    if(len(tempAns) == 1 and tempAns[0] == 0):
        mean = statistics.mean(data)
        tempAns = []
        for i in range(step):
            tempAns.append(mean)
    return tempAns
    # return Draw(data, tempData['p'], tempData['d'], tempData['q'])


def GetTrendsRateData(carNames, timeFrame, location):
    pytrend = TrendReq()
    result = []
    tempDF = GetKeywordsTrend(carNames, timeFrame, location, pytrend)
    tempDateList = tempDF.index.tolist()
    dateValue = tempDateList[1] - tempDateList[0]
    
    lastDate = tempDateList[len(tempDateList)-1]
    date = []
    for keyword in carNames:
        temp = 0
        predictions = [0]
        ans = []
        try:
            dataList = tempDF[keyword].tolist()
            print(keyword)
            temp = ((dataList[len(dataList)-1] -
                     dataList[0]) / dataList[0]) * 100
            predictions = GetPD(keyword, dataList, timeFrame)
            for p in predictions:
                ans.append(p)
        except:
            temp = 0
        result.append({'name': keyword, 'rate': temp,
                       'predictions': ans})
    for aaa in result[0]['predictions']:
        lastDate = lastDate + dateValue
        date.append(lastDate.strftime("%d/%m/%Y, %H:%M:%S"))

    return [date, result]
