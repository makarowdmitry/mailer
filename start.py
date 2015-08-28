#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mailerbears import *
import time
import threading
from Queue import Queue
import logging

# # Сообщение отладочное
# logging.debug( u'This is a debug message' )
# # Сообщение информационное
# logging.info( u'This is an info message' )
# # Сообщение предупреждение
# logging.warning( u'This is a warning' )
# # Сообщение ошибки
# logging.error( u'This is an error message' )
# # Сообщение критическое
# logging.critical( u'FATAL!!!' )


# 	ФУНКЦИЯ ПРЕСТАРТ
# 	На входе получаем список настроек
# 	-Готовим список получателей
# 	-Проверка соксов
# 		Выкачиваем соксы. И сверяем их с предыдущими. Если одинаковые или равны 0.0.0.0 - проверяем ссылку до тех пор пока не будет истина каждую секунду.
# 		Дальше переписываем файл socks и создаем список.


QUEUE = Queue() #Initial Queue	
BEARS = MailerBears() #Initial class MailerBears()	
LOCK = threading.RLock() #Initial Lock	
RECIPIENT = BEARS.get_recipient('data/myemail4.txt') #List recipient	
PATH_SOCKS = 'http://109.234.38.38/media/sss/o4.txt' #List Socks
SOCKS = BEARS.get_socks(PATH_SOCKS)
# SOCKS = ['46.101.224.82,3128,SOCKS5,goemailgo,q8uir']

THREADS_COUNT_SOCKS = len(SOCKS) #Count Threads Socks	
THREADS_COUNT= 10 #Count Threads on every socks
THREADS_COUNT2= 50

TO = 1
BCC = 0 #random.randint(10,16)
CC = 0

