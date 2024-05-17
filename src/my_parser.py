import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog='translation++',
        description='Extracting Hidden LTL Relationships from a Set of Natural Languages',
        epilog='')

    parser.add_argument('--method', type=int, required=True, default=1,
                        help="the method to get hidden relation: 1.semantic reasoning, 2.LTL reasoning")
    parser.add_argument('--nl1', required=True, default="", help='input sentence 1')
    parser.add_argument('--nl2', required=True, default="", help='input sentence 2')
    parser.add_argument('--entity1', required=True, default="", help="the 1st entity to get hidden relation")
    parser.add_argument('--entity2', required=True, default="", help="the 2nd entity to get hidden relation")

    # LLM related arguments
    parser.add_argument('--model', required=False, default="gpt-3.5-turbo", help='chose the Large Language Model')
    parser.add_argument('--fewshots', required=False, default="", help='provide few shot examples')
    parser.add_argument('--keyfile', required=False, default="",
                        help='provide open ai key (for codex usage), or a huggingface api key (for bloom usage)')
    parser.add_argument('--keydir', required=False, default="", help='if not specify keyfile, specify directory')
    parser.add_argument('--prompt', required=False, default="normal", help='specifies the name of the prompt file')
    parser.add_argument('--prompt4translation', required=False, default="minimal",
                        help='specifies the name of the prompt file for translation')
    parser.add_argument('--maxtokens', required=False, default=64, help='Maximum number of tokens to compute')
    parser.add_argument('--num_tries', type=int, required=False, default=3,
                        help="Number of runs the underlying language model attempts a translation.")
    parser.add_argument('--temperature', type=float, required=False, default=0.2, help="Model temperature.")

    args = parser.parse_args()

    return args
