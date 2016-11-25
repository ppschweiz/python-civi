import smtplib
import os
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server_address = os.environ['SMTP_SERVER_ADDRESS']
smtp_server_port = os.environ['SMTP_SERVER_PORT']
smtp_username = os.environ['SMTP_USERNAME']
smtp_password = os.environ['SMTP_PASSWORD']

def send_email(sender, destination, subject, bodyhtml, bodytext, attachment=None, attachment_name=None):
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender.encode('latin-1')
	msg['To'] = destination.encode('latin-1')

	if attachment != None:
		with open(attachment, "rb") as fil:
			part = MIMEApplication(fil.read(), Name=attachment)
			part['Content-Disposition'] = 'attachment; filename="{}"'.format(attachment_name)
			msg.attach(part)

	alt = MIMEMultipart('alternative')
	msg.attach(alt)

	alt.attach(MIMEText(bodytext, "plain"))
	alt.attach(MIMEText(bodyhtml, "html"))

	print(u'Sending mail {} to {} ...'.format(subject, destination))
	#raise Error('oops!')

	s = smtplib.SMTP(smtp_server_address, smtp_server_port)
	s.starttls();
	s.login(smtp_username, smtp_password);
	s.sendmail(sender, destination, msg.as_string())
	s.quit()

def notify_admin(subject, text):
	send_email('info@piratenpartei.ch', 'stefan.thoeni@piratenpartei.ch', subject, text.replace('<', '&lt;').replace(u'\n', u'<br/>'), text)
