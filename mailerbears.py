# -*- coding: utf-8 -*-
import string
import random
import re
import os
import datetime
import sys
import smtplib
import socks
import socket
import quopri
import email.message
from email.parser import Parser
import math
from multiprocessing import Pool
import urllib


class Tag():
	spaces_s = [' ','','']
	spacewords = [' ','   ']
	tabs = ['\n','','\n\n','\t','\t\n']
	punctuation = [',','!','?','.','.','.',',','','','-',';',':']
	br_tag=['<br >','<br/>','<br>','','']
	font_family = ["'Courier New', Courier, monospace","Arial, Helvetica, sans-serif",'Verdana','Tahoma']
	timezones = ['03','02','01']
	

	tag = {
	'table':['dir','align','cellpadding','cellspacing','border','width','style','id','class'],
	'td':['align','valign','width','id','class','border','style'],
	'a':['align','valign','width','id','class','border','style'],
	'img':['align','valign','width','id','class','border','style'],
	'tr':[],
	'tbody':[],
	}

	encodings = {
    'UTF-8':'utf8',
    'CP1251':'cp1251',
    'KOI8-R':'koi8-r',
    'IBM866':'ibm866',
    'ISO-8859-5':'iso-8859-5',
    'MAC':'mac',
	}

	def word_gen(self,count,lang='eng'):
		words =''
		for i,ws in enumerate(range(count)):
			if lang and lang=='eng':
				vowels = ['e','y','u','i','o','a']
				consonants = ['q','w','r','t','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
			else:
				vowels = ['а','у','е','ы','о','э','я','и','ю','ё']
				consonants = ['й','ц','к','н','г','ш','щ','з','х','ъ','ф','в','п','р','л','д','ж','ч','с','м','т','ь','б']

			word = ''
			for w in range(random.randint(1,3)):
				abc_list = [''.join(random.sample(vowels,random.randint(1,2))), ''.join(random.sample(consonants,random.randint(1,2)))]
				random.shuffle(abc_list)
				word += ''.join(abc_list)

			if i>0:
				words+=word+random.choice(self.spacewords)
				if i%4==0:
					words+=random.choice(self.punctuation)
			else:
				words+=word
		return words

	def style_gen(self,opacity="no",attr_effect='yes'):
		# Атрибуты и значения не влияющие на отображение
		if attr_effect=="no":
			attr = {
			'align':random.choice(['']),
			'width': random.choice(['auto','inherit','']),
			'border':'0px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'padding':random.choice(['inherit',str(random.randint(0,3))+'px', str(random.randint(0,3))+'px'+str(random.randint(0,3))+'px'+str(random.randint(0,3))+'px'+str(random.randint(0,3))+'px']),
			# 'color':random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'font-family':random.choice(['Helvetica, Arial, sans-serif','Arial','Tahoma','Verdana','Helvetica']),
			'font-style':random.choice(['normal','italic','oblique','inherit']),
			'background-color': '' ,#random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'font-size':random.choice([str(random.randint(7,18))+random.choice(['px']),'inherit', 'x-small', 'small', 'medium', 'large']),
			'font-weight':random.choice(['bold','bolder','lighter','normal','100','200','300','400','500','600','700','800','900']),
			'height':random.choice(['auto','inherit','']),
			'border-top':random.choice(['','0px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')'])]),
			'border-bottom':random.choice(['','0px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')'])]),
			'border-left':random.choice(['','0px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')'])]),
			'border-right':random.choice(['','0px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')'])]),
			'line-height':random.choice(['normal','inherit','']),
			'display':random.choice(['block','']),
			# 'opacity':str(random.random()),
			}

		else:
			attr = {
			'align':random.choice(['center','left','right','']),
			'width': random.choice([str(random.randint(20,200))+random.choice(['px','%']),'auto','inherit','']),
			'border':str(random.randint(0,2))+'px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'padding':random.choice(['inherit',str(random.randint(0,23))+random.choice(['px','%']), str(random.randint(0,23))+random.choice(['px ','% '])+str(random.randint(0,23))+random.choice(['px ','% '])+str(random.randint(0,23))+random.choice(['px ','% '])+str(random.randint(0,23))+random.choice(['px ','% '])]),
			'color':random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'font-family':random.choice(['Helvetica, Arial, sans-serif','Arial','Tahoma','Verdana','Helvetica']),
			'font-style':random.choice(['normal','italic','oblique','inherit']),
			'background-color':random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'font-size':random.choice([str(random.randint(3,18))+random.choice(['px','pt']),str(random.randint(73,216))+'%','inherit','xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']),
			'font-weight':random.choice(['bold','bolder','lighter','normal','100','200','300','400','500','600','700','800','900']),
			'height':random.choice([str(random.randint(20,200))+random.choice(['px','%']),'auto','inherit','']),
			'border-top':str(random.randint(0,2))+'px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'border-bottom':str(random.randint(0,2))+'px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'border-left':str(random.randint(0,2))+'px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'border-right':str(random.randint(0,2))+'px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'line-height':random.choice(['normal','inherit',str(random.randint(0,20))+'px',str(random.randint(0,4))+'%',str(random.randrange(0,2))]),
			'display':random.choice(['inline-block','block','none','inline','inline-table','list-item','run-in','table','table-caption','table-cell','table-column','table-row','table-row-group','table-footer-group','table-header-group','table-column-group']),
			# 'opacity':str(random.random()),
			}

		# Случайное количество атрибутов
		count_random = random.randint(0,round(len(attr.keys())/2))

		if opacity=="opacity":
			# Удаляем из словаря display и opacity
			attr.pop('display')
			# attr.pop('opacity')
			attr_style = attr.keys()[:count_random]
			attr['display'] = 'none'
			attr['opacity'] = '0'
			# attr_style+=[random.choice(['display','opacity'])]
			attr_style+=['display']+['opacity']



		else:
			attr_style = attr.keys()[:count_random]


		# Выбираем случайные атрибуты и рандомим их если больше одного
		if len(attr_style)>0:
			random.shuffle(attr_style)

		# Формируем строку из атрибутов и их значений
		list_attr = []
		for a in attr_style:
			qoutes = random.choice(['\'','\"'])
			a = random.choice(self.spaces_s)+a+random.choice(self.spaces_s)+':'+random.choice(self.spaces_s)+attr[a]+random.choice(self.spaces_s)+';'
			list_attr.append(a)

		string_style = ' '.join(list_attr)
		return string_style


	def attr_gen(self,tagname,opacity="no",attr_effect='yes'):
		if attr_effect=="no":
			# Атрибуты и значения не влияющие на отображение
			tag_this = {
			'table':['dir','align','cellpadding','cellspacing','border','width','style','id','class'],
			'td':['align','valign','width','id','class','border','style'],
			'tr':[],
			'tbody':[],
			'a':['align','valign','width','id','class','border','style'],
			'img':['align','valign','width','id','class','border','style'],
			}

			attr = {
			'dir':random.choice(['auto','']),
			'align':random.choice(['']),
			'valign':random.choice(['']),
			'width': random.choice(['auto','inherit','']),
			'cellpadding':'0',
			'cellspacing':'0',
			'border':'0px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'style':self.style_gen(attr_effect='no'),
			'id':self.word_gen(1,'eng'),
			'class':self.word_gen(1,'eng'),
			}

		else:
			tag_this = {
			'table':['dir','align','cellpadding','cellspacing','border','width','style','id','class'],
			'td':['align','valign','width','id','class','border','style'],
			'tr':[],
			'tbody':[],
			'a':['align','valign','width','id','class','border','style'],
			'img':['align','valign','width','id','class','border','style'],
			}

			attr = {
			'dir':random.choice(['ltr','rtl','auto','']),
			'align':random.choice(['center','left','right','']),
			'valign':random.choice(['top','middle','bottom','baseline','']),
			'width': random.choice([str(random.randint(20,200))+random.choice(['px','%']),'auto','inherit','']),
			'cellpadding':str(random.randint(0,5)),
			'cellspacing':str(random.randint(0,5)),
			'border':str(random.randint(0,2))+'px '+random.choice(['solid','dotted','dashed','double','groove','ridge','inset','outset'])+' '+random.choice(['#'+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)),'rgb('+str(random.randint(0,255))+','+str(random.randint(0,255))+','+str(random.randint(0,255))+')']),
			'style':self.style_gen(),
			'id':self.word_gen(1,'eng'),
			'class':self.word_gen(1,'eng'),
			}


		count_random = random.randint(0,len(tag_this[tagname]))

		if opacity=="opacity":
					
			# Удаляем из словаря style
			attr.pop('style')
			tag_this[tagname].pop(6)

			attr_tags = tag_this[tagname][:count_random]
			attr['style']=self.style_gen('opacity')	
			attr_tags +=['style']

		else:
			# Выбираем случайные атрибуты и рандомим их если больше одного
			attr_tags = self.tag[tagname][:count_random]



		if len(attr_tags)>0:
			random.shuffle(attr_tags)


		# Формируем строку из атрибутов и их значений
		list_attr = []
		for a in attr_tags:
			qoutes = random.choice(['\'','\"'])
			a = random.choice(self.spaces_s)+a+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes+random.choice(self.spaces_s)+attr[a]+random.choice(self.spaces_s)+qoutes+random.choice(self.spaces_s)
			list_attr.append(a)

		qoutes = random.choice(['\'','\"'])
		string_attrs = ' '.join(list_attr+[random.choice(['data-'+self.word_gen(1,'eng')+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes+random.choice(self.spaces_s)+self.word_gen(1,'eng')+random.choice(self.spaces_s)+qoutes,'','','',''])])

		return string_attrs

	def tag_fake(self,tagname,count=1,opacity='no',lang='eng',text='no'):
		if opacity=='opacity':
			style_table = self.attr_gen(tagname,opacity)
		else:
			style_table = self.attr_gen(tagname)
		
		tag_str = ''
		for i in range(0,count):
			table = '<'+tagname+' '+random.choice(self.spaces_s)+style_table+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)
			table += '<tbody '+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)

			# Генерим tr 
			for tr in xrange(random.randint(1,7)):
				# td = '<'+random.choice(self.spaces_s)+'td'+random.choice(self.spaces_s)+attr_gen('td')+random.choice(self.spaces_s)+'>'
				table += '<tr '+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)
				for i in xrange(random.randint(1,4)):
					if text=='no':
						td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td')+random.choice(self.spaces_s)+'>'+'</td'+random.choice(self.spaces_s)+'>'
					else:
						td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td')+random.choice(self.spaces_s)+'>'+self.word_gen(random.randint(1,27),lang)+'</td'+random.choice(self.spaces_s)+'>'
					table += td+random.choice(self.tabs)
				table += '</tr'+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)

			table += '</tbody'+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)+'</'+tagname+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)
			tag_str += table

		return tag_str


	def tag_general(self,tagname,count=1,opacity='no',lang="eng"):
		domain = open('domain.txt','r').read().strip()
		if opacity=='opacity':
			style_table = self.attr_gen(tagname,opacity)
		else:
			style_table = self.attr_gen(tagname,attr_effect='no')
		
		tag_str = ''
		for i in range(0,count):
			table = '<'+tagname+' '+random.choice(self.spaces_s)+style_table+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)
			table += '<tbody '+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)

			# Генерим tr 
			for i,tr in enumerate(xrange(random.randint(1,7))):
				# td = '<'+random.choice(self.spaces_s)+'td'+random.choice(self.spaces_s)+attr_gen('td')+random.choice(self.spaces_s)+'>'
				table += '<tr '+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)

				if i == 0:
					count_td = random.randint(1,4)
					for c,m in enumerate(xrange(count_td)):
						if c == 0:
							random_for_a = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(3,9)))
							random_for_a2 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(3,9)))
							random_for_img = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(random.randint(3,9)))
							qoutes_a = random.choice(['\'','\"'])
							qoutes_a2 = random.choice(['\'','\"'])
							qoutes_img = random.choice(['\'','\"'])
							# Картинка в ссылке + текст + ссылки текстовые							
							td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td',attr_effect='no')+random.choice(self.spaces_s)+'>'+'<p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'[%%ORandText,paysystem3713_hello%%]'+random.choice(self.spaces_s)+random.choice(['<br/>'+random.choice(self.spaces_s),'<br/>'+random.choice(self.spaces_s)+'<br/>'])+random.choice(self.spaces_s)+'[%%ORandText,title_17_07_aws%%] '+random.choice(self.spaces_s)+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+qoutes_a2+'http://'+domain+'/'+random_for_a2+qoutes_a2+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'[%%ORandText,paysystem3713_link%%]'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'</p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'<br/>'+random.choice(self.spaces_s)+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_a+'http://'+domain+'/'+random_for_a+qoutes_a+random.choice(self.spaces_s)+' '+self.attr_gen('a',attr_effect='no')+'>'+random.choice(self.spaces_s)+'<img '+random.choice(self.spaces_s)+'src'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_img+'http://'+domain+'/'+random_for_img+'.jpg'+qoutes_img+' '+random.choice(self.spaces_s)+self.attr_gen('img',attr_effect='no')+'/>'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'+'</td'+random.choice(self.spaces_s)+'>'

							# Рандом строка вместо текстов. Картинки и ссылки
							# td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td',attr_effect='no')+random.choice(self.spaces_s)+'>'+'<p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+self.word_gen(random.randint(3,38),lang)+random.choice(self.spaces_s)+random.choice(['<br/>'+random.choice(self.spaces_s),'<br/>'+random.choice(self.spaces_s)+'<br/>'])+random.choice(self.spaces_s)+self.word_gen(random.randint(3,48),lang)+random.choice(self.spaces_s)+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+qoutes_a2+'http://'+domain+'/'+random_for_a2+qoutes_a2+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+self.word_gen(random.randint(1,2),lang)+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'</p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'<br/>'+random.choice(self.spaces_s)+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_a+'http://'+domain+'/'+random_for_a+qoutes_a+random.choice(self.spaces_s)+' '+self.attr_gen('a',attr_effect='no')+'>'+random.choice(self.spaces_s)+'<img '+random.choice(self.spaces_s)+'src'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_img+'http://'+domain+'/'+random_for_img+'.jpg'+qoutes_img+' '+random.choice(self.spaces_s)+self.attr_gen('img',attr_effect='no')+'/>'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'+'</td'+random.choice(self.spaces_s)+'>'
							
							# Только картинка в ссылке
							# td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td',attr_effect='no')+random.choice(self.spaces_s)+'>'+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_a+'http://'+domain+'/'+random_for_a+qoutes_a+random.choice(self.spaces_s)+' '+self.attr_gen('a',attr_effect='no')+'>'+random.choice(self.spaces_s)+'<img '+random.choice(self.spaces_s)+'src'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_img+'http://'+domain+'/'+random_for_img+'.jpg'+qoutes_img+' '+random.choice(self.spaces_s)+self.attr_gen('img',attr_effect='no')+'/>'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'+'</td'+random.choice(self.spaces_s)+'>'

							# На месте картинок и ссылок просто рандом
							# td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td',attr_effect='no')+random.choice(self.spaces_s)+'>'+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_a+random_for_img+random_for_a+qoutes_a+random.choice(self.spaces_s)+' '+self.attr_gen('a',attr_effect='no')+'>'+random.choice(self.spaces_s)+'<img '+random.choice(self.spaces_s)+'src'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_img+random_for_a2+random_for_img+'.jpg'+qoutes_img+' '+random.choice(self.spaces_s)+self.attr_gen('img',attr_effect='no')+'/>'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'+'</td'+random.choice(self.spaces_s)+'>'
							
						else:
							td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td','opacity')+random.choice(self.spaces_s)+'>'+'</td'+random.choice(self.spaces_s)+'>'

						table += td+random.choice(self.tabs)
				else:
					for i in xrange(random.randint(1,3)):
						td = '<td '+random.choice(self.spaces_s)+self.attr_gen('td','opacity')+random.choice(self.spaces_s)+'>'+self.word_gen(random.randint(3,38),lang)+'</td'+random.choice(self.spaces_s)+'>'
						table += td+random.choice(self.tabs)

				table += '</tr'+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)

			table += '</tbody'+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)+'</'+tagname+random.choice(self.spaces_s)+'>'+random.choice(self.tabs)
			tag_str += table

		return tag_str

	def tag_simple(self,tag):
		random_for_a = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(3,9)))
		random_for_img = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(random.randint(3,9)))
		random_for_a2 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(3,9)))
		qoutes_a = random.choice(['\'','\"'])
		qoutes_a2 = random.choice(['\'','\"'])
		qoutes_img = random.choice(['\'','\"'])
		domain = open('domain.txt','r').read().strip()

		if tag=="img":
			tag = '<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_a+'http://'+domain+'/'+random_for_a+qoutes_a+random.choice(self.spaces_s)+' >'+random.choice(self.spaces_s)+'<img '+random.choice(self.spaces_s)+'src'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_img+'http://'+domain+'/'+random_for_img+'.jpg'+qoutes_img+' '+random.choice(self.spaces_s)+'/>'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'
		elif tag=='p+a+img':
			tag = '<p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'[%%ORandText,paysystem3713_hello%%]'+random.choice(self.spaces_s)+random.choice(['<br/>'+random.choice(self.spaces_s),'<br/>'+random.choice(self.spaces_s)+'<br/>'])+random.choice(self.spaces_s)+'[%%ORandText,title_17_07_aws%%] '+random.choice(self.spaces_s)+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+qoutes_a2+'http://'+domain+'/'+random_for_a2+qoutes_a2+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'[%%ORandText,paysystem3713_link%%]'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'</p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'<br/>'+random.choice(self.spaces_s)+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_a+'http://'+domain+'/'+random_for_a+qoutes_a+random.choice(self.spaces_s)+' >'+random.choice(self.spaces_s)+'<img '+random.choice(self.spaces_s)+'src'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_img+'http://'+domain+'/'+random_for_img+'.jpg'+qoutes_img+' '+random.choice(self.spaces_s)+'/>'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'
		elif tag=='p+img':
			tag = '<p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'[%%ORandText,paysystem3713_hello%%]'+random.choice(self.spaces_s)+random.choice(['<br/>'+random.choice(self.spaces_s),'<br/>'+random.choice(self.spaces_s)+'<br/>'])+random.choice(self.spaces_s)+'[%%ORandText,title_17_07_aws%%] '+random.choice(self.spaces_s)+random.choice(self.spaces_s)+'</p'+random.choice(self.spaces_s)+'>'+random.choice(self.spaces_s)+'<br/>'+random.choice(self.spaces_s)+'<a '+random.choice(self.spaces_s)+'href'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_a+'http://'+domain+'/'+random_for_a+qoutes_a+random.choice(self.spaces_s)+' >'+random.choice(self.spaces_s)+'<img '+random.choice(self.spaces_s)+'src'+random.choice(self.spaces_s)+'='+random.choice(self.spaces_s)+qoutes_img+'http://'+domain+'/'+random_for_img+'.jpg'+qoutes_img+' '+random.choice(self.spaces_s)+'/>'+random.choice(self.spaces_s)+'</a'+random.choice(self.spaces_s)+'>'
		
		return tag

	def synonyms(self,match):
			list_words = match.group().split('|')
			words = random.choice(list_words).replace('{','').replace('}','')
			return words
	def mix(self,match):
			list_words = match.group().replace('[','').replace(']','').split('%%')
			random.shuffle(list_words)
			words =' '.join(list_words)
			return words

	def replace_spaces(self,match):
		spaces2 = random.choice(self.spacewords)
		return spaces2

	def tabss(self,match):
		tabsr = random.choice(self.tabs)
		return tabsr

	def replace_br(self,match):
		br = random.choice(self.br_tag)
		return br

	def replace_qoutes(self,match):
		qoutes = random.choice(['\'','\"'])
		b=match.group().replace('_QOUTE_',qoutes)
		return b

	def replace_digit(self,match):
		a = match.group()
		str_digit = int(match.group('digit'))
		str_start = int(match.group('s'))
		str_end = int(match.group('e'))
		# if str_start==0:
		# 	a = str(str_digit+random.randint(0,str_end),str_digit-random.randint(str_start,str_end)]))		
		str_ready = str(str_digit+random.randint(-str_start,str_end))
		return str_ready

	def replace_datatag(self,match):	
		str_ready = 'data-'+self.word_gen(1,'eng')+'="'+self.word_gen(1,'eng')+'"'
		return str_ready

	def replace_class(self,match):	
		str_ready = self.word_gen(1,'eng')
		return str_ready

	def replace_faketag(self,match):
		nametag = match.group('name').lower()
		if match.group('lang'):
			lang = match.group('lang').lower()
			var_text = 'yes'
			if match.group('lang')=='NO':
				var_text = 'no'

		faketag = self.tag_fake(nametag,1,'opacity',lang=lang,text=var_text)
		return faketag

	def replace_usertag(self,match):
		nametag = match.group('name').lower().replace('_','')
		list_files = os.listdir('user_macro')

		if nametag in list_files:
			list_files_userdir = os.listdir('user_macro/'+nametag)
			file_choice = random.choice(list_files_userdir)
			datauser = open('user_macro/'+nametag+'/'+file_choice).read()
		elif nametag+'.txt' in list_files:
			datauser_lst = open('user_macro/'+nametag+'.txt').readlines()
			datauser = random.choice(datauser_lst)
		else:
			datauser = ''

		return datauser

	def replace_font_family(self,match):
		font_family_this = 'font-family:'+random.choice(self.font_family)+';'
		return font_family_this

	# Methods for body_raw
	def replace_digit_raw_body(self,match):
		sym1= match.group('sym1')
		sym = match.group('sym')
		digit = match.group('digit')
		if int(digit) in range(10,90):
			new_digit = sym1+'_DIGIT_'+digit+'_2_4_'+sym
		elif int(digit)in range(90,101):
			new_digit = sym1+'_DIGIT_'+digit+'_5_0_'+sym
		elif int(digit)>100:
			new_digit = sym1+'_DIGIT_'+digit+'_35_35_'+sym
		elif int(digit)in range(2,10):
			new_digit = sym1+'_DIGIT_'+digit+'_2_2_'+sym
		else:
			new_digit = sym1+digit+sym			
		return new_digit

	def replace_datatag_raw_body(self,match):	
		return '_DATA_'

	def replace_class_raw_body(self,match):	
		return 'class="_CLASS_"'

	def replace_fontf_raw_body(self,match):
		return '_FONT_FAMILY_'

	def replace_href_raw_body(self,match):
		return 'a href="_LINK'+random.choice(['1','2'])+'_"'

	def replace_src_raw_body(self,match):
		return 'img src="_IMG_"'

	def replace_tabs_raw_body(self,match):
		tag= match.group('tab')
		return tag+'_TAB_'

	def replace_qoutes_raw_body(self,match):
		return '_QOUTE_'

	def replace_spaces_raw_body(self,match):
		return '_SPACES_'

	"""
	Определение кодировки текста
	"""
	def get_codepage(self,str = None):
	    uppercase = 1
	    lowercase = 3
	    utfupper = 5
	    utflower = 7
	    codepages = {}
	    for enc in self.encodings.keys():
	        codepages[enc] = 0
	    if str is not None and len(str) > 0:
	        last_simb = 0
	        for simb in str:
	            simb_ord = ord(simb)

	            """non-russian characters"""
	            if simb_ord < 128 or simb_ord > 256:
	                continue

	            """UTF-8"""
	            if last_simb == 208 and (143 < simb_ord < 176 or simb_ord == 129):
	                codepages['UTF-8'] += (utfupper * 2)
	            if (last_simb == 208 and (simb_ord == 145 or 175 < simb_ord < 192)) \
	                or (last_simb == 209 and (127 < simb_ord < 144)):
	                codepages['UTF-8'] += (utflower * 2)

	            """CP1251"""
	            if 223 < simb_ord < 256 or simb_ord == 184:
	                codepages['CP1251'] += lowercase
	            if 191 < simb_ord < 224 or simb_ord == 168:
	                codepages['CP1251'] += uppercase

	            """KOI8-R"""
	            if 191 < simb_ord < 224 or simb_ord == 163:
	                codepages['KOI8-R'] += lowercase
	            if 222 < simb_ord < 256 or simb_ord == 179:
	                codepages['KOI8-R'] += uppercase

	            """IBM866"""
	            if 159 < simb_ord < 176 or 223 < simb_ord < 241:
	                codepages['IBM866'] += lowercase
	            if 127 < simb_ord < 160 or simb_ord == 241:
	                codepages['IBM866'] += uppercase

	            """ISO-8859-5"""
	            if 207 < simb_ord < 240 or simb_ord == 161:
	                codepages['ISO-8859-5'] += lowercase
	            if 175 < simb_ord < 208 or simb_ord == 241:
	                codepages['ISO-8859-5'] += uppercase

	            """MAC"""
	            if 221 < simb_ord < 255:
	                codepages['MAC'] += lowercase
	            if 127 < simb_ord < 160:
	                codepages['MAC'] += uppercase

	            last_simb = simb_ord

	        idx = ''
	        max = 0
	        for item in codepages:
	            if codepages[item] > max:
	                max = codepages[item]
	                idx = item
	        return idx
	

	def body(self,filename,counttext):
		html = open('body/'+filename,'r').read()
		# encoddingfile = self.encodings[self.get_codepage(html)]
		# html = html.decode(encoddingfile)
		body = ''

		###CONTENT GENERATE

		#HELLO GENERATE
		hello_raw = open('user_macro/+hello.txt','r').readlines()
		hello = hello_raw[counttext%len(hello_raw)]

		#TEXT GENERATE
		text = open('user_macro/+text.txt','r').readlines()
		text = text[counttext%len(text)]

		# Processing synonyms
		regex_synonyms = re.compile(r'(?P<synonyms>{[^{}]+})')
		while text.find('{')!= -1:
			text = regex_synonyms.sub(self.synonyms,text)

		# Processing mix
		regex_mix = re.compile(r'(?P<mix>\[[^\[\]]+\])')
		while text.find('[')!= -1:
			text = regex_mix.sub(self.mix,text)

		# Replace spaces
		spacestemp = re.compile(r'(_SPACES_)')
		while text.find('_SPACES_')!= -1:
			text = spacestemp.sub(self.replace_spaces,text)

		# Replace tabs
		tabs = re.compile(r'(_TAB_)')
		while text.find('_TAB_')!= -1:
			text = tabs.sub(self.tabss,text)

		# Replace br
		brs = re.compile(r'(_BR_)')
		while text.find('_BR_')!= -1:
			text = brs.sub(self.replace_br,text)

		#TEXT_BUTTON GENERATE
		button_text_raw = open('user_macro/+button_text.txt','r').readlines()
		button_text = button_text_raw[counttext%len(button_text_raw)]

		#LINKS GENERATE
		random_link1 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(3,13)))
		random_link2 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(3,13)))
		random_img = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(random.randint(3,13)))		
		domain = open('user_macro/+domain.txt','r').read().strip()
		link1 = 'http://'+domain+'/'+random_link1
		link2 = 'http://'+domain+'/'+random_link2
		img = 'http://'+domain+'/'+random_img+'.jpg'

		body += html.replace('_HELLO_', hello).replace('_TEXT_', text).replace('_LINK1_',link1).replace('_LINK2_',link2).replace('_IMG_',img).replace('_BUTTON_',button_text)

		###CONTENT GENERATE END

		###STYLE GENERATE

		# Replace spaces
		spaces3 = re.compile(r'(_SPACES_)')
		while body.find('_SPACES_')!= -1:
			body = spaces3.sub(self.replace_spaces,body)

		# Replace tabs
		tabs = re.compile(r'(_TAB_)')
		while body.find('_TAB_')!= -1:
			body = tabs.sub(self.tabss,body)

		# Replace qoutes
		qoutes = re.compile(r'(_QOUTE_.*[.]*_QOUTE_)')
		while body.find('_QOUTE_')!= -1:
			body = qoutes.sub(self.replace_qoutes,body)
		
		# Replace digit
		digit_html = re.compile(r'(_DIGIT_(?P<digit>[0-9]+)_(?P<s>[0-9]+)_(?P<e>[0-9]+)_)')
		while body.find('_DIGIT_')!= -1:
			body = digit_html.sub(self.replace_digit,body)

		# Replace datatag
		datatag = re.compile(r'(_DATA_)')
		while body.find('_DATA_')!= -1:
			body = datatag.sub(self.replace_datatag,body)

		# Replace class
		classattr = re.compile(r'(_CLASS_)')
		while body.find('_CLASS_')!= -1:
			body = classattr.sub(self.replace_class,body)

		# Replace FAKETAG
		faketag = re.compile(r'(_FAKETAG_(?P<name>[^_]+)_*(?P<lang>[^_]*)_+)')
		while body.find('_FAKETAG_')!= -1:
			body = faketag.sub(self.replace_faketag,body)

		# Replace USERTAGS
		usertag = re.compile(r'(_USER_(?P<name>[^_]+)_)')
		while body.find('_USER_')!= -1:
			body = usertag.sub(self.replace_usertag,body)

		# Replace FONT FAMILY
		font_family_html = re.compile(r'(_FONT_FAMILY_)')
		while body.find('_FONT_FAMILY_')!= -1:
			body = font_family_html.sub(self.replace_font_family,body)

		headers_my = ''

		body = body.replace('_HEADERS_',headers_my)


		###STYLE GENERATE END
		return body


	def text(self,counttext):
		body = ''

		###CONTENT GENERATE

		#HELLO GENERATE
		hello_raw = open('user_macro/+hello.txt','r').readlines()
		hello = hello_raw[counttext%len(hello_raw)]

		#TEXT GENERATE
		text = open('user_macro/+text.txt','r').readlines()
		text = text[counttext%len(text)]

		# Processing synonyms
		regex_synonyms = re.compile(r'(?P<synonyms>{[^{}]+})')
		while text.find('{')!= -1:
			text = regex_synonyms.sub(self.synonyms,text)

		# Processing mix
		regex_mix = re.compile(r'(?P<mix>\[[^\[\]]+\])')
		while text.find('[')!= -1:
			text = regex_mix.sub(self.mix,text)

		# Replace spaces
		spacestemp = re.compile(r'(_SPACES_)')
		while text.find('_SPACES_')!= -1:
			text = spacestemp.sub(self.replace_spaces,text)

		# Replace tabs
		tabs = re.compile(r'(_TAB_)')
		while text.find('_TAB_')!= -1:
			text = tabs.sub(self.tabss,text)

		#LINKS GENERATE
		random_link1 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(3,13)))
		domain = open('user_macro/+domain.txt','r').read().strip()
		link1 = 'http://'+domain+'/'+random_link1	

		body += text+'  '+link1+'\n\n_HEADERS_'

		###CONTENT GENERATE END		

		headers_my = ''

		body = body.replace('_HEADERS_',headers_my)


		###STYLE GENERATE END
		return body

	def headers_generate(self,fromaddr,toaddr,domain,bcc='no'):
		template_headers = random.choice(['thebat4.2.23'])
		if type(toaddr)==list:
			toaddr=','.join(toaddr)

		now_time = datetime.datetime.now()-datetime.timedelta(minutes=random.randint(23,176))
		# Generate Headers
		from_letter = 'From: '+fromaddr+'\n'
		date_letter = 'Date: '+now_time.strftime('%a, %d %b %Y %H:%M:%S ')+random.choice(['+'])+random.choice(self.timezones)+'00\r\n'#Date: Sat, 22 Aug 2015 07:30:38 +0400		
		priority_x = 'X-Priority: 3 (Normal)\n'
		to_letter = 'To: '+str(toaddr)+'\n'
		message_id = 'Message-ID: <'+str(random.randint(382429100,1892311982))+'.'+now_time.strftime('%Y%m%d%H%M%S')+'@'+domain+'\r\n'
		# subject = 'Subject: '+self.word_gen(random.randint(3,6),'ru')+'\r\n'
		subject = 'Subject: '+'\r\n'
		mime = 'MIME-Version: 1.0\r\n'
		content_type = 'Content-Type: text/plain; charset=windows-1251\r\n'
		content_transfer = 'Content-Transfer-Encoding: quoted-printable\r\n'#quoted-printable 8bit

		header = date_letter+from_letter+priority_x+to_letter+message_id+subject+mime+content_type+content_transfer+'\r\n'
		
		if bcc != False:
			bcc_letter = 'BCC: '+bcc+'\n'
			header = date_letter+from_letter+priority_x+to_letter+bcc_letter+message_id+subject+mime+content_type+content_transfer+'\r\n'

		return header




