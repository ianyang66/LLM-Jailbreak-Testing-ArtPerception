def replace_regardless_case(ins, word, mask):
    index = ins.lower().find(word.lower())
    new_ins = ins[:index] + mask + ins[index+len(word):]
    return new_ins


class Mask_handler:
    def __init__(self) -> None:
        pass

    def word_masker(self,instruction, mask_word_list):
        ins = instruction
        for i, mask_word in enumerate(mask_word_list):
            mask = f'[MASK{i+1}]'
            ins = replace_regardless_case(ins,mask_word,mask)
        
        #word = ''.join(mask_word_list)

        return ins
    
    def char_masker(self,instruction, mask_word_list):
        ins = instruction
        count = 0 
        for mask_word in mask_word_list:
            s = ''
            length = len(mask_word)
            for i in range(length):
                #s += f'[{count+i+1}]'
                s += f'[MASK]'
                
            ins = ins.replace(mask_word,s, 1)
            count += length

        #word = ''.join(mask_word_list)

        return ins




