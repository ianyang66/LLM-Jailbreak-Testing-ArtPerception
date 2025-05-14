import transformers
import torch
from utils.config import model_config


class llm:
    def __init__(self, model_id, dtype=torch.bfloat16) -> None:
        self.model_id = model_id

        if model_id == "llama3-8b":
            model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        elif model_id == "llama3-70b":
            model_name = "meta-llama/Meta-Llama-3-70B-Instruct"
        elif model_id == "gemma2-27b":
            model_name = "google/gemma-2-27b-it"
        elif model_id == "gemma2-9b":
            model_name = "google/gemma-2-9b-it"
        elif model_id == 'mixtral':
            model_name = 'mistralai/Mistral-7B-Instruct-v0.3'
        elif model_id == "Qwen2":
            model_name = "Qwen/Qwen2-7B-Instruct"
        else:
            raise NotImplementedError


        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_name,
            model_kwargs={"torch_dtype": dtype},
            device_map="auto",
            token=model_config['access_token'],
            trust_remote_code=True
        )
        # model = transformers.AutoModelForCausalLM.from_pretrained(
        #     model_id,
        #     trust_remote_code=True,
        #     device_map="auto", 
        #     torch_dtype=dtype, 
        #     token=model_config['access_token']
        # )

        # tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
        # self.pipeline = transformers.pipeline(
        #     "text-generation",
        #     model=model,
        #     tokenizer=tokenizer
        # )

    def get_respone(self, text, max_new_tokens=4096, temperature=0, top_p=0):       
        if 'llama' in self.model_id or 'Qwen2' in self.model_id:
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": text
                },
            ]

        else : 
            messages = [
                {
                    "role": "user",
                    "content": text
                },
            ]       

        prompt = self.pipeline.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
        )

        # terminators = [
        #     self.pipeline.tokenizer.eos_token_id,
        #     self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        # ]

        generation_args = {
            "max_new_tokens": max_new_tokens,
            "return_full_text": False,
            "temperature": temperature,
            "do_sample": False,
            #"eos_token_id": terminators,
            "top_p": top_p,
            "pad_token_id" : self.pipeline.tokenizer.eos_token_id
        }

        outputs = self.pipeline(
            prompt,
            **generation_args
        )
        resp = ''
        for seq in outputs:
            resp += seq['generated_text']
        return resp

def load_model(model_id):
    return llm(model_id)