class Letter():
	"""Letter generate for sent"""		

	def html(self):
		tag = Tag()

		# How sent letter
		count = 1

		counter_file = open('counter.txt','r')
		counter = int(counter_file.read().strip())
		counter_file.close()

		counttext = int(math.ceil(counter/count))

		new_counter = open('counter.txt','w')
		new_counter.write(str(1+counter))
		new_counter.close()

		files_html = os.listdir('body')
		filename = random.choice(files_html)
		letter = tag.body(filename=filename,counttext=counttext)

		return letter

	def text(self):
		tag = Tag()

		# How sent letter
		count = 1

		counter_file = open('counter.txt','r')
		counter = int(counter_file.read().strip())
		counter_file.close()

		counttext = int(math.ceil(counter/count))

		new_counter = open('counter.txt','w')
		new_counter.write(str(1+counter))
		new_counter.close()

		text = tag.text(counttext=counttext)

		return text



	def proc(self):
		tag = Tag()
		new_html_list = os.listdir('body_raw')
		for html in new_html_list:
			html_this = open('body_raw/'+html,'r').read()

			# Замена всех дата тегов
			data_tag = re.compile(r'(data[-\w*\d*]+=".+?")')
			html_this = data_tag.sub(tag.replace_datatag_raw_body,html_this)

			# Замена всех классов
			class_attr = re.compile(r'(class="\w*\d*")')
			html_this = class_attr.sub(tag.replace_class_raw_body,html_this)

			# Замена шрифтов на _FONT_FAMILY_
			font_family = re.compile(r'(font-family:.+?;)')
			html_this = font_family.sub(tag.replace_fontf_raw_body,html_this)		

			# Замена ссылок на _LINK1_ или _LINK2_
			href_attr = re.compile(r'(a\s*href=".+?")')
			html_this = href_attr.sub(tag.replace_href_raw_body,html_this)

			# Замена картинки на _IMG_
			src_attr = re.compile(r'(img\s*src="http.+?")')
			html_this = src_attr.sub(tag.replace_src_raw_body,html_this)

			# Замена всех не нулевых числовых значений на _DIGIT_100_0_1. Если 0 не заменяем. Если от 10 до 90 - делаем вилку +-3. Если Больше 100 вилку +-13
			# pdb.set_trace()
			digit_html = re.compile(r'(?P<sym1>[\(|"|,|\s*]+)\s*(?P<digit>[0-9]+)\s*(?P<sym>[\)|px|%|;|"|,|px;|]+)')
			html_this = digit_html.sub(tag.replace_digit_raw_body,html_this)

			# Подстановка нескольких _TAB_ между тегами
			tad_temp = re.compile(r'(?P<tab></.+?>|<.+?>)')
			html_this = tad_temp.sub(tag.replace_tabs_raw_body,html_this)

			html_this = '_HEADERS_ _USER_HEADERS_'+html_this+'_USER_FOOTERS_'

			# # Замена всех пробелов на _SPACES_
			# spaces_temp = re.compile(r'(\s+)')
			# html_this = spaces_temp.sub(tag.replace_spaces_raw_body,html_this)

			# # Замена кавычек на _QOUTE_
			# qoutes_temp = re.compile(r'(["]+)')
			# html_this = qoutes_temp.sub(tag.replace_qoutes_raw_body,html_this)

			html_name = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S_")+str(random.randint(17,28908))+'.html'
			record_html = open('body/'+html_name,'w')
			record_html.write(html_this)
			record_html.close()

		return True




