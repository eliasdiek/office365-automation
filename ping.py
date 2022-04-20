import smtplib
from email.mime.text import MIMEText
from email.header import Header

server = smtplib.SMTP('smtpout.secureserver.net', 587)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.ehlo()
server.login('raj@kp-partnersllc.com', 'Hariharibol108!')

# msg = MIMEText("Hey, this is a message from the Python mailer!", "text", "utf-8")
# msg["Subject"] = Header("[Python mailer] HEY!", "utf-8")
# msg["from"] = "diektech@gmail.com"
# result = server.sendmail("diektech@gmail.com", "poberezhetspavlo123321123321@gmail.com", msg.as_string())
# print('[result]', result)

server.mail('raj@kp-partnersllc.com')
code, message = server.rcpt("ttggee33@kp-partnersllc.com")
print('[result]', code, message)

server.quit()