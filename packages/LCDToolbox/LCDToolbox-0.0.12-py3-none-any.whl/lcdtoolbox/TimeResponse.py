import math
import numpy as np
import matplotlib.pyplot as plt

from control.matlab import lsim
from control import TransferFunction


def calculate_damping_from_overshoot(Mp: float):
    """
    Mp: Overshoot as decimal
    """
    return -(1/(math.log(Mp)**2 + math.pi**2))**(0.5) * math.log(Mp)

def calculate_overshoot_from_step_response(ymax, yss):
    """
    ymax: The max value of the response
    yss: The steady state value of the response
    """
    return (ymax - yss)/yss

def plot_sine_response(
        G:TransferFunction,
        freq:float,
        t=10,
        t0=0,
        title='Time response'
    ):
    t = np.linspace(0,t,500)
    u = np.sin(freq*t)
    y, _, _ = lsim(G, u, t)

    plt.plot(t,u,label='$u(t)$')
    plt.plot(t,y,label='$y(t)$')
    plt.xlabel('Time [s]')
    plt.title(title)
    plt.xlim(left=t0, right=t[-1])
    plt.legend()
    plt.grid()
    plt.show()