from sympy import Eq, Function, Symbol
from sympy.parsing.sympy_parser import parse_expr

def string_to_symbolic_equation(equation: str):
    equation_parts = equation.split('=')
    if not len(equation_parts) == 2:
        return
    rhs, lhs = equation_parts
    return Eq(parse_expr(rhs), parse_expr(lhs))

def laplace_transform_function(function: str, frequency_symbol: Symbol = Symbol('s')) -> Function:
    transformed_function = function.capitalize()
    symbolic_function = Function(transformed_function)
    return symbolic_function(frequency_symbol)

