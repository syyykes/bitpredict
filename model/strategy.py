import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import numpy as np


def fit_and_trade(data, cols, split, threshold):
    '''
    Fits and backtests a theoretical trading strategy
    '''
    data = data[data.width > 0]
    X = data[cols]
    y = data.mid30
    X_train = X.iloc[:split]
    X_test = X.iloc[split:]
    y_train = y.iloc[:split]
    y_test = y.iloc[split:]
    regressor = RandomForestRegressor(n_estimators=100,
                                      min_samples_leaf=500,
                                      random_state=42,
                                      n_jobs=-1)
    regressor.fit(X_train.values, y_train.values)
    trade(X_test.values, y_test.values, regressor, threshold)


def trade(X, y, index, model, threshold):
    '''
    Backtests a theoretical trading strategy
    '''
    print 'r-squared', model.score(X, y)
    preds = model.predict(X)
    trades = np.zeros(len(preds))
    # active_widths = np.zeros(len(preds))
    count = 0
    active = False
    for i, pred in enumerate(preds):
        if active:
            count += 1
            if count == 30:
                count = 0
                active = False
        elif abs(pred) > threshold:
            active = True
            trades[i] = np.sign(pred)

    returns = trades*y
    mean_return = returns[trades != 0].mean()
    print 'average return', mean_return
    profit = np.cumsum(returns)
    plt.plot(index, profit)
    plt.show()
