import minor_loss as hmin
import sys

unit = { # Unit system defined in FLT using lbf, inches, and seconds as base units.
    'in': 1,
    'ft': 12,
    'lbf': 1,
    's': 1,
}

weight = 62.4*(unit['lbf']/(unit['ft']**3))
g = 32.174*unit['ft']
g_c = g

unit['lbm'] = unit['lbf']*(g_c/g)
unit['psi'] = unit['lbf']/(unit['in']**2)

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
