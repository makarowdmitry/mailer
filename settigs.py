import logging
from ts import *

bears = MailerBears() #Initial class MailerBears()
concurrent = 15
to = 1
bcc = 0 #random.randint(54,85)
cc = 0
logging_file = 'data/mylog.log'

path_socks = 'http://109.234.38.38/media/sss/o4.txt' #List Socks
socks = bears.get_socks(path_socks)

recipients = bears.get_recipient('data/myemail2.txt') #List recipient



count_raz = int(round(len(recipients)/len(socks)))
# print count_raz
# print len(recipients)
# print len(socks)


recipient = []

for i in range(0,len(socks)):
	if i == (len(socks)-1):
		recipient.append(recipients[:])
		
	else:
		recipient.append(recipients[:count_raz])		
		del recipients[:count_raz]



def start_mailer(socks):
	for i,sock in enumerate(socks):	
		p = Process(target=threading_socks, args=(sock,recipient[i],i,concurrent,to,bcc,cc,logging_file))
		p.start()
	return True


# COUNTER = {_.split(',')[0]:{'Success':0,'AuthenticationError':0,'HeloError':0,'ConnectError':0,'Spam rejected':0,'Bounce':0,'Temporarily rejected':0,'Ratelimit exceeded':0,'ProxyConnectionError':0,'ServerDisconnected':0,'SenderRefused':0,'RecipientsRefused':0,'Other':0} for _ in SOCKS}
# COUNTER['All']={'Success':0,'Nosent':0,'AuthenticationError':0,'HeloError':0,'ConnectError':0,'Spam rejected':0,'Bounce':0,'Temporarily rejected':0,'Ratelimit exceeded':0,'ProxyConnectionError':0,'ServerDisconnected':0,'SenderRefused':0,'RecipientsRefused':0,'Other':0}




if __name__ == "__main__":
	if len(sys.argv)!=2:
		print 'Enter the command "r" for round or "c" for many rounds'

	elif sys.argv[1]=='r':
		clears_logs()
		start_mailer(socks)	

	elif sys.argv[1]=='c':
		pass

	else:
		print 'Enter the command "r" for round or "c" for many rounds'
