"""
Tokenizer module for SNOL Interpreter
Contains functions for tokenizing input commands
"""

import re

def tokenize(cmd):
    """Split a command string into tokens, supporting negative numbers"""
    token_pattern = r'\d+\.\d+|\d+|[A-Za-z_][A-Za-z0-9_]*|[()+\-*/%=]'
    tokens = re.findall(token_pattern, cmd)
    result = []
    i = 0
    # Special handling for negative numbers
    while i < len(tokens):
        if tokens[i] == '-' and i + 1 < len(tokens):
            if (i == 0 or tokens[i-1] in ('(', '=', '+', '-', '*', '/', '%')) and re.match(r'^\d+(\.\d+)?$', tokens[i+1]):
                result.append('-' + tokens[i+1])
                i += 2
                continue
        result.append(tokens[i])
        i += 1
    return result