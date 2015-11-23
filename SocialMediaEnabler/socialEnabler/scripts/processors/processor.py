import json
import re
import time
import datetime
import nltk
import sys
from os import path
nltk.data.path.append(path.dirname( path.dirname( path.abspath(__file__) ) )+"/nltk_dep")
from nltk import wordpunct_tokenize
import string

# This is a set of ***language independent*** methods for text processing. It includes functions for the following:
# - replace emoticons
# - replace urls
# - replace user mentions (Twitter)
# - replace repeated character appearences (>3 same chars)
# - remove line changes
# - remove remove unprintable chars
# - # is also replaced, as part of the main processing method
# - text is converted to lowercase


# needed for url replacement - note:could also use entities from twitter json
urls = '(?: %s)' % '|'.join("""http https telnet gopher file wais
ftp""".split())
ltrs = r'\w'
gunk = r'/#~:.?+=&%@!\-'
punc = r'.:?\-'
any = "%(ltrs)s%(gunk)s%(punc)s" % {'ltrs': ltrs,
                                    'gunk': gunk,
                                    'punc': punc}

url = r"""
\b # start at word boundary
%(urls)s : # need resource and a colon
[%(any)s] +? # followed by one or more
# of any valid character, but
# be conservative and take only
# what you need to....
(?= # look-ahead non-consumptive assertion
[%(punc)s]* # either 0 or more punctuation
(?: [^%(any)s] # followed by a non-url char
| # or end of the string
$
)
)
""" % {'urls': urls,
       'any': any,
       'punc': punc}

url_re = re.compile(url, re.VERBOSE | re.MULTILINE)
username_re = re.compile(r"(?:^|\s)(@\w+)")

happyre = re.compile(u'['
    u'\U0001F601-\U0001F60B]+', 
    re.UNICODE)

sadre = re.compile(u'['
    u'\U0001F61E-\U0001F62D]+', 
    re.UNICODE)

lovere = re.compile(u'['
    u'\U0001F60D'
    u'\U00002764]+', 
    re.UNICODE)


def replace_url(text):
    withoutURL = url_re.sub('_url ', text)
    return withoutURL

#TODO rethink regexp when the previous character is not space
def replace_usermentions(text):
    text = text.replace('@',' @')
    withoutUsername = username_re.sub(' _username ', text)
    return withoutUsername

def replace_multichars(text):
    text_no_multichars = re.sub(r'([a-z])\1{2,}', r'\1'+r'\1', text)
    return text_no_multichars

def remove_line_changes(text):
    text = text.replace('\n', ' ').replace('\r', '')
    return text

def replace_emoticons(text):
    text = happyre.sub('_happy_smiley ', text)
    text = sadre.sub('_sad_smiley ', text)
    text = lovere.sub('_love_smiley ', text)
    return text

def remove_unprintable(text):
    text = filter(lambda x: x in string.printable, text)
    return text


def fix_text_format(text):
    text_no_url = replace_url(text)
    text_no_username = replace_usermentions(text_no_url)
    text_no_pound = text_no_username.replace('#', '_hashtag_')
    text_lowcase = text_no_pound.lower()
    text_no_multichars = replace_multichars(text_lowcase)
    text_one_liner = remove_line_changes(text_no_multichars)
    emo_text = replace_emoticons(text_one_liner)
    printable_text = remove_unprintable(emo_text)
    return printable_text

def writeLog(text,fileName):
    with open(fileName, "a") as myfile:
        #myfile.write("\n------------------------------------------------\n")
        myfile.write(text.encode('utf-8'))
        myfile.write("\n")

def process(text):
    #writeLog(text,"twitterProcessorOutput.txt")
    text = fix_text_format(text)
    writeLog(text,"twitterProcessorOutput.txt")
    return text


