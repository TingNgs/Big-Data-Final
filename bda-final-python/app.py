from flask import Flask
from flask import jsonify
from flask import request
from GetTrendsData import GetTrendsData
import json

app = Flask(__name__)

@app.route("/get_car_data")
def GetCarsData():
    with open('CarNameData.txt') as json_file:  
        carNames = json.load(json_file)
        return jsonify(carNames)

@app.route("/get_trends_data",methods=['POST'])
def GetTrendData():
    data = request.get_json()
    return jsonify(GetTrendsData(data['carNames'],data['timeFrame']))

if __name__ == "__main__":
    app.run()