class MailerBears():
	"""docstring for MailerBears"""
	def __init__(self):
		self.tag = Tag()

	def get_socks(self,link_socks):
		return map(lambda x:x.strip(),urllib.urlopen(link_socks).readlines())

	def get_recipient(self,path_recipientfile):
		recipient = map(lambda x:x.strip(),open(path_recipientfile,'r').readlines())
		random.shuffle(recipient)
		return recipient
	

	def socks_activate(self,socks_a):
		try:
			socks_raw = socks_a.strip().split(',')
			socks_active = {'ip':socks_raw[0],'port':int(socks_raw[1]),'hostname':socket.gethostbyaddr(socks_raw[0]),'username':socks_raw[3],'password':socks_raw[4]}
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr=socks_active['ip'], port=socks_active['port'],username=socks_active['username'],password=socks_active['password'])
			socks.wrapmodule(smtplib)
			
			result = (socks_active['hostname'][0],socks_active['ip'])
			# print type(result)
			return result
		except:
			return False

	def get_fromaddr(self):
		# fromaddres = []
		# while (range(count)):
		# 	rand_all_domain = ''.join(random.choice(open(filename,'r').readlines())).strip()
		# 	fromaddr = self.tag.word_gen(1,'eng')+'@'+rand_all_domain
		# 	fromaddres.append(fromaddr)

		# return fromaddres
		filename='data/domain_all.txt'
		fromaddres = self.tag.word_gen(1,'eng')+'@'+''.join(random.choice(open(filename,'r').readlines())).strip()
		return fromaddres

	def get_letter(self,count,hostname,form_addr,toaddr,bcc):
		headers_letters = self.tag.headers_generate(form_addr,toaddr,''.join(form_addr.split('@')[1]),bcc)
		msgs = self.tag.word_gen(random.randint(10,1567),'ru')
		letters = Parser().parsestr(headers_letters+msgs).as_string()


		

		
		# while (range(count)):
		# 	#Generate body letter
		# 	# letter = Letter()
		# 	# body_letter = letter.html()
		# 	headers_letter = self.tag.headers_generate(fromaddr=form_addr,toaddr=toaddr,domain=form_addr.split('@')[1])
		# 	letter1 = self.tag.word_gen(random.randint(10,1567),'ru')
		# 	msg = 
		# 	letters.append(msg)
			#Generate header letter
			# Return dict {'Subject':subject,'Date':date_letter,'X-Priority':priority_x,'Message-ID':message_id,'MIME-Version':mime,'Content-Type':content_type,'Content-Transfer-Encoding':content_transfer}

		# print msg
		return letters


	# def sent_mail_one(self,data_for_sent):
	# 	pass

		


	# def sent_emails(self,count,ehlo,letter,fromaddr,toaddr):
	# 	server_mail = 'mxs.mail.ru'
	# 	server = smtplib.SMTP(server_mail)
	# 	server.set_debuglevel(1)
	# 	server.ehlo(ehlo)
	# 	# generate list for dict
	# 	lst_data = [{'from':i[0],'to':i[1],'letter':i[2]} for i in zip(fromaddr, toaddr, letter)]

	# 	def thread_sent(lst_data):
	# 		server.sendmail(lst_data['from'], lst_data['to'], lst_data['letter'])
	# 		return 'ok'
		
	# 	if __name__ == "__main__":	
		
	# 		pool = Pool(count)
	# 		pool.map(thread_sent, lst_data)
	# 		pool.close()
	# 		pool.join()

		
	# 	server.quit()




