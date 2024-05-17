import json
import os

import openai
import requests
import vertexai
from vertexai.preview.language_models import TextGenerationModel

import src.semantic.prompting as s_prompt
import src.formula.prompting as f_prompt


def gpt_4(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    # request LLM
    if args.method == 1:
        n = 1
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": s_prompt.prompt(args)}],
            n=n,
            temperature=args.temperature,
            stop="FINISH",
        )
        output = response['choices'][0]['message']['content']
        # print(f"[semantic] OUTPUT:\n{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        if args.num_tries == "":
            n = 3
        else:
            n = int(args.num_tries)
            if n > 5:
                n = 5
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": f_prompt.prompt(args, ltl_list)}],
            n=n,
            temperature=args.temperature,
            stop="FINISH",
        )
        outputs = []
        for i in range(0, n):
            output = response["choices"][i]["message"]["content"]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def gpt_35_turbo(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    # request LLM
    if args.method == 1:
        n = 1
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": s_prompt.prompt(args)}],
            n=n,
            temperature=args.temperature,
            stop="FINISH",
        )
        output = response['choices'][0]['message']['content']
        print(f"[semantic] OUTPUT:\n{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        if args.num_tries == "":
            n = 3
        else:
            n = int(args.num_tries)
            if n > 5:
                n = 5
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f_prompt.prompt(args, ltl_list)}],
            n=n,
            temperature=args.temperature,
            stop="FINISH",
        )
        outputs = []
        for i in range(0, n):
            output = response["choices"][i]["message"]["content"]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def code_davinci_002(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    # request LLM
    if args.method == 1:
        n = 1
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=s_prompt.prompt(args),
            temperature=args.temperature,
            n=n,
            max_tokens=300,
            stop=["FINISH"],
            logprobs=5,
        )
        output = response["choice"][0]["message"]["content"]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        if args.num_tries == "":
            n = 3
        else:
            n = int(args.num_tries)
            if n > 5:
                n = 5
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=f_prompt.prompt(args, ltl_list),
            temperature=args.temperature,
            n=n,
            max_tokens=300,
            stop=["FINISH"],
            logprobs=5,
        )
        outputs = []
        for i in range(0, n):
            output = response["choices"][i]["text"]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def text_davinci_003(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    # request LLM
    if args.method == 1:
        n = 1
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=s_prompt.prompt(args),
            temperature=args.temperature,
            n=n,
            max_tokens=300,
            stop=["FINISH"],
            logprobs=5,
        )
        output = response["choice"][0]["message"]["content"]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        if args.num_tries == "":
            n = 3
        else:
            n = int(args.num_tries)
            if n > 5:
                n = 5
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f_prompt.prompt(args, ltl_list),
            temperature=args.temperature,
            n=n,
            max_tokens=300,
            stop=["FINISH"],
            logprobs=5,
        )
        outputs = []
        for i in range(0, n):
            output = response["choices"][i]["text"]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def code_davinci_edit_001(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    # request LLM
    if args.method == 1:
        n = 1
        prompt = s_prompt.prompt(args) + " REPLACE"
        response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=prompt,
            instruction="replace REPLACE with the explanation, an explanation of extracting hidden relation",
            temperature=args.temperature,
            top_p=1,
            n=n,
        )
        output = response["choice"][0]["text"][len(prompt) - 8:].split("FINISH")[0]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        if args.num_tries == "":
            n = 3
        else:
            n = int(args.num_tries)
            if n > 5:
                n = 5
        prompt = f_prompt.prompt(args, ltl_list) + " REPLACE"
        response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=prompt,
            instruction="replace REPLACE with the explanation, an explanation of reasoning formula",
            temperature=args.temperature,
            top_p=1,
            n=n,
        )
        outputs = []
        for i in range(0, n):
            output = response["choices"][i]["text"][len(prompt) - 8:].split("FINISH")[0]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def text_bison_001(args, ltl_list):
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

    def query(prompt):
        return model.predict(
            prompt,
            temperature=args.temperature,
            max_output_tokens=300
        )

    # request LLM
    if args.method == 1:
        input_prompt = s_prompt.prompt(args)
        response = query(input_prompt)
        output = response.text.split("FINISH")[0]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        input_prompt = f_prompt.prompt(args, ltl_list)
        outputs = []
        for i in range(0, n):
            response = query(input_prompt)
            output = response.text.split("FINISH")[0]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def bloom(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "hf_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
    headers = {"Authorization": "Bearer " + key}
    n = args.num_tries

    def query(payload):
        answer = requests.post(API_URL, headers=headers, json=payload)
        return answer.json()

    # request LLM
    if args.method == 1:
        input_prompt = s_prompt.prompt(args)
        response = query(
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
        # print(f"[semantic] RAW OUTPUT:{response}")
        output = response[0]["generated_text"].split("FINISH")[0]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        input_prompt = f_prompt.prompt(args, ltl_list)
        outputs = []
        for i in range(0, n):
            response = query(
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
            # print(f"[formula] RAW OUTPUT:{response}")
            # shots_count = input_prompt.count("FINISH")
            output = response[0]["generated_text"].split("FINISH")[0]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def bloomz(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "hf_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"
    headers = {"Authorization": "Bearer " + key}
    n = args.num_tries

    def query(payload):
        answer = requests.post(API_URL, headers=headers, json=payload)
        return answer.json()

    # request LLM
    if args.method == 1:
        input_prompt = s_prompt.prompt(args)
        response = query(
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
        # print(f"[semantic] RAW OUTPUT:{response}")
        output = response[0]["generated_text"].split("FINISH")[0]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        input_prompt = f_prompt.prompt(args, ltl_list)
        outputs = []
        for i in range(0, n):
            response = query(
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
            # print(f"[formula] RAW OUTPUT:{response}")
            # shots_count = input_prompt.count("FINISH")
            output = response[0]["generated_text"].split("FINISH")[0]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def ernie_bot(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "wenxin_key.txt")
    with open(keyfile, "r") as file:
        API_KEY = file.readline().rstrip("\n")
        SECRET_KEY = file.readline().rstrip("\n")
    n = args.num_tries

    def get_access_token():
        """使用 AK，SK 生成鉴权签名（Access Token）

        :return: access_token，或是None(如果错误)

        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    headers = {
        'Content-Type': 'application/json'
    }

    def query(payload):
        answer = requests.request("POST", API_URL, headers=headers, data=payload)
        answer_content = answer.text
        return json.loads(answer_content)

    # request LLM
    if args.method == 1:
        input_prompt = s_prompt.prompt(args)
        response = query(
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
        # print(f"[semantic] RAW OUTPUT:{response}")
        output = response["result"].split("FINISH")[0]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        input_prompt = f_prompt.prompt(args, ltl_list)
        outputs = []
        for i in range(0, n):
            response = query(
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
            # print(f"[formula] RAW OUTPUT:{response}")
            output = response["result"].split("FINISH")[0]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)


def ernie_bot_turbo(args, ltl_list):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir, "wenxin_key.txt")
    with open(keyfile, "r") as file:
        API_KEY = file.readline().rstrip("\n")
        SECRET_KEY = file.readline().rstrip("\n")
    n = args.num_tries

    def get_access_token():
        """使用 AK，SK 生成鉴权签名（Access Token）

        :return: access_token，或是None(如果错误)

        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    headers = {
        'Content-Type': 'application/json'
    }

    def query(payload):
        answer = requests.request("POST", API_URL, headers=headers, data=payload)
        answer_content = answer.text
        return json.loads(answer_content)

    # request LLM
    if args.method == 1:
        input_prompt = s_prompt.prompt(args)
        response = query(
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
        # print(f"[semantic] RAW OUTPUT:{response}")
        output = response["result"].split("FINISH")[0]
        # print(f"[semantic] OUTPUT:{output}")
        return s_prompt.extract_subinfo(output)
    elif args.method == 2:
        input_prompt = f_prompt.prompt(args, ltl_list)
        outputs = []
        for i in range(0, n):
            response = query(
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
            # print(f"[formula] RAW OUTPUT:{response}")
            output = response["result"].split("FINISH")[0]
            # print(f"[formula] OUTPUT:{output}")
            outputs.append(output)
        return f_prompt.extract_subinfo(outputs, args, n)
