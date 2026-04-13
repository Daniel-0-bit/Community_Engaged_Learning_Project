import minor_loss as hmin
import sys

unit = {
    'ft': 1,
    'in': 1/12,
    'lbf': 1,
    'psi': 1/((1/12)**2),
    'psf': 1,
    'lbm': 1,
    'lbm/cf': 1
}

def Shutdown(msg: str):
    print(msg)
    print("Shutting down")
    sys.exit(1)

def enforceUnit(a: str):
    x = -1
    num = 0
    b = ""
    if "psi" in a:
        b = a[0:a.find("psi")]
        x = 1
    elif "ft" in a:
        b = a[0:a.find("ft")]
        x = 0

    if x == 1:
        n = float(b)
        num = n*2.31
    elif x == 0:
        num = float(b)
    else:
        Shutdown("Invalid unit detected.")

    return num

text = "12"

theta = enforceUnit(text)

print(theta)
