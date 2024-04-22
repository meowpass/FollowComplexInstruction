CUDA_VISIBLE_DEVICES=YOUR_CUDA_DEVICES python ../get_data/do_inference.py \
    --data_path=../get_data/data/data.jsonl \
    --res_path=../get_data/data/res_llama2.jsonl \
    --model_path=PATH_TO_YOUR_MODEL\
    --lora_path=PATH_TO_YOUR_LORA_WEIGHT IF YOU USE LORA \
