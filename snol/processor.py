"""
Processor module for SNOL Interpreter
Contains functions for processing SNOL commands
"""

from snol.validators import is_valid_variable_name, is_valid_literal, parse_literal
from snol.tokenizer import tokenize
from snol.parser import to_rpn
from snol.evaluator import eval_rpn

def evaluate_expression(tokens, ops, variables, keywords):
    """Evaluate an expression from tokens"""
    rpn = to_rpn(tokens, ops, is_valid_variable_name, is_valid_literal, keywords)
    if rpn is None:
        return None
    return eval_rpn(rpn, ops, variables, is_valid_literal, is_valid_variable_name, parse_literal)

def process_command(command, variables, keywords, ops):
    """Process a SNOL command"""
    cmd = command.strip()
    if not cmd:
        return True
    if cmd == "EXIT!":
        print("Interpreter is now terminated...")
        return False

    tokens = tokenize(cmd)

    # Assignment
    if len(tokens) >= 3 and tokens[1] == '=':
        var = tokens[0]
        if not is_valid_variable_name(var, keywords):
            print(f"SNOL> Unknown word [{var}]")
            return True
        val = evaluate_expression(tokens[2:], ops, variables, keywords)
        if val is not None:
            variables[var] = val
        return True

    # Input
    if tokens[0] == "BEG" and len(tokens) == 2:
        var = tokens[1]
        if not is_valid_variable_name(var, keywords):
            print(f"SNOL> Unknown word [{var}]")
            return True
        print(f"SNOL> Please enter value for [{var}]:")
        ui = input("Input: ")
        if is_valid_literal(ui):
            variables[var] = parse_literal(ui)
        else:
            print("SNOL> Invalid number format!")
        return True

    # Print
    if tokens[0] == "PRINT" and len(tokens) == 2:
        tgt = tokens[1]
        if is_valid_literal(tgt):
            print(f"SNOL> {parse_literal(tgt)}")
        elif is_valid_variable_name(tgt, keywords):
            if tgt not in variables:
                print(f"SNOL> Error! [{tgt}] is not defined!")
            else:
                print(f"SNOL> [{tgt}] = {variables[tgt]}")
        else:
            print(f"SNOL> Unknown word [{tgt}]")
        return True

    # Stand-alone expression
    _ = evaluate_expression(tokens, ops, variables, keywords)
    return True
