#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1. Сделать тот в точь заголовки thebat
# 2. Писать логи рассылки в sqlite 
# 3. Сделать многопоточную отправку писем с 9 соксов


 

from mailerbears import *
from functools import partial

m = MailerBears()
ehlo = m.socks_activate("128.199.243.171,3128,goemailgo,q8uir")

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

	
	toaddr=['nikolaiofwt001mum@mail.ru' for x in range(1,500)]

	countprocess=10
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

	

	pool = Pool(count)
	pool.map(thread_sent, lst_data)
	pool.close()
	pool.join()


	server.quit()

	# m.sent_emails(countprocess,hostname,letter,fromaddr,toaddr)
	





