import art
from tqdm.contrib import tzip
ict_font = [
    'smkeyboard', ## ssl
    'roman',  ## hybrid
    'alphabet', ## letter
    'doom', ## MS
    'fbr_stri', ## ss
    'dotmatrix' # SCS
]
ict_font_class = {
    'SSL' : 'smkeyboard', ## ssl
    'hybrid' : 'roman',  ## hybrid
    'letter' : 'alphabet', ## letter
    'MS' : 'doom', ## MS
    'SS' : 'fbr_stri', ## ss
    'SCS' :'dotmatrix' # SCS
}
texts = [
    "AHYR",
    "BIEP",
    "MQZX",
    "SLFN",
    "CDKV",
    "TJGW"
]


answer_prefix = "The answer is"
prompt_prefix = "The following is an ascii art of a letter, which involves the smart placement of typed special characters or letters to make a visual shape that is spread over multiple lines of text.\n"
prompt_sufix = 'Identify the string that have letters in A-Z. Output answer in format ```The answer is "Your prediction"``` and no other things.\nThe ascii art is:\n\n```\n'

def gen_horizontal_ict_prompt():
    prompt = "Below are some example of ASCII art and its answer:\n\n"
    idx = 1
    
    for font, text in tzip(ict_font, texts):
        p = f'Example {idx}: \n\n'
        p += "```\n"
        p += art.text2art(text,font)
        p += "\n```\n"
        p += f'{answer_prefix} {text}.\n'
        p += '\n' + '=' * 20 + '\n\n'
        idx += 1
        prompt += p

    return prompt_prefix + prompt + prompt_sufix


def gen_vertical_ict_prompt():
    prompt = "Below are some example of ASCII art and its answer:\n\n"
    idx = 1

    for font, text in tzip(ict_font, texts):
        p = f'Example {idx}: \n\n'
        p += "```\n"
        for c in text:
            p += art.text2art(c,font)
            p += '\n'
        p += "\n```\n"
        p += f'{answer_prefix} {text}.\n'
        p += '\n' + '=' * 20 + '\n\n'
        idx += 1
        prompt += p
    
    return prompt_prefix + prompt + prompt_sufix

def gen_same_font_horizontal_ict_prompt(font_class, size):
    prompt = "Below are some example of ASCII art and its answer:\n\n"
    idx = 1
    font = ict_font_class[font_class]
    for i in range(size):
        p = f'Example {idx}: \n\n'
        p += "```\n"
        p += art.text2art(texts[i],font)
        p += "\n```\n"
        p += f'{answer_prefix} {texts[i]}.\n'
        p += '\n' + '=' * 20 + '\n\n'
        idx += 1
        prompt += p

    return prompt_prefix + prompt + prompt_sufix

def gen_same_font_vertical_ict_prompt(font_class, size):
    prompt = "Below are some example of ASCII art and its answer:\n\n"
    idx = 1
    font = ict_font_class[font_class]
    for i in range(size):
        p = f'Example {idx}: \n\n'
        p += "```\n"
        for c in texts[i]:
            p += art.text2art(c,font)
            p += '\n'
        p += "\n```\n"
        p += f'{answer_prefix} {texts[i]}.\n'
        p += '\n' + '=' * 20 + '\n\n'
        idx += 1
        prompt += p

    return prompt_prefix + prompt + prompt_sufix


horizontal_ict_prompt = gen_horizontal_ict_prompt()
vertical_ict_prompt = gen_vertical_ict_prompt()