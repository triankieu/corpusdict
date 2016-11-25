import collections


def is_begin_match(token):
    return '({' == token


def is_end_match(token):
    return '})' == token


corpusdic = {}

with open('../data/vn_en.align.A3.final', 'r') as corpus:
    count = 0
    source_token_list = []
    target_token_list = []
    for line in corpus:
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

        if count == 0:
            flag = True
            matched_token_list = {}

            previous_token = ''
            for token in source_token_list:
                if flag:
                    if is_begin_match(token):
                        flag = False
                        if corpusdic.get(previous_token) is None:
                            matched_token_list = {}
                        else:
                            matched_token_list = corpusdic[previous_token]
                    else:
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

for key, value in odcorpus.items():
    if has_item(value.items()):
        print(key + ' : ')
        for ik, iv in value.items():
            if iv > 1:
                print(ik + '(' + str(iv) + ')', end=',')
        print('\r\n')
