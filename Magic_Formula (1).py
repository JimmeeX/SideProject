# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# https://github.com/dpguthrie/yahooquery

import pandas_datareader as pdr
import datetime as dt
import pandas as pd
from yahooquery import Ticker

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width',1000)

# Add CSV File Implementation 

df_stocks = pd.read_csv(r"/Users/matthew/Documents/UNI/Coding/Stock.csv")
df_stocks.columns = ["Stocks"]

stocklist = df_stocks["Stocks"].values.tolist()
tickers = Ticker(stocklist)


# Key Stats Data 
keystats = tickers.key_stats
esg_scores = tickers.summary_detail

# Storing the income statement data into a dataframe
df_balance = tickers.balance_sheet().transpose()
df_income = tickers.income_statement().transpose()
df_cashflow = tickers.cash_flow().transpose()
df_keystats = pd.DataFrame.from_dict(keystats)
df_summary = pd.DataFrame(tickers.summary_detail)


# Defining all the empty directories 
all_stat_income = {}
all_stat_balance = {}
all_stat_cashflow = {}
all_stat_keystat = {}
all_stat_summary = {}


# All the data directories 
stats_income = ["asOfDate", "EBIT", "NetIncome", "NetIncomeCommonStockholders"]
stats_balance = ["asOfDate", "CurrentAssets", "CurrentLiabilities", "NetPPE","StockholdersEquity","TotalDebt"]
stats_cashflow = ["asOfDate", "OperatingCashFlow", "CapitalExpenditure", "NetIncome"]
stats_keystats = ["bookValue", "enterpriseValue"]
stats_summary = ["marketCap"]

# Sorting data into one dataframe, divide up the data into sectors

for stat_income in stats_income:
    all_stat_income[stat_income] = df_income.loc[stat_income]
        
for stat_balance in stats_balance:
    all_stat_balance[stat_balance] = df_balance.loc[stat_balance]
    
for stat_cashflow in stats_cashflow: 
    all_stat_cashflow[stat_cashflow] = df_cashflow.loc[stat_cashflow]
    
for stat_keystat in stats_keystats:
    all_stat_keystat[stat_keystat] = df_keystats.loc[stat_keystat]
    
for stat_summary in stats_summary:
    all_stat_summary[stat_summary] = df_summary.loc[stat_summary]



# Adding the data into a dataframe
# final_stat_income = pd.DataFrame(all_stat_income).transpose()
# final_stat_balance = pd.DataFrame(all_stat_balance).transpose()
# final_stat_cashflow = pd.DataFrame(all_stat_cashflow).transpose()
# final_stat_keystat = pd.DataFrame(all_stat_keystat).transpose()

final_stat_income = pd.DataFrame(all_stat_income)
final_stat_balance = pd.DataFrame(all_stat_balance)
final_stat_cashflow = pd.DataFrame(all_stat_cashflow)


# These two dataframes do not require 
final_stat_keystat = pd.DataFrame(all_stat_keystat).sort_index()
final_stat_summary = pd.DataFrame(all_stat_summary).sort_index()

# Basically need a functionality to sort out the most recent data if possible 
# Possibly a for loop in this case??? 
# Alot of companies have different reporting dates its not possible to sort by dates 
target_date = final_stat_income['asOfDate'][4]
target_date_balance = final_stat_balance['asOfDate'][4]

final_stat_income_recent = final_stat_income[final_stat_income['asOfDate'] == target_date].sort_index()
final_stat_balance_recent = final_stat_balance[final_stat_balance['asOfDate'] == target_date_balance].sort_index()
final_stat_cashflow_recent = final_stat_cashflow[final_stat_cashflow['asOfDate'] == target_date].sort_index()

# For loop? 

# Probably should try to combine all the data 
combine = [final_stat_income_recent, final_stat_balance_recent, final_stat_keystat, final_stat_summary]

df_combine = pd.concat(combine,axis=1)

# Calculations for the Variables, Variables required 
# TEV  - Total Enterprise Value, EBIT - Earnings Before Income Tax 
# Formula for TEV is MarketCap (Summary) + Total Debt (Balance) - Current Assets (Balance) - Current Liabilities (Balance) 
# EBIT - Can be found directly form the income statement 
# Earning Yield = EBIT/TEV
# ROC = EBIT/ PPE + Current Assets - Current Liabilities

# Create new dataframe for the calculations 
df_calc = pd.DataFrame()

df_calc["EBIT"] = df_combine["EBIT"] 
df_calc["TEV"] = df_combine["marketCap"].fillna(0) + df_combine["TotalDebt"].fillna(0) - df_combine["CurrentAssets"].fillna(0) - df_combine["CurrentLiabilities"].fillna(0)
df_calc["Net Assets and Working Capital"] = df_combine["NetPPE"].fillna(0) + df_combine["CurrentAssets"].fillna(0) - df_combine["CurrentLiabilities"].fillna(0)
df_calc["Earnings Yield"] = df_calc["EBIT"] / df_calc["TEV"]
df_calc["Return on Capital"] = df_calc["EBIT"] / df_calc["Net Assets and Working Capital"]
df_calc["EC_Rank"] = df_calc["Earnings Yield"].rank(ascending = False, na_option = "bottom")
df_calc["ROC_Rank"] = df_calc["Return on Capital"].rank(ascending = False,na_option='bottom')
df_calc["Total"] = (df_calc["EC_Rank"] + df_calc["ROC_Rank"])
df_calc["Rank"] = df_calc["Total"].rank(method = "first")
value_stocks = df_calc.sort_values("Rank").iloc[:,[8,3,4,7]]



print(value_stocks)
x = df_calc["Earnings Yield"].mean()
print(x)


#Printing Data Into CSV File to Open on Excel
df_calc.to_csv(r"/Users/matthew/Documents/UNI/Coding/Calculations.csv")
value_stocks.to_csv(r"/Users/matthew/Documents/UNI/Coding/BlankStock.csv")

# Future Ideas Create A Model for it 
# Hypothetically Invest 10K dollars into the top 5 stocks and Track Returns
# Maybe Go Back To Previous Data
# Re adjust every 6 Months 




# Need to start ranking the calculations 

# date = ["asOfDate"]
# stat = ["EBITDA"]
# stat1 = ["DepreciationAndAmortization"]


# all_stat[0] = df_income.loc[date]
# all_stat[1] = df_income.loc[stat]
# all_stat[2] = df_cashflow.loc[stat1]

# final_df = pd.concat(all_stat.values(), ignore_index = False)



# EBIT - Income Statement
# MarketCap - Summary - Data. 
# Depreication and Ammortisation - Cash Flow 
# NetIncome - Income Statement 
# CashFlowOps - Cash Flow 
# Capex - Cashflow 
# Current Assets - Balance Sheet 
# Current Liabilities - Balance Sheet 
# PPE - Balance Sheet 
# Bookvalue - Key Stats 
# EnterpriseValue - Key Stats 