# from concurrent.futures import ThreadPoolExecutor

# with ThreadPoolExecutor(concurrency) as executor:
# 	for _ in executor.map(create_droplet, random.sample(list_region,concurrency)):
# i = 0
# while i<100:
# 	server.sendmail(fromaddr, toaddr, msg)
# 	i+=1


# msg = email.message.Message.(headers_letter+tag.word_gen(random.randint(17,167),'eng'))
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

# date_letter = now_time.strftime('%a, %d %b %Y %H:%M:%S ')+random.choice(['-','+'])+random.choice(self.timezones)+'00'#Date: Sat, 22 Aug 2015 07:30:38 +0400
# from_letter = fromaddr
# priority_x = '3 (Normal)'
# to_letter = toaddr
# message_id = '<'+str(random.randint(382429100,1892311982))+'.'+now_time.strftime('%Y%m%d%H%M%S')+'@'+domain
# subject = self.word_gen(random.randint(3,6),'eng')
# mime = '1.0'
# content_type = 'text/plain; charset="windows-1251"'
# content_transfer = '8bit'

# header = {'Subject':subject,'Date':date_letter,'X-Priority':priority_x,'Message-ID':message_id,'MIME-Version':mime,'Content-Type':content_type,'Content-Transfer-Encoding':content_transfer}

