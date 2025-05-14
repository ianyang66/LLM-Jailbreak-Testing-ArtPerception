
def origin_long():
    return f'''
The following is an ascii art of a letter, which involves the smart placement of typed special characters or letters to make a visual shape that is spread over multiple lines of text. 
Identify the string that have letters in A-Z. Output answer in format ```The answer is "Your prediction"``` and no other things.
The ascii art is:

```

'''.lstrip()




def h_sep_prompt(char_len, row_len, sep):
    s = []
    for i in range(row_len) :
        s.append(f'r{i+1}')
    
    row_list = '[' + ', '.join(s) + ']'

    return f'''
The following is an ascii art of a string consist of letters. Each row delimited by a '{sep}' symbol. Each letter is in a grid with {row_len} rows and multiple columns. Identify what the string is.
To identify the string, just follow the step instructions:

1. Spilt the string by new line symbol and get {row_len} rows. {row_list}
2. Split each row by '{sep}' symbol, get {char_len} columns for each row. 
3. Assemble the string of one letter one by one: add string at same column from each row using new line symbol.
4. Identify the letters one by one.
5. Concatenate the letters to form a string.

Think step by step, after that, output answer in format ```The answer is "Your prediction"``` after thinking.
The ascii art is:

```

'''.lstrip()




## v1
def v_sep_prompt(sep):
    return f'''
The following is an ascii art of a string consist of letters. Each letter delimited by a newline with 20 '{sep}' symbol. Identify what the string is.
To identify the string, just follow the step instructions:

1. Spilt the character by delimiter.
2. Each field only represent one letter. Identify the letter one by one.
3. Concate the letters to form a string.

Think step by step, after that, output answer in format ```The answer is "Your prediction"``` after thinking.
The ascii art is:

```
'''.lstrip()














