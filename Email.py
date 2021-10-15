from __future__ import unicode_literals, print_function
import DFHelpers as dfh
import win32com.client

def send_email(client_object, to, cc, attachment):
    """
    send_email creates an email for the client if needed.
    client_object: the client object and data frame for the email data.
    to: String. The recipient(s) of the email. If more than one recipient, separate the addresses via a semi-colon.
    cc: String. The addresses to be cc'd on the email.
    attachment: If the client requires the model data to be attached, provide the filepath and name of the attachment to be sent. 
    """
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = client_object.client + " " + client_object.dt
    
    # newMail.Body = "I AM\nTHE BODY MESSAGE!"
    # newMail.BodyFormat = 2 # olFormatHTML https://msdn.microsoft.com/en-us/library/office/aa219371(v=office.11).aspx
    # newMail.HTMLBody = "<HTML><BODY>Good evening,<br><br>"\
    #                     "We published the daily model update in Vestmark. We executed the below trades today:<br><br>"\
    #                     '<b><u>Westfield '+ client_object.product + ' Cap:</u></b><br>'\
    #                     + dfh.create_notes_df2(client_object.notesdf) + '</BODY></HTML>' 
    
    newMail.Body = 'Good evening,\n\n'\
    'We published the daily model update. We executed the below trades today:\n\n'\
    'Westfield ' + client_object.product + ' Cap:\n'\
    + dfh.create_notes_string(client_object.notesdf) + '\n'\
    'If there are any questions, please email TAM@wcmgmt.com.\n\nThank you,'
    newMail.To = to
    newMail.cc = cc
    # attachment1 = client_object.filename
    # newMail.Attachments.Add(Source=attachment1)
    newMail.display()