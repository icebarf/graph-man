#    Graph-man : Plots equations and functions on a graph
#    Copyright (C) 2022 Amritpal Singh
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import matplotlib.pyplot
import re
import math
import numpy

def print_input_format():
    print("Quadratic: ax^2 + bx + c")
    print("Linear: bx +c")
    print("\twhere a,b,c are any integer values")

def help():
    print("\nHow to use this tool")
    print("This tool supports different types of equations and functions to be plotted")
    print("""
|__
|  Quadratic - ax^2 + bc + c for all a,b,c belonging to (-∞, ∞)
|__
|  Linear - bx + c for all b,c belonging to (-∞, ∞)
|__
   Trigonometric functions - sin(x), cos(x), tan(x) - x belongs to 0 to 4π

You can plot a single or multiple equations on the graph. Multiple equations should be separated by the pipe (|) symbol.
Multiple Quadratic or Linear equations can be plotted however they cannot be mixed

Single trigonometric functions are supported only.

examples:

> Input: 5x^2 - 12x + 5
> Input: -7x^2 + 5x - 5 | 13x^2 + 3x - 4
> Input: 40x - 100
> Input: 5x - 12 | 32x - 5
> Input: sin()
> Input: cos()
> Input: tan()

'scale' option is the value for upto the values of 'x' in the equation will be generated. Its the maximum.
Default: 10

'base' option is the value from where the values of 'x' start generating. It is the bare minimum 
Default: 0

'gap' option is the value for the difference between the steps of base and scale.
Default: 1

The scale for quadratic and linear functions can be configured as following:
> Input: scale=n
> Input: base=n
> Input: gap=n

where n is some integer

Visit github for more info: https://github.com/icebarf/graph-man\n
""")

def report_bad_format(str):
    print()
    print(str,'\nType \'help\' for help')
    get_input()

color_table = ["#61afef","#be5046","#98c379","#d19a66","#c678dd","#56b6c2","#abb2bf"]
tbl_len = len(color_table)

# Configurable values
scale = 10
base = 0
gap = 1


# Settings function
def configure(input_string):
    global scale
    global base
    global gap

    input_string = str(input_string)
    if input_string.__contains__("scale"):
        scale = int(re.search(r'-?\d+', input_string).group())
        print("Set scale to:",scale)
    
    if input_string.__contains__("base"):
        base = int(re.search(r'-?\d+', input_string).group())
        print("Set scale to:",base)
    
    if input_string.__contains__("gap"):
        gap = int(re.search(r'-?\d+', input_string).group())
        print("Set scale to:",gap)


# Plotting function
def plot(x,y,input_string):    
    if input_string == "sin()":
        matplotlib.pyplot.plot(x,y,color=color_table[-2])
        return
    if input_string == "cos()":
        matplotlib.pyplot.plot(x,y,color=color_table[-3])
        return
    if input_string == "tan()":
        matplotlib.pyplot.plot(x,y,color=color_table[-4])
        return
    if input_string == "cosec()":
        matplotlib.pyplot.plot(x,y,color=color_table[0])
        return
    if input_string == "sec()":
        matplotlib.pyplot.plot(x,y,color=color_table[1])
        return
    if input_string == "cot()":
        matplotlib.pyplot.plot(x,y,color=color_table[2])
        return
    
    # Plot quadratic or linear equations
    colc = 0
    for yval in y:
        if (colc >= tbl_len):
            colc = 0

        matplotlib.pyplot.plot(x,yval,color=color_table[colc]) # Color code is blue - from OneDarkPro Color Scheme
        colc = colc + 1

def print_graph(x, y, input_string):
    matplotlib.pyplot.xlabel("x")
    matplotlib.pyplot.ylabel("f(x)")
    matplotlib.pyplot.title(("f(x) =" + input_string))    
    
    plot(x,y,input_string)

    obj = matplotlib.pyplot.gca()
    obj.set_facecolor("#282c34") # Grey background color - from OneDarkPro Color Scheme

    matplotlib.pyplot.show()

# Calculation functions

def do_quadratic(digits,input_string):
    y_ = []
    y_.append([])
    x = [z for z in range(base,scale,gap)]

    for val in range(0,len(digits)):
        for idx in x:
            y_[val].append(digits[val][0] * math.pow(idx,2) + digits[val][1] * idx + digits[val][2])
        y_.append([])

    y = [lst for lst in y_ if bool(lst)]

    print_graph(x,y,input_string)
    
# does the same thing as above except without ax^2
def do_linear(digits, input_string):
    y_ = []
    y_.append([])
    x = [z for z in range(base,scale,gap)]

    for val in range(0,len(digits)):
        for idx in x:
            y_[val].append(digits[val][0] * idx + digits[val][1])
        y_.append([])

    y = [lst for lst in y_ if bool(lst)]

    print_graph(x,y,input_string)


# String modification and list creation

# takes a string and strips away numbers from it
# stores them in a list of list, lists createed per equations
def get_digits_from_str(numbers):
    digits= []
    count = 0

    for dig in numbers.split():
        if (count == 0):
            digits.append([])
        if dig == '|':
            digits.append([])
            count = count + 1
            continue
        digits[count].append(int(dig))
    
    return digits

