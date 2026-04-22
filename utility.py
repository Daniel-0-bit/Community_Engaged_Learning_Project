import sys

g_c = 32.174*12 #lbm*in/lbf/s^2

unit = { # Unit system defined in FLT using lbf, inches, and seconds as base units.  Temperature in degrees Rankine
    'in': 1,
    'ft': 12,
    'lbf': 1,
    'lbm': 1,
    's': 1,
    'degR': 1
}

unit['psi'] = unit['lbf']/(unit['in']**2)
unit['min'] = 60*unit['s']
unit['hr'] = 60*unit['min']
unit['gal'] = 231 # Cubic inches in a gallon
unit['gpm'] = unit['gal']/unit['min'] # Gallons per minute
unit['F>R'] = lambda T: T+459.67
unit['R>F'] = lambda T: T-459.67
unit['BTU'] = 778.17*unit['ft']*unit['lbf']

def Shutdown(msg: str):
    print(msg)
    print("Shutting down")
    sys.exit(1)

def enforceUnit(a: str, u: str):

    return #Returns in base number format.
