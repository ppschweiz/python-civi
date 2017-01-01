import smtplib
import os
from email.Header import Header
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server_address = os.environ['SMTP_SERVER_ADDRESS']
smtp_server_port = os.environ['SMTP_SERVER_PORT']
smtp_username = os.environ['SMTP_USERNAME']
smtp_password = os.environ['SMTP_PASSWORD']

def format_address(name, address):
	return ('"' + str(Header(unicode(name), 'UTF-8')) + '" <' + address + '>').encode('ascii')

def send_email(sender, receipient, subject, bodyhtml, bodytext, attachment=None, attachment_name=None):
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = receipient

	if attachment != None:
		with open(attachment, "rb") as fil:
			part = MIMEApplication(fil.read(), Name=attachment)
			part['Content-Disposition'] = 'attachment; filename="{}"'.format(attachment_name)
			msg.attach(part)

	alt = MIMEMultipart('alternative')
	msg.attach(alt)

	alt.attach(MIMEText(bodytext, 'plain', 'utf-8'))
	alt.attach(MIMEText(bodyhtml, 'html', 'utf-8'))

	print('Sending mail...')

	s = smtplib.SMTP(smtp_server_address, smtp_server_port)
	s.starttls();
	s.login(smtp_username, smtp_password);
	s.sendmail(sender, receipient, msg.as_string())
	s.quit()

def notify_admin(subject, text):
	send_email(u'info@piratenpartei.ch', u'stefan.thoeni@piratenpartei.ch', subject, text.replace(u'<', u'&lt;').replace(u'\n', u'<br/>'), text)
