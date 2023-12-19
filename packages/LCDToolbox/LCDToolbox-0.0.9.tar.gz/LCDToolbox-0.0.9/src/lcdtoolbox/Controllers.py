import numpy as np


def calculate_phi_i(Ni):
    """
    Calculates the phase effect of a I controller in degrees.
    """
    return np.rad2deg(-np.arctan(1/Ni))


def calculate_phi_d(alpha):
    """
    Calculates the phase effect of a lead controller in degrees.
    """
    return np.rad2deg(np.arcsin((1-alpha)/(1 + alpha)))


def calculate_open_loop_phase_at_crossover_frequency(gamma_m, phi_i=0, phi_d=0):
    """
    Calculates the open loop phase at the crossover frequency.
    Parameters:
        gamma_m: The phase margin of the system [deg]
        phi_i: The phase effect of a I controller [deg]
        phi_d: The phase effect of a lead controller [deg]
    """
    return -180 + gamma_m - phi_i - phi_d

def calc_gamma_m(angle_Gwc):
    """
    parameters:
    - angle_Gwc: The open loop phase at the crossover frequency [deg]
    """
    return angle_Gwc - (-180)

def calc_K_m(mag_Gwpi):
    """
    parameters:
    - mag_Gwpi: The open loop magnitude at the pi frequency [dB]
    """
    return 0 - mag_Gwpi
