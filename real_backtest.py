import pandas as pd
import pyfolio
import matplotlib
import numpy as np
matplotlib.use('Agg')


def get_daily_return(df):
    df['daily_return']=df.account_value.pct_change(1)
    #df=df.dropna()
    print('Sharpe: ',(252**0.5)*df['daily_return'].mean()/ df['daily_return'].std())
    return df
def backtest_strat(df):
    strategy_ret= df.copy()
    strategy_ret['Date'] = pd.to_datetime(strategy_ret['Date'])
    strategy_ret.set_index('Date', drop = False, inplace = True)
    strategy_ret.index = strategy_ret.index.tz_localize('UTC')
    del strategy_ret['Date']
    ts = pd.Series(strategy_ret['daily_return'].values, index=strategy_ret.index)
    return ts
def get_account_value(model_name):
    df_account_value=pd.DataFrame()
    for i in range(rebalance_window+validation_window, len(unique_trade_date)+1,rebalance_window):
        temp = pd.read_csv('results/account_value_trade_{}_{}.csv'.format(model_name,i))
        df_account_value = df_account_value.append(temp,ignore_index=True)
    df_account_value = pd.DataFrame({'account_value':df_account_value['0']})
    sharpe=(252**0.5)*df_account_value.account_value.pct_change(1).mean()/df_account_value.account_value.pct_change(1).std()
    print(sharpe)
    df_account_value=df_account_value.join(df_trade_date[63:].reset_index(drop=True))
    return df_account_value

dji = pd.read_csv("data/^DJI.csv")
test_dji = dji[(dji['Date']>='2016-01-01') & (dji['Date']<='2020-06-30')]
test_dji = test_dji.reset_index(drop=True)
print(test_dji.shape)
print(test_dji.head())
test_dji['daily_return']=test_dji['Adj Close'].pct_change(1)
dow_strat = backtest_strat(test_dji)
df=pd.read_csv('data/dow_30_2009_2020.csv')
rebalance_window = 63
validation_window = 63
unique_trade_date = df[(df.datadate > 20151001)&(df.datadate <= 20200707)].datadate.unique()
df_trade_date = pd.DataFrame({'datadate':unique_trade_date})
ensemble_account_value = get_account_value('ensemble')
ensemble_account_value.account_value.plot()
ensemble_account_value = get_daily_return(ensemble_account_value)
ensemble_account_value['Date'] = test_dji['Date']
ensemble_account_value.head()
ensemble_strat = backtest_strat(ensemble_account_value[0:1097])
with pyfolio.plotting.plotting_context(font_scale=1.1):
    pyfolio.create_full_tear_sheet(returns = ensemble_strat,
                                   benchmark_rets=dow_strat, set_context=False)
