#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1. Сделать тот в точь заголовки thebat
# 2. Писать логи рассылки в sqlite 
# 3. Сделать многопоточную отправку писем с 9 соксов
 
import sys
import smtplib
import dns.resolver
import socks
from letter import *
import socket
import quopri
import email.message
from email.parser import Parser

IP_SOCKS = "128.199.198.210"
SOCKS_MY = {'ip':IP_SOCKS,'port':3128,'hostname':socket.gethostbyaddr(IP_SOCKS),'username':'goemailgo','password':'q8uir'}

answers = dns.resolver.query('mail.ru', 'MX')
if len(answers) <= 0:
    sys.stderr.write('No mail servers found for destination\n')
    sys.exit(1)
 
# Just pick the first answer
server = str(answers[0].exchange)
# server = 'mxs.mail.ru'

rand_all_domain = ''.join(random.choice(open('data/domain_all.txt','r').readlines())).strip()
print rand_all_domain

tag = Tag()
# Add the From: and To: headers
fromaddr = tag.word_gen(1,'eng')+'@'+rand_all_domain
toaddr = 'nikolaiofwt001mum@mail.ru'
toaddrbcc = 'Nikolaiofwt001mum@mail.ru,Nikolaypkpw002nox@mail.ru,Ninabombass003jin@mail.ru,Ninelraselg004ppo@mail.ru,Oksananickk005sam@mail.ru,Oktyabrinah006qwn@mail.ru,Olegmatrosm007huo@mail.ru,Olesyajonnd008bre@mail.ru,Olganiklucm009orr@mail.ru,Osipbendere010lli@mail.ru,Pavelchoicj012bra@mail.ru,Pavlinastre013ohe@mail.ru,Pelageyabwp014num@mail.ru,Petrorientw015tir@mail.ru,Platonvojep016bra@mail.ru,Platonidaqh017mar@mail.ru,Polinalnsae018div@mail.ru,Potappronsn019kre@mail.ru,Praskovyaqn020ree@mail.ru'

#Generate body letter
letter = Letter()
body_letter = letter.html()



#Generate header letter
# Return dict {'Subject':subject,'Date':date_letter,'X-Priority':priority_x,'Message-ID':message_id,'MIME-Version':mime,'Content-Type':content_type,'Content-Transfer-Encoding':content_transfer}
headers_letter = tag.headers_generate(fromaddr=fromaddr,toaddr=toaddr,domain=rand_all_domain)

msg = Parser().parsestr(headers_letter+tag.word_gen(random.randint(10,1567),'ru'))
# msg = email.message.Message.(headers_letter+tag.word_gen(random.randint(17,167),'eng'))
# print msg

# msg = MIMEText(tag.word_gen(random.randint(6,21),'eng').encode('cp1251'))
# msg = MIMEText('hi')

# del msg['Content-Type']
# del msg['MIME-Version']
# del msg['Content-Transfer-Encoding']
# msg['Date'] = headers_letter['Date']
# msg['From'] = fromaddr
# msg['X-Priority'] = headers_letter['X-Priority']
# # msg['X-MAX'] = 'gwegwegweg'
# msg['Message-ID'] = headers_letter['Message-ID']
# msg['To'] = toaddr
# msg['Subject'] = tag.word_gen(random.randint(4,6),'eng')
# # msg['CC'] = toaddrbcc
# msg['MIME-Version'] = headers_letter['MIME-Version']
# msg['Content-Type'] = headers_letter['Content-Type']
# msg['Content-Transfer-Encoding'] = headers_letter['Content-Transfer-Encoding']




# msg = headers_letter+'\r\n\r\n'+quopri.decodestring(tag.word_gen(random.randint(6,21),'eng'))
# msg = 'From: {0}\r\n To: {1}\r\n\n {2}'.format(fromaddr,toaddr,'Hello my friends')

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr=SOCKS_MY['ip'], port=SOCKS_MY['port'],username=SOCKS_MY['username'],password=SOCKS_MY['password'])
socks.wrapmodule(smtplib) 
server = smtplib.SMTP(server)
server.set_debuglevel(1)
server.ehlo(SOCKS_MY['hostname'][0])
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
