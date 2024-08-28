import json
import nltk

from collections import Counter
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords



with open('sample.jsonl','r') as f:
    selected_papers = json.load(f)

bigrams = []
unigrams = []
for paper in selected_papers:
    text_tokens = word_tokenize(paper['target_population'])
    unigrams.extend([word for word in text_tokens if not word in stopwords.words()])

    sentences = sent_tokenize(paper['target_population'])
    bigrams.extend([b for s in sentences for b in zip(s.split(" ")[:-1], s.split(" ")[1:])])

for unigram in Counter(unigrams).most_common(30):
    if len(unigram[0])>1:
        print(unigram)

print()
for bigram in Counter(bigrams).most_common(80):
    if bigram[0][1] not in stopwords.words() and bigram[0][0] not in stopwords.words() and len(bigram[0][1])>1 and len(bigram[0][0])>1:
        print(bigram)


