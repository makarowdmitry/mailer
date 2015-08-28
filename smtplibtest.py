import smtplib
import socks
from mailerbears import *
import re

BEARS = MailerBears()


ehlo = BEARS.socks_activate('188.226.250.38,3128,SOCKS5,goemailgo,q8uir')
fromaddr = BEARS.get_fromaddr()
bcc=0 #','.join(['nikolaiofwt001musm@mail.ru','nikolaiofwt00wegewg1musm@mail.ru','nikolaiofwt001ewgewgewgmusm@mail.ru','wegewgewg@mail.ru','nikolaiofwt00ewgeg1musm@mail.ru','nikolaiofgwegwt001musm@mail.ru','nikolaiofwt0gweg01musm@mail.ru','nikolaiofwt0gweg01musm@mail.ru','nikolaiofwwegewgt001musm@mail.ru'])
recipient = ['nikolaiofwt001mum@mail.ru']
# recipients = ['nikolaiofwt001musm@mail.ru','nikolaiofwt00wegewg1musm@mail.ru','nikolaiofwt001ewgewgewgmusm@mail.ru','wegewgewg@mail.ru','nikolaiofwt00ewgeg1musm@mail.ru','nikolaiofgwegwt001musm@mail.ru','nikolaiofwt0gweg01musm@mail.ru','nikolaiofwt0gweg01musm@mail.ru','nikolaiofwwegewgt001musm@mail.ru']
letter = BEARS.get_letter(1,ehlo,fromaddr,recipient,bcc)
server_mail = 'mxs.mail.ru'


try:
	server = smtplib.SMTP(server_mail)
	server.ehlo(ehlo)
	answersmtp = server.sendmail(fromaddr,recipient,letter+'http:paysystem.tv')#'http:paysystem.tv'
	server.quit()

	result = 'Success sent'
	print result

except socks.ProxyConnectionError as error:
	result = 'ProxyConnectionError:'+str(error)
	print result

except smtplib.SMTPServerDisconnected as error:
	result = 'ServerDisconnected:'+str(error)
	print result

# except smtplib.SMTPResponseException as error:
# 	print 'ResponseException:'+str(error)

except smtplib.SMTPSenderRefused as error:
	result = 'SenderRefused: '+str(error[0])+' '+error[1]
	print result

except smtplib.SMTPRecipientsRefused as error:
	result = 'RecipientsRefused:'+str(error)
	print result

except smtplib.SMTPDataError as error:
	result1='DataError: '+str(error[0])+' '+error[1][:55]+'...'
	print result1
	
	#421 Ratelimit exceeded for 103.253.146.218. Try again later.
	if error[0]==421 and error[1].find('Ratelimit exceeded')!=-1:
		regex = re.compile(r'for\s+\b([\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3})\b')
		ratelimit_exceeded = regex.search(error[1])
		result = ratelimit_exceeded.group()
		print result

	#421 Temporarily rejected for 46.101.11.242. Try again later.
	if error[0]==421 and error[1].find('Temporarily rejected')!=-1:
		regex = re.compile(r'for\s+\b([\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3})\b')
		temporarily_rejected = regex.search(error[1])
		result = temporarily_rejected.group()
		print result

	#421 Problem resolving DNS for domain jmmon.com (DNS query timed out)
	if error[0]==421 and error[1].find('DNS')!=-1:
		regex = re.compile(r'domain\s+\b([\w\d.]+[.][\w\d.]+)\b')
		problem_resolving = regex.search(error[1])
		print problem_resolving.group()	

	#550 spam message rejected. Please visit
	#550
	if error[0]==550 and error[1].find('invalid mailbox')!=-1:
		regex = re.compile(r'\b([\w.]+@[\w.]+[.][\w]+)\b')
		invalid_mailbox = regex.search(error[1])
		result = invalid_mailbox.group()
		print result

except smtplib.SMTPConnectError as error:
	result='ConnectError:'+str(error)
	print result

except smtplib.SMTPHeloError as error:
	result='HeloError:'+str(error[0])+' '+error[1]
	print result

except smtplib.SMTPAuthenticationError as error:
	result='AuthenticationError:'+str(error)
	print result

except BaseException as error:
	print error