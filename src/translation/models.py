import json
import os
from statistics import mode

import openai
import requests
# import transformers
import vertexai
# from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, pipeline
from vertexai.preview.language_models import TextGenerationModel

import src.translation.prompting as prompting


def gpt_4(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompting.prompt(args)}],
        n=n,
        temperature=args.temperature,
        stop="FINISH",
    )
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["message"]["content"]
        # print(f"[translation] OUTPUT:{output}")
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def gpt_35_turbo(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompting.prompt(args)}],
        n=n,
        temperature=args.temperature,
        stop="FINISH",
    )
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["message"]["content"]
        print(f"[translation] OUTPUT:{output}")
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def code_davinci_002(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    temperature = args.temperature
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompting.prompt(args),
        temperature=temperature,
        n=n,
        max_tokens=300,
        stop=["FINISH"],
        logprobs=5,
    )
    # print(response["choices"][0]["text"])
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["text"]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def text_davinci_003(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    temperature = args.temperature
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompting.prompt(args),
        temperature=temperature,
        n=n,
        max_tokens=300,
        stop=["FINISH"],
        logprobs=5,
    )
    # print(response["choices"][0]["text"])
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["text"]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def code_davinci_edit_001(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5

    temperature = args.temperature
    prompt = prompting.prompt(args) + " REPLACE"

    response = openai.Edit.create(
        model="code-davinci-edit-001",
        input=prompt,
        instruction="replace REPLACE with the explanation, an explanation dictionary and the final translation",
        temperature=temperature,
        top_p=1,
        n=n,
    )
    # print(response["choices"][0]["text"])
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["text"][len(prompt) - 8:].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def text_bison_001(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "google_project_id.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    vertexai.init(project=key)
    model = TextGenerationModel.from_pretrained("text-bison@001")
    n = args.num_tries

    def query():
        return model.predict(
            prompting.prompt(args), temperature=args.temperature, max_output_tokens=300
        )

    choices = []
    for i in range(0, n):
        repsonse = query()
        output = repsonse.text.split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def bloom(args):
    n = args.num_tries
    input_prompt = prompting.prompt(args)
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "hf_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    headers = {"Authorization": "Bearer " + key}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    choices = []
    for i in range(0, n):
        raw_output = query(
            {
                "inputs": input_prompt,
                "options": {"use_cache": False, "wait_for_model": True},
                "parameters": {
                    "return_full_text": False,
                    "do_sample": False,
                    "max_new_tokens": 300,
                    "temperature": args.temperature,
                },
            }
        )
        # print(f"RAW OUTPUT:{raw_output}")
        # shots_count = input_prompt.count("FINISH")
        output = raw_output[0]["generated_text"].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def bloomz(args):
    n = args.num_tries
    input_prompt = prompting.prompt(args)
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "hf_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    headers = {"Authorization": "Bearer " + key}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    choices = []
    for i in range(0, n):
        raw_output = query(
            {
                "inputs": input_prompt,
                "options": {"use_cache": False, "wait_for_model": True},
                "parameters": {
                    "return_full_text": False,
                    "do_sample": False,
                    "max_new_tokens": 300,
                    "temperature": args.temperature,
                },
            }
        )
        # print(f"RAW OUTPUT:{raw_output}")
        # shots_count = input_prompt.count("FINISH")
        output = raw_output[0]["generated_text"].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def ernie_bot(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "wenxin_key.txt")
    with open(keyfile, "r") as file:
        API_KEY = file.readline().rstrip("\n")
        SECRET_KEY = file.readline().rstrip("\n")

    def get_access_token():
        """使用 AK，SK 生成鉴权签名（Access Token）

        :return: access_token，或是None(如果错误)

        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    n = args.num_tries
    input_prompt = prompting.prompt(args)
    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    headers = {
        'Content-Type': 'application/json'
    }

    def query(payload):
        response = requests.request("POST", API_URL, headers=headers, data=payload)
        response_content = response.text
        return json.loads(response_content)

    choices = []

    for i in range(0, n):
        raw_output = query(
            json.dumps(
                {
                    "messages": [
                        {"role": "user", "content": input_prompt}
                    ],
                    "temperature": args.temperature,
                    "stream": False
                }
            )
        )
        # print(f"RAW OUTPUT:{raw_output}")
        output = raw_output["result"].split("FINISH")[0]
        choices.append(output)

    return prompting.extract_subinfo(choices, args, n)


def ernie_bot_turbo(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "wenxin_key.txt")
    with open(keyfile, "r") as file:
        API_KEY = file.readline().rstrip("\n")
        SECRET_KEY = file.readline().rstrip("\n")

    def get_access_token():
        """使用 AK，SK 生成鉴权签名（Access Token）

        :return: access_token，或是None(如果错误)

        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    n = args.num_tries
    input_prompt = prompting.prompt(args)
    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()

    headers = {
        'Content-Type': 'application/json'
    }

    def query(payload):
        response = requests.request("POST", API_URL, headers=headers, data=payload)
        response_content = response.text
        return json.loads(response_content)

    choices = []

    for i in range(0, n):
        raw_output = query(
            json.dumps(
                {
                    "messages": [
                        {"role": "user", "content": input_prompt}
                    ],
                    "temperature": args.temperature,
                    "stream": False
                }
            )
        )
        # print(f"RAW OUTPUT:{raw_output}")
        output = raw_output["result"].split("FINISH")[0]
        choices.append(output)

    return prompting.extract_subinfo(choices, args, n)
