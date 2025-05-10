"""
Validators module for SNOL Interpreter
Contains functions for validating variable names, literals, etc.
"""

import re

def is_valid_variable_name(name, keywords):
    """Check if a string is a valid variable name"""
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9]*$', name)) and name not in keywords

def is_integer_literal(tok):
    """Check if a string is an integer literal"""
    return bool(re.match(r'^-?\d+$', tok))

def is_float_literal(tok):
    """Check if a string is a float literal"""
    return bool(re.match(r'^-?\d+\.\d*$', tok))

def is_valid_literal(tok):
    """Check if a string is a valid numeric literal"""
    return is_integer_literal(tok) or is_float_literal(tok)

def parse_literal(tok):
    """Parse a string into an integer or float"""
    if is_integer_literal(tok): return int(tok)
    if is_float_literal(tok):   return float(tok)
    return None
