import os 
import argparse
#import nltk
#nltk.download('stopwords')
import time 
import datetime
import json
from tqdm.contrib import tzip
import random
import string

from utils.model import load_model
from utils.dataset import  load_harmful_word_list
from utils.safe_eval import LLM_evaluator
from utils.masker import Mask_handler
from gen_jb_prompt import vertical_horizontal_jb, horizontal_jb, vertical_jb, mutator

def same_seed(seed=42): 
    '''Fixes random number generator seeds for reproducibility.'''
    random.seed(seed)

def mask_instruction(mask_type, instruction, mask_word_list):
    msk = Mask_handler()
    if mask_type == 'char':
        return msk.char_masker(instruction,mask_word_list)
    elif mask_type == 'word':
        return msk.word_masker(instruction,mask_word_list)
    else :
        raise NotImplementedError

def sort_words_by_order(word_list, string):
    string = string.lower()
    # Sort the words based on the index of their first occurrence in the string
    sorted_words = sorted(word_list, key=lambda word: string.index(word.lower()))
    return sorted_words


def main(args):
    same_seed(args.seed)

    ## setting argument
    model_id = args.model
    ps = args.ps
    dataset = args.dataset
    mask_type = args.mType
    direction = args.direction 
    font = args.font
    num = args.num 
    mutate = args.mutate

    result_dir = args.dir
    os.makedirs(f'{result_dir}', exist_ok=True)
    ### setting 
    jb_dict = vars(args)
    jb_dict["jb_artifacts"] = []
    timestamp_start = datetime.datetime.now()
    ### load model
    
    llm = load_model(model_id)
    evaluator = LLM_evaluator(llm)


    
    jb_file = f'{result_dir}/model={model_id}-font={font}-d={direction}-ps={ps}-mask={mask_type}-top_n={args.top_n}'
    if num != -1:
        jb_file += f'-num={num}'
    if mutate != 0:
        jb_file += f'-mutate={mutator}'
    
    jb_file += '.json'

    ### load dataset 
    ins_list, harmful_word_lists = load_harmful_word_list()
    if num != -1 :
        ins_list = ins_list[:num]
        harmful_word_lists = harmful_word_lists[:num]

    if direction == 'h':
        jb_cli = horizontal_jb()

    elif direction == 'v':
        jb_cli = vertical_jb()  

    elif direction == 'hv':
        jb_cli = vertical_horizontal_jb()
    else :
        raise ValueError('Only direction h, v, hv')

    if args.mutate != 0  :
        black_list = ""
        jb_dict['mutate_table'] = []
        mutator.set_is_mutate(True)
        
        for idx in range(args.mutate):  
            table = mutator.make_symbol_replace_table(black_list)
            table_data ={
                'idx' : idx,
                'table_mapping' : table
            }
            jb_dict['mutate_table'].append(table_data)


    idx = 0
    time1 = time.time()
    total_rule_jailbroken = 0

    if mutate == 0:
        for instruction, harmful_word_list in tzip(ins_list,harmful_word_lists):
            harmful_word_list = harmful_word_list[:args.top_n]
            
            # remove puncuation in head or tail
            harmful_word_list = [word.strip(string.punctuation) for word in harmful_word_list] 
            ## remove broken puncuation
            harmful_word_list_new = []
            for word in harmful_word_list:
                if '\\' in word:
                    word = word[:word.find('\\')]
                harmful_word_list_new.append(word)


            sorted_list = sort_words_by_order(harmful_word_list_new,instruction)
            # if sorted_list == harmful_word_list:
                
            #     idx += 1 
            #     jb_dict["jb_artifacts"].append({'idx' : idx})
            #     continue
            masked_instruction = mask_instruction(mask_type, instruction, sorted_list)
            #print(masked_ins_word)

            prompt = jb_cli.gen_prompt(
                masked_instruction=masked_instruction,
                masked_word_list=sorted_list, ## broken
                font=font,
                ps=ps,
                mask_type=mask_type
            )
            # print('\n###############\n')
            # print(prompt)

            resp = llm.get_respone(prompt)
            # print('\n###############\n')
            # print(resp)
            #rule_jailbroken, harmful_score = evaluator.evaluation(instruction,resp)
            rule_jailbroken = evaluator.evaluation(instruction,resp)

            if rule_jailbroken:
                total_rule_jailbroken += 1

            jb_artifact = {
                "idx" : idx,
                "instruction": instruction, 
                "response": resp, 
                "mask_word_list" : sorted_list,
                "jailbroken_rules": rule_jailbroken, 
                #'jailbroken_llama': harmful_llama
            }
            jb_dict["jb_artifacts"].append(jb_artifact) 

            
            with open(jb_file, 'w') as f:
                json.dump(jb_dict, f, indent=4)    

            idx +=1

    elif mutate > 0:
        for i in range(mutate):
            mutator.set_current_table(i)
            for instruction, harmful_word_list in tzip(ins_list,harmful_word_lists):
                harmful_word_list = harmful_word_list[:args.top_n]
                
                # remove puncuation in head or tail
                harmful_word_list = [word.strip(string.punctuation) for word in harmful_word_list] 
                ## remove broken puncuation
                harmful_word_list_new = []
                for word in harmful_word_list:
                    if '\\' in word:
                        word = word[:word.find('\\')]
                    harmful_word_list_new.append(word)


                sorted_list = sort_words_by_order(harmful_word_list_new,instruction)

                masked_instruction = mask_instruction(mask_type, instruction, sorted_list)
                #print(masked_ins_word)

                prompt = jb_cli.gen_prompt(
                    masked_instruction=masked_instruction,
                    masked_word_list=harmful_word_list,
                    font=font,
                    ps=ps,
                    mask_type=mask_type
                )
                
                #print(prompt)

                resp = llm.get_respone(prompt)

                #rule_jailbroken, harmful_score = evaluator.evaluation(instruction,resp)
                rule_jailbroken = evaluator.evaluation(instruction,resp)

                if rule_jailbroken:
                    total_rule_jailbroken += 1

                jb_artifact = {
                    "idx" : idx,
                    "instruction": instruction, 
                    "response": resp, 
                    "mask_word_list" : sorted_list,
                    "jailbroken_rules": rule_jailbroken, 
                    #'jailbroken_llama': harmful_llama
                }
                jb_dict["jb_artifacts"].append(jb_artifact) 

                
                with open(jb_file, 'w') as f:
                    json.dump(jb_dict, f, indent=4)    

                idx +=1

    time2 = time.time()
    print(f"Time elapsed for inference: {time2-time1:.2f}s")
    print(f'Total rule jailbroken rate : {(total_rule_jailbroken/idx):.2f}')
    jb_dict["exe_time"] = f'{time2-time1:.2f}'
    with open(jb_file, 'w') as f:
        json.dump(jb_dict, f, indent=4)    
    


