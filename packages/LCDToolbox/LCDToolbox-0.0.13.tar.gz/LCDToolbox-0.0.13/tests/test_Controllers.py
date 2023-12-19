from lcdtoolbox.Controllers import calculate_phi_d, calculate_phi_i, calculate_open_loop_phase_at_crossover_frequency


class Test_calculate_phi_i:
    def test_TestCase1(self):
        """
        From exam 2021
        """
        assert calculate_phi_i(Ni=3) - 18.4 < 0.1


class Test_calculate_phi_d:
    def test_TestCase1(self):
        """
        From exam 2021
        """
        assert calculate_phi_d(alpha=0.25) - 36.9 < 0.1


class Test_calculate_open_loop_phase_at_crossover_frequency:
    def test_TestCase1(self):
        """
        From exam 2021
        """
        assert calculate_open_loop_phase_at_crossover_frequency(gamma_m=60, phi_i=20, phi_d=0) - (-100) < 1e-5
