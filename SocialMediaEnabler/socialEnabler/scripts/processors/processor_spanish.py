# This is a set of ***language dependent*** methods for ***spanish*** text processing. It includes functions for the following:
# - find swear words

swear_words = ["puta"]


def is_swearing_es(text):
    swear = False
    for w in swear_words:
        if w in text:
            swear = True
            break
    return swear

def process_sp(text):
    return text