# headers_generate('fromaddr','toaddr','domain')
# from randletter import *
# Example header
# thebat4.2.23
# Date: Sat, 22 Aug 2015 06:34:47 +0400
# From: Ostapbuzzer011nee@mail.ru
# X-Priority: 3 (Normal)
# Message-ID: <475829410.20150822063447@mail.ru>
# To: Osipbendere010lli@mail.ru
# Subject: fewf
# MIME-Version: 1.0
# Content-Type: text/plain; charset=windows-1251
# Content-Transfer-Encoding: 8bit


# Date: Sat, 22 Aug 2015 07:11:44 +0400
# From: Nikolaypkpw002nox@mail.ru
# X-Priority: 3 (Normal)
# Message-ID: <1724811729.20150822071144@mail.ru>
# To: Nikolaiofwt001mum@mail.ru, Platonvojep016bra@mail.ru, 
# <Platonidaqh017mar@mail.ru>, <Olganiklucm009orr@mail.ru>, 
# <Petrorientw015tir@mail.ru>
# CC: Platonvojep016bra@mail.ru, Platonidaqh017mar@mail.ru
# Subject: Привет дорогой друг
# MIME-Version: 1.0
# Content-Type: text/plain; charset=windows-1251
# Content-Transfer-Encoding: 8bit


