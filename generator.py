"""
Spec - 
top row is column labels
optional weight item to the right of each
anything in brackets should be a column label

TODO:

[rule.ed] produces past tense of a verb at the end of a produced string
[rule.ing] produces gerund of verb at the end of a produced string
[rule.cap] capitalizes the first letter of produced string. All other capitalization left the same

Shouls have compatibility with csv, tsv, xlsx

Completed:

Variables:
[a=rule] defines a variable a to be equal to a random selection from rule.
[a] references variable a again, exactly how it was generated before.

Commands:
[rule.a] puts a or an before a noun at the beginning of a produced string
"""
from random import randint
import re
import sys
import nltk
from nltk.corpus import cmudict

items = [i.split("\t") for i in open(sys.argv[1],'r').read().split("\n")]
items_t = []
for i in range(0,len(items)):
    for j in range(0,len(items[i])):
        if items[i][j]=='':
            continue
        while len(items_t) <= j:
            items_t.append([])
        while len(items_t[j]) <= i:
            items_t[j].append(None)
        items_t[j][i]=items[i][j]
items=items_t

# texts, weights, total weight
grammar = {}

i=0
while i < len(items):
    column = items[i]
    grammar[column[0]]=[column[1:]]
    if i+1 >= len(items) or items[i+1][0]!='weight':
        i+=1
        grammar[column[0]].append([1]*(len(column)-1))
        grammar[column[0]].append(len(column)-1)
        continue
    weight = [int(i) for i in items[i+1][1:] if len(i)>0]
    grammar[column[0]].append(weight)
    grammar[column[0]].append(sum(weight))
    i+=2

def weighted_choice(entry):
    val = randint(0,entry[2]-1)
    sum=0
    for i in range(0,len(entry[1])):
        sum+=entry[1][i]
        if val < sum:
            return entry[0][i]
    return None

try:
    pronunciations = cmudict.dict()
except:
    nltk.download('cmudict')
    pronunciations = cmudict.dict()

exceptions = {"a":set(),"an":set()}

def a_or_an(string):
    if len(string)==0:
        return "a"
    if " " in string:
        word = string[:string.index(" ")-1].lower()
    else:
        word = string.lower()
    # from https://stackoverflow.com/questions/20336524/verify-correct-use-of-a-and-an-in-english-texts-python
    if word in exceptions['a']:
        return 'a'
    if word in exceptions['an']:
        return 'an'
    pron = pronunciations.get(word)
    if pron is None:
        return "an" if word[0] in {'a','e','i','o','u'} else 'a'
    for syllables in pron:
        return "an" if syllables[0][-1].isdigit() else "a"

rule_re = r"\[[^\[\]]*\]"
def generate_text(variables={},from_rule='root'):
    text_value = weighted_choice(grammar[from_rule])
    # print("Initial value:",text_value)
    match = re.search(rule_re,text_value)
    # print(match)
    while match:
        match_text = match.group()[1:len(match.group())-1]
        split_by_equals = match_text.split("=")
        split_by_dot = match_text.split(".")
        commands = []
        if len(split_by_dot)>1:
            match_text = split_by_dot[0]
            commands = split_by_dot[1:]
        span = match.span()
        val = ""
        if len(split_by_equals)==1:
            if match_text in variables:
                # print("Getting value of variable",match_text)
                val = variables[match_text]
            else:
                # print("Generating text for variable",match_text)
                val = generate_text(variables,match_text)
        else:
            # Declare variable
            # print("Declaring variable",split_by_equals,"with value determined by rule",split_by_equals[1])
            val = generate_text(variables,split_by_equals[1])
            variables[split_by_equals[0]]=val
        for command in commands:
            if command=="cap" and len(val) > 0:
                val = val[0].upper() + (val[1:] if len(val)>1 else "")
            if command=="a":
                val = a_or_an(val) + " " + val
        text_value = text_value[:span[0]]+val+text_value[span[1]:]
        match = re.search(rule_re,text_value)
        # print(match)
        # print("New Value: " + text_value)
    text_value = text_value.replace("\\n","\n")
    return text_value

print(generate_text())