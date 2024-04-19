import random
from tqdm import tqdm
import json
import re
import argparse

import taxonomy
import GPT_api
import instructions_registry
import instructions_util
import prompts
import utils


def get_keyword(seed_inst, api_key):
    prompt = prompts.keyword_prompt
    prompt = prompt.format(str(seed_inst))
    keyword_pattern = r'keywords:\n?(.*)\n?'
    response = GPT_api.get_res(prompt, api_key)
    try:
        keywords = re.findall(keyword_pattern, response)[0]
        keywords = eval(keywords)
    except:
        keywords = random.choices(instructions_util.WORD_LIST, k=3)
    return keywords


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed_path",type=str,default='../data/seed_data.jsonl',help="Path to your seed data")
    parser.add_argument("--data_path",type=str,default='../data/data.jsonl',help="Path to the output compositional data")
    parser.add_argument("--api_key",type=str,default='',help="Your api key to access OpenAI GPT-4")
    args = parser.parse_args()

    # select how many constraints to be incorporated
    lower_bound = 3
    upper_bound = 5

    cons_dict = taxonomy.taxonomy
    conflict_dict = instructions_registry.INSTRUCTION_CONFLICTS
    conflict_dict = instructions_registry.conflict_make(conflict_dict)

    seed_datas = utils.readjsonl(args.seed_path)
    for seed_index, seed_data in tqdm(enumerate(seed_datas)):
        select_num = random.randint(lower_bound, upper_bound)
        instruction_id_list = []
        index = 0
        recur_count = 0
        while index < select_num:
            random_key= random.choice(list(cons_dict.keys()))
            # constrained respose
            if index == 0 and 'constrained_response' in random_key:
                instruction_id_list.append(random_key)
                break
            # json
            if index == 0 and ('json_format' in random_key or 'xml_format' in random_key): 
                instruction_id_list.append(random_key)
                instruction_id_list.append(random.choice(['keywords:forbidden_words', 'keywords:existence']))
                break
            if list(set(conflict_dict[random_key]) & set(instruction_id_list)):
                recur_count += 1
                if(recur_count > 1000):
                    print(instruction_id_list)
                    print(random_key)
                    break
                continue
            instruction_id_list.append(random_key)
            index +=1

        seed_inst = seed_data['instruction'] + ' '+ seed_data['input']
        # directly incorporated
        woGPT_list = ['detectable_format:multiple_sections', 'change_case:capital_word_frequency', 'detectable_format:number_highlighted_sections', 'detectable_format:number_bullet_lists', 'detectable_content:postscript', 'detectable_content:number_placeholders', 'length_constraints:number_words', 'length_constraints:number_paragraphs','length_constraints:number_sentences', 'language:response_language', 'keywords:letter_frequency', 'startend:end_checker']
        # employ ChatGPT to come up the keyword
        wGPT_list = ['keywords:existence', 'keywords:frequency', 'keywords:forbidden_words', 'length_constraints:nth_paragraph_first_word']

        constraints = []
        kwargs = []
        flag = -1
        position = ''
        for i, inst_id in enumerate(instruction_id_list):
            if len(cons_dict[inst_id]['args']) == 0:
                kwargs.append({})
                constraints.append(random.choice(cons_dict[inst_id]['description']))

            elif inst_id in woGPT_list:
                
                if "number_words" in inst_id:
                    description = random.choice(cons_dict[inst_id]['description'])
                    relation = random.choice(cons_dict[inst_id]['args']['relation'])
                    if relation == 'at least':
                        num_words = random.randint(10, 25)
                    elif relation == 'less than':
                        num_words = random.randint(30, 100)
                    kwargs.append({'relation': relation, 'num_words': num_words})
                    description = description.replace('<relation>', relation)
                    description = description.replace('<num_words>', str(num_words))
                    constraints.append(description)

                elif "response_language" in inst_id:
                    description = random.choice(cons_dict[inst_id]['description'])
                    lang_code = random.choice(cons_dict[inst_id]['args']['language'])
                    lang_dict = instructions_util.LANGUAGE_CODES
                    language = lang_dict[lang_code]
                    kwargs.append({'language': lang_code})
                    description = description.replace('<language>', language)
                    constraints.append(description)

                else:
                    description = random.choice(cons_dict[inst_id]['description'])
                    args_keys = cons_dict[inst_id]['args'].keys()
                    temp = {}
                    for args_key in args_keys:
                        temp[args_key] = random.choice(cons_dict[inst_id]['args'][args_key])
                        description = description.replace('<'+args_key+'>', str(temp[args_key]))
                    kwargs.append(temp)
                    constraints.append(description)        
                
            elif inst_id in wGPT_list:
                if 'existence' in inst_id:
                    description = random.choice(cons_dict[inst_id]['description'])
                    keywords = get_keyword(seed_inst, args.api_key)
                    keywords = random.choice(keywords) if type(keywords) == list else keywords
                    keywords = keywords.split(' ')[0]
                    kwargs.append({'keywords':[keywords]})
                    description = description.replace('<keywords>', keywords)
                    constraints.append(description)
                elif 'frequency' in inst_id:
                    description = random.choice(cons_dict[inst_id]['description'])
                    keywords = get_keyword(seed_inst, args.api_key)
                    keywords = random.choice(keywords)
                    keywords = keywords.split(' ')[0]
                    relation = random.choice(cons_dict[inst_id]['args']['relation'])
                    frequency = random.choice(cons_dict[inst_id]['args']['frequency'])
                    kwargs.append({
                        "relation": relation,
                        "keyword": keywords,
                        "frequency": frequency
                    })
                    description =description.replace('<relation>', str(relation))
                    description =description.replace('<keyword>', str(keywords))
                    description =description.replace('<frequency>', str(frequency))
                    constraints.append(description)
                elif 'forbidden_words' in inst_id:
                    description = random.choice(cons_dict[inst_id]['description'])
                    keywords = get_keyword(seed_inst, args.api_key)
                    keywords = random.choice(keywords)
                    keywords = keywords.split(' ')[0]
                    kwargs.append({'forbidden_words':[keywords]})
                    description =description.replace('<forbidden_words>', keywords)
                    constraints.append(description)
                elif 'nth_paragraph_first_word' in inst_id:
                    description = random.choice(cons_dict[inst_id]['description'])
                    keywords = get_keyword(seed_inst, args.api_key)
                    keywords = random.choice(keywords) if type(keywords) == list else keywords
                    keywords = keywords.split(' ')[0]
                    first_word = keywords
                    num_paragraphs = random.choice(cons_dict[inst_id]['args']['num_paragraphs'])
                    nth_paragraph = random.randint(1,num_paragraphs)
                    kwargs.append({
                        "first_word": first_word,
                        "num_paragraphs": num_paragraphs,
                        "nth_paragraph": nth_paragraph
                    })
                    nth_paragraph = cons_dict[inst_id]['args']['nth_paragraph'][nth_paragraph]
                    description = description.replace('<first_word>', first_word)
                    description = description.replace('<num_paragraphs>', str(num_paragraphs))
                    description = description.replace('<nth_paragraph>', str(nth_paragraph))
                    constraints.append(description)
                else:
                    print('error in seed inst {}'.format(seed_index))
                    exit(-1)
            elif 'repeat_prompt' in inst_id:
                flag = i
                position = random.choice(cons_dict[inst_id]['args']['position'])
                if position == 'end':
                    description = random.choice(cons_dict[inst_id]['description'][:4])
                else:
                    description = random.choice(cons_dict[inst_id]['description'][4:])
                kwargs.append({'prompt_to_repeat': ''})
                constraints.append(description)
            else:
                print('error {} not supported'.format(inst_id))
                exit(-1)

        new_data = {}
        new_inst = seed_inst
        if flag == -1:
            for constraint in constraints:
                new_inst = new_inst + constraint + '. '
            new_data['prompt'] = new_inst
            new_data['instruction_id_list'] = instruction_id_list
            new_data['kwargs'] = kwargs
            new_data['constraints'] = constraints
        else:
            for ci, constraint in enumerate(constraints):
                if ci == flag:
                    continue
                new_inst = new_inst + constraint + '. '
            kwargs[flag]['prompt_to_repeat'] = new_inst

            if position == 'end':
                new_inst = new_inst + constraints[flag]
            else:
                new_inst = constraints[flag] + new_inst
            

            new_data['prompt'] = new_inst
            new_data['instruction_id_list'] = instruction_id_list
            new_data['kwargs'] = kwargs
            new_data['constraints'] = constraints
            
        with open(args.data_path,'a',encoding='utf-8') as f:
            f.write(json.dumps(new_data, ensure_ascii=False) + '\n')


        