# Date: Sat, 22 Aug 2015 07:18:14 +0400
# From: Ostapbuzzer011nee@mail.ru
# X-Priority: 3 (Normal)
# Message-ID: <382429868.20150822071814@mail.ru>
# To: Nikolaiofwt001mum@mail.ru, Nikolaypkpw002nox@mail.ru, 
#         <Ninabombass003jin@mail.ru>, <Ninelraselg004ppo@mail.ru>, 
#         <Oksananickk005sam@mail.ru>, <Oktyabrinah006qwn@mail.ru>, 
#         <Olegmatrosm007huo@mail.ru>, <Olesyajonnd008bre@mail.ru>, 
#         <Olganiklucm009orr@mail.ru>, <Osipbendere010lli@mail.ru>, 
#         <Pavelchoicj012bra@mail.ru>, <Pavlinastre013ohe@mail.ru>, 
#         <Pelageyabwp014num@mail.ru>, <Petrorientw015tir@mail.ru>, 
#         <Platonvojep016bra@mail.ru>, <Platonidaqh017mar@mail.ru>, 
#         <Polinalnsae018div@mail.ru>, <Potappronsn019kre@mail.ru>, 
#         <Praskovyaqn020ree@mail.ru>
# CC: Nikolaiofwt001mum@mail.ru, Nikolaypkpw002nox@mail.ru, 
#         <Ninabombass003jin@mail.ru>, <Ninelraselg004ppo@mail.ru>, 
#         <Oksananickk005sam@mail.ru>, <Oktyabrinah006qwn@mail.ru>, 
#         <Olegmatrosm007huo@mail.ru>, <Olesyajonnd008bre@mail.ru>, 
#         <Olganiklucm009orr@mail.ru>, <Osipbendere010lli@mail.ru>, 
#         <Pavelchoicj012bra@mail.ru>, <Pavlinastre013ohe@mail.ru>, 
#         <Pelageyabwp014num@mail.ru>, <Petrorientw015tir@mail.ru>, 
#         <Platonvojep016bra@mail.ru>, <Platonidaqh017mar@mail.ru>, 
#         <Polinalnsae018div@mail.ru>, <Potappronsn019kre@mail.ru>, 
#         <Praskovyaqn020ree@mail.ru>
# Subject: fwegweqgweqg
# MIME-Version: 1.0
# Content-Type: text/plain; charset=windows-1251
# Content-Transfer-Encoding: 8bit

