import os
from statistics import mode
from typing import Tuple, Any, Hashable

from ltlf2dfa.parser.ltlf import LTLfParser


def prompt(args, ltl_list: list) -> str:
    en1 = args.entity1
    en2 = args.entity2
    prompt_dir = os.path.join("prompts", "formula")
    if args.prompt == "normal":
        fixed_prompt_file = open(os.path.join(prompt_dir, "normal.txt"))
        fixed_prompt = fixed_prompt_file.read()
    else:
        fixed_prompt = args.prompt
    final_prompt = (
            fixed_prompt
            + "\nYour answers need to follow the following <output> format."
            + "\n<input>"
            + "\nLTL formula 1: "
            + str(ltl_list[0])
            + "\nLTL formula 2: "
            + str(ltl_list[1])
            + f"\nRequest: Give the LTL relationship between `{en1}`and `{en2}`"
            + "\n<output>"
            + "\nThe relationship expressed by the LTL formula: "
            + "\nExplanation: "
    )
    # print(f"[formula] FINAL PROMPT:{final_prompt}")
    return final_prompt


def extract_subinfo(outputs, args, n):
    hidden_relations = parse_ltl_relation(outputs)
    final_relation = process_final_relation(hidden_relations, n)
    return final_relation


def parse_ltl_relation(outputs: str) -> list:
    parser = LTLfParser()
    ltl_relations = []
    for o in outputs:
        try:
            ltl_formula = o.split("Explanation:")[0].split("The relationship expressed by the LTL formula: ")[1].strip()
        except:
            print("[formula] Parse error!")
            ltl_formula = ""
            continue
        try:
            parsed_formula = parser(ltl_formula)
            ltl_relations.append(parsed_formula)
        except:
            ltl_relations.append(ltl_formula)
    return ltl_relations


def process_final_relation(relation_list: list, n: int) -> tuple:
    mf_relation = find_most_freq(relation_list)
    frequency = cal_freq(mf_relation, relation_list, n)
    return mf_relation, frequency


def find_most_freq(ls: list):
    if len(ls) == 0:
        return "No output"
    try:
        res = mode(ls)
    except:
        res = ls[0]
    return res


def cal_freq(elem, ls, n) -> float:
    occ = count_occurrences(elem, ls)
    return occ / n


def count_occurrences(elem, ls) -> int:
    count = 0
    for e in ls:
        if e == elem:
            count += 1
    return count
