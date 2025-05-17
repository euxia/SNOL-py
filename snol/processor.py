"""
Processor module for SNOL Interpreter
Contains functions for processing SNOL commands
"""

from snol.validators import is_valid_variable_name, is_valid_literal, parse_literal
from snol.tokenizer import tokenize
from snol.parser import to_rpn
from snol.evaluator import eval_rpn

def evaluate_expression(tokens, ops, variables, keywords):
    """
    Evaluate an expression from tokens.
    Converts tokens to Reverse Polish Notation (RPN) and evaluates the result.
    Returns the evaluated value or None if invalid.
    """
    rpn = to_rpn(tokens, ops, is_valid_variable_name, is_valid_literal, keywords)
    if rpn is None:
        return None
    return eval_rpn(rpn, ops, variables, is_valid_literal, is_valid_variable_name, parse_literal)

def process_command(command, variables, keywords, ops):
    """
    Process a SNOL command.
    Handles assignment, input, print, and expression evaluation.
    Returns False to terminate, True to continue.
    """
    cmd = command.strip()  # Remove leading/trailing whitespace
    if not cmd:
        return True  # Ignore empty commands
    if cmd == "EXIT!":
        print("Interpreter is now terminated...")
        return False  # Signal to terminate interpreter

    tokens = tokenize(cmd)  # Tokenize the command string

    # Assignment: e.g., X = 5
    if len(tokens) >= 3 and tokens[1] == '=':
        var = tokens[0]
        # Validate variable name
        if not is_valid_variable_name(var, keywords):
            print(f"SNOL> Error! [{var}] is not a valid variable name.")
            return True
        # Evaluate the right-hand side expression
        val = evaluate_expression(tokens[2:], ops, variables, keywords)
        if val is not None:
            variables[var] = val  # Assign value to variable
        return True

    # Input: e.g., BEG X
    if tokens[0] == "BEG" and len(tokens) == 2:
        var = tokens[1]
        # Validate variable name
        if not is_valid_variable_name(var, keywords):
            print(f"SNOL> Error! [{var}] is not a valid variable name.")
            return True
        print(f"SNOL> Please enter value for [{var}]:")
        ui = input("Input: ")  # Prompt user for input
        if is_valid_literal(ui):
            variables[var] = parse_literal(ui)  # Store parsed value
        else:
            print("SNOL> Invalid number format!")
        return True

    # Print: e.g., PRINT X or PRINT 5
    if tokens[0] == "PRINT" and len(tokens) == 2:
        tgt = tokens[1]
        if is_valid_literal(tgt):
            print(f"SNOL> {parse_literal(tgt)}")  # Print literal value
        elif is_valid_variable_name(tgt, keywords):
            if tgt not in variables:
                print(f"SNOL> Error! [{tgt}] is not defined!")
            else:
                print(f"SNOL> [{tgt}] = {variables[tgt]}")  # Print variable value
        else:
            print(f"SNOL> Unknown word [{tgt}]")
        return True

    # Stand-alone expression: evaluate but do not assign or print
    _ = evaluate_expression(tokens, ops, variables, keywords)
    return True
