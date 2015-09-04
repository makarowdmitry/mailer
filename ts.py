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

	def recipient_get(self,to,bcc,cc):
		global RECIPIENT
		#Get recipient for sent
		try:
			if bcc>0:
				recipients = RECIPIENT[:bcc]
				recipient = recipients[0]
				del RECIPIENT[:bcc]
				bcc_r = ','.join(recipients)
			elif to>1:
				recipient = RECIPIENT[:to]
				del RECIPIENT[:to]
				bcc_r = False

			else:
				recipient = RECIPIENT[0]
				# fff = open('data/rec.txt','a')
				# fff.write(recipient+'\n')
				# fff.close()
				# print recipient
				del RECIPIENT[0]
				bcc_r = False

			# print len(RECIPIENT)
			return bcc_r,recipient,len(RECIPIENT)

		except:
			print '!!!!'
			return False


	def record_log_and_counter(self,stat_sent,ip,recipients):
		# global COUNTER
		# Принимает данные после отправки пакетов. Пишет в лог. И записывает в общий счетчик статусов отправки(ok,spam и прочее) по этому соксу
		# Возвращает True
		# Record success_recipients or error_recipients
		if recipients[0] !=False:
			recipients_result = recipients[0].split(',')
		elif type(recipients[1])==list:
			recipients_result=recipients[1]
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

		# # Record counter
		# if stat_sent.find('Success')!=-1:
		# 	COUNTER[ip]['Success']+=len(recipients_result)
		# 	COUNTER['All']['Success']+=len(recipients_result)
		# elif stat_sent.find('AuthenticationError')!=-1:
		# 	COUNTER[ip]['AuthenticationError']+=1
		# 	COUNTER['All']['AuthenticationError']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('HeloError')!=-1:
		# 	COUNTER[ip]['HeloError']+=1
		# 	COUNTER['All']['HeloError']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('ConnectError')!=-1:
		# 	COUNTER[ip]['ConnectError']+=1
		# 	COUNTER['All']['ConnectError']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('spam rejected')!=-1 and stat_sent.find('DataError')!=-1:
		# 	COUNTER[ip]['Spam rejected']+=1
		# 	COUNTER['All']['Spam rejected']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('invalid mailbox')!=-1:
		# 	COUNTER[ip]['Bounce']+=1
		# 	COUNTER['All']['Bounce']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('Temporarily rejected')!=-1:
		# 	COUNTER[ip]['Temporarily rejected']+=1
		# 	COUNTER['All']['Temporarily rejected']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('Ratelimit exceeded')!=-1:
		# 	COUNTER[ip]['Ratelimit exceeded']+=1
		# 	COUNTER['All']['Ratelimit exceeded']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('ProxyConnectionError')!=-1:
		# 	COUNTER[ip]['ProxyConnectionError']+=1
		# 	COUNTER['All']['ProxyConnectionError']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('ServerDisconnected')!=-1:
		# 	COUNTER[ip]['ServerDisconnected']+=1
		# 	COUNTER['All']['ServerDisconnected']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('SenderRefused')!=-1:
		# 	COUNTER[ip]['SenderRefused']+=1
		# 	COUNTER['All']['SenderRefused']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# elif stat_sent.find('RecipientsRefused')!=-1:
		# 	COUNTER[ip]['RecipientsRefused']+=1
		# 	COUNTER['All']['RecipientsRefused']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
		# else:
		# 	COUNTER[ip]['Other']+=1
		# 	COUNTER['All']['Other']+=1
		# 	COUNTER['All']['Nosent']+=len(recipients_result)
			
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
				result = 'Ratelimit exceeded '+ratelimit_exceeded.group()
				#print result

			#421 Temporarily rejected for 46.101.11.242. Try again later.
			elif error[0]==421 and error[1].find('Temporarily rejected')!=-1:
				regex = re.compile(r'for\s+\b([\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3})\b')
				temporarily_rejected = regex.search(error[1])
				result = 'Temporarily rejected '+temporarily_rejected.group()
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

	def start_sent(self,socks_active,to,bcc,cc,c):
		
		ehlo = socks_active[0]
		ip = socks_active[1]
		
		try:
			i=1
			while i>0:				
				with self._lock:
					recipients = self.recipient_get(to,bcc,cc)
					# print str(c)+'  '+recipients[1]
					
				if recipients==False:
					return True
				else:						

					# i = recipients[2]

					# print str(i)+' '+str(''.join(recipients[1]))
					# print i

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
			# print 'Error2'
			return False

		return True

def threading_socks(socks,recipient,c,concurrent,to,bcc,cc,logging_file):
	global RECIPIENT
	RECIPIENT = recipient
	logging.basicConfig(format = '%(asctime)s   %(message)s', level = logging.DEBUG, filename = logging_file)

	socks_active = MailerBears().socks_activate(socks)
	pool = ''
	mailer = Mailerhi(pool)

	ff = open('data/file_'+str(c)+'.txt','w')
	ff.writelines(map(lambda x:x+'\n',recipient))
	ff.close()

	thread_n = []

	for i in range(concurrent):
		thread_ = threading.Thread(target=mailer.start_sent,args=(socks_active,to,bcc,cc,i))
		thread_n.append(thread_)
		# print 'create thread '+str(c)+' '+str(i)
	for th in thread_n:
		th.start()

	for th in thread_n:
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








		
