# From Complex to Simple: Enhancing Multi-Constraint Complex Instruction Following Ability of Large Language Models
Official implementation of the paper "From Complex to Simple: Enhancing Multi-Constraint Complex Instruction Following Ability of Large Language Models". We propose a framework to efficiently construct complex instructions meanwhile obtaining instance pairs for DPO training.

![image](https://github.com/meowpass/FCS/assets/56729976/debacf40-1858-402b-b94a-700e7b7ad20b)

## 🔥Updates
* 2024/4/22: We released the data and code of FCS
* 2024/4/22 We released the first version of our [paper](https://arxiv.org/xxxxxxx).

## ⚙️How to use the code

### Get the data

#### Generate the complex data

In practice, human instructions are usually complex, incorporated with multiple constraints. To obtain those complex data, we construct a taxonomy for different types of constraints and automatically incorporate them into an initial seed instruction to compose a complex one. Here, you can complete the whole procedure by running the script `gen_inst.sh`:

```shell
python ../get_data/gen_inst.py \
    --seed_path=PATH_TO_SEED_DATA \
    --data_path=PATH_TO_SAVE_THE_COMPOSITIONAL_DATA \
    --api_key=YOUR_API_KEY_TO_ACESS_GPT4\
```

An example of complex instrutcion is shown as below:
![image](https://github.com/meowpass/FollowComplexInstruction/assets/56729976/cd6810af-d472-42e7-afff-43b83e30dc42)
Here are 3 different constraints in the instructions

#### Do inference with your model

You need to do inference with your model to get the responses to the generated data. Here, we provide a script to do inference for LLaMA via the script `do_inference.sh`:

```shell
CUDA_VISIBLE_DEVICES=YOUR_CUDA_DEVICES python ../get_data/do_inference.py \
    --data_path=PATH_TO_YOUR_DATA \
    --res_path=PATH_TO_SAVE_RES \
    --model_path=PATH_TO_YOUR_MODEL\
    --lora_path=PATH_TO_YOUR_LORA_WEIGHT
```



#### Check your answer

We found it better to correct the wrong answer produced by the model to obtain an accurate one instead of directly employing an advanced LLM to answer. Hence, we first use rules to check whether the model has followed the constraints in the generated complex data. Simply run the script `check.sh`:

```shell
python ../get_data/check.py \
    --input_data=PATH_TO_SAVE_THE_COMPOSITIONAL_DATA \
    --input_response_data=PATH_TO_SAVED_RES \
    --output_dir=PATH_TO_SAVE_CHECKED_RES \
    --output_file_name=NAME_OF_CHECKED_RES
```



#### Teacher correct

Then, We employ the GPT3.5-turbo to correct the wrong response produced by the model. You can correct the response to simultaneously get data for IFT and DPO with the script `correct.sh`:

```shell
python ../get_data/correct.py \
    --res_path=PATH_TO_SAVED_RES \
    --ift_data_path=PATH_TO_SAVE_DATA_FOR_IFT_TRAINING \
    --dpo_data_path=PATH_TO_SAVE_DATA_FOR_DPO_TRAINING \
    --api_key=YOUR_API_KEY_TO_ACESS_GPT4\
```



### Go for DPO training

Now that you have obtained the training data, you can utilize them to train your own DPO model. Here, we provide a revised implementation for DPO in `dpo_train`. You can set your model_path and data_path in `dpo_train/dpo_train.py`. Then, you can train the model with the script `train_dpo.sh`:

```shell
CUDA_VISIBLE_DEVICES=YOUR_CUDA_DEVICES accelerate launch \
    --config_file ../dpo_train/deepspeed_zero1.yaml dpo_train.py \
    --output_dir=PATH_TO_SAVE_MODEL \
```

