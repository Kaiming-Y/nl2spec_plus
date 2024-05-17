import src.models as models
import src.translation.nl2ltl as nl2ltl


def call(args):
    if args.method == 1:
        '''
            method 1:
            1. reasoning semantic relation
            2. translate semantic relation to LTL formula 
        '''
        hidden_relation = call_model(args)
        print(f"[semantic] The hidden relation is: {hidden_relation}")
        if hidden_relation != "":
            relation_ltl = nl2ltl.translate(nl=hidden_relation, model=args.model, keyfile=args.keyfile, keydir=args.keydir,
                                            prompt=args.prompt4translation, maxtokens=args.maxtokens,
                                            num_tries=args.num_tries, temperature=args.temperature)
        else:
            relation_ltl = "unknown"
            print("[translation] The relation is unknown. We can't translate it to LTL formula!")
        return relation_ltl
    elif args.method == 2:
        '''
            method 2:
            1. translate both of nl1 and nl2 to LTL formulas
            2. reasoning LTL formula 
        '''
        ltl1 = nl2ltl.translate(nl=args.nl1, model=args.model, keyfile=args.keyfile, keydir=args.keydir,
                                prompt=args.prompt4translation, maxtokens=args.maxtokens, num_tries=args.num_tries,
                                temperature=args.temperature)[0]
        ltl2 = nl2ltl.translate(nl=args.nl2, model=args.model, keyfile=args.keyfile, keydir=args.keydir,
                                prompt=args.prompt4translation, maxtokens=args.maxtokens, num_tries=args.num_tries,
                                temperature=args.temperature)[0]
        print(f"[translation]ltl 1: {ltl1}")
        print(f"[translation]ltl 2: {ltl2}")
        ltl_list = [ltl1, ltl2]
        relation_ltl = call_model(args, ltl_list=ltl_list)
        return relation_ltl


def call_model(args, ltl_list=None):
    if ltl_list is None:
        ltl_list = []
    model = args.model
    if model == "code-davinci-002":
        res = models.code_davinci_002(args, ltl_list)
        return res
    if model == "text-bison@001":
        res = models.text_bison_001(args, ltl_list)
        return res
    if model == "text-davinci-003":
        res = models.text_davinci_003(args, ltl_list)
        return res
    if model == "code-davinci-edit-001":
        res = models.code_davinci_edit_001(args, ltl_list)
        return res
    if model == "bloom":
        res = models.bloom(args, ltl_list)
        return res
    if model == "gpt-3.5-turbo":
        res = models.gpt_35_turbo(args, ltl_list)
        return res
    if model == "gpt-4":
        res = models.gpt_4(args, ltl_list)
        return res
    if model == "bloomz":
        res = models.bloomz(args, ltl_list)
        return res
    if model == "ernie-bot":
        res = models.ernie_bot(args, ltl_list)
        return res
    if model == "ernie-bot-turbo":
        res = models.ernie_bot_turbo(args, ltl_list)
        return res
    raise Exception("Not a valid model.")
