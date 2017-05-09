import csv
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

stemmer = PorterStemmer()

with open('labeled_news_stem.csv', 'wb') as outf:
	newswriter = csv.writer(outf, delimiter=',', quotechar='"')

	with open('labeled_news.csv', 'rb') as csvf:
		newsreader = csv.reader(csvf, delimiter=',', quotechar='"')
		count = 0
		for line in newsreader:
			count += 1
			if len(line[1]) == 0:
				print '\nnews %i: no TITILE' % count
				print line
				continue

			# news with no description, replaced by title
			if len(line[2]) == 0:
				print '\nnews %i: no DESCRIPTION' % count
				line[2] = line[1]

			# stemming description
			words = word_tokenize(line[2])
			words_stemed = map(lambda x: stemmer.stem(x), words)
			line[2] = " ".join(words_stemed)
			newswriter.writerow(line)
			
		print 'done %i' % count