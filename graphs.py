import matplotlib.pyplot
import re
import math
import numpy

def print_input_format():
    print("Quadratic: ax^2 + bx + c")
    print("Linear: bx +c")
    print("\twhere a,b,c are any integer values")

def help():
    print()
    print("How to use this tool")
    print("This tool supports two types of equations to be plotted on the graph")
    print("""
|__
|  Quadratic - ax^2 + bc + c for all a,b,c belonging to (-∞, ∞)
|__
   Linear - bx + c for all b,c belonging to (-∞, ∞)

examples:

> Input: 5x^2 - 12x + 5
> Input: -7x^2 + 5x - 5
> Input: 40x - 100
> Input: 5x - 12
""")
print()

def report_bad_format(str):
    print()
    print(str,'\nType \'help\' for help')
    exit()

def print_graph(xval, yval, input_string):

    matplotlib.pyplot.plot(xval,yval)
    matplotlib.pyplot.xlabel("x")
    matplotlib.pyplot.ylabel("f(x)")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.title(("f(x) =" + input_string))
    matplotlib.pyplot.show()

def do_quadratic(a, b, c,input_string):
    # we do a little bit of type casting
    a = int(a)
    b = int(b)
    c = int(c)
    input_string = str(input_string)

    y = [None] * 10
    x = [z for z in range(0,10)]

    for idx in x:
        y[idx] = a * math.pow(idx,2) + b * idx + c

    print_graph(x,y,input_string)
    

def do_linear(b, c, input_string):
    b = int(b)
    c = int(c)

    x = [z for z in range(0, 10)]
    y = [None] * 10
    
    for idx in x:
        y[idx] = b * idx + c

    print_graph(x, y, input_string)    

def separate_quad_to_digits(input_string):
    numbers = ""
    digits= []
    for word in input_string.split():        
        for idx,ch in enumerate(word):
            if ch == 'x' or ch == '^' or (ch == '2' and input_string[idx-1] == '^') or ch == '+':
                continue
            numbers = numbers + str(ch)
       
        if (numbers[len(numbers)-1] == '-'):
            continue
        numbers = numbers + ' '
    
    for dig in numbers.split():
        digits = digits + [int(dig)]
    
    return digits;

def separate_lin_to_digits(input_string):
    numbers = ""
    digits = []
    for word in input_string.split():
        for idx, ch in enumerate(word):
            if ch == 'x' or ch == '+':
                continue
            numbers = numbers + str(ch)

        if numbers[len(numbers)-1] == '-':
            continue
        numbers = numbers + ' '

    for dig in numbers.split():
        digits= digits + [int(dig)]

    return digits

def parse_input(input_string):
    # Remove any spaces from left or right
    input_string = input_string.strip()

    parser_quadratic = re.compile(r"^-?\d+x\^2 [-+] ?\d+x [-+] ?\d+$")
    parser_linear = re.compile(r"^-?\d+x [-+] ?\d+$")
    parser_help = re.compile(r"^help$")
    parser_exit = re.compile(r"^exit$")

    parsed_str_quadratic = parser_quadratic.fullmatch(input_string)
    parsed_str_linear = parser_linear.fullmatch(input_string)
    parsed_str_help = parser_help.fullmatch(input_string)
    parsed_str_exit = parser_exit.fullmatch(input_string)

    if parsed_str_quadratic is None and parsed_str_linear is None and parsed_str_help is None and parsed_str_exit is None:
        report_bad_format("Invalid input")

    digits = "poty"

    if parsed_str_help is not None and parsed_str_linear is None and parsed_str_quadratic is None and parsed_str_exit is None:
        help()
    
    if parsed_str_exit is not None and parsed_str_linear is None and parsed_str_quadratic is None and parsed_str_help is None:
        exit()

    if (parsed_str_quadratic is not None and parsed_str_linear is None):
        digits = separate_quad_to_digits(input_string)
        do_quadratic(digits[0],digits[1], digits[2], input_string)

    if (parsed_str_quadratic is None and parsed_str_linear is not None):
        digits = separate_lin_to_digits(input_string)
        do_linear(digits[0],digits[1], input_string)
    

def get_input():
    print_input_format()

    print("Input: ",end='')
    x = str(input())
    parse_input(x)
    
while(True):
    get_input()