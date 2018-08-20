# -*- coding: UTF-8 -*- 
import os


if __name__ == '__main__':
	path_prefix = 'C:/travaux/web_crawling/frenchcorpus/downloads/full/secondExtract/extracted/'
	path_suffix = '/etc/PROMPTS'

	with open('./outputs/output.txt', 'w') as output: 
		for sentences_group in os.listdir(path_prefix):
			with open(path_prefix + sentences_group + path_suffix, 'r', encoding='utf-8') as prompts:
				for line in prompts.readlines():
					output.write(line.split(' ', 1)[1].lower())