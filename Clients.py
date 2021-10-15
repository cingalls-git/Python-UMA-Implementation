import DFHelpers as dfh
import pandas as pd
from datetime import datetime
from ClientTemplate import ClientTemplate

# Client subclass. Inherits from ClientTemplate superclass, adds any custom functionality for the client template.
class Client(ClientTemplate):
    def __init__(self, client, product, rounding, CashSymbol, WeightMultiplier, WeightColumnName, template, SymbolColumnName, mgrfilename = None, fileheader = True):   
        super().__init__(client, product, rounding, CashSymbol, WeightMultiplier, WeightColumnName, template, SymbolColumnName, mgrfilename = None, fileheader = True)
        if self.template == "Vestmark":
                self.clientdf = self.clientdf[[SymbolColumnName, self.WeightColumnName]] # reduce client dataframe down to needed columns
                self.clientdf.insert(len(self.clientdf.columns), 'DoNotBuy', 'FALSE') # add DoNotBuy column
                self.clientdf.insert(len(self.clientdf.columns), 'DoNotSell', 'FALSE') # add DoNotSell column
        
        elif self.template == "MMS":
            self.clientdf = self.clientdf[[self.SymbolColumnName, self.WeightColumnName, 'Notes']] # reduce client dataframe down to needed columns
            self.clientdf.insert(len(self.clientdf.columns), 'CUSIP', '') # add CUSIP column
            self.clientdf.insert(len(self.clientdf.columns), 'SEDOL', '') # add Sedol column

        elif self.template == "Parametric":
            self.fileheader = False # remove header from file
            self.mgrfilename = mgrfilename # set manager file name. To be used for Manager column.
            self.clientdf = self.clientdf[[self.SymbolColumnName, self.WeightColumnName, 'CUSIP', 'SecurityDesc']] # reduce client dataframe down to needed columns
            today = datetime.today().strftime('%Y%m%d') # set today in 'yyyymmdd' format. To be used for Date column.
            self.clientdf.insert(len(self.clientdf.columns), 'Date', today)
            self.clientdf.insert(len(self.clientdf.columns), 'Manager', self.mgrfilename)
            self.clientdf = dfh.Set_Value_in_DF(self.clientdf, self.SymbolColumnName, self.CashSymbol, 'CUSIP', 'CASH_USD') # set CUSIP value for cash ticker to 'CASH_USD'
            self.clientdf = dfh.Set_Value_in_DF(self.clientdf, self.SymbolColumnName, self.CashSymbol, 'SecurityDesc', 'U S DOLLAR') # set SecurityDesc value for cash ticker to 'U S DOLLAR'
        
        elif self.template == "SWT":
            self.clientdf = self.clientdf[[self.SymbolColumnName, self.WeightColumnName]] # reduce client dataframe down to needed columns
            self.clientdf.insert(len(self.clientdf.columns), 'Model ID', 2555)
            self.clientdf.insert(len(self.clientdf.columns), 'Model Name', "Westfield - MCG")
            self.clientdf.insert(len(self.clientdf.columns), 'Fund Name', '')
            self.clientdf.insert(len(self.clientdf.columns), 'Mgmt Style Code', 'Westfield - MCG')
            self.clientdf.insert(len(self.clientdf.columns), 'Share Class', '0')
            self.clientdf.insert(len(self.clientdf.columns), 'Lower Tolerance', '')
            self.clientdf.insert(len(self.clientdf.columns), 'Upper Tolerance', '')
            self.clientdf.insert(len(self.clientdf.columns), 'Model Notes', '')
            self.clientdf.insert(len(self.clientdf.columns), 'Model Type', '')
        
        elif self.template == "FTB":
            self.clientdf = self.clientdf[[self.SymbolColumnName, 'CUSIP', 'SecurityDesc','CalcPrice', self.WeightColumnName, 'Notes']] # reduce client dataframe down to needed columns
        
        elif self.template == "Harbor":
            self.t1df = pd.read_csv(self.p1 + "T-1/Disruptive UMA TEST File T-1.csv") # load yesterday's file in to new dataframe. Ending weight for T-1 will be used for start weight in T0 file. 
            self.clientdf = self.clientdf[[self.SymbolColumnName, self.WeightColumnName, 'SecurityDesc', 'CUSIP', 'Sedol', 'Notes']] # reduce client dataframe down to needed columns
            self.dt2 = datetime.today().strftime("%#m/%#d/%Y") # set date to 'dd/mm/yyyy' format. To be used for MODEL_DATE, TRADE_DATE columns.
            self.clientdf = self.clientdf.rename(columns={'SecurityDesc': 'SECURITY_NAME', 'Notes': 'NOTES'})
            self.clientdf.insert(len(self.clientdf.columns), 'MODEL_DATE', self.dt2)
            self.clientdf.insert(len(self.clientdf.columns), 'MODEL_CODE', 'DIF')
            self.clientdf.insert(len(self.clientdf.columns), 'SUBADVISOR_CODE', 'WEST')
            self.clientdf.insert(len(self.clientdf.columns), 'MODEL_NAME', 'Harbor Disruptive and Innovation Fund')
            self.clientdf.insert(len(self.clientdf.columns), 'ISIN', '')
            self.clientdf.insert(len(self.clientdf.columns), 'BLOOMBERG_ID', '')
            self.clientdf.insert(len(self.clientdf.columns), 'BLOOMBERG_YELLOW_KEY', '')
            self.clientdf.insert(len(self.clientdf.columns), 'PRIMARY_MIC', '')
            self.clientdf.insert(len(self.clientdf.columns), 'SECURITY_TYPE', '')
            self.clientdf.insert(len(self.clientdf.columns), 'TRADE_DATE', self.dt2)
            self.clientdf.insert(len(self.clientdf.columns), 'TRADE_TYPE', '')
            self.clientdf.insert(len(self.clientdf.columns), 'TRADING_CURRENCY', '')
            self.clientdf.insert(len(self.clientdf.columns), 'BOD_WEIGHT', self.t1df['ENDING_WEIGHT'])
            self.clientdf.insert(len(self.clientdf.columns), 'TRADED_WEIGHT', '')
            self.clientdf.to_csv(self.p1 + "T-1/Disruptive UMA TEST File T-1.csv", index=False, header = self.fileheader) # overwrite T-1 file with T0 file for use in T+1 file.


