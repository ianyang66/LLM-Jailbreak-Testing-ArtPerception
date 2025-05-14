import art 
from utils.mutator import Art_mutator
import reg_prompt as RegP
from ict_prompt import vertical_ict_prompt, horizontal_ict_prompt, gen_same_font_horizontal_ict_prompt, gen_same_font_vertical_ict_prompt
mutator = Art_mutator()

def replace_by_index(art, char, idx, replace_space):
    if replace_space == 'no':
        black_list = '\n '
    else:
        black_list = '\n'

    i = idx

    ## search forward 
    while  i < len(art) and art[i] in black_list :
        i += 1
    
    ### search backword if idx reach the end 
    if i == len(art):
        i = idx
        while i > 0 and art[i] in black_list :
            i -= 1  

    return "".join((art[:i],char,art[i+1:]))

### add letter hint to ascii art
def generate_alphabet_ascii_modified(text, font, ps):
    ## cards-sep-no-yes
    ps_list = ps.split('-')
    prompt_type = ps_list[0]
    replace_type = ps_list[1]
    replace_space = ps_list[2]

    ascii_list = []

    if replace_type == 'no' :
        for char in text :              
            art_char = art.text2art(char, font=font)
            art_char = art_char.split('\n')
            ascii_list.append(art_char)

    ## replace at head 
    elif replace_type == 'head':

        for char in text :
            idx = 0 #head 
            art_char = art.text2art(char, font=font)
            art_char = replace_by_index(art_char,char,idx,replace_space)
            art_char = mutator.replace_symbol(art_char)
            art_char = art_char.split('\n')                  
            ascii_list.append(art_char)
    
    elif replace_type == 'mid':

        for char in text :
            art_char = art.text2art(char, font=font)
            idx = len(art_char) // 2
            art_char = replace_by_index(art_char,char,idx,replace_space) 
            art_char = mutator.replace_symbol(art_char)
            art_char = art_char.split('\n')                  
            ascii_list.append(art_char)              

    elif replace_type == 'tail':

        for char in text :
            art_char = art.text2art(char, font=font)
            idx = len(art_char) - 1
            art_char = replace_by_index(art_char,char,idx,replace_space)
            art_char = mutator.replace_symbol(art_char)
            art_char = art_char.split('\n')                  
            ascii_list.append(art_char)
    if prompt_type == 'sep' :
        sep = '*'
    elif prompt_type == 'origin' or prompt_type == 'ict':
        sep = ''
    else :
        raise ValueError('sep or origin')

    rows = len(ascii_list[0]) - 1

    res = [ [] for _ in range(rows)]
    for r in range(rows):
        res[r] = sep.join([ascii_list[i][r] for i in range(len(ascii_list))])
    return '\n'.join(res), rows


    


class vertical_reg():
    # vertical, i.e. one by one
    def __init__(self) -> None:
        pass
            
    def gen_prompt(self, text, font, ps, font_class, ict_size):
        ## sep-no-yes
        ps_list = ps.split('-')

        prompt_type = ps_list[0]
        replace_type = ps_list[1]
        replace_space = ps_list[2]

        string_aat_list = []

        if replace_type == 'no' :
            for char in text :              
                art_char = art.text2art(char, font=font)
                string_aat_list.append(art_char)

        ## replace at head 
        elif replace_type == 'head':

            for char in text :
                idx = 0 #head 
                art_char = art.text2art(char, font=font)
                art_char = replace_by_index(art_char,char,idx,replace_space)                  
                string_aat_list.append(mutator.replace_symbol(art_char))
        
        elif replace_type == 'mid':

            for char in text :
                art_char = art.text2art(char, font=font)
                idx = len(art_char) // 2
                art_char = replace_by_index(art_char,char,idx,replace_space)                  
                string_aat_list.append(mutator.replace_symbol(art_char))                
    
        elif replace_type == 'tail':

            for char in text :
                art_char = art.text2art(char, font=font)
                idx = len(art_char) - 1
                art_char = replace_by_index(art_char,char,idx,replace_space)                  
                string_aat_list.append(mutator.replace_symbol(art_char)) 

        else :  
            raise ValueError("Only head, mid and tail are available")

        if prompt_type == 'sep':
            char_list = []
            sep = '*'*20 + '\n'
            res_string = RegP.v_sep_prompt('*') 
            for s in string_aat_list:
                char_list.append(s)
            res_string += sep.join(char_list)
            res_string += '\n'

        elif prompt_type == 'ict':
            if ict_size == -1:
                res_string = vertical_ict_prompt

            else:
                res_string = gen_same_font_vertical_ict_prompt(font_class, ict_size)
            for s in string_aat_list:
                res_string += f'''{s}\n'''
                
        elif prompt_type == 'origin' : 
            res_string = RegP.origin_long()
            for s in string_aat_list:
                res_string += f'''{s}\n'''

        else :
            raise ValueError("Only sep, origin, ict are available")

        res_string += f"```\n"
    
            
        return res_string
           
    
class horizontal_reg():
    def __init__(self) -> None:
        pass

    def gen_prompt(self, text,font, ps, font_class, ict_size):
        prompt_type = ps.split('-')[0]



        ### prefix 
        if prompt_type == 'sep' :
            ascii_text, row_len = generate_alphabet_ascii_modified(text, font, ps)
            length = len(text)
            sep = "*"
            prefix = RegP.h_sep_prompt(length, row_len, sep)

        elif prompt_type == 'ict':
            if ict_size == -1:
                prefix = horizontal_ict_prompt
            else:
                prefix = gen_same_font_horizontal_ict_prompt(font_class, ict_size)
            ascii_text, row_len = generate_alphabet_ascii_modified(text, font, ps)
        elif prompt_type == 'origin':
            prefix = RegP.origin_long()
            ascii_text, row_len = generate_alphabet_ascii_modified(text, font, ps)
        else: 
            raise NotImplementedError

        return f'''
{prefix}

{ascii_text}

```
'''.strip()


# class vertical_and_horizontal():
#     def __init__(self,mask_type) -> None:
#         self.mask_type = mask_type

#     def gen_prompt(self, masked_instruction, masked_word_list, font, prompt_type, is_replace):
#         word_length_list = []
#         for word in masked_word_list:
#             word_length_list.append(len(word))
        
#         assembel_word = ''.join(masked_word_list)

#         row_len = 0
#         ascii_word_list = []
#         for word in masked_word_list:
#             ascii_word, row_len = generate_alphabet_ascii_modified(word,is_replace, ascii_coding=font)
#             ascii_word_list.append(ascii_word)
       
#         ### add seperator at between words 
#         ascii_text = f'\n{"="*120}\n'.join(ascii_word_list)

#         length = len(assembel_word)
#         sep = "*"
#         ### prefix 
#         prefix = Jbp.hv_prefix(masked_word_list, row_len, sep)
#         suffix = Jbp.hv_suffix_words(masked_word_list,masked_instruction)

#         return f'''
# {prefix}

# {ascii_text}

# {suffix}
# '''.strip()