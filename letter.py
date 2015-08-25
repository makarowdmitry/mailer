# -*- coding: utf-8 -*-
from randletter import *
import random
import math
import os
import re
import datetime

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
