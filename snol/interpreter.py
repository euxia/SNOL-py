"""
Interpreter module for SNOL Interpreter
Contains the main SNOLInterpreter class
"""

from snol.processor import process_command

class SNOLInterpreter:
    def __init__(self):
        # Initialize a dictionary to store variables defined in the interpreter
        self.variables = {}
        # Define a set of reserved keywords for the SNOL language
        self.keywords = {"BEG", "PRINT", "EXIT!"}
        # Define supported operators with their precedence and associativity
        self.ops = {
            '+': (1, 'L'),
            '-': (1, 'L'),
            '*': (2, 'L'),
            '/': (2, 'L'),
            '%': (2, 'L'),
        }

    def process_command(self, command):
        """Process a SNOL command"""
        # Delegate command processing to the external process_command function
        # Pass the current variables, keywords, and operators
        return process_command(command, self.variables, self.keywords, self.ops)

    def run(self):
        """Run the SNOL interpreter"""
        # Print a welcome message to the user
        print("The SNOL environment is now active, you may proceed with giving your commands.")
        while True:
            try:
                # Prompt the user for a command
                cmd = input("Command: ")
                # Process the command; if it returns False, exit the loop
                if not self.process_command(cmd):
                    break
            except (EOFError, KeyboardInterrupt):
                # Handle user interruption (Ctrl+D or Ctrl+C) gracefully
                print("\nInterpreter is now terminated...")
                break
            except Exception as e:
                # Catch and display any unexpected errors
                print(f"SNOL> Internal error: {e}")
