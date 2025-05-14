import json 
import pandas as pd

def load_harmful_word_list():
    file_name = './dataset/harmful_word_gpt-4o-mini-2024-07-18.json'

    f = open(file_name,'r')
    data = json.loads(f.read())
    f.close()

    ins_list = []
    word_lists = []
    for i in range(len(data)):
        instruction = data[i]['instruction']
        word_list = data[i]['word_list']
        while '' in word_list:
            word_list.remove('')
        ins_list.append(instruction)
        word_lists.append(word_list)
    
    return ins_list, word_lists


hex_phi_path = '../dataset/HEx_PHI_sub10.json'
Harmful_behavior_custom_path  = '../dataset/harmful_behaviors_custom.csv'

def load_harmful_ins_dataset(dataset):
    if 'hexphi' in dataset:
        f = open(hex_phi_path,'r')
        ins_json = json.loads(f.read().strip())
        f.close()

        ins_list = []
        for ins in ins_json:
            ins_list += ins['data']

        return ins_list
    
    elif 'custom' in dataset:
        df = pd.read_csv(Harmful_behavior_custom_path)
        ins_list = df["goal"].to_list()

        return ins_list
    
    else :
        raise NotImplementedError
