from os import error
from numpy.matrixlib import defmatrix
from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd
from scipy.stats import gmean
import numpy as np
from numpy_financial import npv
stockName = input('Enter a stock ticker: ')
fd = FundamentalData(key='ALPHAVANTAGE API KEY')
data, meta_data = fd.get_company_overview(str(stockName))
incomee, meta_datat = fd.get_income_statement_annual(str(stockName))
income = incomee.fillna(0)
balancee, meta_datata = fd.get_balance_sheet_annual(str(stockName))
balance = balancee.fillna(0)

cashh, meta_datatat = fd.get_cash_flow_annual(str(stockName))
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

discountRatee = input("Discount rate: ")
discountRate = float(discountRatee)/100
terminalGRR = input("Terminal growth rate: ")
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
print(intrinsicValue)
