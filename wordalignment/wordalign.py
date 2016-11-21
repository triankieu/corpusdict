def is_begin_match(token):
    return '({' == token

def is_end_match(token):
    return '})' == token


with open('../data/en_vn.align.A3.final', 'r') as corpus:
    count = 0
    corpusdic = {}
    source_token_list = []
    target_token_list = []
    for line in corpus:
        if (line[0] == '#'):
            count = 2
            continue
        elif count == 2:
            target_token_list = line.split()
            count -= 1
            continue
        elif count == 1:
            source_token_list = line.split()
            count -= 1

        if (count == 0):
            flag = True
            matched_token_list = []

            previous_token = ''
            for token in source_token_list:
                if True == flag:
                    if is_begin_match(token):
                        flag = False
                        if corpusdic.get(previous_token) is None:
                            matched_token_list = []
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
                        if (target_item not in matched_token_list):
                            matched_token_list.append(target_item)


    print(corpusdic)