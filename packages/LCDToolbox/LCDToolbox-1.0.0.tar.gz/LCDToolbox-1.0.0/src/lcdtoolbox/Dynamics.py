from math import pi

from sympy import fraction, degree, Symbol, zoo, Expr, laplace_transform, LaplaceTransform, diff, Function, Subs, Derivative, solve, linear_eq_to_matrix

from .Symbolic import string_to_symbolic_equation, laplace_transform_function

def system_order(system, laplace_variable = Symbol('s')):
    """
    Calculates the order of a symbolic system.
    """
    _, denominator = fraction(system.factor())
    order = degree(denominator, laplace_variable)
    return order

def system_type(G_ol: Expr, laplace_variable: Symbol = Symbol('s')):
    r"""
    Returns the amount of pure integrators in the open loop transfer function G_ol.
    """
    G = G_ol.factor()
    K0 = G.subs(laplace_variable, 0)

    
    s_type = 0
    while zoo in K0.atoms():
        s_type += 1
        G *= laplace_variable
        K0 = G.subs(laplace_variable, 0)
    
    return s_type

def calculate_static_loop_gain(G_ol: Expr, laplace_variable=Symbol('s')):
    """
    Calculates the static loop gain of a system given the open loop transfer function G_ol.
    """
    N = system_type(G_ol, laplace_variable=laplace_variable)
    G_ol = G_ol.factor()
    G_ol *= laplace_variable**N
    K0 = G_ol.subs(laplace_variable, 0)

    return K0

def calculate_system_gain(input_ymax: float, system_ymax: float)->float:
    return system_ymax/input_ymax

def calculate_system_phase_change(input_x0: float, system_x0:float, input_frequency: float)->float:
    
    delta_t = input_x0 - system_x0
    T = calculate_period(input_frequency)
    P_pct = delta_t/T
    P_deg = pct_to_degrees(P_pct)
    return P_deg

def calculate_period(frequency):
    return (2 * pi)/(frequency)

def pct_to_degrees(pct: float):
    return pct*360

def phase_margin(angle_Gwc):
    """
    parameters:
    - angle_Gwc: The open loop phase at the crossover frequency [deg]
    """
    return angle_Gwc - (-180)

def gain_margin(mag_Gwpi):
    """
    parameters:
    - mag_Gwpi: The open loop magnitude at the pi frequency [dB]
    """
    return 0 - mag_Gwpi


def laplace_transform_string_equation(string_equation: str, functions: list[str], time_symbol: str = 't', frequency_symbol: str = 's'):
    eq = string_to_symbolic_equation(string_equation)
    t = Symbol(time_symbol)
    s = Symbol(frequency_symbol)

    expression = eq.lhs - eq.rhs
    transformed = laplace_transform(expression, t, s, noconds=True)
    transformed = clean_laplace_transform_expression(transformed, functions, t, s)

    return transformed

def clean_laplace_transform_expression(expression: Expr, functions: list[str], time_symbol: Symbol = Symbol('t'), frequency_symbol: Symbol = Symbol('s')):
    clean_expression = expression.simplify()
    for function in functions:
        transformed_function = laplace_transform_function(function, frequency_symbol=frequency_symbol)
        function = Function(function)
        clean_expression = clean_expression.subs(LaplaceTransform(function(time_symbol), time_symbol, frequency_symbol), transformed_function)
        clean_expression = clean_expression.subs(function(0), 0)
        clean_expression = clean_expression.subs(Subs(Derivative(function(time_symbol), time_symbol), time_symbol, 0), 0)

    return clean_expression


def get_transfer_functions(string_equations: list[str], input_functions: list[str], output_functions: list[str], time_symbol: Symbol = Symbol('t'), frequency_symbol: Symbol = Symbol('s')):
    transformed_equations = []
    for string_equation in string_equations:
        transformed_equations.append(laplace_transform_string_equation(string_equation, input_functions + output_functions, time_symbol=str(time_symbol), frequency_symbol=str(frequency_symbol)))

    transformed_output_functions = []
    for output_function in output_functions:
        transformed_output_functions.append(laplace_transform_function(output_function, frequency_symbol=frequency_symbol))

    A, b = linear_eq_to_matrix(transformed_equations, transformed_output_functions)
    detA = A.det()
    solutions = {}

    for i, output_function in enumerate(transformed_output_functions):
        A_function = A.copy()
        A_function.col_del(i)
        A_function = A_function.col_insert(i, b)

        solution = A_function.det()/detA

        for input_function in input_functions:
            input_function = laplace_transform_function(input_function, frequency_symbol=frequency_symbol)
            solutions[str(output_function) + '/' + str(input_function)] = solution/input_function
    
    return solutions