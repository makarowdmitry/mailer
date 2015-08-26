#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1. Сделать тот в точь заголовки thebat
# 2. Писать логи рассылки в sqlite 
# 3. Сделать многопоточную отправку писем с 9 соксов

Каждый процесс
Перед каждым процессом

Параметры
_RECIPIENT_BASE_1_1800000_TO_1_100_BCC_1_100_CC_1_100_,_THREADING_20_,_FROM_(RANDSTR/USER_URL)_USER_LIST_

_THREADING_20_
_FROM_(RANDSTR/USER_LIST)_USER_LIST_
_DOMAINS_(NEXT/RAND)_1_USER_LIST_


Обновить
_RECIPIENT_BASE_1_1800000_TO_1_100_BCC_1_100_CC_1_100_
На каждый раунд



Подготовка
1.Берем получателей из файла - записываем их в список
2.Берем соксы из файла - записываем их в список
3.Выделяем нужно количество процессов (Сколько соксов столько и процессов)
4.Передаем каждому процессу функцию рассылки и аргументы(сокс)

Функция рассылки
1. 

from mailerbears import *
from functools import partial
import time

start_time = time.time()

m = MailerBears()
ehlo = m.socks_activate("162.243.207.126,3128,goemailgo,q8uir")

server_mail = 'mxs.mail.ru'
server = smtplib.SMTP(server_mail)

def thread_sent(lst_data):
	try:
		server.sendmail(lst_data['from'], lst_data['to'], lst_data['letter'])
		return 'ok'
	except:
		return 'ok'

def printing(lim):
	print lim

if __name__ == '__main__':

	
	toaddr=['nikolaiofwt001mum@mail.ru' for x in range(1,100)]

	countprocess=20
	count = len(toaddr)
	# print count
	
	fromaddr = m.get_fromaddr(count)
	# print len(fromaddr)
	letter = m.get_letter(count,ehlo,fromaddr,toaddr)
	# print len(letter)

	lst_data = [{'from':i[0],'to':i[1],'letter':i[2]} for i in zip(fromaddr, toaddr, letter)]

	# Connect mail server
	
	# server.set_debuglevel(1)
	server.ehlo(ehlo)
	# generate list for dict
	print time.time()-start_time
	

	pool = Pool(count)
	pool.map(thread_sent, lst_data)
	pool.close()
	pool.join()


	server.quit()

	print time.time()-start_time

	# m.sent_emails(countprocess,hostname,letter,fromaddr,toaddr)
	





