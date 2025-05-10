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
        """Initialize the SNOL interpreter environment"""
        # Dictionary to store variable names and their values
        self.variables = {}
        # Reserved keywords in the SNOL language
        self.keywords = ["BEG", "PRINT", "EXIT!"]

    def is_valid_variable_name(self, name):
        """Check if a string is a valid variable name according to SNOL rules"""
        # Variable names cannot be keywords and must match the naming pattern
        if name in self.keywords:
            return False
        return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', name))

    def is_defined_variable(self, name):
        """Check if a variable has been defined"""
        return name in self.variables

    def is_integer_literal(self, value):
        """Check if a string represents an integer literal"""
        return bool(re.match(r'^-?\d+$', value))

    def is_float_literal(self, value):
        """Check if a string represents a floating-point literal"""
        return bool(re.match(r'^-?\d+\.\d*$', value))

    def is_valid_literal(self, value):
        """Check if a string represents a valid literal (integer or float)"""
        return self.is_integer_literal(value) or self.is_float_literal(value)

    def parse_literal(self, value):
        """Parse a string into either an integer or a float"""
        if self.is_integer_literal(value):
            return int(value)
        elif self.is_float_literal(value):
            return float(value)
        else:
            return None

    def get_value_type(self, value):
        """Get the type of a value (integer or float)"""
        if isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        else:
            return None

    def tokenize(self, command):
        """Split a command into tokens, preserving operators"""
        # Replace operators with space-padded versions to ensure they're separated
        cmd = command
        for op in ['+', '-', '*', '/', '%', '=']:
            cmd = cmd.replace(op, f" {op} ")
        
        # Split by whitespace and filter out empty tokens
        return [token for token in cmd.split() if token]

    def evaluate_expression(self, expr):
        """Evaluate a SNOL expression and return its value"""
        # Handle simple cases - single variable or literal
        if len(expr) == 1:
            token = expr[0]
            if self.is_valid_literal(token):
                # If it's a literal, parse and return its value
                return self.parse_literal(token)
            elif self.is_valid_variable_name(token):
                # If it's a variable, check if it's defined
                if not self.is_defined_variable(token):
                    print(f"SNOL> Error! [{token}] is not defined!")
                    return None
                return self.variables[token]
            else:
                print(f"SNOL> Unknown word [{token}]")
                return None
                
        # Handle arithmetic operations
        if len(expr) == 3:
            left = expr[0]
            op = expr[1]
            right = expr[2]
            
            # Parse left operand
            if self.is_valid_literal(left):
                left_val = self.parse_literal(left)
            elif self.is_valid_variable_name(left):
                if not self.is_defined_variable(left):
                    print(f"SNOL> Error! [{left}] is not defined!")
                    return None
                left_val = self.variables[left]
            else:
                print(f"SNOL> Unknown word [{left}]")
                return None
                
            # Parse right operand
            if self.is_valid_literal(right):
                right_val = self.parse_literal(right)
            elif self.is_valid_variable_name(right):
                if not self.is_defined_variable(right):
                    print(f"SNOL> Error! [{right}] is not defined!")
                    return None
                right_val = self.variables[right]
            else:
                print(f"SNOL> Unknown word [{right}]")
                return None
                
            # Check if operands are of the same type
            if (isinstance(left_val, int) and isinstance(right_val, float)) or \
               (isinstance(left_val, float) and isinstance(right_val, int)):
                print("SNOL> Error! Operands must be of the same type in an arithmetic operation!")
                return None
                
            # Perform operation based on operator
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                if right_val == 0:
                    print("SNOL> Error! Division by zero!")
                    return None
                # Handle integer division vs float division
                if isinstance(left_val, int) and isinstance(right_val, int):
                    return left_val // right_val
                return left_val / right_val
            elif op == '%':
                if not (isinstance(left_val, int) and isinstance(right_val, int)):
                    print("SNOL> Error! Modulo operation requires integer operands!")
                    return None
                if right_val == 0:
                    print("SNOL> Error! Modulo by zero!")
                    return None
                return left_val % right_val
            else:
                print(f"SNOL> Unknown operator [{op}]")
                return None
        
        # If the expression doesn't match any valid pattern
        print("SNOL> Unknown command! Does not match any valid command of the language.")
        return None

    def process_command(self, command):
        """Process a SNOL command"""
        if not command:
            # Empty command, continue executing
            return True
            
        # Check for exit command
        if command == "EXIT!":
            print("Interpreter is now terminated...")
            return False  # Stop execution
            
        # Tokenize the command into parts
        tokens = self.tokenize(command)
        
        # Handle assignment operation: var = expr
        if len(tokens) >= 3 and tokens[1] == '=':
            var_name = tokens[0]
            
            # Check if variable name is valid
            if not self.is_valid_variable_name(var_name):
                print(f"SNOL> Unknown word [{var_name}]")
                return True
                
            # Evaluate the right side expression
            expr_result = self.evaluate_expression(tokens[2:])
            if expr_result is not None:
                # Store the result in the variable
                self.variables[var_name] = expr_result
            return True
            
        # Handle input operation: BEG var
        if len(tokens) == 2 and tokens[0] == "BEG":
            var_name = tokens[1]
            
            # Check if variable name is valid
            if not self.is_valid_variable_name(var_name):
                print(f"SNOL> Unknown word [{var_name}]")
                return True
                
            # Prompt for input
            print(f"SNOL> Please enter value for [{var_name}]:")
            user_input = input("Input: ")
            
            # Validate input format
            if self.is_integer_literal(user_input):
                self.variables[var_name] = int(user_input)
            elif self.is_float_literal(user_input):
                self.variables[var_name] = float(user_input)
            else:
                print("SNOL> Invalid number format!")
            return True
            
        # Handle output operation: PRINT var or PRINT literal
        if len(tokens) == 2 and tokens[0] == "PRINT":
            target = tokens[1]
            
            if self.is_valid_literal(target):
                # If it's a literal, parse and print its value
                value = self.parse_literal(target)
                print(f"SNOL> {value}")
            elif self.is_valid_variable_name(target):
                # If it's a variable, check if it's defined and print its value
                if not self.is_defined_variable(target):
                    print(f"SNOL> Error! [{target}] is not defined!")
                    return True
                value = self.variables[target]
                print(f"SNOL> [{target}] = {value}")
            else:
                print(f"SNOL> Unknown word [{target}]")
            return True
            
        # Handle arithmetic operations or single expressions
        result = self.evaluate_expression(tokens)
        # No output for successful arithmetic operations
        
        return True

    def run(self):
        """Run the SNOL interpreter environment"""
        print("The SNOL environment is now active, you may proceed with giving your commands.")
        
        running = True
        while running:
            try:
                # Prompt user for a command
                command = input("Command: ")
                # Process the command and determine if the interpreter should continue
                running = self.process_command(command)
            except EOFError:
                # Handle end-of-file (Ctrl+D) gracefully
                print("\nInterpreter is now terminated...")
                break
            except KeyboardInterrupt:
                # Handle keyboard interrupt (Ctrl+C) gracefully
                print("\nInterpreter is now terminated...")
                break
            except Exception as e:
                # Catch and display any unexpected errors
                print(f"SNOL> Internal error: {str(e)}")


if __name__ == "__main__":
    # Create an instance of the interpreter and start it
    interpreter = SNOLInterpreter()
    interpreter.run()