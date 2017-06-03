import sys
import os
import io
import smtplib
import gnupg
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server_address = os.environ['SMTP_SERVER_ADDRESS']
smtp_server_port = os.environ['SMTP_SERVER_PORT']
smtp_username = os.environ['SMTP_USERNAME']
smtp_password = os.environ['SMTP_PASSWORD']
gpg = gnupg.GPG()

def format_address(name, address):
	return ('"' + Header(str(name), 'UTF-8').encode() + '" <' + address + '>')

def send_encrypted_email(sender, receipient, subject, bodyhtml, bodytext, attachment=None, attachment_name=None, sign=None, encrypt_for=None):
	msg = MIMEMultipart('encrypted')
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = receipient
	
	alt = MIMEMultipart('alternative')
	alt.attach(MIMEText(bodytext, 'plain', 'utf-8'))
	alt.attach(MIMEText(bodyhtml, 'html', 'utf-8'))
	
	if attachment != None:
		mixed = MIMEMultipart('mixed')
		mixed.attach(alt)
		with open(attachment, "rb") as fil:
			part = MIMEApplication(fil.read(), Name=attachment)
			part['Content-Disposition'] = 'attachment; filename="{}"'.format(attachment_name)
			mixed.attach(part)
		alt = mixed
	
	version = MIMEText('Version: 1', 'plain', 'ascii')
	version['Content-Type'] = 'application/pgp-encrypted'
	version['Content-Disposition'] = 'attachment'
	msg.attach(version)

	if encrypt_for == None:
		receipients = [receipient]
	else:
		receipients = encrypt_for

	encrypted_data = gpg.encrypt(str(alt).encode('ascii'), receipients, sign=sign)
	if not encrypted_data.ok:
		raise Exception('Encryption failed: ' + encrypted_data.stderr)

	encrypted_mime = MIMEApplication(str(encrypted_data), Name='msg.asc')
	encrypted_mime['Content-Disposition'] = 'inline; filename="msg.asc"'
	msg.attach(encrypted_mime)

	sys.stderr.write('Sending encrypted mail...\n')

	s = smtplib.SMTP(smtp_server_address, smtp_server_port)
	s.starttls();
	s.login(smtp_username, smtp_password);
	s.sendmail(sender, receipient, msg.as_string())
	s.quit()

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

	sys.stderr.write('Sending mail...\n')

	s = smtplib.SMTP(smtp_server_address, smtp_server_port)
	s.starttls();
	s.login(smtp_username, smtp_password);
	s.sendmail(sender, receipient, msg.as_string())
	s.quit()

def notify_admin(subject, text):
	send_email(u'info@piratenpartei.ch', u'stefan.thoeni@piratenpartei.ch', subject, text.replace(u'<', u'&lt;').replace(u'\n', u'<br/>'), text)
