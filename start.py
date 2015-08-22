#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import smtplib
import dns.resolver
import socks
from letter import *
import socket
import quopri
from email.mime.text import MIMEText

IP_SOCKS = "188.166.126.101"
SOCKS_MY = {'ip':IP_SOCKS,'port':3128,'hostname':socket.gethostbyaddr(IP_SOCKS),'username':'goemailgo','password':'q8uir'}

answers = dns.resolver.query('mail.ru', 'MX')
if len(answers) <= 0:
    sys.stderr.write('No mail servers found for destination\n')
    sys.exit(1)
 
# Just pick the first answer
server = str(answers[0].exchange)
# server = 'mxs.mail.ru'

rand_all_domain = ''.join(random.choice(open('data/domain_all.txt','r').readlines())).strip()
tag = Tag()
# Add the From: and To: headers
fromaddr = tag.word_gen(1,'eng')+'@'+rand_all_domain
toaddr = 'dzhoniana@mail.ru'

letter = Letter()
headers_letter = tag.headers_generate(fromaddr=fromaddr,toaddr=toaddr,domain=rand_all_domain)
body_letter = letter.html()

msg = MIMEText(tag.word_gen(random.randint(6,21),'eng').encode('cp1251'),None,None)
msg['Date'] = headers_letter['Date']
msg['From'] = fromaddr
msg['X-Priority'] = headers_letter['X-Priority']
# msg['X-MAX'] = 'gwegwegweg'
msg['Message-ID'] = headers_letter['Message-ID']
msg['To'] = toaddr
msg['Subject'] = tag.word_gen(random.randint(4,6),'eng')
msg['MIME-Version'] = headers_letter['MIME-Version']
msg['Content-Type'] = headers_letter['Content-Type']
msg['Content-Transfer-Encoding'] = headers_letter['Content-Transfer-Encoding']

# {'Subject':subject,'Date':date_letter,'X-Priority':priority_x,'Message-ID':message_id,'MIME-Version':mime,'Content-Type':content_type,'Content-Transfer-Encoding':content_transfer}


# msg = headers_letter+'\r\n\r\n'+quopri.decodestring(tag.word_gen(random.randint(6,21),'eng'))
# msg = 'From: {0}\r\n To: {1}\r\n\n {2}'.format(fromaddr,toaddr,'Hello my friends')

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr=SOCKS_MY['ip'], port=SOCKS_MY['port'],username=SOCKS_MY['username'],password=SOCKS_MY['password'])
socks.wrapmodule(smtplib) 
server = smtplib.SMTP(server)
server.set_debuglevel(1)
server.ehlo(SOCKS_MY['hostname'][0])
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
