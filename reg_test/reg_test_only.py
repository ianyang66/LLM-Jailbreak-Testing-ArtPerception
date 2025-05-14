import sys
sys.path.append('..')

import string
import os 

import argparse
import random
import json
import time
from Levenshtein import distance
from tqdm import tqdm

from utils.model import load_model
from utils.l_font import  font_for_dataset, font_class_for_dataset
from reg_prompt_gen import horizontal_reg, vertical_reg, mutator
from utils.reg_eval import eval_res
from tqdm.contrib import tzip
# os.environ['CUDA_VISIBLE_DEVICES'] = "1,2"

def random_uppercase_string(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def same_seed(seed=42): 
    '''Fixes random number generator seeds for reproducibility.'''
    random.seed(seed)





def main(args):
    same_seed()

    text_length_list = args.length.split(',')
    #result_store_dir = './mutation'
    result_store_dir = args.dir
    #result_store_dir = './exp'
    os.makedirs(f'{result_store_dir}',exist_ok=True)

    dataset_dict = vars(args)
    dataset_dict['data'] = []
    file_path = f'{result_store_dir}/model={args.model}-direction={args.direction}-ps={args.ps}-mutate={args.mutate}-text_length={args.length}-text_num={args.num}-only={args.only}-ict_size={args.ict_size}.json'
    

    print("Start running inference")
    # run inference

    
    if args.direction == 'h':
        reg_cli = horizontal_reg()

    elif args.direction == 'v':
        reg_cli = vertical_reg()  

    else :
        raise ValueError('Only direction h or v')




    model = load_model(args.model)
    ### create mutation mapping table
    if args.mutate != 0  :
        black_list = ""
        dataset_dict['mutate_table'] = []
        mutator.set_is_mutate(True)
        
        for idx in range(args.mutate):  
            table = mutator.make_symbol_replace_table(black_list)
            table_data ={
                'idx' : idx,
                'table_mapping' : table
            }
            dataset_dict['mutate_table'].append(table_data)
    time1 = time.time()

    idx = 0
    correct = 0 
    AMR = 0
    lev_distance = 0

    only_length_list = args.only.split(',') 
    only_num_list = args.only_num.split(',')

    if '-1' in only_length_list:
        only_length_list = text_length_list

    same_seed()
    for length in text_length_list:  

        text_list = []
        for i in range(args.num):
            text_list.append(random_uppercase_string(int(length)))
        
        if length not in only_length_list:
            continue
        
        if '-1' not in only_num_list:
            text_list = text_list[int(only_num_list[0]):int(only_num_list[1])]

        for font, font_class in tqdm(tzip(font_for_dataset, font_class_for_dataset)): 
            if args.mutate == 0 :
                #mutator.set_is_mutate(False)
                for text in text_list:             
                    prompt = reg_cli.gen_prompt(text, font, args.ps, font_class, ict_size=args.ict_size)
                    response = model.get_respone(prompt,max_new_tokens=args.max_token)
                    correct_i, AMR_i, answer, fail_i, lev_distance_i = eval_res(response, text, AMR=True)
    
                    dataset_data ={
                        'idx' : idx,
                        'text' : text,
                        'font' : font,
                        'font_class': font_class,
                        'prompt' : prompt,
                        'response' : response,
                        'answer' : answer,
                        'correct' : correct_i,
                        'AMR' : AMR_i,
                        'lev_distance': lev_distance_i,
                        'fail' : fail_i
                    }

                    if correct_i:
                        correct += 1
                    AMR += AMR_i
                    lev_distance += lev_distance_i

                    dataset_dict['data'].append(dataset_data)
                    idx += 1
                with open(file_path, "w") as f:
                    json.dump(dataset_dict, f, indent=4)

            else :
                for text in text_list:
                    for i in range(args.mutate):
                        mutator.set_current_table(i)
                        prompt = reg_cli.gen_prompt(text,font, args.ps)
                        response = model.get_respone(prompt,max_new_tokens=args.max_token)

                        correct_i, AMR_i, answer, fail_i, lev_distance_i = eval_res(response, text, AMR=True)
                        lev_distance_i = distance(answer, text.lower())
 
                        dataset_data ={
                            'idx' : idx,
                            'text' : text,
                            'font' : font,
                            'mutation_id': i,
                            'prompt' : prompt,
                            'response' : response,
                            'answer' : answer,
                            'correct' : correct_i,
                            'AMR' : AMR_i,
                            'lev_distance': lev_distance_i,
                            'fail' : fail_i
                        }

                        if correct_i:
                            correct += 1
                        AMR += AMR_i
                        lev_distance += lev_distance_i

                        dataset_dict['data'].append(dataset_data)
                        idx += 1


                with open(file_path, "w") as f:
                    json.dump(dataset_dict, f, indent=4)

    time2 = time.time()
    print(f"Accuracy: {correct/idx}")
    print(f"AMR: {AMR/idx}")
    print(f"Levenshtein distance : {lev_distance/idx}")
    print(f"Time elapsed for inference: {time2-time1:.2f}s")

    dataset_dict['AMR'] = AMR/idx
    dataset_dict['Accuracy'] = correct/idx
    dataset_dict['Levenshtein distance'] = lev_distance/idx
    dataset_dict["Exe_time"] = f'{time2-time1:.2f}'
    with open(file_path, 'w') as f:
        json.dump(dataset_dict, f, indent=4)    


        



if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--model", type=str, default="llama3-8b", choices=['llama3-8b','gemma2-9b','Qwen2','mixtral'], help="Model name for evaluation")
    args.add_argument("--direction",type=str,default='h',choices=['h','v'], help="direction of ASCII ART")
    args.add_argument("--ps", type=str, default="origin-no-no", help="prompt type : origin/sep/ict\n Replace position : head/mid/tail/no\n Replace space or not : yes/no")
    args.add_argument("--num", type=int, default=1, help="Number of samples of text")
    args.add_argument("--length",type=str, default='2,3', help="length of text sample. Use ',' to set multiple length")
    args.add_argument("--mutate",type=int, default=0, help="Number of mutation sample. Set to 0 for no mutation")
    args.add_argument("--seed", type=int, default=42, help="Setting random seed for reproduce")
    args.add_argument("--only",type=str,default='-1')
    args.add_argument("--only_num",type=str,default='-1')
    args.add_argument("--dir",type=str,default="./result")
    args.add_argument("--max_token",type=int,default=2048)
    args.add_argument("--ict_size",type=int, default=-1)
    args = args.parse_args()
    print(args)
    main(args)