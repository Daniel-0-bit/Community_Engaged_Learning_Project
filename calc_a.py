import numpy as np

import minor_loss as hmin
import utility as utl

from utility import unit

g = 32.174*12 #in/s^2

#Pipe and network parameters
length = 100
pipe_rough = 0.02
k_min = 10*hmin.fittings['elb90'] # Minor loss coefficient
k_min += 6*hmin.fittings['gate'](1) #minor loss coefficient.  gate(1) means open gate, which is assumed
diameter = 2.067 #in
cross_area = np.pi*(diameter/2)**2 #square inches

#Heat exchangers
H_x = lambda Q: (0.0049*np.pow(Q,1.852)) # Q must be in gallons per minute.  Loss in ft*lbf/lbm
A_hx = 5000*unit['ft']**2
U = lambda Q: (1/(1/(13*np.pow(Q,0.8))+0.047)) # Q in gpm.  Returns U in BTU/(hr*ft^2*degF)

# Air properties
T_in = unit['F>R'](72) #Temperature converted to degrees Rankine
T_out = unit['F>R'](10)
air_mass = 25 #lbm/sec

# Water properties
density_w = 62.4 #lbm/ft^3
c_p = 1.00 # BTU/lbm/degF
mu = 0.88e-3 #dynamic viscosity lbm/ft/s
nu = 1.4e-5 #kinematic viscosity ft^2/s
k_w = 0.332 #BTU/hr/ft/degF
Pr = 9.55
alpha = 5.33 #ft^2/hr
beta = 0.49 #1/degF

w_mass = 62.4 #lbm/s
w_flow = w_mass/density_w # ft^3/s
w_flow *= unit['ft']**3/unit['in']**3 #Converting to cubic inches

u_w = w_flow/cross_area #velocity in in/s
u_w *= unit['in']/unit['ft'] #Convert to feet/s

h_min = k_min*u_w**2/(2*utl.g_c)

print(f'test_variable = {u_w}')