if __name__ == '__main__':
    args = argparse.ArgumentParser()

    ### ASCII art direction setting  
    args.add_argument('--direction', type=str, default='h',help='ASCII direction setting',choices=['h','v','hv'])

    ### ASCII font setting 
    args.add_argument('--font',type=str,default='cards',help='ASCII art font setting')

    ### ASCII art seperate setting 
    args.add_argument('--ps', type=str, default='sep-mid-no',help="prompt type setting")

    ### Masked type setting 
    args.add_argument('--mType', type=str, default='word',help="Masked word method. Support : word, char")


    ### dataset 
    args.add_argument('--dataset',type=str,default='custom')  # PHI and custom

    ### target model

    args.add_argument('--model',type=str,default='llama3-8b',choices=['llama3-8b','gemma2-9b','mixtral','Qwen2'])

    ### number of instruction to use 
    args.add_argument('--num',type=int,default=-1,help="number of instruction")

    ### round of mutation 
    args.add_argument('--mutate',type=int,default=0,help="number of mutation")

    ### random seed 
    args.add_argument('--seed',type=int,default=42,help="seed setting")

    args.add_argument('--top_n',type=int,default=2,help='mask top n harmful word')
    
    args.add_argument('--dir',type=str,default='./result',help='directory to store result')

    args = args.parse_args()
    print(args)
    main(args)
