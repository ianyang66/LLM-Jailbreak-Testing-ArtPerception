import random
import string
class Art_mutator:
    #TODO : rewrite it with index parameter available
    def __init__(self,seed=42) -> None:
        #self.random_replace_table_list = []
        self.symbol_replace_table_list = []
        #self.seed = seed
        self.current_table = [] 
        self.is_mutate = False
        #random.seed(seed)

    def set_is_mutate(self,is_mutate):
        self.is_mutate = is_mutate

    def make_table(self,char_list):
        # https://www.reddit.com/r/learnpython/comments/qk1wo8/how_do_i_replace_a_string_using_a_dictionary/
        replace_list = char_list 
        letters = char_list 
        random_replace  = ''.join(random.sample(replace_list,len(replace_list)))
        dict_cipher = str.maketrans(letters,random_replace)
        return dict_cipher
    
    def replace_text(self, text, replace_table):
        return text.translate(replace_table)
    
    # def make_random_replace_table(self, random_list) -> None:
    #     tmp_table= self.make_table(random_list)
    #     self.random_replace_table_list.append(tmp_table)

    # def replace_random(self,text):

    #     t = self.current_table
    #     replaced_ascii = self.replace_text(text,t)

    #     return replaced_ascii   
    #                                                  
    def make_symbol_replace_table(self, black_list):
        # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        symbol_list = string.printable[62:94].translate({ord(x): '' for x in black_list}) # make sure don't mutate black list symbol 
        tmp_table= self.make_table(symbol_list)
        self.symbol_replace_table_list.append(tmp_table)
        return tmp_table

    def replace_symbol(self,text):
        t = self.current_table
        replaced_ascii = self.replace_text(text,t)

        return replaced_ascii
    
    def set_current_table(self, idx) -> None:
        ### original symbol mapping 
        if not self.is_mutate :
            self.current_table = {}
        else :
            self.current_table = self.symbol_replace_table_list[idx]
        # else :
        #     self.current_table = self.random_replace_table_list[idx]