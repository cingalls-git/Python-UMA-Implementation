import pandas as pd
from datetime import datetime
from pathlib import Path
import DFHelpers as dfh
import os

"""
Superclass for client template. All clients will inherit ClientTemplate superclass.
    - client: String parameter for the client name.
    - product: String parameter identifying the product that the client subscribes to. Used to pull the correct source file e.g. "Mid" or "Large"
    - CashSymbol: Client's required symbol for cash e.g. "USD CASH"
    - Weight Multiplier: Float parmeter for the multiplier of the weight column. For clients that add up to 100 (representing 100%), WeightMultiplier == 1. For clients that add up to 1 (representing 100%), WeightMultiplier == .01.
    - rounding: Integer parameter for rounding precision. Works in tandem with weight multiplier. If the multiplier is 1 and you want to go out to 3 / 1000 of a percentage point, rounding == 3. If the multiplier is .01 and you want to round to the nearest 
      thousandth of a percent, the multiplier is 5 (3 + 2).
    - WeightColumnName: String parameter for the client's required name for the weight column.
    - template: String parameter for the template output for the client. It will correspond to the template in the Client subclass.
    - mgrfilename: String parameter for clietn's that use a manager moniker in the output, mgrfilename can be used to input in to the file. Specific to the Parametric template but can be applied to other clients. Optional. Default is None.
    - fileheader: boolean parameter for if the headers are output in the output file. Optional. Default is True.

"""

class ClientTemplate(object):
    def __init__(self, client, product, rounding, CashSymbol, WeightMultiplier, WeightColumnName, template, SymbolColumnName = "Symbol", mgrfilename = None, fileheader = True):
        self.client = client
        self.product = product
        self.rounding = rounding
        self.CashSymbol = CashSymbol
        self.WeightMultiplier = WeightMultiplier
        self.WeightColumnName = WeightColumnName
        self.template = template
        self.mgrfilename = mgrfilename
        self.fileheader = fileheader
        self.SymbolColumnName = SymbolColumnName
        
        # Setting up filename and path for saving data
        self.uprofile = os.environ['USERPROFILE']
        self.uprofile = self.uprofile.replace("\\", "/")
        self.p1 = self.uprofile + "/OneDrive - WESTFIELD CAPITAL MANAGEMENT/TAM/UMA/Python Implementation/"
        self.p2 =  " UMA TEST File.csv"
        self.dt = datetime.today().strftime("%m-%d-%y")
        self.filename = Path(self.p1 + self.client + " Upload " + self.dt + ".csv")
        
        # Setting up the dataframe and translating to client format
        self.Tdf = pd.read_csv(self.p1 + self.product + self.p2)
        self.Tdf['CUSIP'] = self.Tdf['CUSIP'].str.rjust(9, "0")
        
        # Create a copy of the data frame to transact on. 
        self.clientdf = self.Tdf.copy()
        self.clientdf.insert(len(self.clientdf.columns), 'Notes', '')
        self.clientdf['CurrentMktValue%'] = self.clientdf['CurrentMktValue%'].astype(float)*WeightMultiplier # apply a multiplier as some clients prefer sum of 100 vs. others who prefer a sum of 1 for weights.
        self.clientdf = self.clientdf.rename(columns={'CurrentMktValue%': self.WeightColumnName, "Symbol": self.SymbolColumnName}) # rename Symbol and CurrentMktValue% to client preferred symbol and weight column header names.
        self.clientdf = self.clientdf.round({self.WeightColumnName : rounding}) # round the data to the client's preferred precision.

        self.EqWeight = self.clientdf.loc[self.clientdf[self.SymbolColumnName] != "@CASHUSD", self.WeightColumnName].sum() # Calc equity aggregate weight.
        self.CashWeight = round(100 * self.WeightMultiplier - self.EqWeight, self.rounding) # Calc cash plug to sum weights to 100%.

        self.clientdf = dfh.Set_Value_in_DF(self.clientdf, self.SymbolColumnName, '@CASHUSD', self.SymbolColumnName, self.CashSymbol) # Set cash ticker to client's preferred cash name.
        self.clientdf = dfh.Set_Value_in_DF(self.clientdf, SymbolColumnName, self.CashSymbol, self.WeightColumnName, self.CashWeight) # Set cash weight in the data frame - to plug to 100% weights.
        self.clientdf = dfh.create_notes_in_df(self.clientdf, self.WeightColumnName, self.SymbolColumnName, self.CashSymbol) # Add notes to the client data frame.
        self.notesdf = dfh.create_notes_df(self.clientdf) # create a separate notes dataframe. Will be used to help create the notes for the email.
        self.notesstr = dfh.create_notes_string(self.notesdf) # Creates string for notes in email from the notes data frame.
    
    def get_client(self):
        return self.client
    
    def get_product(self):
        return self.product
    
    def get_rounding(self):
        return self.rounding
    
    def get_cash_symbol(self):
        return self.CashSymbol
    
    def get_WeightColumnName(self):
        return self.WeightColumnName
    
    def print_client_df(self):
        print(self.clientdf)