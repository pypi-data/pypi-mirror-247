
# Basic Calculator

A basic Python class for arithmetic calculations. `Calculator` performs simple arithmetic calculations:
- Addition / Subtraction
- Multiplication / Division
- Take (n) root of a number.

## Installation
You can incorporate the Calculator class into your Python project by importing it :

## Installation

You can incorporate the `Calculator` class into your Python project by importing it :

```bash
  pip install calculator_linpel_calc
```
    
## Usage/Examples
### Setting up a calculator
To set up `Calculator` calss by importing `Calculator` from `calculator_linpel_calc` and creating an instance.
```python
from Calculator.Calculator import Calculator

# Creata an instance of the Calculator
calculator = Calculator()
```
### Executing Calculator operations
The `Calculator` class able is able to perform calculations:
- `Addition(*arg: float)`: Sum numbers.
- `Subtraction(*arg: float)`: Subtract numbers.
- `Multiplication(*arg: float)`: Multiply numbers together.
- `Division(*arg: float)`: Divide numbers.
- `Root(nth_root: float, number: float)`: Take nth root of number.
Example of Usage
```python
calculator = Calculator()

calculator.Addition(1, 2, 3)    # Adds 1, 2, 3, result: 6.0
calculator.Subtraction(1, 2, 3) # Subracts 1, 2, 3 from self.memory = 0, result: -6.0
calculator.Multiplication(7, 3) # Multiplies 7 by 3, result: 21.0
calculator.Division(9, 3)       # Divides 9 by 3, result: 3.0
calculator.Root(2, 9)           # Takes n-th root (2) of 9, result: 3.0
```
### Error Handling
The `Calculator` class raises a `ZeroDivisionError` when attempting to divide by zero, or 0 root calculations.
### License
This code is released under the [MIT License](https://opensource.org/license/mit/)