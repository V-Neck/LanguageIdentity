# encoding=utf8
# /Users/vneck/Drive/Spring 2017/Ling 472/Final Project
import os, re, codecs
from sys import argv
from bs4 import UnicodeDammit

ORIG_CORP_PATH = os.path.abspath(argv[-1])
SECTIONS = ["clean", "train", "test", "dev"]
DIRS = ["%s/../%s" % (ORIG_CORP_PATH, section) for section in SECTIONS]
DIRS = dict(zip(SECTIONS, DIRS))
PERCENTS = [.8, .11, .09]

assert sum(PERCENTS) == 1.0 and len(PERCENTS) == (len(SECTIONS) - 1)

SECTION_PERCENTS = dict(zip(SECTIONS[1:], PERCENTS))

for d in DIRS:
    if not os.path.exists(DIRS[d]):
        os.mkdir(DIRS[d])

# lines to lop-off ends
MARGIN = 20
# By products of Google Drive and OSX
IRRELEVANT = [".DS_Store", 'Icon\r', '', None]

language_list = [x for x in os.listdir(ORIG_CORP_PATH) if x not in IRRELEVANT]

# TRIM
for directory in language_list:
    print "cleaning %s..." % directory
    # clean file
    clean_file = codecs.open("%s/%s.txt" % (DIRS['clean'], directory), "w", "utf-8")
    for filename in os.listdir("%s/%s" % (ORIG_CORP_PATH, directory)):
        if re.match(r'.*\.txt', filename):
            dirty_file = open("%s/%s/%s" % (ORIG_CORP_PATH, directory, filename), "r").readlines()
            flag = False
            for i in range(MARGIN, len(dirty_file)-MARGIN ):
                if (re.match(r'\*\*\* END *.', dirty_file[i + MARGIN])):
                    break
                if flag:
                    # CLEAN
                    clean_text = UnicodeDammit(dirty_file[i]).unicode_markup
                    clean_text = re.sub(r'(\s+|\.\.\.|…)', " ", clean_text)
                    clean_text = re.sub(r' [.0-9 -*_\(\)]+[ .,]', "", clean_text)
                    clean_text = re.sub(r'[-=+ ]{2}', "", clean_text)
                    clean_text = re.sub(r'-*([A-Za-z]+)-*', r'\g<1>', clean_text)
                    clean_file.write(clean_text)
                if not flag and (re.match(r'\*\*\*[ ]*START *.', dirty_file[i - MARGIN])):
                    flag = True
    clean_file.close()

# Divide into tests
for language in language_list:
    language_text = codecs.open("%s/%s.txt" % (DIRS['clean'], language), "r", "utf-8").read()
    language_file_length = len(language_text)
    cur = 0
    for section in SECTIONS[1:]:
        section_len = int(SECTION_PERCENTS[section] * language_file_length)
        section_text = codecs.open("%s/%s.txt" % (DIRS[section], language), "w", "utf-8")
        section_text.write(language_text[cur : cur + section_len])
        cur += (1 + section_len)
