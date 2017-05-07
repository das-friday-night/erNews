import csv

with open('test.csv', 'wb') as outf:
	newswriter = csv.writer(outf, delimiter=',', quotechar='"')

	with open('labeled_news.csv', 'rb') as csvf:
		newsreader = csv.reader(csvf, delimiter=',', quotechar='"')
		count = 0
		for line in newsreader:
			count += 1
			# print line
			# if len(line[1]) == 0:
			# 	print '\nnews %i: no TITILE' % count
			# 	print line
			if len(line[2]) == 0:
				print '\nnews %i: no DESCRIPTION' % count
				line[2] = line[1]
				newswriter.writerow(line)
			else:
				newswriter.writerow(line)
			# if len(line[3]) == 0:
			# 	print '\nnews %i: no SOURCE' % count
			# 	print line

		print 'done'