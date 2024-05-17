from statistics import mode


def get_overlaps(explain_dict_list, k):
    overlaps = []
    for dict in explain_dict_list:
        if k in dict:
            overlaps.append(dict[k])
    return overlaps


def merge_dicts(explain_dict_list):
    merge_dict = {}
    for dict in explain_dict_list:
        for k in dict:
            if k.lower() not in merge_dict:
                merge_dict[k.lower()] = [dict[k]]
            else:
                merge_dict[k.lower()].append(dict[k])
    return merge_dict


def all_equal(l):
    return all(x == l[0] for x in l)


def fill_with_none(dict, n):
    for k in dict:
        i = 0
        while len(dict[k]) < n:
            dict[k].append("None" + str(i))
            i += 1
    return dict


def most_freq(l):
    if len(l) == 0:
        return "No output"
    try:
        res = mode(l)
    except:
        res = l[0]
    return res


def count_occurences(l, el):
    count = 0
    for e in l:
        if e == el:
            count += 1
    return count


def calc_certainty_score(l, el, n):
    occ = count_occurences(l, el)
    return occ / n


def ambiguity_detection_ast():
    return


def add_certainty_and_reduce(merge_d, n):
    reduced = {}
    for k, v in merge_d.items():
        certainty_list = []
        for e in v:
            score = calc_certainty_score(v, e, n)
            if not e.startswith("None"):
                certainty_list.append((e, round(score * 100, 2)))
        certainty_list = list(set(certainty_list))  # remove duplicates
        certainty_list = sorted(certainty_list, key=lambda x: x[1], reverse=True)  # sort from largest to smallest according to freq.
        reduced[k] = certainty_list
    return reduced


def ambiguity_detection_translations(explain_dict_list, n, locked_translations):
    merge_d = merge_dicts(explain_dict_list)  # 统计所有组（即LLM每次的回答结果）的解释中所有翻译键值对（键：nl经解析后的各个成分, 值：各成分对应的子翻译）, 一个键可能存在几个值, 即一个nl成分可能有几种子翻译
    merge_d = fill_with_none(merge_d, n)  # 由于上一步每个nl成分对应的子翻译可能不足n个, 故补none, 保证一个nl成分对应的子翻译有n个
    reduced_d = add_certainty_and_reduce(merge_d, n)  # 通过计算每个nl成分的子翻译的频率打分, 对每个成分对应的子翻译按得分从高到低排序, 排序结果以’子翻译-得分’形式的dict作为每个成分的子翻译dict
    reduced_d = add_locked_subtranslation(reduced_d, locked_translations)  # 将用户给出的子翻译放入翻译结果中，并且此时翻译结果为——nl子成分：三元组(子翻译,得分,true/false), true表示来自用户, false表示来自LLM
    certainty_triple_list = [
        (
            k,
            [e[0] for e in reduced_d[k]],
            [e[1] for e in reduced_d[k]],
            [e[2] for e in reduced_d[k]],
        )
        for k in reduced_d.keys()
    ]
    return sorted(certainty_triple_list, key=lambda x: max(x[2]))


def add_locked_subtranslation(model_subt, locked_subt):
    model_subt = {k: [(e[0], e[1], False) for e in model_subt[k]] for k in model_subt}  # 取每个nl成分的子翻译结果的频率最高的结果的子翻译（ltl公式）、对应的得分和false组成三元组
    for k in locked_subt:
        if k in model_subt:
            elem = None
            for e in model_subt[k]:
                if e[0] == locked_subt[k]:
                    elem = e
            if elem is None:
                model_subt[k] = [(locked_subt[k], 0.0, True)] + model_subt[k]  # 将用户输入的子翻译放入结果开头, 此时是用户对于nl成分的提取与LLM一样, 但子翻译结果不一, 此时子翻译结果都会保留
            else:
                model_subt[k].remove(elem)  # 将用户输入的子翻译替换LLM给出的子翻译
                model_subt[k] = [(locked_subt[k], elem[1], True)] + model_subt[k]  # 将用户输入的子翻译放入结果开头
        else:
            model_subt[k] = [(locked_subt[k], 0.0, True)]  # 用户给出的对于nl成分的提取结果与LLM给出的提取结果不同, 直接加入用户给出的nl成分的子翻译结果
    return model_subt


def ambiguity_final_translation(parsed_result_formulas, n):
    mf = most_freq(parsed_result_formulas)
    cert = calc_certainty_score(parsed_result_formulas, mf, n)
    return (mf, cert)
