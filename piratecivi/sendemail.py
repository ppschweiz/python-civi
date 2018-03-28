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
from email.encoders import encode_7or8bit

smtp_server_address = os.environ['SMTP_SERVER_ADDRESS']
smtp_server_port = os.environ['SMTP_SERVER_PORT']

if 'SMTP_USERNAME' in os.environ:
	smtp_username = os.environ['SMTP_USERNAME']
else:
	smtp_username = ''

if 'SMTP_PASSWORD' in os.environ:
	smtp_password = os.environ['SMTP_PASSWORD']
else:
    smtp_password = ''

if 'SMTP_STARTTLS' in os.environ:
	smtp_starttls = (os.environ['SMTP_STARTTLS'] != '0')
else:
	smtp_starttls = True

gpg = gnupg.GPG()

def format_address(name, address):
	return ('"' + Header(str(name), 'UTF-8').encode() + '" <' + address + '>')

def send_signed_email(sender, receipient, subject, bodyhtml, bodytext, keyid, attachment=None, attachment_name=None):
	msg = MIMEMultipart('signed', protocol='application/pgp-signature')
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
	tobe_signed = str(alt).replace("MIME-Version: 1.0\n", "").replace("\n", "\r\n")
	msg.attach(alt)
	
	signature = gpg.sign(tobe_signed, keyid=keyid, detach=True)
	if '-----BEGIN PGP SIGNATURE-----' not in str(signature):
		raise Exception('Signing failed: ' + str(signature))

	signature_mime = MIMEApplication(str(signature), 'pgp-signature', encode_7or8bit, Name='signature.asc')
	signature_mime['Content-Disposition'] = 'attachement; filename="signature.asc"'
	msg.attach(signature_mime)

	sys.stderr.write('Sending signed mail...\n')

	s = smtplib.SMTP(smtp_server_address, smtp_server_port)

	if smtp_starttls:
		s.starttls();

	if smtp_username != '':
		s.login(smtp_username, smtp_password);

	s.sendmail(sender, receipient, msg.as_string())
	s.quit()

def send_encrypted_email(sender, receipient, subject, bodyhtml, bodytext, attachment=None, attachment_name=None, sign=None, encrypt_for=None):
	msg = MIMEMultipart('encrypted', protocol='application/pgp-encrypted')
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
	
	version = MIMEApplication('Version: 1\n', 'pgp-encrypted', encode_7or8bit)
	version['Content-Disposition'] = 'attachment'
	msg.attach(version)

	if encrypt_for == None:
		receipients = [receipient]
	else:
		receipients = encrypt_for

	encrypted_data = gpg.encrypt(str(alt).encode('ascii'), receipients, sign=sign)
	if not encrypted_data.ok:
		raise Exception('Encryption failed: ' + encrypted_data.stderr)

	encrypted_mime = MIMEApplication(str(encrypted_data), 'octet-stream', encode_7or8bit, Name='msg.asc')
	encrypted_mime['Content-Disposition'] = 'inline; filename="msg.asc"'
	msg.attach(encrypted_mime)

	sys.stderr.write('Sending encrypted mail...\n')

	s = smtplib.SMTP(smtp_server_address, smtp_server_port)

	if smtp_starttls:
		s.starttls();

	if smtp_username != '':
		s.login(smtp_username, smtp_password);

	s.sendmail(sender, receipient, msg.as_string())
	s.quit()

def send_email(sender, receipient, subject, bodyhtml, bodytext, attachment=None, attachment_name=None, cc=None):
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = receipient
	receipients = []
	receipients.append(receipient)

	if cc != None:
		msg['CC'] = cc
		receipients.append(cc)

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

	if smtp_starttls:
		s.starttls();

	if smtp_username != '':
		s.login(smtp_username, smtp_password);

	s.sendmail(sender, receipients, msg.as_string())
	s.quit()

def notify_admin(subject, text):
	send_email(u'info@piratenpartei.ch', u'stefan.thoeni@piratenpartei.ch', subject, text.replace(u'<', u'&lt;').replace(u'\n', u'<br/>'), text)
