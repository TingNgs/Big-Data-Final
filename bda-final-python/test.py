from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')


DataError = []
def test(p,d,q):
    series = read_csv('test.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    X = series.values
    #print(series)
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    
    try:
        for t in range(len(test)):
            model = ARIMA(history, order=(p,d,q))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            #print('predicted=%f, expected=%f' % (yhat, obs))
        error = mean_squared_error(test, predictions)
        #print('Test MSE: %.3f' % error)
        print(error ,p,d,q)
        DataError.append({'error':error,'p':p,'d':d,'q':q})
        
    except:
        print()
    '''# plot
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()'''

for i in range(6):
    for j in range(3):
        for k in range(3):
            test(i,j,k)
for data in DataError:
    print(data)
