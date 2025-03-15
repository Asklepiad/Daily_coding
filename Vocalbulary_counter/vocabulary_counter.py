#!/usr/bin/env python

## Importing packages
import os
import argparse
import re
import string
import json

## Reading arguments
parser = argparse.ArgumentParser(\
        prog="Words frequency counter",
        description="Utility for counting the number of unique words or word combinations in the txt file.",
        epilog="Dixi et animam levavi.")

parser.add_argument("-i", "--input_file", type=str, 
        help="Path to input txt file")
parser.add_argument("-o", "--output_file", type=str,
        help="Path to output word frequencies txt file")
parser.add_argument("-b", "--black_list", type=str, nargs='?', default=None,
        help="Path to words black list, which wiil be excluded from the output (json format required)")
parser.add_argument("-r", "--regimen", type=str, nargs='?', default="word",
        help="Regimen of working: 'word' -- for single word frequencies (default), 'k_word' -- for word combinations (word combination separated with whitespaces)")
parser.add_argument("-k", "--k_words", type=int, nargs='?', default=2,
        help="Number of words in the combinations in 'k_word' regimen (default is 2)")

arguments = parser.parse_args()

input_file = arguments.input_file
output_file = arguments.output_file
regimen = arguments.regimen
k_words = arguments.k_words
black_list = arguments.black_list

## Reading file, preparing variables
with open(input_file, "r") as text_file, open(output_file, "w") as voc_file:
    text_string = text_file.read().lower()

    ## Processing
    if regimen == "word":
        match_pattern = re.findall(r'\b[a-z\-0-9]{3,25}\b', text_string)  
        
    elif regimen == "k_word":
        match_pattern = [phrase[0] for phrase in re.findall(r'(([a-z\-0-9]{3,25} ){'+ str(var_num) +'}[a-z\-0-9]{3,25})', text_string)]

    ## Final list creating
    frequency = dict.fromkeys(match_pattern, 0)
    for word in match_pattern:
        frequency[word] += 1
    
    ## Stop-words excluding
    if black_list != None:
        with open(black_list, "r") as black_list_json:
            black_list_words = json.load(black_list_json)
            for stop_word in black_list_words:
                if stop_word in frequency:
                    del frequency[stop_word]


    final_vocalbulary = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

    ## Writing the list into the document
    for word, frequency in final_vocalbulary.items():
        voc_file.write(f"{word}: {frequency}\n")

print("Commander, all words in the documents have just been counted.")
