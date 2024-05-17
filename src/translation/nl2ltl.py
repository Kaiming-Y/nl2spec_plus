import src.translation.models as models


class arg:
    def __init__(self, nl, model, keyfile, keydir, prompt, maxtokens, num_tries, temperature, given_translations):
        self.nl = nl
        self.model = model
        self.keyfile = keyfile
        self.keydir = keydir
        self.prompt = prompt
        self.maxtokens = maxtokens
        self.num_tries = num_tries
        self.temperature = temperature
        self.given_translations = given_translations


def translate(nl, model, keyfile, keydir, prompt="minimal", maxtokens=64, num_tries=3, temperature=0.2, given_translations=""):
    args = arg(nl, model, keyfile, keydir, prompt, maxtokens, num_tries, temperature, given_translations)
    res = call(args)
    return res


def call(args):
    model = args.model
    if model == "code-davinci-002":
        res = models.code_davinci_002(args)
        return res
    if model == "text-bison@001":
        res = models.text_bison_001(args)
        return res
    if model == "text-davinci-003":
        res = models.text_davinci_003(args)
        return res
    if model == "code-davinci-edit-001":
        res = models.code_davinci_edit_001(args)
        return res
    if model == "bloom":
        res = models.bloom(args)
        return res
    if model == "gpt-3.5-turbo":
        res = models.gpt_35_turbo(args)
        return res
    if model == "gpt-4":
        res = models.gpt_4(args)
        return res
    if model == "bloomz":
        res = models.bloomz(args)
        return res
    if model == "ernie-bot":
        res = models.ernie_bot(args)
        return res
    if model == "ernie-bot-turbo":
        res = models.ernie_bot_turbo(args)
        return res
    raise Exception("Not a valid model.")
