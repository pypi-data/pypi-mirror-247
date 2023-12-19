
from lcdtoolbox.TransferFunctions import InputType, steady_state_error, calculate_closed_loop_transfer_function, calculate_open_loop_transfer_function
from sympy import symbols, parse_expr, simplify, Symbol

class Test_steady_state_error:
    def test_TestCase1(self):
        """
        From exam 2021
        """
        Kp, b, c = symbols('Kp b c')
        K0 = Kp*b*c

        assert steady_state_error(N=1, input_type=InputType.RAMP, K0=K0, h0=1) == 1/K0

    def test_TestCase2(self):
        """
        From exam 2015 Q20
        """

        assert steady_state_error(N=0, input_type=InputType.STEP, K0=10, h0=1) - 0.9 < 0.1

    def test_TestCase3(self):
        """
        From exam 2020 Q6
        """

        assert steady_state_error(N=1, input_type=InputType.STEP, K0=parse_expr('Kp*c/b'), h0=1) - 0 < 1e-5

    def test_TestCase4(self):
        """
        From exam 2017 Q4
        """

        assert steady_state_error(N=1, input_type=InputType.STEP, K0=Symbol('K'), h0=1) - 0 < 1e-5

    def test_TestCase5(self):
        """
        From exam 2017 Q16
        """
        expected_out = parse_expr('1/(1 + K)')
        out = steady_state_error(
            N=0, 
            input_type=InputType.STEP, 
            K0=Symbol('K'), 
            h0=1
        )
        assert out - expected_out == 0

class Test_calculate_open_loop_transfer_function:
    def test_TestCase1(self):
        """
        From exam 2021
        """
        G, H1, H2, C = symbols('G H1 H2 C')

        G_inner_cl = calculate_closed_loop_transfer_function(G, H1*H2)
        G_ol = C*G_inner_cl*H1
        G_ol
        assert G_ol == parse_expr('C*G*H1/(G*H1*H2 + 1)')

class Test_calculate_closed_loop_transfer_function:
    def test_TestCase1(self):
        """
        From exam 2020 Q3
        """
        G1, G2, G3 = symbols('G1, G2, G3')

        G12 = G1+G2
        G3_cl = calculate_closed_loop_transfer_function(G3)

        G_ol = G12*G3_cl
        G_cl = calculate_closed_loop_transfer_function(G_ol)
        assert simplify(G_cl - parse_expr('(G1+G2)*G3/(1+(1+G1+G2)*G3)')) == 0

    def test_TestCase2(self):
        """
        From exam 2017 Q3
        """
        G = parse_expr('Kp*c/(s*(a*s + b + s**2))') 

        G_cl = calculate_closed_loop_transfer_function(G)
        expected_out = parse_expr('c*Kp/(s*(s**2+a*s+b) + c*Kp)')

        assert (G_cl - expected_out).simplify() == 0

    def test_TestCase3(self):
        """
        From exam 2017 Q14
        """
        G1 = parse_expr('a/(4*s+1)') 
        G2 = parse_expr('1/s')

        G_cl = calculate_closed_loop_transfer_function(G1*G2)
        expected_out = parse_expr('a/(s*(4*s + 1) + a)')

        assert (G_cl - expected_out).simplify() == 0
