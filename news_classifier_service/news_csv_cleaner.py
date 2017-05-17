import csv
import os
import yaml
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()

TRAINER_DIR = os.path.dirname(__file__)
NEWSCLASS = config['NEWSCLASSES']['reverse_map']
STEM_ON = True
CLASSDETECT_OVERWRITE_EXIST_CLASS = False
TBDCLASS = '0'

def classDetect(url):
    corpus = {
        "World" : ["world"],
        "Entertainment" : ["movie", "art", "entertain", "tv", "season", "episode", "television", "music", "film", "theater"],
        "Politics & Government" : ["politic", "govern", "trump", "healthcare", "election", "presiden", "health-care"],
        "Sports" : ["sport", "espn", "football", "soccer"],
        "Technology" : ["technology", "iphone", "facebook", "uber", "microsoft"],
        "Economic & Corp" : ["economi", "business", "financ"],
        "Crime" : ["kill", "crime", "police", "dead", "death", "die", "murder"]
    }
    for newsclass, keylist in corpus.iteritems():
        if any(word in url for word in keylist):
            return NEWSCLASS[newsclass]
    return TBDCLASS


def cleanser():
    # inFile format: class, title, description, url
    inFile = 'label.csv'
    outFile = 'labeled_news_cleaned.csv'
    outFile2 = 'labeled_news_tbd.csv'
    stemmer = None
    if STEM_ON:
        inFile = 'labeled_news.csv'
        outFile = 'labeled_news_stem.csv'
        stemmer = PorterStemmer()
    inFile = os.path.join(TRAINER_DIR, inFile)
    outFile = os.path.join(TRAINER_DIR, outFile)
    outFile2 = os.path.join(TRAINER_DIR, outFile2)

    with open(outFile, 'wb') as outf:
        newswriter = csv.writer(outf, delimiter=',', quotechar='"')

        with open(outFile2, 'wb') as outf2:
            newswriter2 = csv.writer(outf2, delimiter=',', quotechar='"')

            with open(inFile, 'rb') as inf:
                newsreader = csv.reader(inf, delimiter=',', quotechar='"')
                count = 0
                for line in newsreader:
                    count += 1
                    # convert existing class name to number
                    # convert only those class name is not 1~17
                    if not line[0].isdigit():
                        if len(line[0]) != 0:
                            if CLASSDETECT_OVERWRITE_EXIST_CLASS:
                                line[0] = classDetect(line[3])
                            else:
                                line[0] = NEWSCLASS[line[0]]
                        else:
                            line[0] = classDetect(line[3])

                    # news with no title, skip
                    if len(line[1]) == 0:
                        print '\nnews %i: no TITILE' % count
                        print line
                        continue

                    # news with no description, replaced by title
                    if len(line[2]) == 0:
                        print '\nnews %i: no DESCRIPTION' % count
                        line[2] = line[1]

                    # stemming description
                    if STEM_ON:
                        words = word_tokenize(line[2])
                        words_stemed = map(lambda x: stemmer.stem(x), words)
                        line[2] = " ".join(words_stemed)

                    if line[0] == TBDCLASS:
                        newswriter2.writerow(line)
                    else:
                        newswriter.writerow(line)

                print 'stem: %r. class overwrite: %r. num: %i' % (STEM_ON, CLASSDETECT_OVERWRITE_EXIST_CLASS, count)


cleanser()