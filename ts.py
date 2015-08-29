#!/usr/bin/env python
# -*- coding: utf-8 -*-


#!/home/andrew/projects/py3k/python

import threading
from concurrent import futures
from collections import defaultdict, namedtuple
from mailerbears import *
import time
import logging

BEARS = MailerBears() #Initial class MailerBears()	
RECIPIENT = BEARS.get_recipient('data/myemail4.txt') #List recipient	
PATH_SOCKS = 'http://109.234.38.38/media/sss/o4.txt' #List Socks
SOCKS = BEARS.get_socks(PATH_SOCKS)
# SOCKS = ['46.101.224.82,3128,SOCKS5,goemailgo,q8uir']
CONCURRENT = 30000
TO = 1
BCC = 15 #random.randint(10,16)
CC = 0

LOCK = threading.RLock() #Initial Lock	

LOGGING_FILE = 'data/mylog.log'
logging.basicConfig(format = '%(levelname)-3s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = LOGGING_FILE)

IPS = {}

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
			with self._lock:
				if BCC>0:
					recipients = RECIPIENT[:BCC]
					recipient = recipients[0]
					del RECIPIENT[:BCC]
					bcc = ','.join(recipients)
				else:
					recipient = RECIPIENT[0]
					del RECIPIENT[0]
					bcc = False

				print len(RECIPIENT)
				return bcc,recipient
		except:
			return False

	def record_log_and_counter(self,stat_sent,ip):
		# Принимает данные после отправки пакетов. Пишет в лог. И записывает в общий счетчик статусов отправки(ok,spam и прочее) по этому соксу
		# Возвращает True
		logging.info(ip+' '+stat_sent)
		return True

	def sent_email(self,server,ehlo,recipient,bcc):
		# Generate letter, generate fromaddress, activate_socks,отправка.
		# Возврат результатов данной отправки
		fromaddr = BEARS.get_fromaddr()
		hostname = fromaddr.split('@')[1]
		letter = BEARS.get_letter(1,hostname,fromaddr,recipient,bcc)
		
		try:	

			server.sendmail(fromaddr,recipient,letter)
			result = 'Success'

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
			#(421, 'Command out of sequence; try again later', 'pruam@athoning.com')
			print result

		except smtplib.SMTPRecipientsRefused as error:
			result = 'RecipientsRefused:'+str(error)
			print result

		except smtplib.SMTPDataError as error:
			
			#421 Ratelimit exceeded for 103.253.146.218. Try again later.
			if error[0]==421 and error[1].find('Ratelimit exceeded')!=-1:
				regex = re.compile(r'for\s+\b([\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3})\b')
				ratelimit_exceeded = regex.search(error[1])
				result = ratelimit_exceeded.group()
				print result

			#421 Temporarily rejected for 46.101.11.242. Try again later.
			elif error[0]==421 and error[1].find('Temporarily rejected')!=-1:
				regex = re.compile(r'for\s+\b([\d]{1,3}[.][\d]{1,3}[.][\d]{1,3}[.][\d]{1,3})\b')
				temporarily_rejected = regex.search(error[1])
				result = temporarily_rejected.group()
				print result

			#421 Problem resolving DNS for domain jmmon.com (DNS query timed out)
			elif error[0]==421 and error[1].find('DNS')!=-1:
				regex = re.compile(r'domain\s+\b([\w\d.]+[.][\w\d.]+)\b')
				problem_resolving = regex.search(error[1])
				result = problem_resolving.group()
				print result

			#550 spam message rejected. Please visit
			#550
			elif error[0]==550 and error[1].find('invalid mailbox')!=-1:
				regex = re.compile(r'\b([\w.]+@[\w.]+[.][\w]+)\b')
				invalid_mailbox = regex.search(error[1])
				result = invalid_mailbox.group()
				print result

			else:
				result='DataError: '+str(error[0])+' '+error[1][:55]+'...'
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
			result = error
			print result



		return result

	# def record_recipient_ok_fail(self,fail_recipient,ok_recipient,bounce_recipient):
	# 	# Принимает три списка с получателями, дописывает в списки. 
	# 	# Если ок не пустой - в список success_sent.txt. Если bounce не пустой - в список bounce.txt. Если fail не пустой - дописываем в список RECIPIENT
	# 	pass

	def start_sent(self,socks_active,count):
		# Получаем получаетелей
		# Отправляем письмо
		# Записываем статистику
		# Записываем все успешные и неуспешно отправленные адреса и отскоки
		# with self._lock:
		# 	ehlo = BEARS.socks_activate(socks)
		# with self._lock:
			# print socks_active[0]
		ehlo = socks_active['hostname'][0]
		print ehlo
		ip = socks_active['ip']
		print ip
		try:
			server_mail = 'mxs.mail.ru'
			server = smtplib.SMTP(server_mail)
			server.ehlo(ehlo)
			i=100
			while i!=1:
				with self._lock:
					recipients = self.recipient_get()
					i=len(RECIPIENT)
				stat_sent = self.sent_email(server,ehlo,recipients[1],recipients[0])
				with self._lock:
					self.record_log_and_counter(stat_sent,ip)
			server.quit()

		except:
			return False
		return True

def threading_socks(socks,concurrent):
	with futures.ThreadPoolExecutor(max_workers=concurrent) as pool:
		mailer = Mailerhi(pool)

		LOCK.acquire()
		socks_active = BEARS.socks_activate(socks)
		
		
		for _ in pool.map(mailer.start_sent,BEARS.socks_activate(socks),range(concurrent)):
			print socks_active
			pass	
		LOCK.release()	

	return True


if __name__ == '__main__':
	# Проверяем по stat, когда останавливать рассылку
	# for _ in range(3):


	for socks in SOCKS:
		thread_ = threading.Thread(target=threading_socks,args=(socks,CONCURRENT))
		thread_.start()

	# m = Mailerhi()
	# m.record_log_and_counter('wegweg')