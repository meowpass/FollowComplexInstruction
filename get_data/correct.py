import json
import argparse
from tqdm import tqdm
import re

import utils
import GPT_api
from prompts import  corrector_template


def get_corrected(response, constraint, correct_out_path, api_key):
    correct_input = corrector_template.format(response, constraint)
    correct_output = GPT_api.get_res(correct_input, api_key)
    dic = {}
    dic['correct_input'] = correct_input
    dic['correct_output'] = correct_output
    # Save the log files
    with open(correct_out_path,'a',encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False) + '\n')

    correct_pattern = r'-?-?-?r?R?evised r?R?esponse-?-?-?:?\n*([\s\S]*)'
    corrected = re.findall(correct_pattern, correct_output)
    # print(corrected)
    print(correct_output)
    print('-'*50) 
    corrected = corrected[0]
    return corrected


def correct_response(res_path, ift_data_path, dpo_data_path, api_key, correct_out_path = '../data/log/correct_log.jsonl'):

    dpo = open(dpo_data_path,'a',encoding='utf-8')
    ift = open(ift_data_path,'a',encoding='utf-8')
    datas = utils.readjsonl(res_path)
    for i, data in enumerate(tqdm(datas)):
        
        prompt = data['prompt']
        constraints = data['constraints']
        followed_list = data['follow_instruction_list']
        
        if len(followed_list) != len(constraints):
            print('number of folllowed list does not match the constraints! Please check!')
            continue
        
        dpo_list = []
        chosen = data['response']
        for index, followed in enumerate(followed_list):
            if followed == True:
                continue
            dic = {}
            dic['prompt'] = prompt
            dic['constraint'] = constraints[index]
            dic['reject'] = chosen
            try:
                chosen = get_corrected(chosen, constraints[index], correct_out_path, api_key)
            except:
                print('\033[31mERROR in {} th sample\033[0m'.format(i))
                continue
            dic['chosen'] = chosen
            dpo_list.append(dic)

        if len(dpo_list) < 1:
            continue
        for x in dpo_list:
            x['chosen'] = chosen
            dpo.write(json.dumps(x, ensure_ascii=False) + '\n')

        # ift data
        ift_data = data.copy()
        ift_data['response'] = chosen
        ift.write(json.dumps(ift_data, ensure_ascii=False) + '\n')

    dpo.close()
    ift.close()

# filter out those samples with the same 'reject' and 'chosen'
def process_dpo_data(dpo_data_path):
    dpo_datas = utils.readjsonl(dpo_data_path)
    res = []
    for data in dpo_datas:
        if data['reject'] == data['chosen']:
            continue
        res.append(data)
    print(len(res))
    utils.writejsonl(res, dpo_data_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--res_path",type=str,default='../data/data_response.jsonl',help="Path to your data with model's response")
    parser.add_argument("--ift_data_path",type=str,default='../data/train/ift_data.jsonl',help="Path to the corrected IFT data for training")
    parser.add_argument("--dpo_data_path",type=str,default='../data/train/dpo_data.jsonl',help="Path to the corrected DPO data for training")
    parser.add_argument("--api_key",type=str,default='',help="Your api key to access OpenAI GPT-4")
    args = parser.parse_args()

    correct_response(args.res_path, args.ift_data_path, args.dpo_data_path, args.api_key)
    process_dpo_data (args.dpo_data_path)



