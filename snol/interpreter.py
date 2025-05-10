"""
Interpreter module for SNOL Interpreter
Contains the main SNOLInterpreter class
"""

from snol.processor import process_command

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

    def process_command(self, command):
        """Process a SNOL command"""
        return process_command(command, self.variables, self.keywords, self.ops)

    def run(self):
        """Run the SNOL interpreter"""
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
