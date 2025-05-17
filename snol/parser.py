"""
Parser module for SNOL Interpreter
Contains functions for parsing tokens into RPN notation
"""

def to_rpn(tokens, ops, is_valid_variable_name_func, is_valid_literal_func, keywords):
    """Convert infix notation to Reverse Polish Notation"""
    out, stack = [], []  # Output list and operator stack
    for tok in tokens:
        # If token is a literal or valid variable name, add to output
        if is_valid_literal_func(tok) or is_valid_variable_name_func(tok, keywords):
            out.append(tok)
        # If token is an operator
        elif tok in ops:
            # While stack is not empty and top of stack is an operator
            while stack and stack[-1] in ops:
                p1, _ = ops[tok]           # Current operator precedence
                p2, assoc = ops[stack[-1]] # Stack top operator precedence and associativity
                # Pop operators from stack to output based on precedence and associativity
                if (assoc == 'L' and p1 <= p2) or (assoc == 'R' and p1 < p2):
                    out.append(stack.pop())
                else:
                    break
            stack.append(tok)  # Push current operator to stack
        # If token is left parenthesis, push to stack
        elif tok == '(':
            stack.append(tok)
        # If token is right parenthesis
        elif tok == ')':
            # Pop operators to output until left parenthesis is found
            while stack and stack[-1] != '(':
                out.append(stack.pop())
            # If no matching left parenthesis, error
            if not stack or stack[-1] != '(':
                print("SNOL> Error! Mismatched parentheses!")
                return None
            stack.pop()  # Remove the left parenthesis
        # If token is unknown, print error and return
        else:
            print(f"SNOL> Unknown word [{tok}]")
            return None
    # After processing all tokens, pop remaining operators to output
    while stack:
        if stack[-1] in ('(', ')'):
            print("SNOL> Error! Mismatched parentheses!")
            return None
        out.append(stack.pop())
    return out
