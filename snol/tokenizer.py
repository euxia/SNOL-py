"""
Tokenizer module for SNOL Interpreter
Contains functions for tokenizing input commands
"""

import re

def tokenize(cmd):
    # Regex: match negative/positive integers/floats, operators, or parentheses
    token_pattern = r'-?\d+\.\d+|-?\d+|[()+\-*/%=]|[A-Za-z][A-Za-z0-9]*'
    return re.findall(token_pattern, cmd)