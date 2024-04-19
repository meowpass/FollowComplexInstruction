# 0. imports
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "4"
import json #hqx
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union
import torch
from datasets import Dataset, load_dataset
from peft import AutoPeftModelForCausalLM, LoraConfig
from transformers import LlamaTokenizer, LlamaForCausalLM, AutoTokenizer, AutoModelForCausalLM
from transformers import AutoTokenizer, HfArgumentParser, TrainingArguments
from typing import Tuple
from trl import DPOTrainer
from config import ScriptArguments
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
import pdb

if __name__ == "__main__":
    parser = HfArgumentParser(ScriptArguments)
    script_args = parser.parse_args_into_dataclasses()[0]

    # Set your model and dataset
    model_name_or_path = ""
    data_files = {"train": "dpo_train_mix.json", "test": "dpo_test.json"}
    dataset_name = './data/'

    model = LlamaForCausalLM.from_pretrained(
        model_name_or_path,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16
    )
    model.enable_input_require_grads()
    model.gradient_checkpointing_enable() 
    model.config.use_cache = False

    if script_args.ignore_bias_buffers:
        # torch distributed hack
        model._ddp_params_and_buffers_to_ignore = [
            name for name, buffer in model.named_buffers() if buffer.dtype == torch.bool
        ]

    model_ref = LlamaForCausalLM.from_pretrained(
        model_name_or_path,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16
    )

    tokenizer = LlamaTokenizer.from_pretrained(model_name_or_path)
    tokenizer.pad_token = tokenizer.eos_token


    dataset = load_dataset(dataset_name, data_files=data_files)

    # 4. initialize training arguments:
    training_args = TrainingArguments(
        per_device_train_batch_size=script_args.per_device_train_batch_size,
        per_device_eval_batch_size=script_args.per_device_eval_batch_size,
        max_steps=script_args.max_steps,
        logging_steps=script_args.logging_steps,
        save_steps=script_args.save_steps,
        gradient_accumulation_steps=script_args.gradient_accumulation_steps,
        gradient_checkpointing=script_args.gradient_checkpointing,
        learning_rate=script_args.learning_rate,
        evaluation_strategy="steps",
        eval_steps=script_args.eval_steps,
        output_dir=script_args.output_dir,
        report_to=script_args.report_to,
        lr_scheduler_type=script_args.lr_scheduler_type,
        warmup_steps=script_args.warmup_steps,
        optim=script_args.optimizer_type,
        bf16=True,
        remove_unused_columns=False,
        run_name="dpo_llama2",
    )

    peft_config = LoraConfig(
        r=script_args.lora_r,
        lora_alpha=script_args.lora_alpha,
        lora_dropout=script_args.lora_dropout,
        target_modules=[
            "q_proj",
            "v_proj",
            "k_proj",
            "out_proj",
            "fc_in",
            "fc_out",
            "wte",
        ],
        bias="none",
        task_type="CAUSAL_LM",
    )

    class MyDPOTrainer(DPOTrainer):
        def masked_cross_entropy_loss(self, logits, labels, **kwargs):
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()

            loss_fct = CrossEntropyLoss()
            shift_logits = shift_logits.view(-1, shift_logits.shape[-1])
            shift_labels = shift_labels.view(-1)
            shift_labels = shift_labels.to(shift_logits.device)
            loss = loss_fct(shift_logits, shift_labels)
            return loss

        def concatenated_forward(
            self, model: nn.Module, batch: Dict[str, Union[List, torch.LongTensor]]
        ) -> Tuple[torch.FloatTensor, torch.FloatTensor, torch.FloatTensor, torch.FloatTensor]:
            """Run the given model on the given batch of inputs, concatenating the chosen and rejected inputs together.

            We do this to avoid doing two forward passes, because it's faster for FSDP.
            """
            print(batch)
            pdb.set_trace()

            concatenated_batch = self.concatenated_inputs(batch)
            len_chosen = batch["chosen_labels"].shape[0]
            model_kwargs = (
                {
                    "labels": concatenated_batch["concatenated_labels"],
                    "decoder_input_ids": concatenated_batch.pop("concatenated_decoder_input_ids", None),
                }
                if self.is_encoder_decoder
                else {}
            )

            outputs = model(
                concatenated_batch["concatenated_input_ids"],
                attention_mask=concatenated_batch["concatenated_attention_mask"],
                labels=concatenated_batch["concatenated_labels"],
                **model_kwargs,
            )
            all_logits = outputs.logits.to(torch.float32)

            all_logps = self.get_batch_logps(
                all_logits,
                concatenated_batch["concatenated_labels"],
                average_log_prob=False,
            )
            chosen_logps = all_logps[:len_chosen]
            rejected_logps = all_logps[len_chosen:]

            chosen_logits = all_logits[:len_chosen]
            rejected_logits = all_logits[len_chosen:]

            return (chosen_logps, rejected_logps, chosen_logits, rejected_logits)

        def get_batch_loss_metrics(
            self,
            model,
            batch: Dict[str, Union[List, torch.LongTensor]],
            train_eval: Literal["train", "eval"] = "train",
        ):
            """Compute the DPO loss and other metrics for the given batch of inputs for train or test."""
            concatenated_batch = self.concatenated_inputs(batch)
            metrics = {}
            (
                policy_chosen_logps,
                policy_rejected_logps,
                policy_chosen_logits,
                policy_rejected_logits,
            ) = self.concatenated_forward(model, batch)
            with torch.no_grad():
                if self.ref_model is None:
                    with self.accelerator.unwrap_model(self.model).disable_adapter():
                        (
                            reference_chosen_logps,
                            reference_rejected_logps,
                            _,
                            _,
                        ) = self.concatenated_forward(self.model, batch)
                else:
                    (
                        reference_chosen_logps,
                        reference_rejected_logps,
                        _,
                        _,
                    ) = self.concatenated_forward(self.ref_model, batch)

            losses_old, chosen_rewards, rejected_rewards = self.dpo_loss(
                policy_chosen_logps,
                policy_rejected_logps,
                reference_chosen_logps,
                reference_rejected_logps,
            )

            pi_logratios = policy_chosen_logps - policy_rejected_logps
            ref_logratios = reference_chosen_logps - reference_rejected_logps
            pi_ref_logits = pi_logratios - ref_logratios

            model_kwargs = (
                {
                    "labels": concatenated_batch["concatenated_labels"],
                    "decoder_input_ids": concatenated_batch.pop("concatenated_decoder_input_ids", None),
                }
                if self.is_encoder_decoder
                else {}
            )            

            chosen_labels = concatenated_batch["concatenated_labels"][:batch["chosen_labels"].shape[0]]
            sft_loss = self.masked_cross_entropy_loss(policy_chosen_logits, chosen_labels, **model_kwargs)
            losses = losses_old + sft_loss
            reward_accuracies = (chosen_rewards > rejected_rewards).float()

            prefix = "eval_" if train_eval == "eval" else ""
            metrics[f"{prefix}dpo/loss"] = losses_old.cpu().mean()
            metrics[f"{prefix}sft/loss"] = sft_loss.cpu().mean()
            metrics[f"{prefix}pi/logratios"] = pi_logratios.cpu().mean()
            metrics[f"{prefix}ref/logratios"] = ref_logratios.cpu().mean()  
            metrics[f"{prefix}pi/ref"] = pi_ref_logits.cpu().mean()  
            metrics[f"{prefix}rewards/chosen"] = chosen_rewards.cpu().mean()
            metrics[f"{prefix}rewards/rejected"] = rejected_rewards.cpu().mean()
            metrics[f"{prefix}rewards/accuracies"] = reward_accuracies.cpu().mean()
            metrics[f"{prefix}rewards/margins"] = (chosen_rewards - rejected_rewards).cpu().mean()
            metrics[f"{prefix}logps/rejected"] = policy_rejected_logps.detach().cpu().mean()
            metrics[f"{prefix}logps/chosen"] = policy_chosen_logps.detach().cpu().mean()
            metrics[f"{prefix}logits/rejected"] = policy_rejected_logits.detach().cpu().mean()
            metrics[f"{prefix}logits/chosen"] = policy_chosen_logits.detach().cpu().mean()

            return losses.mean(), metrics
        

    # 5. initialize the DPO trainer
    dpo_trainer = MyDPOTrainer(
        model = None,
        nodel_ref = None,
        args=training_args,
        beta=script_args.beta,
        train_dataset=dataset['train'],
        eval_dataset=dataset['test'],
        tokenizer=tokenizer,
        # peft_config=None,
        peft_config=peft_config,
        max_prompt_length=script_args.max_prompt_length,
        max_length=script_args.max_length,
    )

    # 6. train
    dpo_trainer.train()
    dpo_trainer.save_model(script_args.output_dir)

    # 7. save
    output_dir = os.path.join(script_args.output_dir, "final_checkpoint")
    dpo_trainer.model.save_pretrained(output_dir)