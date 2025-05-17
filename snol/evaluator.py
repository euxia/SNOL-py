"""
Evaluator module for SNOL Interpreter
Contains functions for evaluating RPN expressions
"""


def eval_rpn(rpn, ops, variables, is_valid_literal_func, is_valid_variable_name_func, parse_literal_func):
    """Evaluate a Reverse Polish Notation expression"""
    st = []  # Stack to hold operands and intermediate results
    for tok in rpn:
        if tok in ops:
            # If token is an operator, pop two operands from the stack
            if len(st) < 2:
                print("SNOL> Unknown command! Does not match any valid command of the language.")
                return None
            b = st.pop(); a = st.pop()
            # Type check: operands must be of the same type (int or float)
            if (isinstance(a,int) and isinstance(b,float)) or (isinstance(a,float) and isinstance(b,int)):
                print("SNOL> Error! Operands must be of the same type in an arithmetic operation!")
                return None
            # Perform the operation based on the operator
            if tok == '+':   res = a + b
            elif tok == '-': res = a - b
            elif tok == '*': res = a * b
            elif tok == '/':
                # Division by zero check
                if b == 0:
                    print("SNOL> Error! Division by zero!")
                    return None
                # Integer division if both operands are int, else float division
                res = a//b if isinstance(a,int) and isinstance(b,int) else a/b
            elif tok == '%':
                # Modulo operation requires integer operands
                if not isinstance(a,int) or not isinstance(b,int):
                    print("SNOL> Error! Modulo operation requires integer operands!")
                    return None
                if b == 0:
                    print("SNOL> Error! Modulo by zero!")
                    return None
                res = a % b
            st.append(res)  # Push result back onto the stack
        else:
            # Token is either a literal or a variable
            if is_valid_literal_func(tok):
                val = parse_literal_func(tok)  # Parse literal value
            else:
                # Validate variable name
                if not is_valid_variable_name_func(tok, {}):  # Empty set for keywords check here
                    print(f"SNOL> Error! [{tok}] is not a valid variable name.")
                    return None
                # Check if variable is defined
                if tok not in variables:
                    print(f"SNOL> Error! [{tok}] is not defined!")
                    return None
                val = variables[tok]  # Get variable value
            st.append(val)  # Push value onto the stack

    # After processing all tokens, there should be exactly one result on the stack
    if len(st) != 1:
        print("SNOL> Unknown command! Does not match any valid command of the language.")
        return None

    return st[0]  # Return the final result
