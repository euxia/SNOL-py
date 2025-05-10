"""
Parser module for SNOL Interpreter
Contains functions for parsing tokens into RPN notation
"""

from snol.validators import is_valid_literal, is_valid_variable_name

def to_rpn(tokens, ops, is_valid_variable_name_func, is_valid_literal_func, keywords):
    """Convert infix notation to Reverse Polish Notation"""
    out, stack = [], []
    for tok in tokens:
        if is_valid_literal_func(tok) or is_valid_variable_name_func(tok, keywords):
            out.append(tok)
        elif tok in ops:
            while stack and stack[-1] in ops:
                p1,_ = ops[tok]
                p2,assoc = ops[stack[-1]]
                if (assoc=='L' and p1<=p2) or (assoc=='R' and p1<p2):
                    out.append(stack.pop())
                else:
                    break
            stack.append(tok)
        elif tok=='(':
            stack.append(tok)
        elif tok==')':
            while stack and stack[-1]!='(':
                out.append(stack.pop())
            if not stack or stack[-1]!='(':
                print("SNOL> Error! Mismatched parentheses!")
                return None
            stack.pop()
        else:
            print(f"SNOL> Unknown word [{tok}]")
            return None
    while stack:
        if stack[-1] in ('(',')'):
            print("SNOL> Error! Mismatched parentheses!")
            return None
        out.append(stack.pop())
    return out
