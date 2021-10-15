import ClientTemplate
import DFHelpers as dfh
import pandas as pd
import numpy as np
import os
from datetime import datetime
from pathlib import Path

pd.options.display.max_columns = None
pd.options.display.max_rows = None

cashtgtweight = .00507
c = ClientTemplate.ClientTemplate("PNC", "Mid", 3, "USD CASH", 1, "Weight", "Vestmark", "Symbol", None)

totalassets = c.clientdf['CurrentMktVal*'].sum()
originalinvestable = c.clientdf.loc[(c.clientdf['FilledAmount'] == 0) & (c.clientdf['Ordered'] == 0) & (c.clientdf['Symbol'] != c.CashSymbol), 'CurrentMktVal*'].sum()
openordermktval = totalassets - originalinvestable - c.clientdf.loc[(c.clientdf['Symbol'] == c.CashSymbol), 'CurrentMktVal*'].sum()
cashmktvaltarget = cashtgtweight * totalassets
# currentcash = c.clientdf.loc[c.clientdf[c.SymbolColumnName] == c.CashSymbol, 'CurrentMktVal*']
c.clientdf.set_index(c.SymbolColumnName, inplace = True)
currentcash = c.clientdf.loc[c.CashSymbol, 'CurrentMktVal*']
cashchange = cashmktvaltarget - currentcash
newinvestable = totalassets - cashmktvaltarget - openordermktval
calcratio = newinvestable / originalinvestable - 1

c.clientdf['mktvalchg'] = 0
c.clientdf.loc[(c.clientdf['FilledAmount'] == 0) & (c.clientdf['Ordered'] == 0), 'mktvalchg'] = calcratio * c.clientdf['CurrentMktVal*']
c.clientdf.loc[c.CashSymbol, 'mktvalchg'] = cashchange
c.clientdf['proratamktval'] = c.clientdf['CurrentMktVal*'] + c.clientdf['mktvalchg']
c.clientdf['roundedshares'] = round(c.clientdf['proratamktval'] / c.clientdf['CalcPrice'], 0)
c.clientdf['newmktval'] = c.clientdf['CalcPrice'] * c.clientdf['roundedshares']
c.clientdf['prorataweight'] = c.clientdf['newmktval'] / totalassets * 100
c.clientdf['prorataweight'] = round(c.clientdf['prorataweight'], c.rounding)
EqWeight = c.clientdf.loc[c.clientdf.index != c.CashSymbol, 'prorataweight'].sum()
CashWt = 100 - EqWeight
c.clientdf.loc[c.clientdf.index == c.CashSymbol, 'prorataweight'] = CashWt

print(c.clientdf)
c.clientdf.reset_index(inplace = True)