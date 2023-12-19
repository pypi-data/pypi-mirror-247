from lcdtoolbox.Controllers import calculate_phi_d, calculate_phi_i, calculate_open_loop_phase_at_crossover_frequency, calc_gamma_m, calc_K_m


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

class Test_calc_gamma_m:
    def test_TestCase1(self):
        """
        From exam 2020 Q11
        """
        assert calc_gamma_m(angle_Gwc=-65) - 115 < 1e-5


class Test_calc_K_m:
    def test_TestCase1(self):
        """
        From exam 2020 Q11
        """
        assert calc_K_m(mag_Gwpi=-10) - 10 < 1e-5