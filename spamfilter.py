#!python3

import os
from math import log
from collections import OrderedDict

DICTFILE = 'dict.txt'
MAILFOLDER = './mails/'
SEP = 150
fformat = '.3f'

def getSpamDictionary(filename):
	f = open(filename, 'r')
	words = f.read()
	words = [word.strip().lower() for word in words.split('\n')]
	return words


def main():

	sdict = getSpamDictionary(DICTFILE)
	
	docs = OrderedDict()
	for fi in os.listdir(MAILFOLDER):
		if fi.endswith(".txt"):
			f = open(MAILFOLDER + fi, 'r')
			docs[fi] = OrderedDict()
			docs[fi]['data'] = f.read().strip().lower().replace('-', ' ').replace('\n', ' ')

	for word in sdict:
		for doc in docs:
			data = docs[doc]['data'].split(' ')
			count = []
			for w in word.split(' '):
				count.append(data.count(w))

			if 'count' not in docs[doc].keys():
				docs[doc]['count'] = OrderedDict()

			docs[doc]['count'][word] = min(count)


	for doc in docs:
		if 'tf' not in docs[doc].keys():
			docs[doc]['tf'] = OrderedDict()
		if 'idf' not in docs[doc].keys():
			docs[doc]['idf'] = OrderedDict()
		for word in sdict:
			count = docs[doc]['count'][word]
			if count:
				docs[doc]['tf'][word] = 1 + log( 1 + log(count, 10), 10)
			else:
				docs[doc]['tf'][word] = 0

			freq = 0
			for d in docs:
				if docs[d]['count'][word] > 0:
					freq += 1
			if freq:
				docs[doc]['idf'][word] = log((1+len(docs))/freq, 10)
			else:
				docs[doc]['idf'][word] = 0

	print('-'*SEP)
	print('Spam dictionary:', ','.join(sdict))

	print('-'*SEP)
	print('IDF')
	for doc in docs:
		print("\t".join([str(format(docs[doc]['idf'][word],fformat)) for word in docs[doc]['idf']]))
		break;

	print('-'*SEP)
	print('Word frequency table')
	for doc in docs:
		print(doc, "\t".join([str(docs[doc]['count'][word]) for word in docs[doc]['count']]))

	print('-'*SEP)
	print('TF table')
	for doc in docs:
		print(doc, "\t".join([str(format(docs[doc]['tf'][word], fformat)) for word in docs[doc]['tf']]))
	print('-'*SEP)

if __name__ == '__main__':
	main()