import json
import os
import re
import pickle


def writejsonl(data, datapath):
    with open(datapath, "w", encoding='utf-8') as f:
        for item in data:
            json_item = json.dumps(item, ensure_ascii=False)
            f.write(json_item + "\n")

def writejson(data, json_path):
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    with open(json_path, "w", encoding='utf-8') as json_file:
        json_file.write(json_str)

def readjsonl(datapath):
    res = []
    with open(datapath, "r", encoding='utf-8') as f:
        for line in f.readlines():
            res.append(json.loads(line))
    return res

def readjson(datapath):
    with open(datapath, "r", encoding='utf-8') as f:
        res = json.load(f)
    return res

def writepickle(data, datapath):
    with open(datapath, "wb") as f:
        pickle.dump(data, f)

def readpickle(datapath):
    with open(datapath, "rb") as f:
        res = pickle.load(f)
    return res

def readlargepickle(load_file):
    with open(load_file, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

def check_folder(path):
    if not os.path.exists(path):
        print(f"{path} not exists, create it")
        os.makedirs(path)

def get_name(name, pattern, mode = 0):
    match = re.search(pattern, name)
    # 提取结果
    if match:
        extracted_content = match.group(mode)
        return extracted_content
    else:
        print("Pattern not found")
    x = json.JSONEncode()