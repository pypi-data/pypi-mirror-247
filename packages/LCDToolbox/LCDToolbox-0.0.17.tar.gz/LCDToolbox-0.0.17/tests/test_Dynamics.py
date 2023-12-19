from sympy import symbols, Symbol
from sympy.parsing.sympy_parser import parse_expr

from lcdtoolbox.Dynamics import system_order, system_type, calculate_static_loop_gain, laplace_transform_string_equation, gain_margin, phase_margin, get_transfer_functions


class Test_system_order:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        s, a, b, c, gamma, beta = symbols('s a b c gamma beta')
        system = gamma*(b*s+c)/(a*s*(s**2+s*a+beta))

        assert system_order(system) == 3
    
    def test_TestCase2(self):
        """
        From exam 2015 Q6
        """
        system = parse_expr('b*d * (gmm*s + phi)/(alpha*s + bet) * 1/(s + a) * 1/(s + c)')

        assert system_order(system) == 3

    def test_TestCase3(self):
        """
        From exam 2015 Q15
        """
        system = parse_expr('Kp*1/(s+1)*1/(s+2)*1/(s+a)')

        assert system_order(system) == 3


    def test_TestCase4(self):
        """
        From exam 2020 Q4
        """
        G_ol = parse_expr('K3*(K1 + K2/s)/(s*(K3/s + 1))')

        assert system_order(G_ol) == 2

class Test_system_type:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        s, a, b, c, gamma, beta = symbols('s a b c gamma beta')
        system = gamma*(b*s+c)/(a*s*(s**2+s*a+beta))

        assert system_type(system) == 1

    def test_TestCase2(self):
        """
        From exam 2021 Q14
        """
        system = parse_expr('Kp*b*c/(s*(s*tau + 1))')

        assert system_type(system) == 1

    def test_TestCase3(self):
        """
        From exam 2015 Q6
        """
        system = parse_expr('b*d * (gmm*s + phi)/(alpha*s + bet) * 1/(s + a) * 1/(s + c)')

        assert system_type(system) == 0

    def test_TestCase4(self):
        """
        From exam 2015 Q15
        """
        system = parse_expr('Kp*1/(s+1)*1/(s+2)*1/(s+a)')

        assert system_type(system) == 0

    def test_TestCase5(self):
        """
        From textbook 'Feedback control techniques' sec. 11.12 Chapter problem 3.
        """
        system = parse_expr('511/(s**3+22*s**2+225*s)')

        assert system_type(system) == 1

    def test_TestCase6(self):
        """
        From exam 2020 Q4
        """
        G_ol = parse_expr('K3*(K1 + K2/s)/(s*(K3/s + 1))')

        assert system_type(G_ol) == 1

    def test_TestCase7(self):
        """
        From exam 2020 Q2
        """
        G_ol = parse_expr('Kp/(a*s + b + s**2)')

        assert system_type(G_ol) == 0

    def test_TestCase8(self):
        """
        From exam 2017 Q16
        """
        G_ol = parse_expr('K*a/((a + s*(4*s + 1))*(s + 1))')

        assert system_type(G_ol) == 0


class Test_calculate_static_loop_gain:
    def test_TestCase1(self):
        """
        From exam 2021 Q14
        """
        G_ol = parse_expr('Kp*b*c/(s*(s*tau + 1))')
        Kp, b, c = symbols('Kp b c')
        K0 = calculate_static_loop_gain(G_ol)
        assert K0 == Kp*b*c

    def test_TestCase2(self):
        """
        From textbook 'Feedback control techniques' sec. 11.4
        """
        G_ol = parse_expr('Kp * 22/(100*s**2 + 5*s + 1)')
        Kp, s = symbols('Kp, s')
        K0 = calculate_static_loop_gain(G_ol)

        assert K0 == Kp * 22
        
    def test_TestCase3(self):
        """
        From exam 2015 Q15
        """
        system = parse_expr('Kp*1/(s+1)*1/(s+2)*1/(s+a)')
        K0_answer = parse_expr('Kp/(2*a)')

        K0 = calculate_static_loop_gain(system)

        assert K0 == K0_answer

    def test_TestCase4(self):
        """
        From exam 2020 Q6
        """
        system = parse_expr('K3*(K1 + K2/s)/(s*(K3/s + 1))')
        K0_answer = parse_expr('K2')

        K0 = calculate_static_loop_gain(system)

        assert K0 == K0_answer

    def test_TestCase5(self):
        """
        From exam 2017 Q16
        """
        system = parse_expr('K*a/((a + s*(4*s + 1))*(s + 1))')
        K0_answer = parse_expr('K')
    
        K0 = calculate_static_loop_gain(system)

        assert K0 == K0_answer
    

class Test_laplace_transform_string_equation:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        string_equation = 'a*Derivative(x(t),t) = b*Derivative(z(t),t) + c*z(t)'
        expected_out = parse_expr('a*s*X(s) - b*s*Z(s) - c*Z(s)')
        out = laplace_transform_string_equation(string_equation, ['x', 'z'])
        assert out == expected_out

    def test_TestCase2(self):
        """
        From exam 2021 Q1
        """
        string_equation = 'Derivative(y(t),t,t) = - alpha*Derivative(y(t),t) - bet*y(t) + gam*x(t)'
        expected_out = parse_expr('s**2*Y(s) + alpha*s*Y(s) + bet*Y(s) - gam*X(s)')

        out = laplace_transform_string_equation(string_equation, ['y', 'x'])
        assert out == expected_out

    def test_TestCase3(self):
        """
        From exam 2020 Q18
        """
        string_equation = 'Derivative(y(t),t,t) + 7.5*Derivative(y(t),t) + 10*y(t) = 100*Derivative(u(t),t) + 125*u(t)'
        expected_out = parse_expr('s**2*Y(s) + 7.5*s*Y(s) + 10*Y(s) - 100*s*U(s) - 125*U(s)')

        out = laplace_transform_string_equation(string_equation, ['y', 'u'])
        assert out == expected_out
    
    def test_TestCase4(self):
        """
        From exam 2017 Q1
        """
        string_equation = 'Derivative(y(t),t,t) = -a*Derivative(y(t),t) - b*y(t) + c*x(t)'
        expected_out = parse_expr('s**2*Y(s)+a*s*Y(s)+b*Y(s)-c*X(s)')

        out = laplace_transform_string_equation(string_equation, ['y', 'x'])
        assert out == expected_out

