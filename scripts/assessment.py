# encoding=utf8
# Vaughn Johnson CSE 472 Final Project
from sys import argv
from tf_idf import TF_IDF as tfidf
import os, codecs

n = 4

TF_IDF = tfidf(argv[-2], n=3, retrain=True)

TEST_PATH = argv[-1]
TEST_LEN = 200

language_list = dict(zip(TF_IDF.languages, range(0, len(TF_IDF.languages))))

confusion_matrix = [[0 for i in range(0, len(language_list))] for j in range(0, len(language_list))]

tests = {}

def test_split(text, n):
    tests = []
    for i in range(0, len(text)/n):
        tests.append(text[n * (i): n * (i + 1)])
    return tests

for language in language_list:
        file_path = "%s%s.txt" % (TEST_PATH, language)
        test_suite = test_split(codecs.open(file_path, "r", "utf-8").read(), TEST_LEN)
        tests[language] = test_suite

for language in language_list:
    lang_idx = language_list[language]
    for test in tests[language]:
        col = lang_idx
        row = language_list[TF_IDF.most_likely_language(test)]
        #row = language_list['Italian']
        confusion_matrix[row][col] += 1
    print "done with %s" % language

precision = {}
recall = {}
print confusion_matrix
for language in language_list:
    lang_idx = language_list[language]

    true_postive = confusion_matrix[lang_idx][lang_idx]

    negatives = sum([confusion_matrix[i][lang_idx] for i in range(len(language_list))])
    positives = sum([confusion_matrix[lang_idx][j] for j in range(len(language_list))])

    fals_pos = positives - true_postive
    fals_neg = negatives - true_postive

    if positives == 0 and true_postive == 0:
        precision[language] = 0
    else:
        precision[language] = float(true_postive) / float(positives)

    if (true_postive + fals_neg) == 0 and true_postive == 0:
        recall[language] = 0
    else:
        recall[language] = float(true_postive) / float(true_postive + fals_neg)

for l in language_list:
    print l
    print "\tPrecision: %f" % precision[l]
    print "\tRecall: %f" % recall[l]

avg_precision = float(sum([x[1] for x in precision.items()]))/float(len(precision))
avg_recall = float(sum([x[1] for x in recall.items()]))/float(len(precision))
print "\tPrecision: ", avg_precision
print "\tRecall: ", avg_recall
print "\tAccuracy: ", 2 * avg_precision * avg_recall / (avg_recall + avg_precision)
