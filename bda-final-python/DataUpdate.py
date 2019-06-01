from GetTrendsData import GetTrendsData
import json
import statistics
with open('./data/CarNameData.txt') as json_file:  
    dataArray = json.load(json_file)
    oneMonthData = GetTrendsData(dataArray,"today 1-m")
    with open('./data/OneMonthData.txt', 'w') as outfile:  
        json.dump(oneMonthData, outfile)

def mean_sort(t):
    return t['mean']

with open('./data/OneMonthData.txt') as json_file:
    maxValue = 0
    dataArray = json.load(json_file)
    brandArray = {'brandName':[], 'brandTrend':[]}
    brandTrend = []
    for data in dataArray[1] :
        brandName = data['name'].split(' ', 1)[0]
        if(brandName in brandArray['brandName']):
            index = brandArray['brandName'].index(brandName)
            for i in range(len(data['data'])):
                brandArray['brandTrend'][index]['value'][i] += data['data'][i]
                if(brandArray['brandTrend'][index]['value'][i] > maxValue):
                    maxValue = brandArray['brandTrend'][index]['value'][i]
            brandArray['brandTrend'][index]['count'] += 1
        else:
            brandArray['brandName'].append(brandName)
            brandArray['brandTrend'].append({'value' : data['data'], 'count' : 1})
            
    rate = 100/maxValue
    for i in range(len(brandArray['brandTrend'])):
        for j in range(len(brandArray['brandTrend'][i]['value'])):
            brandArray['brandTrend'][i]['value'][j] *= rate
        mean = statistics.mean(brandArray['brandTrend'][i]['value'])
        brandTrend.append({'name' : brandArray['brandName'][i], 'data': brandArray['brandTrend'][i]['value'],'mean': mean})
    brandTrend.sort(key = mean_sort,reverse = True)
    brandTrend = [dataArray[0],brandTrend]
    with open('./data/BrandOneMonthData.txt', 'w') as outfile:  
        json.dump(brandTrend, outfile)
