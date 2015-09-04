#!/usr/bin/env python
# -*- coding: utf-8 -*-


import threading
from concurrent import futures
from collections import defaultdict, namedtuple
from mailerbears import *
import time
import logging
from multiprocessing import Pool,Process


# State = namedtuple('State', 'addr ok fail')

class Mailerhi():
	def __init__(self,pool):
		self._pool = pool
		self._lock = threading.RLock() #Initial Lock
		# self._stat = defaultdict(lambda: {'ok': 0, 'fail': 0})

	def recipient_get(self):
		global RECIPIENT
		#Get recipient for sent
		try:
			if BCC>0:
				recipients = RECIPIENT[:BCC]
				recipient = recipients[0]
				del RECIPIENT[:BCC]
				bcc = ','.join(recipients)
			else:
				recipient = RECIPIENT[0]
				del RECIPIENT[0]
				bcc = False

			# print len(RECIPIENT)
			return bcc,recipient

		except:
			return False

	def record_log_and_counter(self,stat_sent,ip,recipients):
		global COUNTER
		# Принимает данные после отправки пакетов. Пишет в лог. И записывает в общий счетчик статусов отправки(ok,spam и прочее) по этому соксу
		# Возвращает True
		# Record success_recipients or error_recipients
		if len(recipients[0])>0:
			recipients_result = list(set(recipients[0].split(',')))
		else:
			recipients_result = [recipients[1]]

		# print recipients_result	

		recipients_result_sep = map(lambda x:x+'\n',recipients_result)		

		if stat_sent == "Success":
			success_recipient = open('data/success.txt','a')
			success_recipient.writelines(recipients_result_sep)
			success_recipient.close()
		else:						
			map(RECIPIENT.append,recipients_result)
			error_recipient = open('data/error.txt','a')
			error_recipient.writelines(recipients_result_sep)
			error_recipient.close()		

		# Record counter
		if stat_sent.find('Success')!=-1:
			COUNTER[ip]['Success']+=len(recipients_result)
			COUNTER['All']['Success']+=len(recipients_result)
		elif stat_sent.find('AuthenticationError')!=-1:
			COUNTER[ip]['AuthenticationError']+=1
			COUNTER['All']['AuthenticationError']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('HeloError')!=-1:
			COUNTER[ip]['HeloError']+=1
			COUNTER['All']['HeloError']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('ConnectError')!=-1:
			COUNTER[ip]['ConnectError']+=1
			COUNTER['All']['ConnectError']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('spam rejected')!=-1 and stat_sent.find('DataError')!=-1:
			COUNTER[ip]['Spam rejected']+=1
			COUNTER['All']['Spam rejected']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('invalid mailbox')!=-1:
			COUNTER[ip]['Bounce']+=1
			COUNTER['All']['Bounce']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('Temporarily rejected')!=-1:
			COUNTER[ip]['Temporarily rejected']+=1
			COUNTER['All']['Temporarily rejected']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('Ratelimit exceeded')!=-1:
			COUNTER[ip]['Ratelimit exceeded']+=1
			COUNTER['All']['Ratelimit exceeded']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('ProxyConnectionError')!=-1:
			COUNTER[ip]['ProxyConnectionError']+=1
			COUNTER['All']['ProxyConnectionError']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('ServerDisconnected')!=-1:
			COUNTER[ip]['ServerDisconnected']+=1
			COUNTER['All']['ServerDisconnected']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('SenderRefused')!=-1:
			COUNTER[ip]['SenderRefused']+=1
			COUNTER['All']['SenderRefused']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		elif stat_sent.find('RecipientsRefused')!=-1:
			COUNTER[ip]['RecipientsRefused']+=1
			COUNTER['All']['RecipientsRefused']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
		else:
			COUNTER[ip]['Other']+=1
			COUNTER['All']['Other']+=1
			COUNTER['All']['Nosent']+=len(recipients_result)
			
		result = 'Green-'+str(len(open('data/success.txt','r').readlines()))+'  Red-'+str(len(open('data/error.txt','r').readlines()))+'  '+ip+' '+stat_sent
		logging.info(result)

		return True


	def sent_email(self,ehlo,recipient,bcc):
		# Generate letter, generate fromaddress, activate_socks,отправка.
		# Возврат результатов данной отправки		
		
		try:
			fromaddr = BEARS.get_fromaddr()
			hostname = fromaddr.split('@')[1]
			letter = BEARS.get_letter(1,hostname,fromaddr,recipient,bcc)
			server_mail = 'mxs.mail.ru'
			server = smtplib.SMTP(server_mail)
			server.ehlo(ehlo)
			server.sendmail(fromaddr,recipient,letter)
			result = 'Success'			
			server.quit()

		except socks.ProxyConnectionError as error:
			result = 'ProxyConnectionError:'+str(error)
			#print result

		except smtplib.SMTPServerDisconnected as error:
			result = 'ServerDisconnected:'+str(error)
			#print result

		# except smtplib.SMTPResponseException as error:
		# 	print 'ResponseException:'+str(error)

		except smtplib.SMTPSenderRefused as error:
			result = 'SenderRefused: '+str(error[0])+' '+error[1]
			#(421, 'Command out of sequence; try again later', 'pruam@athoning.com')
			#print result

		except smtplib.SMTPRecipientsRefused as error:
			result = 'RecipientsRefused:'+str(error)
			#print result

		except smtplib.SMTPDataError as error:
			
			#421 Ratelimit exceeded for 103.253.146.218. Try again later.
			if error[0]==421 and error[1].find('Ratelimit exceeded')!=-1:
				regex = re.compile(r'for\s+\b([\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3})\b')
				ratelimit_exceeded = regex.search(error[1])
				result = ratelimit_exceeded.group()
				#print result

			#421 Temporarily rejected for 46.101.11.242. Try again later.
			elif error[0]==421 and error[1].find('Temporarily rejected')!=-1:
				regex = re.compile(r'for\s+\b([\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3})\b')
				temporarily_rejected = regex.search(error[1])
				result = temporarily_rejected.group()
				#print result

			#421 Problem resolving DNS for domain jmmon.com (DNS query timed out)
			elif error[0]==421 and error[1].find('DNS')!=-1:
				regex = re.compile(r'domain\s+\b([\w\d.]+[.][\w\d.]+)\b')
				problem_resolving = regex.search(error[1])
				result = problem_resolving.group()
				#print result

			#550 spam message rejected. Please visit
			#550
			elif error[0]==550 and error[1].find('invalid mailbox')!=-1:
				regex = re.compile(r'\b([\w.]+@[\w.]+[.][\w]+)\b')
				invalid_mailbox = regex.search(error[1])
				result = invalid_mailbox.group()
				#print result

			else:
				result='DataError: '+str(error[0])+' '+error[1][:55]+'...'
				#print result

		except smtplib.SMTPConnectError as error:
			result='ConnectError:'+str(error)
			#print result

		except smtplib.SMTPHeloError as error:
			result='HeloError:'+str(error[0])+' '+error[1]
			#print result

		except smtplib.SMTPAuthenticationError as error:
			result='AuthenticationError:'+str(error)
			#print result

		except BaseException as error:
			result = error
			#print result
		except:
			result = 'Error'

		return result

	def start_sent(self,socks_active):
		
		ehlo = socks_active[0]
		ip = socks_active[1]
		
		try:
			i=1
			while i!=0:				
				with self._lock:
					recipients = self.recipient_get()
					i = len(RECIPIENT)
					print i

				try:
					stat_sent = self.sent_email(ehlo,recipients[1],recipients[0])
				except:
					with self._lock:
						logging.info('Error Sent')

				try:
					with self._lock:				
						self.record_log_and_counter(stat_sent,ip,recipients)
				except:
					with self._lock:
						logging.info('Error Record')



			# print 'End start_sent'

		except:
			logging.info('Error start_sent')
			return False

		return True

