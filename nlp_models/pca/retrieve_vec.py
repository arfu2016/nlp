"""
@Project   : CubeGirl
@Module    : retrieve_vec.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/23/17 9:02 PM
@Desc      : save word vectors as json file
"""

from Daka.chatbot.logic.text_table.retrieve_template import \
    retrieve_tpl_from_file
import string
import jieba.analyse
from collections import Counter
import json


def clean_sentence(st):
    intab = string.punctuation + '。，“”‘’（）：；？·—《》、'
    outtab = ' '
    table = str.maketrans(dict.fromkeys(intab, outtab))
    st1 = st.translate(table)
    tags = jieba.analyse.extract_tags(st1, topK=100,
                                      allowPOS=(
                                          'eng', 'n', 'ns', 'nr', 'nt', 'nz',
                                          'vn'))
    # allowPOS=('eng', 'n', 'v', 'ns', 'nr', 'nt', 'nz', 'vd', 'vn'))
    clean = ' '.join(tags)
    return clean


def sentence_tokenization(tpl_list):
    data_tokenized = [(clean_sentence(tpl), intent)
                      for tpl, intent in tpl_list]
    return data_tokenized


def word_exist(counts):
    vecfile = open('data/wiki.zh.vec', 'r')
    words = (line.split(' ')[0] for line in vecfile)
    fast_words = [word for word in words if word in counts]
    vecfile.close()
    print(len(fast_words), ':', fast_words)
    return fast_words


tpl_intent = retrieve_tpl_from_file('data/tpls.csv')
tpl_intent = [(tpl, intent) for tpl, intent in tpl_intent
              if intent != 1 and intent != 2]
data = sentence_tokenization(tpl_intent)

templates = [tpl.lower() for tpl, intent in data]
intentions = [intent for tpl, intent in data]

person_counts = Counter()
team_counts = Counter()
citiao_counts = Counter()
for i in range(len(templates)):
    if intentions[i] == 3:
        for word in templates[i].split(" "):
            person_counts[word] += 1
    elif intentions[i] == 4:
        for word in templates[i].split(" "):
            team_counts[word] += 1
    else:
        for word in templates[i].split(" "):
            citiao_counts[word] += 1

word_need = list(set(word_exist(person_counts) + word_exist(team_counts)
                     + word_exist(citiao_counts)))
print(len(word_need), ':', word_need)

vecfile = open('data/wiki.zh.vec', 'r')
word_vectors = (line.strip() for line in vecfile)
word_vec = [word for word in word_vectors if word.split(' ')[0] in word_need]
vecfile.close()
print(len(word_vec), ':')
# for word in word_vec:
#     print(word)

word_dict = {word_str.split(' ')[0]: word_str.split(' ')[1:] for word_str
             in word_vec}

# for word, vector in word_dict.items():
word2vec = {word: [float(f_string) for f_string in vector] for word, vector
            in word_dict.items()}
for word, vector in word2vec.items():
    print(word, vector)

with open('data/cube_vec.json', 'w') as vecFile:
    json.dump(word2vec, vecFile)
