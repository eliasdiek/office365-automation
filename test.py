from smtplib import SMTP

# with SMTP("bensemann.co.nz") as smtp:
#     smtp.noop()

def sendEhlo():
    connection = SMTP("smtp.gmail.com", 587)
    connection.ehlo()

sendEhlo()