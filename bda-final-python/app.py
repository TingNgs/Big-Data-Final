from flask import Flask
from flask import jsonify
from flask import request
from GetTrendsData import GetTrendsData
import json

app = Flask(__name__)

@app.route("/get_car_data",methods=['Get'])
def GetCarsData():
    with open('./data/CarNameData.txt') as json_file:  
        return jsonify(json.load(json_file))

@app.route("/get_brand_data",methods=['Get'])
def GetBrandData():
    with open('./data/BrandData.txt') as json_file:  
        return jsonify(json.load(json_file))

@app.route("/get_one_month_data",methods=['Get'])
def GetOneMonthData():
    with open('./data/OneMonthData.txt') as json_file:  
        return jsonify(json.load(json_file))

@app.route("/get_one_month_brand_data",methods=['Get'])
def GetOneMonthBrandData():
    with open('./data/BrandOneMonthData.txt') as json_file:  
        return jsonify(json.load(json_file))

@app.route("/get_trends_data",methods=['POST'])
def GetTrendData():
    data = request.get_json()
    return jsonify(GetTrendsData(data['carNames'],data['timeFrame']))

if __name__ == "__main__":
    app.run()
