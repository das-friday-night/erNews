from sklearn.feature_extraction.text import TfidfVectorizer

doc1 = "I like apples. I like oranges too"
doc2 = "I love apples. I hate doctors"
doc3 = "An apple a day keeps the doctor away"
doc4 = "Never compare an apple to an orang"

documents = [doc1, doc2, doc3, doc4]

tfidf = TfidfVectorizer().fit_transform(documents)

# pairwise_sim is a n*n matrix of cosine similarity.
#   cell (i,j) is the ith document cosine similarity to jth
#   * is dot product
pairwise_sim = tfidf * tfidf.T

# Cosine Similarity between the first document with each of the other documents of the set:
doc1_sim = tfidf[0] * tfidf.T

print tfidf.T.shape
print tfidf.shape
print tfidf[0].shape

print pairwise_sim.A
print doc1_sim.A
