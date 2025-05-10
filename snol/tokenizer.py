"""
Tokenizer module for SNOL Interpreter
Contains functions for tokenizing input commands
"""

def tokenize(cmd):
    """Split a command string into tokens"""
    for op in ['(',')','+','-','*','/','%','=']:
        cmd = cmd.replace(op, f' {op} ')
    return [t for t in cmd.split() if t]
