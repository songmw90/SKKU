# -*- coding: utf-8 -*-
from lxml import etree
import os, sys
from unidecode import unidecode

__author__ = "SDN and IoT"

#@func: fast_iter
#@param context : iterparsed (chunk of xml) data
#@param func : handler
#@desc: Read xml chunk. After read, clear and delete chunk to release memory.
#		Also, replace html encoding to similar ascii code

def fast_iter(context, func,*args, **kwargs):
    collaborations = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
    #xml categories
    author_array = []
    title = ''

    #read chunk line by line
    #we focus author and title
    for event, elem in context:
        if elem.tag == 'author':
            author_array.append(unidecode(elem.text))

        if elem.tag == 'title':
        	if elem.text:
	        	title = unidecode(elem.text)

        if elem.tag in collaborations:
        	if len(author_array) is not 0 and title is not '':
	        	#rejected paper has no author or title
	        	#it should be check

        		for a in author_array:
        			func(a+"||"+title, *args, **kwargs)
        			#write into kv file

        		title = ''
    		 	del author_array[:]
 
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    #clear chunks

#@func: process_element
#@param elem : parsed data of chunk
#@param fout : file name to write
#@desc: It is handler to write content. just write content to file
def process_element(elem, fout):
	print "writing ... " + elem
	print >>fout, elem

if __name__ == "__main__":
	fout = open('parsed_data.txt', 'w')
	context = etree.iterparse('dblp.xml', load_dtd=True,html=True)
	#To use iterparse, we don't need to read all of xml.
	fast_iter(context, process_element, fout)