LOGGING_FILE = 'data/mylog.log'
logging.basicConfig(format = '%(levelname)-3s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = LOGGING_FILE)

	
  

def sent_email(threads_count,sock):
	ehlo = BEARS.socks_activate(sock)
	server_mail = 'mxs.mail.ru'
	server = smtplib.SMTP(server_mail)
	server.ehlo(ehlo)

	# Generate from and letter
	for _ in xrange(threads_count):
		
		if BCC>0:
			recipients = [QUEUE.get_nowait() for i in range(BCC)]
			recipient = recipients[0]
			bcc = ','.join(recipients)

			if ehlo==False:
				map(QUEUE.put,recipients)
		else:
			recipient = QUEUE.get_nowait()
			bcc = False
			if ehlo==False:
				QUEUE.put(recipient)
		
		fromaddr = BEARS.get_fromaddr()
		letter = BEARS.get_letter(1,ehlo,fromaddr,recipient,bcc)			
		thread_ = threading.Thread(target=server.sendmail,args=(fromaddr,recipient,letter))
		thread_.start()
		thread_.join()
	
	server.quit()


def main():
	start_time = time.time()
	print "STARTED"

	for recipient in RECIPIENT:
		QUEUE.put(recipient)

	for sock in SOCKS:
		for _ in xrange(THREADS_COUNT):
			thread_ = threading.Thread(target=sent_email,args=(THREADS_COUNT,sock))
			thread_.start()
			thread_.join()

	while threading.active_count()>1:
		time.sleep(1)

	print "FINISHED"
	print time.time()-start_time




if __name__ == '__main__':
	main()




# Скрипт должен иметь следующие управление
# 1. start - запускает рассылку. Рассылка заканчивается, когда все соксы выдали больше 1 раз ошибку 441 templory limit каждый или перестали работать

# 	ФУНКЦИЯ ПРЕСТАРТ
# 	На входе получаем список настроек
# 	-Готовим список получателей
# 	-Проверка соксов
# 		Выкачиваем соксы. И сверяем их с предыдущими. Если одинаковые или равны 0.0.0.0 - проверяем ссылку до тех пор пока не будет истина каждую секунду.
# 		Дальше переписываем файл socks и создаем список.


# 	ФУНКЦИЯ РАССЫЛКИ 
# 	Берем соксы из переменной - запускаем потоки.	
# 	По каждой отправке пишем лог (с какого ip отправили, ответ сервера) и обновляем значение в словаре по кол. (сколько успешных, сколько spam, сколько ошибок fromadd, сколько темплори лимит)
# 	Останавливаем когда соксы выдали больше 1 раз ошибку 441 templory limit каждый или перестали работать.
# 	По окончанию:
# 	-Пишем кол. ответов сервера из словаря (сколько успешных, сколько spam, сколько ошибок fromadd, сколько темплори лимит) в файл результаты.
# 	-Пишем получателей (красных, зеленых в разные списки). Переписываем файл получателей
	



# 2. cycle - запускает рассылку по циклу. Рассылка заканчивается тогда, когда заканчивается база
# 	Цикл
# 	ФУНКЦИЯ ПРЕСТАРТ
# 	ФУНКЦИЯ ПРОВЕРКИ КОЛ. В БАЗЕ (если меньше 0) - останавливается
# 	ФУНКЦИЯ РАССЫЛКИ





# try:
# 		go_thread_socks()	
# 	except:
# 		new_socks = BEARS.get_socks(PATH_SOCKS)

# 		while new_socks==SOCKS or new_socks[0]=='0.0.0.0':
# 			new_socks = BEARS.get_socks(PATH_SOCKS)
# 			time.sleep(3)

# 		SOCKS = new_socks
# 		go_thread_socks()

# 1. Сделать тот в точь заголовки thebat
# 2. Писать логи рассылки в sqlite 
# 3. Сделать многопоточную отправку писем с 9 соксов

# Каждый процесс
# Перед каждым процессом

# Параметры
# _RECIPIENT_BASE_1_1800000_TO_1_100_BCC_1_100_CC_1_100_,_THREADING_20_,_FROM_(RANDSTR/USER_URL)_USER_LIST_

# _THREADING_20_
# _FROM_(RANDSTR/USER_LIST)_USER_LIST_
# _DOMAINS_(NEXT/RAND)_1_USER_LIST_


# Обновить
# _RECIPIENT_BASE_1_1800000_TO_1_100_BCC_1_100_CC_1_100_
# На каждый раунд




# Подготовка
# 1.Берем получателей из файла - записываем их в список
# 2.Берем соксы из файла - записываем их в список
# 3.Выделяем нужно количество процессов (Сколько соксов столько и процессов)
# 4.Передаем каждому процессу функцию рассылки и аргументы(сокс)



# start_time = time.time()
# def printi():
# 	print 'hi'

# def thread_sent(class_):
# 	"""Sent one letter in one process"""
# 	fromaddr = class_.get_fromaddr(1)
# 	toaddr = 
# 	try:
# 		server.sendmail(lst_data['from'], lst_data['to'], lst_data['letter'])
# 		return 'ok'
# 	except:
# 		return 'ok'

# def mailer_proc(socks,count_threading):
# 	start_time = time.time()
# 	# activate socks
# 	m = MailerBears()
# 	# ehlo = m.socks_activate(socks)

# 	# # open connection
# 	# server_mail = 'mxs.mail.ru'	
# 	# server = smtplib.SMTP(server_mail)

# 	result = []

# 	for i in range(count_threading):
# 		t = threading.Thread(target=printi)
# 		t.start()
# 		# result.append(t)

# 	print time.time()-start_time

# 	# print 'Ative '+str(threading.activeCount())+' '+' '.join(result)

# 	# print ' '.join(result)




# # mailer_proc("162.243.207.126,3128,goemailgo,q8uir",100000)
# i=0
# while i<100000:
# 	printi()

# print time.time()-start_time



# start_time = time.time()

# m = MailerBears()
# ehlo = m.socks_activate("162.243.207.126,3128,goemailgo,q8uir")

# server_mail = 'mxs.mail.ru'
# server = smtplib.SMTP(server_mail)

# def thread_sent(lst_data):
# 	try:
# 		server.sendmail(lst_data['from'], lst_data['to'], lst_data['letter'])
# 		return 'ok'
# 	except:
# 		return 'ok'

# if __name__ == '__main__':

	
# 	toaddr=['nikolaiofwt001mum@mail.ru' for x in range(1,100)]

# 	countprocess=20
# 	count = len(toaddr)
# 	# print count
	
# 	fromaddr = m.get_fromaddr(count)
# 	# print len(fromaddr)
# 	letter = m.get_letter(count,ehlo,fromaddr,toaddr)
# 	# print len(letter)

# 	lst_data = [{'from':i[0],'to':i[1],'letter':i[2]} for i in zip(fromaddr, toaddr, letter)]

# 	# Connect mail server
	
# 	# server.set_debuglevel(1)
# 	server.ehlo(ehlo)
# 	# generate list for dict
# 	print time.time()-start_time
	

# 	pool = Pool(count)
# 	pool.map(thread_sent, lst_data)
# 	pool.close()
# 	pool.join()


# 	server.quit()

# 	print time.time()-start_time

	# m.sent_emails(countprocess,hostname,letter,fromaddr,toaddr)
	