class Test_get_transfer_functions:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        string_equation = 'a*Derivative(x(t),t) = b*Derivative(z(t),t) + c*z(t)'
        expected_out = parse_expr('(b*s + c)/(a*s)')

        out = get_transfer_functions([string_equation], ['z'], ['x'])['X(s)/Z(s)']
        assert (out - expected_out).simplify() == 0

    def test_TestCase2(self):
        """
        From exam 2021 Q1
        """
        string_equation = 'Derivative(y(t),t,t) = - alpha*Derivative(y(t),t) - bet*y(t) + gam*x(t)'
        expected_out = parse_expr('gam/(s**2 + alpha*s + bet)')

        out = get_transfer_functions([string_equation], ['x'], ['y'])['Y(s)/X(s)']
        assert (out - expected_out).simplify() == 0

    def test_TestCase3(self):
        """
        From exam 2020 Q18
        """
        string_equation = 'Derivative(y(t),t,t) + 7.5*Derivative(y(t),t) + 10*y(t) = 100*Derivative(u(t),t) + 125*u(t)'
        expected_out = parse_expr('12.5*(0.8*s + 1)/(0.1*s**2 + 0.75*s + 1)')

        out = get_transfer_functions([string_equation], ['u'], ['y'])['Y(s)/U(s)']
        assert (out - expected_out).simplify() == 0

    def test_TestCase4(self):
        """
        From exam 2017 Q1
        """
        string_equation = 'Derivative(y(t),t,t) = -a*Derivative(y(t),t) - b*y(t) + c*x(t)'
        expected_out = parse_expr('c/(a*s + b + s**2)')

        out = get_transfer_functions([string_equation], ['x'], ['y'])['Y(s)/X(s)']
        assert (out - expected_out).simplify() == 0

    def test_TestCase5(self):
        """
        From exam 2017 Q1
        """
        string_equation = 'Derivative(x(t),t) = u(t)'
        expected_out = parse_expr('1/s')

        out = get_transfer_functions([string_equation], ['u'], ['x'])['X(s)/U(s)']
        assert (out - expected_out).simplify() == 0

    def test_TestCase6(self):
        """
        From exam 2022 Q1
        """
        string_equation_1 = 'Derivative(x(t),t) = f0 - a*(x(t) - x0) + b*(u(t)-u0)'
        string_equation_2 = 'y(t) = c*x(t)'

        G0 = get_transfer_functions([string_equation_1, string_equation_2], ['u'], ['x', 'y'])['Y(s)/U(s)']
        G0 = G0\
            .subs(Symbol('f0'), 0)\
            .subs(Symbol('u0'),0)\
            .subs(Symbol('x0'),0)

        expected_out = parse_expr('c*b/(s+a)')

        assert (G0 - expected_out).simplify() == 0

    def test_TestCase7(self):
        """
        From exam 2022 Q2
        """
        string_equation_1 = 'Derivative(x(t),t) = f0 - a*(x(t) - x0) + b*(u(t)-u0)'
        string_equation_2 = 'y(t) = c*x(t) + d*u(t)'

        G0 = get_transfer_functions([string_equation_1, string_equation_2], ['u'], ['x', 'y'])['Y(s)/U(s)']
        G0 = G0\
            .subs(Symbol('f0'), 0)\
            .subs(Symbol('u0'),0)\
            .subs(Symbol('x0'),0)

        expected_out = parse_expr('c*b/(s+a) + d')

        assert (G0 - expected_out).simplify() == 0

    def test_TestCase6(self):
        """
        From exam 2022 Q3
        """
        string_equation_1 = 'Derivative(x(t),t,t) = f0 - a*(x(t) - x0) + b*(u(t)-u0)'
        string_equation_2 = 'y(t) = c*x(t)'

        G0 = get_transfer_functions([string_equation_1, string_equation_2], ['u'], ['x', 'y'])['Y(s)/U(s)']
        G0 = G0\
            .subs(Symbol('f0'), 0)\
            .subs(Symbol('u0'),0)\
            .subs(Symbol('x0'),0)

        expected_out = parse_expr('b*c/(a + s**2)')

        assert (G0 - expected_out).simplify() == 0


class Test_phase_margin:
    def test_TestCase1(self):
        """
        From exam 2020 Q11
        """
        assert phase_margin(angle_Gwc=-65) - 115 < 1e-5

    def test_TestCase2(self):
        """
        From exam 2017 Q7
        """
        assert phase_margin(angle_Gwc=-86) - 94 < 1e-5


class Test_gain_margin:
    def test_TestCase1(self):
        """
        From exam 2020 Q11
        """
        assert gain_margin(mag_Gwpi=-10) - 10 < 1e-5

    def test_TestCase2(self):
        """
        From exam 2017 Q7
        """
        assert gain_margin(mag_Gwpi=-3.5) - 3.5 < 1e-5
