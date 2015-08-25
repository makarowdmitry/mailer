from multiprocessing import Pool

def sent_emails(count,ehlo,letter,fromaddr,toaddr):	
	# generate list for dict
	lst_data = [ehlo,count]+[{'from':i[0],'to':i[1],'letter':i[2]} for i in zip(fromaddr, toaddr, letter)]
	

	def thread_sent(lst_data):
		server.sendmail(lst_data['from'], lst_data['to'], lst_data['letter'])
		return 'ok'
	
	
	
		

	
	server.quit()

if __name__ == "__main__":
	sent_emails_data = sent_

	server_mail = 'mxs.mail.ru'
	server = smtplib.SMTP(server_mail)
	# server.set_debuglevel(1)
	server.ehlo(ehlo)

	pool = Pool(count)
	pool.map(thread_sent, lst_data)
	pool.close()
	pool.join()
