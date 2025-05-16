"""
Tokenizer module for SNOL Interpreter
Contains functions for tokenizing input commands
"""

import re

def tokenize(cmd):
    """Split a command string into tokens, supporting negative numbers"""
    # Regex: match negative/positive numbers, operators, or parentheses
    token_pattern = r'-?\d+(?:\.\d+)?|[()+\-*/%=]'
    return re.findall(token_pattern, cmd)