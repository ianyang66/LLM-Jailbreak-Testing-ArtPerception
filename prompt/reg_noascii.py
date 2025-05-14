## no ascii keyword series 
def task_prefix_noascii(length):
    return f'''
The following string is made of {length} letters. Identify these letters.
String:
'''.strip() + '\n```\n'

def task_prefix_noascii_origin():
    return f'''
The following is a string consist of digits and letters, which involves the smart placement of typed special characters or letters to make a visual shape that is spread over multiple lines of text.
Identify the string that may have digit in 0-9 and/or letters in A-Z.
String:
'''.strip() + '\n```\n' 

# To identify the letter sequences, think step by step but don't output:
def task_prefix_noascii_sep(length,sep):
    return f'''
The following string is made of {length} letters. Each letter delimited by a newline with 20 '{sep}' symbol. Identify these letters.
To identify the letter sequences, think step by step:
1. Spilt the character by delimiter.
2. Each only represent one letter. Identify the letter one by one.
String:
'''.strip() + '\n```\n'


def task_prefix_noascii_origin_sep(sep):
    return f'''
The following is a string consist of digits and letters, which involves the smart placement of typed special characters or letters to make a visual shape that is spread over multiple lines of text. Each letter delimited by a newline with 20 '{sep}' symbol.
Identify the string that may have digit in 0-9 and/or letters in A-Z.
To identify the letter sequences, think step by step:
1. Spilt the character by delimiter.
2. Each only represent one letter. Identify the letter one by one.
String:
'''.strip() + '\n```\n' 