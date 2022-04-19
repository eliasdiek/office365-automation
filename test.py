from smtplib import SMTP

with SMTP("bensemann.co.nz") as smtp:
    smtp.noop()