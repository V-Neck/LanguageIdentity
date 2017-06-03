from tf_idf import TF_IDF
from collections import Counter
tf_idf = TF_IDF("../data/dev/", retrain=True)

print "type q to quit. Otherwise, just type some text!"

test_string = raw_input("> ")

while test_string != "q":
    print tf_idf.most_likely_language(test_string, True)
    test_string = raw_input("> ")
