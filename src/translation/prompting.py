import os
import src.translation.ambiguity as ambiguity
from ltlf2dfa.parser.ltlf import LTLfParser
import ast


def prompt(args):
    inpt = args.nl
    prompt_dir = os.path.join("prompts", "translation")
    if args.prompt == "minimal":
        fixed_prompt_file = open(os.path.join(prompt_dir, "minimal.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "minimal_par":
        fixed_prompt_file = open(os.path.join(prompt_dir, "minimal_par.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "smart":
        fixed_prompt_file = open(os.path.join(prompt_dir, "smart.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "stl":
        fixed_prompt_file = open(os.path.join(prompt_dir, "stl.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "indistribution":
        fixed_prompt_file = open(os.path.join(prompt_dir, "indistribution.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "amba_master":
        fixed_prompt_file = open(
            os.path.join(prompt_dir, "amba_master_assumptions.txt")
        )
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "amba_slave":
        fixed_prompt_file = open(os.path.join(prompt_dir, "amba_slave_guarantees.txt"))
        fixed_prompt = fixed_prompt_file.read()
    else:
        fixed_prompt = args.prompt
    if args.given_translations != "":
        final_prompt = (
            fixed_prompt
            + "\nNatural Language: "
            + inpt
            + "\nGiven translations: "
            + args.given_translations
            + "\nExplanation:"
        )
    else:
        final_prompt = (
            fixed_prompt
            + "\nNatural Language: "
            + inpt
            + "\nGiven translations: {}"
            + "\nExplanation:"
        )
    # print("FINAL PROMPT:")
    # print(final_prompt)
    return final_prompt


def parse_formulas(choices):
    parser = LTLfParser()
    parsed_result_formulas = []
    for c in choices:
        try:
            formula_str = c.split("So the final LTL translation is: ")[1].strip(".")
        except:
            # formula_str = c
            # formula_str = ""
            continue

        try:
            parsed_formula = parser(formula_str)
            parsed_result_formulas.append(parsed_formula)
        except:
            parsed_result_formulas.append(formula_str)
    return parsed_result_formulas


def parse_explanation_dictionary(choices, nl):
    parsed_explanation_results = []
    for c in choices:
        try:
            dict_string = (
                "{" + c.split("dictionary")[1].split("{")[1].split("}")[0] + "}"
            )
            parsed_dict = ast.literal_eval(dict_string)  # ast.literal_eval returns a dictionary , ast 用于处理python抽象语法树, 这里安全评估一个字面量并转化为字典
            parsed_dict = dict(filter(lambda x: x[0] != nl, parsed_dict.items()))
            if parsed_dict:
                parsed_explanation_results.append(parsed_dict)
        except:
            pass
    return parsed_explanation_results


def generate_intermediate_output(intermediate_translation):
    nl = []
    ltl = []
    cert = []
    locked = []
    for t in intermediate_translation:
        nl.append(t[0])
        ltl.append(t[1])
        cert.append(t[2])
        locked.append(t[3])
    return [nl, ltl, cert, locked]


def extract_subinfo(choices, args, n):
    parsed_result_formulas = parse_formulas(choices)  # 提取LLM返回的结果中的LTL公式, 返回值为每一组LTL公式结果的dict
    # print("Results of multiple runs:")
    # print(parsed_result_formulas)
    final_translation = ambiguity.ambiguity_final_translation(parsed_result_formulas, n)  # 通过计算频率找到频率最高的公式作为最终翻译结果
    # parse_explain = parse_explanation_dictionary(choices, args.nl)  # 将LLM返回的dictionary后的解释内容（nl的每个组成部分及其对应的LTL公式）提取出来, 本质是每组子翻译字典的dict
    # intermediate_translation = ambiguity.ambiguity_detection_translations(
    #     parse_explain,
    #     n,
    #     ast.literal_eval(args.locked_translations)
    #     if "locked_translations" in args
    #     else {},
    # )
    # intermediate_output = generate_intermediate_output(intermediate_translation)
    # return final_translation, intermediate_output
    return final_translation
