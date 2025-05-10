"""
Evaluator module for SNOL Interpreter
Contains functions for evaluating RPN expressions
"""

from snol.validators import is_valid_literal, is_valid_variable_name, parse_literal

def eval_rpn(rpn, ops, variables, is_valid_literal_func, is_valid_variable_name_func, parse_literal_func):
    """Evaluate a Reverse Polish Notation expression"""
    st = []
    for tok in rpn:
        if tok in ops:
            if len(st) < 2:
                print("SNOL> Unknown command! Does not match any valid command of the language.")
                return None
            b = st.pop(); a = st.pop()
            # type check
            if (isinstance(a,int) and isinstance(b,float)) or (isinstance(a,float) and isinstance(b,int)):
                print("SNOL> Error! Operands must be of the same type in an arithmetic operation!")
                return None
            if tok == '+':   res = a + b
            elif tok == '-': res = a - b
            elif tok == '*': res = a * b
            elif tok == '/':
                if b == 0:
                    print("SNOL> Error! Division by zero!")
                    return None
                res = a//b if isinstance(a,int) and isinstance(b,int) else a/b
            elif tok == '%':
                if not isinstance(a,int) or not isinstance(b,int):
                    print("SNOL> Error! Modulo operation requires integer operands!")
                    return None
                if b == 0:
                    print("SNOL> Error! Modulo by zero!")
                    return None
                res = a % b
            st.append(res)
        else:
            # literal or variable
            if is_valid_literal_func(tok):
                val = parse_literal_func(tok)
            else:
                if not is_valid_variable_name_func(tok, {}):  # Empty set for keywords check here
                    print(f"SNOL> Error! [{tok}] is not a valid variable name.")
                    return None
                if tok not in variables:
                    print(f"SNOL> Error! [{tok}] is not defined!")
                    return None
                val = variables[tok]
            st.append(val)

    # if there isn't exactly one item left, it's a syntax error
    if len(st) != 1:
        print("SNOL> Unknown command! Does not match any valid command of the language.")
        return None

    return st[0]