# 382429868.20150822071814@mail.ru
# 1724811729.20150822071144@mail.ru
# 475829410.20150822063447@mail.ru
# 914340047.20150822073038@mail.ru
# 1892311982.20150822075945@mail.ru

# Date: Sat, 22 Aug 2015 07:30:38 +0400
# From: Ostapbuzzer011nee@mail.ru
# X-Priority: 3 (Normal)
# Message-ID: <914340047.20150822073038@mail.ru>
# To: Nikolaiofwt001mum@mail.ru, Nikolaypkpw002nox@mail.ru, 
#         <Ninelraselg004ppo@mail.ru>
# CC: Potappronsn019kre@mail.ru
# BCC: Nikolaiofwt001mum@mail.ru, Ninabombass003jin@mail.ru, 
#         <Osipbendere010lli@mail.ru>, <Pavelchoicj012bra@mail.ru>
# MIME-Version: 1.0
# Content-Type: text/plain; charset=windows-1251
# Content-Transfer-Encoding: 8bit

# Здравствуйте, Nikolaiofwt001mum.

# Date: Sat, 22 Aug 2015 07:59:45 +0400
# From: Ostapbuzzer011nee@mail.ru
# X-Priority: 2 (High)
# Message-ID: <1892311982.20150822075945@mail.ru>
# To: Nikolaiofwt001mum@mail.ru
# Subject: ewgwgwqgewqg
# MIME-Version: 1.0
# Content-Type: text/plain; charset=windows-1251
# Content-Transfer-Encoding: 8bit44