# This function strips away a,b,c from ax^2 + bx + c type string and stores them in a list
def separate_eqn_to_digits(input_string):    
    numbers = ""

    # Split input string - and iterate over each token
    for word in input_string.split():        
    
        # enumerate each token character by character
        for idx,ch in enumerate(word):
    
            # Place separator in string and continue
            if ch == '|':
                numbers = numbers + str(ch)
                continue
            # Skip over these characters
            if ch == 'x' or ch == '^' or (ch == '2' and input_string[idx-1] == '^') or ch == '+':
                continue
            # Put numbers in string
            numbers = numbers + str(ch)
        
        # Handles the '-' sign when for "- c" when input is "ax^2 (+-) bx - c"
        if (numbers[len(numbers)-1] == '-'):
            continue
        # Put space after reading one number (not after the negaitve sign)
        numbers = numbers + ' '

    return get_digits_from_str(numbers)

# This function strips away b,c from bx + c type string and stores them in a list
# Performs same operation as above but does not handle "ax^2"
def separate_lin_to_digits(input_string):
    numbers = ""
    for word in input_string.split():
        for idx, ch in enumerate(word):
            if ch == '|':
                numbers = numbers + str(ch)
                continue
            if ch == 'x' or ch == '+':
                continue
            numbers = numbers + str(ch)

        if numbers[len(numbers)-1] == '-':
            continue
        numbers = numbers + ' '

    return get_digits_from_str(numbers)


# Trigonometric Functions and the like

# Computes x and y values for sin
def sin(input_string):
    x = numpy.arange(0,4*numpy.pi,0.1)
    y = numpy.sin(x)
    print_graph(x,y,input_string)

# Computes x and y values for cos
def cos(input_string):
    x = numpy.arange(0,4*numpy.pi,0.1)
    y = numpy.cos(x)
    print_graph(x,y,input_string)

# Computes x and y values for tan
def tan(input_string):
    x = numpy.arange(0,4*numpy.pi,0.1)
    y = numpy.tan(x)
    print_graph(x,y,input_string)
    
# Computes x and y values for cosec
def cosec(input_string):
    x = numpy.arange(0,4*numpy.pi,0.1)
    y = 1/numpy.sin(x)
    print_graph(x,y,input_string)

# Computes x and y values for sec
def sec(input_string):
    x = numpy.arange(0,4*numpy.pi,0.1)
    y = 1/numpy.cos(x)
    print_graph(x,y,input_string)

# Computes x and y values for cot
def cot(input_string):
    x = numpy.arange(0,4*numpy.pi,0.1)
    y = numpy.tan(x)
    print_graph(x,y,input_string)

# Calls respective trigonometric function based on input
def trig_fun(input_string):
    if (input_string == "sin()"):
        sin(input_string)
    if (input_string == "cos()"):
        cos(input_string)
    if (input_string == "tan()"):
        tan(input_string)
    if (input_string == "cosec()"):
        cosec(input_string)
    if (input_string == "sec()"):
        sec(input_string)
    if (input_string == "cot()"):
        cot(input_string)

# Main program - REPL based
# Read - Evaluate - Print Loop
# In this case, Get input and parse - Calculate, Plot graph Loop 

# Parses input with regex and then does respective operations
def parse_input(input_string):
    # Remove any spaces from left or right
    input_string = input_string.strip()

    # Regular expressions for different commands
    # If these seem gibberish to you then visit https://regex101.com/
    parser_quadratic    = re.compile(r"^( ?-?\d+x\^2 [-+] ?\d+x [-+] ?\d+ ?\|?)+$")
    parser_linear       = re.compile(r"^( ?-?\d+x [-+] ?\d+ ?\|?)+$")
    parser_trig         = re.compile(r"^sin\(\)|cos\(\)|tan\(\)|cosec\(\)|sec\(\)|cot\(\)$")
    parser_settings     = re.compile(r"^scale ?= ?-?\d+|base ?= ?-?\d+|gap ?= ?-?\d+")
    parser_help         = re.compile(r"^help$")
    parser_exit         = re.compile(r"^exit|quit|q|stop$")

    # Full match of input string
    parsed_str_quadratic    = parser_quadratic.fullmatch(input_string)
    parsed_str_linear       = parser_linear.fullmatch(input_string)
    parsed_str_trig         = parser_trig.fullmatch(input_string)
    parsed_str_help         = parser_help.fullmatch(input_string)
    parsed_str_exit         = parser_exit.fullmatch(input_string)
    parsed_str_setting      = parser_settings.fullmatch(input_string)

    if all(parsed_str_quadratic, parsed_str_linear, parsed_str_trig, parsed_str_help, parsed_str_exit, parsed_str_setting):
        report_bad_format("Invalid input")

    # call respective function based on input string matches
    if parsed_str_help is not None:
        help()
    
    if parsed_str_exit is not None:
        print("Exiting...")
        exit()

    if parsed_str_setting is not None:
        configure(input_string)

    if parsed_str_quadratic is not None:
        digits = separate_eqn_to_digits(input_string)
        digits_new = [lst for lst in digits if bool(lst)]
        do_quadratic(digits_new, input_string)

    if parsed_str_linear is not None:
        digits = separate_eqn_to_digits(input_string)
        digits_new = [lst for lst in digits if bool(lst)]
        do_linear(digits_new, input_string)

    if parsed_str_trig is not None:
        trig_fun(input_string)

# Get input from user and parse it
def get_input():
    print_input_format()
    print("Input: ",end='')
    x = str(input())
    parse_input(x)
    
# Loop
while(True):
    get_input()
