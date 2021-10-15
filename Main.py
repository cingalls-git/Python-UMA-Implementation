import Clients
import Email
import pandas as pd

# Uses Pandas to import a CSV, iterate through the dataframe and produce an output file that will be posted to a folder for upload/submission.

pd.options.display.max_columns = None
pd.options.display.max_rows = None

# client_dict provides the characteristics to create the objects and can be iterated through to create all files needed.
# (client, product, rounding, CashSymbol, WeightMultiplier, WeightColumnName, template, SymbolColumnName, mgrfilename = None, fileheader = True)
client_dict = {
                "WFC" : ["Mid", 5, "$$$$", .01, "Weight", "MMS", "Symbol", None]
                , "AMP" : ["Mid", 5, "$$$$", .01, "Weight", "MMS", "Symbol", None]
                , "PNC" : ["Mid", 3, "USD CASH", 1, "Weight", "Vestmark", "Symbol", None]
                , "UBSMid" : ["Mid", 3, "USD CASH", 1, "Weight", "Vestmark", "Symbol", None]
                , "STA": ["All", 3, "USD CASH", 1, "Weight", "Vestmark", "Symbol", None]
                , "STL": ["Large", 3, "USD CASH", 1, "Weight", "Vestmark", "Symbol", None]
                , "UBSLarge" : ["Large", 3, "USD CASH", 1, "Weight", "Vestmark", "Symbol", None]
                , "UBSSmid" : ["Smid", 3, "USD CASH", 1, "Weight", "Vestmark", "Symbol", None]
                , "Zeke" : ["Smid", 3, "$", 1, "Weight", "Parametric", "Symbol","westsmid"]
                , "FTG" : ["Mid", 3, "$", 1, "Weight", "Parametric", "Symbol","westmcg"]
                , "SWT" : ["Mid", 2, "CASH:SWEEP", 1,  "Target Percent", "SWT", "Symbol", None]
                , "FTB" : ["Mid", 3, "@CASHUSD", 1, "Weight", "FTB", "Symbol", None]
                , "Harbor": ["Disruptive", 4, "USD", 1, "ENDING_WEIGHT", "Harbor", "TICKER", None]
               }

# client_email provides clients and corresponding data to create the requisite emails for the client. The client key must match the client key in client_dict.
client_email = {
                "FTB": ["cingalls@wcmgmt.com; c.w.ingalls@gmail.com", "test@gmail.com", ""]
                , "SWT": ["cingalls@wcmgmt.com; c.w.ingalls@gmail.com", "test@gmail.com", ""]
                , "STA": ["cingalls@wcmgmt.com; c.w.ingalls@gmail.com", "test@gmail.com", ""]
                } 

def main():
    # Loop through clients in client_dict to create the client object and corresponding output file. if there is an email associated with the client object as outlined in client_email dictionary, the corresponding email is generated.
    for i in client_dict:
        c = Clients.Client(i, client_dict[i][0], client_dict[i][1], client_dict[i][2], client_dict[i][3], client_dict[i][4], client_dict[i][5], client_dict[i][6], client_dict[i][7])
        c.clientdf.to_csv(c.filename, index=False, header = c.fileheader)
        if i in client_email:
            Email.send_email(c, client_email[i][0], client_email[i][1], client_email[i][2])

main()