# SNOL Interpreter - README

## Overview
SNOL (Simple Number-Only Language) is a custom programming language that handles integer and real values, operations, and expressions. This interpreter implements the SNOL language according to the provided specifications.

## Code Structure

Several modules based on functionality:

1. **snol/init.py**: Defines the package and exports the main class
2. **snol/validators.py**: Contains functions for validating variable names and literals
3. **snol/tokenizer.py**: Handles tokenizing input commands
4. **snol/parser.py**: Converts tokens to Reverse Polish Notation
5. **snol/evaluator.py**: Evaluates RPN expressions
6. **snol/processor.py**: Processes SNOL commands
7. **snol/interpreter.py**: Contains the main SNOLInterpreter class
8. **main.py**: Entry point that imports and runs the interpreter

## Setup Instructions

### Prerequisites
- Python 3.x installed on your system
- PyInstaller (only needed for creating the executable)

### Creating the Executable

1. **Install PyInstaller**
   ```
   pip install pyinstaller
   ```

2. **Create the executable**
   ```
   pyinstaller --onefile snol_interpreter.py
   ```

3. **Locate your executable**
   - The executable will be in the `dist` folder
   - Windows: `dist\snol_interpreter.exe`
   - macOS/Linux: `dist/snol_interpreter`

### Rebuilding After Changes

If you make changes to the Python source code:

1. **Rebuild the executable: Just do this**:
   ```
   pyinstaller --onefile snol_interpreter.py
   ```

2. **Clean previous build: It it causes problems** (optional):
   ```
   # Windows
   rmdir /s /q build dist
   del snol_interpreter.spec

## Using the SNOL Interpreter

### Running the Interpreter
- **Windows**: Double-click on `snol_interpreter.exe` or run it from the command line

### SNOL Commands

1. **Assignment Operation**:
   - Syntax: `var = expr`
   - Example: `num = 5` or `result = 2 + 3`
   - Purpose: Assigns the value of an expression to a variable

2. **Input Operation**:
   - Syntax: `BEG var`
   - Example: `BEG num`
   - Purpose: Reads a value from user input and stores it in the specified variable

3. **Output Operation**:
   - Syntax: `PRINT out`
   - Example: `PRINT num` or `PRINT 42`
   - Purpose: Displays the value of a variable or literal

4. **Arithmetic Operations**:
   - Addition: `expr1 + expr2` (Example: `5 + 3` or `num + 2`)
   - Subtraction: `expr1 - expr2` (Example: `5 - 3` or `num - 2`)
   - Multiplication: `expr1 * expr2` (Example: `5 * 3` or `num * 2`)
   - Division: `expr1 / expr2` (Example: `6 / 3` or `num / 2`)
   - Modulo: `expr1 % expr2` (Example: `7 % 3` or `num % 2`)
   - Note: Arithmetic operations can be used as standalone commands or as part of an expression

5. **Exit Operation**:
   - Syntax: `EXIT!`
   - Purpose: Terminates the interpreter

### Example Session

```
The SNOL environment is now active, you may proceed with giving your commands.
Command: num = 10
Command: PRINT num
SNOL> [num] = 10
Command: BEG x
SNOL> Please enter value for [x]:
Input: 5
Command: result = num + x
Command: PRINT result
SNOL> [result] = 15
Command: EXIT!
Interpreter is now terminated...
```

## Language Rules

1. **Variables**:
   - Must start with a letter followed by letters or digits
   - Must be defined (through assignment or input) before use
   - No explicit type declaration; type is determined by the assigned value

2. **Data Types**:
   - Integer: Examples: `0`, `42`, `-7`
   - Floating-point: Examples: `3.14`, `-0.5`, `1.0`

3. **Type Constraints**:
   - Operands in arithmetic operations must be of the same type
   - Modulo operation requires integer operands

4. **Errors**:
   - Undefined variables
   - Type mismatches in operations
   - Invalid number formats
   - Unknown commands
   - Division by zero

## Troubleshooting

- If the executable doesn't run, ensure Python is properly installed
- If commands aren't recognized, check syntax according to SNOL specifications
- For any internal errors, check the error message for details

## Additional Notes

- The interpreter is case-sensitive
- Whitespace is used to separate tokens but is otherwise irrelevant
- Keywords (BEG, PRINT, EXIT!) cannot be used as variable names