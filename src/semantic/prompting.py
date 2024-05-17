import os


def prompt(args) -> str:
    nl1 = args.nl1
    nl2 = args.nl2
    en1 = args.entity1
    en2 = args.entity2
    prompt_dir = os.path.join("prompts", "semantic")
    if args.prompt == "normal":
        fixed_prompt_file = open(os.path.join(prompt_dir, "normal.txt"))
        fixed_prompt = fixed_prompt_file.read()
    else:
        fixed_prompt = args.prompt
    final_prompt = (
            fixed_prompt
            + "\nYour answers need to follow the following <output> format."
            + "\n<input>"
            + "\nSentence 1: "
            + nl1
            + "\nSentence 2: "
            + nl2
            + f"\nRequest: Give the relationship between `{en1}` and `{en2}`"
            + "\n<output>"
            + "\nHidden Relationship: "
            + "\nExplanation: "
    )
    # print(f"[semantic] FINAL PROMPT:\n{final_prompt}")
    return final_prompt


def extract_subinfo(output: str) -> str:
    hidden_relations = parse_semantic_relation(output)
    return hidden_relations


def parse_semantic_relation(output: str) -> str:
    try:
        semantic_relations = output.split("Explanation:")[0].split("Hidden Relationship: ")[1].strip()
    except:
        print("[semantic] Parse error!")
        semantic_relations = ""
    return semantic_relations
