#import smtplib for the actual sending function
import smtplib
import credentials
from email import encoders
import os
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
# Import the email modules we'll need
from email.message import EmailMessage

password = credentials.login['password']
def generate_message_id(msg_from):
	domain = msg_from.split("@")[1]
	r = "%s.%s" % (time.time(), random.randint(0, 100))
	mid = "<%s@%s>" % (r, domain)
	return mid

def send_mail(msg_from, to, subject, text, files=[],server="localhost", debug=False):
	assert type(to)==list
	assert type(files)==list
	
	# create message object instance
	msg = MIMEMultipart()

	# setup the parameters of the message
	msg['From'] = msg_from
	msg['To'] = COMMASPACE.join(to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject
	
	message = text.encode("utf-8")
	# add in the message body
	msg.attach(MIMEText(message, 'plain', "utf-8"))
	
	msg.add_header('Message-ID', generate_message_id(msg_from))
	
	for file in files:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(file,"rb").read() )
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
		msg.attach(part)

	if not debug:
		# Send the message via own SMTP server.
		s = smtplib.SMTP('mail.company.com',587)
		s.ehlo()
		s.starttls()
		s.login("user@email.com", password)
		#s.send_message(msg)
		s.sendmail(msg['From'], msg['To'], msg.as_string())
		s.quit()
		print("successfully sent email to {}".format(to))
	return msg
send_mail('user@email.com', ["rcpt@email.com"], "Reports from zabbix.","Please find the reports in the attachment.\ncheers", ["textfile.txt"])
