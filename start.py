#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1. Сделать тот в точь заголовки thebat
# 2. Писать логи рассылки в sqlite 
# 3. Сделать многопоточную отправку писем с 9 соксов
 

from mailerbears import *	

if __name__ == '__main__':

	m = MailerBears()
	toaddr=['nikolaiofwt001mum@mail.ru' for x in range(1,10)]
	countprocess=10
	count = len(toaddr)
	hostname = m.socks_activate("128.199.198.210,3128,goemailgo,q8uir")
	fromaddr = m.get_fromaddr(count)
	# print fromaddr
	letter = m.get_letter(count,hostname,fromaddr,toaddr)
	# print letter
	m.sent_emails(countprocess,hostname,letter,fromaddr,toaddr)
	





