"""
SNOL Interpreter - Simple Number-Only Language Interpreter
Members:
Natividad, Deniel Dave
Palarpalar, Cherlie Joy
Siosana, Cedric 
Suello, Carl Raymund
"""

import re

class SNOLInterpreter:
    def __init__(self):
        self.variables = {}
        self.keywords = {"BEG", "PRINT", "EXIT!"}
        # operator: (precedence, associativity)
        self.ops = {
            '+': (1, 'L'),
            '-': (1, 'L'),
            '*': (2, 'L'),
            '/': (2, 'L'),
            '%': (2, 'L'),
        }

    def is_valid_variable_name(self, name):
        return bool(re.match(r'^[A-Za-z][A-Za-z0-9]*$', name)) and name not in self.keywords

    def is_integer_literal(self, tok):
        return bool(re.match(r'^-?\d+$', tok))

    def is_float_literal(self, tok):
        return bool(re.match(r'^-?\d+\.\d*$', tok))

    def is_valid_literal(self, tok):
        return self.is_integer_literal(tok) or self.is_float_literal(tok)

    def parse_literal(self, tok):
        if self.is_integer_literal(tok): return int(tok)
        if self.is_float_literal(tok):   return float(tok)
        return None

    def tokenize(self, cmd):
        for op in ['(',')','+','-','*','/','%','=']:
            cmd = cmd.replace(op, f' {op} ')
        return [t for t in cmd.split() if t]

    def to_rpn(self, tokens):
        out, stack = [], []
        for tok in tokens:
            if self.is_valid_literal(tok) or self.is_valid_variable_name(tok):
                out.append(tok)
            elif tok in self.ops:
                while stack and stack[-1] in self.ops:
                    p1,_ = self.ops[tok]
                    p2,assoc = self.ops[stack[-1]]
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

    def eval_rpn(self, rpn):
        st = []
        for tok in rpn:
            if tok in self.ops:
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
                if self.is_valid_literal(tok):
                    val = self.parse_literal(tok)
                else:
                    if not self.is_valid_variable_name(tok):
                        print(f"SNOL> Error! [{tok}] is not a valid variable name.")
                        return None
                    if tok not in self.variables:
                        print(f"SNOL> Error! [{tok}] is not defined!")
                        return None
                    val = self.variables[tok]
                st.append(val)

        # **NEW**: if there isn't exactly one item left, it's a syntax error
        if len(st) != 1:
            print("SNOL> Unknown command! Does not match any valid command of the language.")
            return None

        return st[0]

    def evaluate_expression(self, tokens):
        rpn = self.to_rpn(tokens)
        if rpn is None:
            return None
        return self.eval_rpn(rpn)

    def process_command(self, command):
        cmd = command.strip()
        if not cmd:
            return True
        if cmd == "EXIT!":
            print("Interpreter is now terminated...")
            return False

        tokens = self.tokenize(cmd)

        # Assignment
        if len(tokens) >= 3 and tokens[1] == '=':
            var = tokens[0]
            if not self.is_valid_variable_name(var):
                print(f"SNOL> Error! [{var}] is not a valid variable name.")
                return True
            val = self.evaluate_expression(tokens[2:])
            if val is not None:
                self.variables[var] = val
            return True

        # Input
        if tokens[0] == "BEG" and len(tokens) == 2:
            var = tokens[1]
            if not self.is_valid_variable_name(var):
                print(f"SNOL> Error! [{var}] is not a valid variable name.")
                return True
            print(f"SNOL> Please enter value for [{var}]:")
            ui = input("Input: ")
            if self.is_integer_literal(ui):
                self.variables[var] = int(ui)
            elif self.is_float_literal(ui):
                self.variables[var] = float(ui)
            else:
                print("SNOL> Invalid number format!")
            return True

        # Print
        if tokens[0] == "PRINT" and len(tokens) == 2:
            tgt = tokens[1]
            if self.is_valid_literal(tgt):
                print(f"SNOL> {self.parse_literal(tgt)}")
            elif self.is_valid_variable_name(tgt):
                if tgt not in self.variables:
                    print(f"SNOL> Error! [{tgt}] is not defined!")
                else:
                    print(f"SNOL> [{tgt}] = {self.variables[tgt]}")
            else:
                print(f"SNOL> Unknown word [{tgt}]")
            return True

        # Stand-alone expression
        _ = self.evaluate_expression(tokens)
        return True

    def run(self):
        print("The SNOL environment is now active, you may proceed with giving your commands.")
        while True:
            try:
                cmd = input("Command: ")
                if not self.process_command(cmd):
                    break
            except (EOFError, KeyboardInterrupt):
                print("\nInterpreter is now terminated...")
                break
            except Exception as e:
                print(f"SNOL> Internal error: {e}")


if __name__ == "__main__":
    SNOLInterpreter().run()
