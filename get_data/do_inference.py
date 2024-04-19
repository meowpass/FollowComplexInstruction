import json
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, GenerationConfig
import transformers
from peft import PeftModel
import torch
from tqdm import tqdm
import argparse
import utils

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
overall_instruction = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

def format_prompt(query, history=[], input=None):
    prompt = ""
    if len(history) == 0:
        prompt += f"<s>{B_INST} {B_SYS} {overall_instruction} {E_SYS} {query} {E_INST} "
    else:
        for i, (old_query, response) in enumerate(history):
            prompt += f"{old_query} {response}</s>"
        prompt += f"<s>{B_INST} {query} {E_INST}"
    # print(prompt)
    return prompt

def generate(q, history):
    prompt = format_prompt(q, history)

    input_ids = tokenizer(prompt, return_tensors="pt", padding=False, truncation=False, add_special_tokens=False)
    device = torch.device("cuda")
    input_ids = input_ids["input_ids"].to(device)

    with torch.no_grad():
        outputs= model.generate(input_ids=input_ids,
                generation_config= generation_config,
                return_dict_in_generate=True,
                output_scores=True,
        )

    s = outputs.sequences[0][input_ids.shape[1]:]
    response = tokenizer.decode(s, skip_special_tokens=True, spaces_between_special_tokens=False)
    return response


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path",type=str, required=True, default='',help="Path to the data file.")
    parser.add_argument("--res_path",type=str, required=True, default='',help="Path to save the mode output")
    parser.add_argument("--mode_path",type=str, required=True, default='',help="Path to the model weights.")
    parser.add_argument("--lora_path",type=str, default='',help="Path to the lora model weights if used")
    args = parser.parse_args()

    data_path =  args.data_path
    res_path = args.res_path

    LORA_WEIGHTS = args.lora_path
    tokenizer = LlamaTokenizer.from_pretrained(args.model_path)
    model = LlamaForCausalLM.from_pretrained(
        args.model_path,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    model.eval()
    if LORA_WEIGHTS:
        print('use lora weights!')
        model = PeftModel.from_pretrained(model, LORA_WEIGHTS)
    device = torch.device("cuda")

    generation_config = GenerationConfig(
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.0,
        max_new_tokens=2048,
    )

    datas = utils.readjsonl(data_path)
    
    output_file = open(res_path, 'a', encoding='utf-8')
    for data in tqdm(datas):
        prompt = data['prompt']
        response = generate(prompt, [])
        data['output'] = response
        output_file.write(json.dumps(data, ensure_ascii=False) + "\n")
    output_file.close()