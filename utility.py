import sys
import numpy as np

g_c = 32.174*12 #lbm*in/lbf/s^2

unit = { # Unit system defined in FLT using lbf, inches, and seconds as base units.  Temperature in degrees Rankine
    'in': 1,
    'ft': 12,
    'lbf': 1,
    'lbm': 1,
    's': 1,
    'degR': 1,
    'F>R': lambda T: T+459.67,
    'R>F': lambda T: T-459.67,
}

unit['psi'] = unit['lbf']/(unit['in']**2)
unit['min'] = 60*unit['s']
unit['hr'] = 60*unit['min']
unit['gal'] = 231*unit['in']**3 # Cubic inches in a gallon
unit['gpm'] = unit['gal']/unit['min'] # Gallons per minute
unit['BTU'] = 778.17*unit['ft']*unit['lbf']

def Shutdown(msg: str = 'Unknown error'):
    print(msg)
    print("Shutting down")
    sys.exit(1)

def enforceUnit(a: str, u: str):

    return #Returns in base number format.

def heatCapacity(a: float,b: float):
    C = []
    Cr: float
    if a<b:
        C = [a,b]
    else:
        C = [b,a]

    Cr = C[0]/C[1]

    return C,Cr

def eff_crossflow(Cr: float, NTU: float, mixed: str = "neither"):
    eff: float
    
    method = {
        "neither": lambda cr, ntu: 1-np.exp((1/cr)*np.pow(ntu,0.22)*(np.exp(-cr*np.pow(ntu,0.78))-1)),

        "min": lambda cr, ntu: 1-np.exp(-(1/cr)*(1-np.exp(-cr*ntu))),

        "max": lambda cr, ntu: (1/cr)*(1-np.exp(-cr*(1-np.exp(-ntu))))
    }

    try:
        if Cr <= 1e-10:
            raise KeyError
        else:
            eff = method[mixed](Cr,NTU)
    except KeyError:
        print("Invalid.  Defaulting")
        eff = 1-np.exp(-NTU)

    return eff

HX_HeadLoss = lambda Q: (0.0049*np.pow(Q,1.852)) # Q must be in gallons per minute.  Loss in ft*lbf/lbm

def differential(func, x: float, h: float = 1e-6):
    return float((func(x+h) - func(x-h))/(2*h))