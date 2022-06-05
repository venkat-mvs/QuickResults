import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mailer:
	'''
		Mailer
		- for sending a email to a email address securly
	'''

	def __init__(self,sender,password):
		self.sender_email = sender
		self.password = password
		self.context = ssl.create_default_context()
		self.server = None

	def login(self):
		'''
			Server creation and login
		'''
		if self.server == None:
			self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context)
		self.server.login(self.sender_email, self.password)
		
	def mail_to(self,mail: str,html: str,subject: str) -> None:
		'''
			mail: recipient mail address
			html: proper html mail message for the recipient
			subject: subject for the mail
		'''
		message = MIMEMultipart("alternative")
		message["Subject"] = subject
		message["From"] = self.sender_email
		message["To"] = mail
		part = MIMEText(html, "html")
		message.attach(part)
		self.server.sendmail(
		    self.sender_email, mail, message.as_string()
		)

	def die(self):
		'''
			To make server quit
		'''
		self.server.quit()


if __name__ == '__main__':
	mail = Mailer('praveenkumar6022@gmail.com','****')
	mail.login()
	mail.mail_to('venkatsaimaragani@gmail.com','<h1>hello</h1>',"testmail")
	mail.die()
	
	
	   