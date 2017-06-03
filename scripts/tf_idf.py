# encoding=utf8
# Vaughn Johnson CSE 472 Final Project

import os, re, codecs, math, pickle
from collections import Counter
from sys import argv
from sklearn.preprocessing import normalize
from nltk.tokenize import word_tokenize

# By-products of Google Drive and OSX
IRRELEVANT = [".DS_Store", 'Icon\r', '', None]
SAVE_FILE = "model.txt"

class TF_IDF:
    def __init__(self, train_data_path, n=3, retrain=True):
        self.TRAIN_DATA_PATH = train_data_path
        # N in n-grams, default tri-grams
        self.N = n
        self.model = self.gen_tf_idf(retrain)
        self.languages = self.model.keys()

    def gen_tf_idf(self, retrain):
        if not retrain and os.stat(SAVE_FILE).st_size > 2:
            tf_idf = pickle.load(open(SAVE_FILE, "rb"))
        else:
            # The names of the languages used
            languages = set()

            for f in os.listdir(self.TRAIN_DATA_PATH):
                language = f.split(".")[0]
                if not language in IRRELEVANT:
                    languages.add(language)

            # key: language, value: training text of that lanague
            language_texts = {}

            # Counts for individual languages, 1-N_grams
            n_grams = {}

            # num of uni-gram through tri-gram tokens encountered
            total_tokens = {}

            for language in languages:
                text = codecs.open("%s/%s.txt" %(self.TRAIN_DATA_PATH, language), 'r', 'utf-8').read()
                language_texts[language] = text

            # Tokenize
            print "Tokenizing..."
            for language in language_texts:
                text = language_texts[language]
                counts = self.n_tokenize(text)
                n_grams[language] = counts
                total_tokens[language] = sum([x[1] for x in counts.items()])

            corpus_tokens = Counter()

            tf_idf = {}
            # Does the tf  of tf-idf
            print "Calculating tf-idf..."
            for language in n_grams:
                tf_idf[language] = {}
                language_counts = n_grams[language]
                for token in language_counts:
                    corpus_tokens[token] += language_counts[token]
                    tf = float(language_counts[token]) / float(total_tokens[language])
                    tf_idf[language][token] = tf

            corp_tokens_total = sum([x[1] for x in corpus_tokens.items()])

            # Does the idf of tf-idf
            for language in tf_idf:
                for token in tf_idf[language]:
                    idf = math.log(float(corp_tokens_total) / float(corpus_tokens[token]))
                    tf_idf[language][token] *= idf

            pickle.dump(tf_idf, open(SAVE_FILE, "wb"))

        print "done training model"
        return tf_idf

    def n_tokenize(self, string, debug=False):
        tokens = Counter()
        word_tokens = word_tokenize(string)
        for j in range(1, self.N + 1):
            for i in range(0, len(string) - j):
                tokens[string[ i : i + j]] += 1
            for i in range(0, len(word_tokens) - j):
                tokens[(" ").join(word_tokens[i : i+j])] += 1
        if debug:
            print tokens
            raw_input()
        return tokens

    def most_likely_language(self, input_string, debug=False):
        score = {}
        tokens = self.n_tokenize(input_string, debug)
        for language in self.model:
            score[language] = 0
            for token in tokens:
                if token in self.model[language]:
                    score[language] += self.model[language][token] * tokens[token]

        return max(score.items(), key=lambda x: x[1])[0]
