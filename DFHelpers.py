import pandas as pd

# def Get_Equity_Aggregate_Weight2(df, SymbolColumnName, WeightColumnName):
#     EqWeight = 0
#     for r, c in df.iterrows():
#         if c[SymbolColumnName] != "@CASHUSD":
#             currwt = df.at[r, WeightColumnName]
#             EqWeight += currwt
#     return EqWeight

# def Get_Equity_Aggregate_Weight2(df, LookupColumnName, LookupColumnValue, AddColumnName):
#     EqWeight = df.loc[df[LookupColumnName] != LookupColumnValue, AddColumnName].sum()
#     print(EqWeight)
#     return EqWeight

# def Set_Value_in_DF(df, LookupColumnName, LookupColumnValue, ColumnNameToChange, Value):
#     for r, c in df.iterrows():
#         if c[LookupColumnName] == LookupColumnValue:
#             df.at[r, ColumnNameToChange] = Value
#             break
#     return df

def Set_Value_in_DF(df, LookupColumnName, LookupColumnValue, ColumnNameToChange, Value):
    """ 
    Given a data frame, allows a lookup for a column/value combination and then allows you to update a value in a specified column for that indexed row.
    df: the data frame you want to update
    LookupColumnName: The column you want to look up to identify your indexed row to update. For example, if you want to put a note in the column for symbol AAPL, Lookup Column name would be symbol.
    LookupColumnValue: The value you want to look up / reference in the LookupColumnName column. Using the previous example, the LookupColumnValue would be AAPL.
    ColumnNameToChange: The column you want to update based on your referenced lookup.
    Value: The value you want to input in the ColumnNameToChange.
    Using our example, if I want to change the Weight column to 5% where Symbol AAPL on the ABC data frame : Set_Value_in_DF("ABC", "Symbol", "AAPL", "Weight", .05 (or 5 depending on client mutliplier).
    Returns the updated dataframe.
    """
     
    df.loc[(df[LookupColumnName] == LookupColumnValue), ColumnNameToChange] = Value
    return df

# def create_notes_in_df(df, WeightColumnName):
#     for r, c in df.iterrows():
#         # print(c['Start'])
#         if c['Start'] == 0 and c['FilledAmount'] > 0 and c['SecurityDesc'] != "CASH":
#             df.at[r, 'Notes'] = c['Symbol'] + ' - Bought to ' + str(c[WeightColumnName]) + '%'
#         elif c['Current'] == 0 and c['FilledAmount'] < 0 and c['SecurityDesc'] != "CASH":
#             df.at[r, 'Notes'] = c['Symbol'] + ' - Sold to 0'
#         elif c['Start'] > 0 and c['FilledAmount'] > 0 and c['SecurityDesc'] != "CASH":
#             df.at[r, 'Notes'] = c['Symbol'] + ' - Added to ' + str(c[WeightColumnName]) + '%'
#         elif c['Current'] > 0 and c['FilledAmount'] < 0 and c['SecurityDesc'] != "CASH":
#             df.at[r, 'Notes'] = c['Symbol'] + ' - Trimmed to ' + str(c[WeightColumnName]) + '%'
#     return df

# def create_notes_in_df(df, WeightColumnName):
#     for index in df.index:
#         if df.loc[index, 'Start'] == 0 and df.loc[index, 'FilledAmount'] > 0 and df.loc[index, 'SecurityDesc'] != "CASH":
#             df.loc[index, 'Notes'] = df.loc[index, 'Symbol'] + ' - Bought to ' + str(df.loc[index, WeightColumnName]) + '%'
#         elif df.loc[index, 'Start'] > 0 and df.loc[index, 'Current'] == 0 and df.loc[index, 'SecurityDesc'] != "CASH":
#             df.loc[index, 'Notes'] = df.loc[index, 'Symbol'] + ' - Sold to 0'
#         elif df.loc[index, 'Start'] > 0 and df.loc[index, 'FilledAmount'] > 0 and df.loc[index, 'SecurityDesc'] != "CASH":
#             df.loc[index, 'Notes'] = df.loc[index, 'Symbol'] + ' - Added to ' + str(df.loc[index, WeightColumnName]) + '%'
#         if df.loc[index, 'Current'] > 0 and df.loc[index, 'FilledAmount'] < 0 and df.loc[index, 'SecurityDesc'] != "CASH":
#             df.loc[index, 'Notes'] = df.loc[index, 'Symbol'] + ' - Trimmed to ' + str(df.loc[index, WeightColumnName]) + '%'
#     return df

# def create_notes_df(df):
#     notesdf = pd.DataFrame({'Note': []})
#     for r, c in df.iterrows():
#         if c['Notes'] != "":
#             notesdf = notesdf.append({'Note': c['Notes']}, ignore_index = True)
#     return notesdf

def create_notes_df(df):
    """ 
    iterates through the provided data frame and adds Notes to a single data frame. Removes blank note fields from the original data frame column and condenses down to just active/traded notes.
    Returns a new data frame with just notes.
    """
    
    notedf = pd.DataFrame({'Note': []})
    for i in df['Notes']:
        if i != '':
            notedf = notedf.append({'Note': i}, ignore_index = True)
    return notedf

def create_notes_in_df(df, WeightColumnName, SymbolColumnName, CashSymbol):
    """ 
    For non-cash securities where there was an active trade, creates the appropriate note and adds the note to the Notes column of the client's data frame.
    df: the data frame we will add the notes column to.
    WeightColumnName: String, the column that has the security's current weight.
    SymbolColumnName: String, the column that has the security's Symbol (will differ by client).
    CashSymbol: String, the client's required symbol identifier for cash.
    """
    
    df[WeightColumnName] = df[WeightColumnName].astype(str)
    df['Notes'] = ''
    df.loc[(df.Start > 0) & (df.FilledAmount > 0) & (df[SymbolColumnName] != CashSymbol), 'Notes'] = df[SymbolColumnName] + " - Added to " + df[WeightColumnName] + '%'
    df.loc[(df.Start == 0) & (df.FilledAmount > 0) & (df[SymbolColumnName] != CashSymbol), 'Notes'] = df[SymbolColumnName] + " - Bought to " + df[WeightColumnName] + '%'
    df.loc[(df.Current > 0) & (df.FilledAmount < 0) & (df[SymbolColumnName] != CashSymbol), 'Notes'] = df[SymbolColumnName] + " - Trimmed to " + df[WeightColumnName] + '%'
    df.loc[(df.Current == 0) & (df.FilledAmount < 0) & (df[SymbolColumnName] != CashSymbol), 'Notes'] = df[SymbolColumnName] + " - Sold to 0"
    df[WeightColumnName] = df[WeightColumnName].astype(float)
    return df

def create_notes_string(df):
    """
    Takes the notes data frame and compiles it in to a string, separated by a line break. Will be used/called to create client emails.
    df: the notes data frame for the client.
    Returns the notes string with each note separated by a line break. IF there are no active trades (i.e. no active notes), returns "Daily update. No product trades today."
    """
    noteslst = df.values.tolist()
    notesstring = '\t'
    for i in noteslst:
        notesstring += i[0]
        notesstring += '\n\t'
    if notesstring == '\t':
        notesstring = '\tDaily update. No product trades today.\n'
    return notesstring