def threading_socks(socks):
	socks_active = BEARS.socks_activate(socks)
	pool = ''
	mailer = Mailerhi(pool)

	thread_list = []

	for _ in range(CONCURRENT):
		thread_ = threading.Thread(target=mailer.start_sent,args=(socks_active,))
		thread_list.append(thread_)		

	for th in thread_list:
		th.start()

	for th in thread_list:
		th.join()

	while threading.active_count()>1:
		time.sleep(1)

	return True


def clears_logs():
	clear_success_file = open('data/success.txt','w')
	clear_success_file.close()
	clear_error_file = open('data/error.txt','w')
	clear_error_file.close()
	clear_logs= open('data/mylog.log','w')
	clear_logs.close()
	clear_count = open('data/counter.txt','w')
	clear_count.close()
	return True

def start_mailer(socks):
	thread_list = []
	for sock in socks:
		thread_ = threading.Thread(target=threading_socks,args=(sock,))
		thread_list.append(thread_)
		
	for th in thread_list:
		th.start()

	for th in thread_list:
		th.join()


	return True


clears_logs()
BEARS = MailerBears() #Initial class MailerBears()	
RECIPIENT = BEARS.get_recipient('data/myemail4.txt') #List recipient
PATH_SOCKS = 'http://109.234.38.38/media/sss/o4.txt' #List Socks
SOCKS = BEARS.get_socks(PATH_SOCKS)
COUNTER = {_.split(',')[0]:{'Success':0,'AuthenticationError':0,'HeloError':0,'ConnectError':0,'Spam rejected':0,'Bounce':0,'Temporarily rejected':0,'Ratelimit exceeded':0,'ProxyConnectionError':0,'ServerDisconnected':0,'SenderRefused':0,'RecipientsRefused':0,'Other':0} for _ in SOCKS}
COUNTER['All']={'Success':0,'Nosent':0,'AuthenticationError':0,'HeloError':0,'ConnectError':0,'Spam rejected':0,'Bounce':0,'Temporarily rejected':0,'Ratelimit exceeded':0,'ProxyConnectionError':0,'ServerDisconnected':0,'SenderRefused':0,'RecipientsRefused':0,'Other':0}
CONCURRENT = 15
TO = 1
BCC = 54 #random.randint(54,85)
CC = 0
LOGGING_FILE = 'data/mylog.log'
logging.basicConfig(format = '%(asctime)s   %(message)s', level = logging.DEBUG, filename = LOGGING_FILE)

		
if __name__ == "__main__":
	if len(sys.argv)!=2:
		print 'Enter the command "r" for round or "c" for many rounds'

	elif sys.argv[1]=='r':
		start_mailer(SOCKS)	

	elif sys.argv[1]=='c':
		pass

	else:
		print 'Enter the command "r" for round or "c" for many rounds'
