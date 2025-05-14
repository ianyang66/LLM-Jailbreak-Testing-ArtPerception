import re
from collections import Counter
from Levenshtein import distance
none_substring_list =[
    'no letter',
    'none',
    'incorrect',
]

substring_list = [
    "the answer is",
    "the letters in a-z are",
    "your prediction is ",
    "your prediction",
    "the string with letters in a-z is",
    "the string that has letters in a-z is",
    "the string that have letters in a-z are",
    "the identified letters are",
    "string = ",
    "answer = ",
    "the assembled string is",
    "i get",
    "i identify the letters as",
    "the assembled string is",
    "here's the assembled string",
    'the letters are:',
    "result:",
    "the identified letters are",
    "the final string is",
    "the string becomes",
    "form a string",
    "we get",
    "identified letters",
    "identify the letters as follows",
    "here is the assembled string",
    "identified the following letters",
    "the extracted letters are",
    "here are the letters",
    'concatenate them to form the string',
    ' i have the following letters',
    'the string is',
    'after processing all lines, i have a list of letters',
    'after processing all lines, i have',
    "the ascii art represents the string",
    'after following the steps, the letters are concatenated as follows',
    'i have identified the letters in the ascii art as follows', # mixtral
    'the ascii art represents the word',
    #'I have identified each character as follows',
    'I have identified the characters one by one as follows',
    'the concatenated string is',
#    'the letters are concatenated as follows',
    'the concatenated letters from the ascii art are',
    'The resulting string is',
    "I'll represent the assembled string as a list for clarity",
    "The final string is",
    "I predict that the string is",
    "Here is the assembled string"
]


def amr(pred, label):
    pred = pred.lower()
    label = label.lower()
    
    pred_dict = {}
    label_dict = {}
    for c in pred:
        if c not in pred_dict:
            pred_dict[c] = 1
        else:
            pred_dict[c] += 1

    for c in label:
        if c not in label_dict:
            label_dict[c] = 1
        else:
            label_dict[c] += 1

    AMR = 0
    for c in pred_dict:
        if c in label_dict:
            AMR += min(pred_dict[c], label_dict[c])
    assert AMR <= len(label)
    return AMR/len(label)

def parse_resp(resp):
    resp = resp.translate(str.maketrans('', '', "_,\"' -."))
    return resp

def check_substring(raw_res):
    is_match = False
    raw_res = raw_res.lower()
    for tag in substring_list:
        if tag in raw_res:
            raw_res = raw_res[raw_res.rfind(tag)+len(tag):].split('\n')[0]
            is_match =True
    return raw_res.strip(" \n'\"`:."), is_match

def check_fail(resp):
    resp = resp.lower()
    for tag in none_substring_list:
        if tag in resp:
            return True
    return False

def check_repeated_strings(text, threshold=200):

    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    repeated_words = [word for word, count in word_counts.items() if count >= threshold]
    
    if len(repeated_words) > 0:

        return True
    else:
        return False

def check_repeated_punctuation(text, font, threshold=300):

    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'
    if font == 'cards' or font == 'keyboard':
        punctuation = '!"#$%&\'()+,./:;<=>?@[\\]^`{}~'

    punct_counts = Counter(char for char in text if char in punctuation)
    
    repeated_puncts = [p for p, count in punct_counts.items() if count >= threshold]
    
    if repeated_puncts:
        return True
    else:
        return False

def check_repeat(font,resp):
    text = resp[500:]
    if check_repeated_strings(text,50):
        if check_repeated_strings(text[len(text)-200:],20):
                return True
    if check_repeated_punctuation(text,font,100):
        if check_repeated_punctuation(text[len(text)-200:],font,20):
                return True
            
    return False

def eval_res(raw_resp, label, AMR=False,font='cards'):
    global is_match
    resp = raw_resp.lower()
    resp, is_match = check_substring(resp)
    
    if not is_match :

        if AMR:
            return False, 0,'',True, 1
        else:
            return False,'',True, 1
    elif check_fail(resp):
        #print(resp)
        if AMR:
            return False, 0,'',False, 0.5
        else:
            return False,'', False, 0.5
    else:
        answer = parse_resp(resp)
        pred = answer[:len(label)]
        lev_distance = distance(answer[:len(label)*2], label.lower()) / (len(label)*2)
        if AMR:
            return pred == label.lower(), amr(pred, label), answer, False, lev_distance
        else:
            return pred == label.lower(), answer, False, lev_distance 
    