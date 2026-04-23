import numpy as np
import matplotlib.pyplot as plt

import minor_loss as hmin
import utility as utl

from utility import unit

g = 32.174 #ft/s^2

#Pipe and network parameters
L = 100
Rough = 0.02 #ft
D = 0.1722 #ft
cross_area = np.pi*(D/2)**2 #square feet

#Heat exchangers
H_x = lambda Q: (0.0049*np.pow(Q,1.852)) # Q must be in gallons per minute.  Loss in ft*lbf/lbm
A_hx = 5000 #ft^2
U = lambda Q: (1/(1/(13*np.pow(Q,0.8))+0.047)) # Q in gpm.  Returns U in BTU/(hr*ft^2*degF)

#Minor loss factor
f_t = 0.3086/np.log10((Rough/(3.7*D))**1.11)**2
k_min = 10*hmin.fittings['elb90'](f_t) # Minor loss coefficient
k_min += 6*hmin.fittings['gate'](f_t) #minor loss coefficient

# Air properties
T_in = unit['F>R'](72) #Temperature converted to degrees Rankine
T_out = unit['F>R'](10)
Air_Mass = 25 #lbm/sec

# Water properties
Density_w = 62.4 #lbm/ft^3
Mu = 0.88e-3 #dynamic viscosity lbm/ft/s
Nu = 1.4e-5 #kinematic viscosity ft^2/s

w_mass = [] #lbm/s
h_maj =[]
h_min = []
h_hx = []
h_total = []

w_mass = np.linspace(0,62.4,100)

for i,q in enumerate(w_mass):
    w_flow = q/Density_w # ft^3/s
    w_flow_gpm = w_flow*(unit['ft']**3/unit['gpm']) #GPM

    u_w = w_flow/cross_area #velocity in ft/s

    Re = u_w*D/Nu

    #Major loss
    if Re <= 1e-8:
        f = 0
    elif Re < 2300:
        f = 64/Re
    else:
        f = 0.3086/(np.log10(6.9/Re+np.pow((Rough/(3.7*D)),1.11))**2)
    
    h_maj.append(f*(L/D)*(u_w**2/2/utl.g_c))

    #Minor loss
    h_min.append(k_min*(u_w**2/2/utl.g_c))

    #HX loss
    h_hx.append(H_x(w_flow_gpm))

    h_total.append(h_maj[i]+h_min[i]+h_hx[i])

#Plot rendering
plt.plot(w_mass,h_maj)
plt.plot(w_mass,h_min)
plt.plot(w_mass,h_hx)
plt.plot(w_mass,h_total)

plt.title("Head losses")
plt.xlabel("Mass flow rate (lbm/s)")
plt.ylabel("Head loss (ft*lbf/lbm)")

plt.legend([
    'major head loss',
    "minor head loss",
    "HX head loss",
    "total head loss"
])

plt.show()