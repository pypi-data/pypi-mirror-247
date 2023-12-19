import math


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