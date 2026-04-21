import minor_loss as hmin
import utility as utl
import numpy as np

from utility import unit

#Pipe parameters
length = 100
pipe_rough = 0.02

#Heat exchangers
H_x = lambda Q: (0.0049*np.pow(Q,1.852)) # Q must be in gallons per minute.  Loss in ft*lbf/lbm
A_hx = 5000*unit['ft']**2
U = lambda Q: (1/(1/(13*np.pow(Q,0.8))+0.047)) # Q in gpm.  Returns U in BTU/(hr*ft^2*degF)

# Air temperatures
T_in = unit['F>R'](72)
T_out = unit['F>R'](10)

# Water properties
density = 62.4 #lbm/ft^3
c_p = 1.00
mu = 0.88e-3
nu = 1.4e-5
k_w = 0.332
Pr = 9.55
alpha = 5.33
beta = 0.49
