import sys

unit = { # Unit system defined in FLT using lbf, inches, and seconds as base units.  Temperature in degrees Rankine
    'in': 1,
    'ft': 12,
    'lbf': 1,
    's': 1,
    'degR': 1
}

weight = 62.4*(unit['lbf']/(unit['ft']**3))
g = 32.174*unit['ft']
g_c = 32.174 #lbm*ft/lbf/s^2

unit['lbm'] = unit['lbf']*(g_c/g) # Under earth conditions, lbm should be 1:1 with lbf
unit['psi'] = unit['lbf']/(unit['in']**2)
unit['gal'] = 231*unit['ft']**3 # Cubic feet in a gallon
unit['min'] = 60*unit['s']
unit['gpm'] = unit['gal']/unit['min'] # Gallons per minute
unit['F>R'] = lambda T: T+459.67
unit['R>F'] = lambda T: T-459.67

def Shutdown(msg: str):
    print(msg)
    print("Shutting down")
    sys.exit(1)

def enforceUnit(a: str):
    x = -1
    num: float
    b = ""
    if "psi" in a:
        b = a[0:a.find("psi")]
        num = float(b)/weight
    elif "ft" in a:
        b = a[0:a.find("ft")]
        num = float(b)*unit['ft']
    else:
        Shutdown("Invalid unit detected.")

    return num #Returns in base number format.

text = "23 ft"

theta = enforceUnit(text)

print(theta/unit['ft'])
