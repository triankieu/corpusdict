# word align extract to dictionary
# author: kieutran
import collections
import nltk


def is_begin_match(token):
    return '({' == token


def is_end_match(token):
    return '})' == token


corpusdic = {}

with open('../data/vn_en.align.A3.final', 'r') as align_result:
    count = 0
    source_token_list = []
    target_token_list = []
    en_corpus_lines = open('../data/source.tok', 'r').readlines()
    corpus_line_number = 0
    for line in align_result:
        if line[0] == '#':
            count = 2
            continue
        elif count == 2:
            target_token_list = line.split()
            count -= 1
            continue
        elif count == 1:
            source_token_list = line.split()
            count -= 1
            corpus_line_number += 1

        if count == 0:
            flag = True
            matched_token_list = {}

            previous_token = ''
            en_corpus_line_tokens = en_corpus_lines[corpus_line_number - 1].split()
            pos_tag_source_token_list = nltk.pos_tag(en_corpus_line_tokens)
            word_token_index = 0

            for i in range(len(source_token_list)):
                token = source_token_list[i]

                if flag:
                    if is_begin_match(token):
                        flag = False
                        if corpusdic.get(previous_token) is None:
                            matched_token_list = {}
                        else:
                            matched_token_list = corpusdic[previous_token]
                    else:
                        word_token_index += 1
                        ptag = pos_tag_source_token_list[word_token_index - 1]
                        print(ptag)
                        previous_token = token
                else:
                    if is_end_match(token):
                        flag = True
                        corpusdic[previous_token] = matched_token_list
                    else:
                        target_item = target_token_list[int(token) - 1]
                        if target_item in matched_token_list.keys():
                            matched_token_list[target_item] += 1
                        else:
                            matched_token_list[target_item] = 1


odcorpus = collections.OrderedDict(sorted(corpusdic.items()))


def has_item(items):
    for ik, iv in items:
        if iv > 1:
            return True
    return False

'''
for key, value in odcorpus.items():
    if has_item(value.items()):
        print(key + ' : ')
        for ik, iv in value.items():
            if iv > 1:
                print(ik + '(' + str(iv) + ')', end=',')
        print('\r\n')
'''