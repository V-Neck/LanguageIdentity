import pickle, numpy
from collections import Counter
import matplotlib.pyplot as plt

model = pickle.load(open("model.txt", "rb"))

languages = model.keys()

for language in languages:
    scores = model[language]
    percent = numpy.percentile(scores.values(), 50)
    model[language] = dict([s for s in scores.items() if s[1] > percent])

pickle.dump(model, open("model.txt", "wb"))
