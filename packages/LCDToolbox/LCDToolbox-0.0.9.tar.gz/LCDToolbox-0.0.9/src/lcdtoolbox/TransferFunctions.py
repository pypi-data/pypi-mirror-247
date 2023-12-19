from enum import Enum
import numpy as np

class InputType(Enum):
    STEP = 0
    RAMP = 1
    PARABOLA = 2

def steady_state_error(N: int, input_type: InputType, K0: float, h0: float = 1) -> float:
    """
    N: System type
    input_type: Input type
    h0: Height of input
    K0: Steady state gain of system
    """
    if (N < 0 or not isinstance(N, int)):
        raise ValueError('Invalid system type')

    if (input_type == InputType.STEP):
        if (N == 0):
            return h0/(1 + K0)
        elif (N > 0):
            return 0

    elif (input_type == InputType.RAMP):
        if (N == 0):
            return np.inf
        
        elif (N == 1):
            return h0/K0
        
        elif (N > 1):
            return 0
    
    elif (input_type == InputType.PARABOLA):
        if (N < 2):
            return np.inf
        elif(N == 2):
            return h0/K0
        elif (N > 2):
            return 0 
        
def calculate_open_loop_transfer_function(G, H=1):
    return G*H

def calculate_closed_loop_transfer_function(G, H=1):
    return G/(1 + G*H)