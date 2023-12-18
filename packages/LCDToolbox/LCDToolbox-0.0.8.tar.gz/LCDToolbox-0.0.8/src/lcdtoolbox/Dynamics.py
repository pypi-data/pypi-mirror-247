from math import pi

from sympy import fraction, degree, Symbol, zoo, Expr

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
    N = system_type(G_ol, laplace_variable=Symbol('s'))

    G_ol *= Symbol('s')**N
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