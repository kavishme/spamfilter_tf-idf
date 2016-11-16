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
	idf = OrderedDict()

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
		for word in sdict:
			count = docs[doc]['count'][word]
			if count:
				docs[doc]['tf'][word] = 1 + log( 1 + log(count, 10), 10)
			else:
				docs[doc]['tf'][word] = 0


	for word in sdict:
		freq = 0
		for d in docs:
			if docs[d]['count'][word] > 0:
				freq += 1
		if freq:
			idf[word] = log((1+len(docs))/freq, 10)
		else:
			idf[word] = 0


	for doc in docs:
		if 'tfidf' not in docs[doc].keys():
			docs[doc]['tfidf'] = OrderedDict()
		for word in sdict:
			docs[doc]['tfidf'][word] = idf[word] * docs[doc]['tf'][word]


	print('-'*SEP)
	print('***Spam dictionary***', ','.join(sdict), sep='\n\n')

	print('-'*SEP)
	print('***Word frequency table***')
	print('\n')
	for doc in docs:
		print(doc, " \t".join([str(docs[doc]['count'][word]) for word in docs[doc]['count']]))


	print('-'*SEP)
	print('***IDF***')
	print('\n')
	print("  \t".join([str(format(idf[word],fformat)) for word in sdict]))

	print('-'*SEP)
	print('***TF table***')
	print('\n')
	for doc in docs:
		print(doc, " \t".join([str(format(docs[doc]['tf'][word], fformat)) for word in docs[doc]['tf']]))

	print('-'*SEP)
	print('***TF-IDF table***')
	print('\n')
	for doc in docs:
		print(doc, " \t".join([str(format(docs[doc]['tfidf'][word], fformat)) for word in docs[doc]['tfidf']]))
	print('-'*SEP)

if __name__ == '__main__':
	main()