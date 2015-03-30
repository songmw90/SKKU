#!/usr/bin/env python

# Author : Myeong-Uk (fantazm@skku.edu)
# Date : 2015. 03. 24
# Desc : 
# Python program to count word in RFC
# command : <python wordcount.py filename>
# Download any text file e.g. wget https://tools.ietf.org/html/rfc5432
# OUTPUT > filename_word_count.out

import sys,re,string,operator,csv

def read_file(filename):
	fp = open(filename, 'r')
	text = prepare_raw_text(fp.read())
	fp.close()
	return text

def prepare_raw_text(rawtext):
	text = re.sub('[^A-Za-z]+', ' ', rawtext) #alphabetize word
	text = text.lower().split() # convert to lowercase , split words using white space
	return text


def group_words(words):
	dict = {}
	for word in words: #loop 0 to word 
		if len(word) > 1: #word should longer than 1 (optional)
			if word in dict:
				dict[word] += 1
			else:
				dict[word] = 1
	return sorted(dict.items(), key=operator.itemgetter(1), reverse=True) #sort dictionary to check frequency

def record_frequency(filename,list):
	fp = open(filename+"_word_count.out","w")
	for item in list:
	  fp.write(item[0] + " " + str(item[1]) + "\n")
	fp.close()

if __name__ == '__main__':
	filename = sys.argv[1]
	text = read_file(sys.argv[1])
	list = group_words(text)
	record_frequency(filename,list)
	print "done!"
