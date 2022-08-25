from re import X
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
from charset_normalizer import from_path
import requests
import csv
import pandas as pd
from numpy_financial import npv
import numpy as np
import time
from scipy.stats.mstats import gmean

fd = FundamentalData(key= 'D47XV4JKJ6A3NMRJ')
ts = TimeSeries(key='D47XV4JKJ6A3NMRJ')


table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv('S&P500-Info.csv')
df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])
x = (df['Symbol'])
def valuation(stocks):
    for stock in stocks:
        
        data, meta_data = fd.get_company_overview(str(stock))
        prices=[]
        stockPrices, meta_data = ts.get_daily(str(stock), 'full')
        for i in stockPrices.items(): 
            prices.append(i[1]['4. close'])
        incomee, meta_datat = fd.get_income_statement_annual(str(stock))
        income = incomee.fillna(0)
        balancee, meta_datata = fd.get_balance_sheet_annual(str(stock))
        balance = balancee.fillna(0)
        cashh, meta_datatat = fd.get_cash_flow_annual(str(stock))
        cash = cashh.fillna(0)
        pd.set_option('display.max_columns', 500)
        CAPEX = cash['capitalExpenditures'].iloc[0]
        margin = data['ProfitMargin']
        sharesOutstanding = data['SharesOutstanding']
        revenues = income['totalRevenue']
        operatingCF = cash['operatingCashflow']
        yearoneCF = operatingCF.iloc[0]
        yeartwoCF = operatingCF.iloc[1]
        yearthreeCF = operatingCF.iloc[2]
        yearfourCF = operatingCF.iloc[3]
        yearfiveCF = operatingCF.iloc[4]
        yearone = revenues.iloc[0]
        yeartwo = revenues.iloc[1]
        yearthree = revenues.iloc[2]
        yearfour = revenues.iloc[3]
        yearfive = revenues.iloc[4]
        CFMargina = int(yearoneCF)/int(yearone)
        CFMarginb = int(yeartwoCF)/int(yeartwo)
        CFMarginc = int(yearthreeCF)/int(yearthree)
        CFMargind = int(yearfourCF)/int(yearfour)
        CFMargine = int(yearfiveCF)/int(yearfive)
        CFMargin = (CFMargina + CFMarginb + CFMarginc + CFMargind + CFMargine)/5

        #discountRatee = input("Discount rate: ")
        discountRatee = 6
        discountRate = float(discountRatee)/100
        #terminalGRR = input("Terminal growth rate: ")
        terminalGRR = 2
        terminalGR = float(terminalGRR)/100

        a = int(yearone)/int(yeartwo)
        b = int(yeartwo)/int(yearthree)
        c = int(yearthree)/int(yearfour)
        d = int(yearfour)/int(yearfive)
        growthRate = gmean([d,c,b,a])

        FYone = ((growthRate**1*int(yearone))*float(CFMargin)) - int(CAPEX)
        FYtwo = ((growthRate**2*int(yearone))*float(CFMargin)) - int(CAPEX)
        FYthree = ((growthRate**3*int(yearone))*float(CFMargin)) - int(CAPEX)
        FYfour = ((growthRate**4*int(yearone))*float(CFMargin)) - int(CAPEX)
        FYfive = ((growthRate**5*int(yearone))*float(CFMargin)) - int(CAPEX)
        NPV = npv(discountRate, [int(FYone), int(FYtwo), int(FYthree), int(FYfour), int(FYfive)])
        tVal = FYfive*(1+terminalGR)/(discountRate-terminalGR)
        PVTV = tVal/(1+discountRate)**5
        totalEquityVal = PVTV + NPV


        cashEquiv = balance['cashAndCashEquivalentsAtCarryingValue'].iloc[0]
        shortTermInvestments = balance['cashAndShortTermInvestments'].iloc[0]
        shortlongtermdebt = balance['shortLongTermDebtTotal'].iloc[0]
        currentDebt = balance['currentDebt'].iloc[0]
        currentlongtermdebt  = balance['currentLongTermDebt'].iloc[0]
        longtermdebtnoncurrent = balance['longTermDebtNoncurrent'].iloc[0]
        netCash = int(cashEquiv) + int(shortTermInvestments) - int(shortlongtermdebt) - int(currentDebt) - int(currentlongtermdebt) - int(longtermdebtnoncurrent)
        intrinsicValue = (int(netCash) + int(totalEquityVal))/int(sharesOutstanding)
        print(f" {stock} : {intrinsicValue}   {((intrinsicValue - float(prices[0]))/float(prices[0]))*100}%")


for symbol in x:
  valuation(symbol)


