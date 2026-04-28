import numpy as np
import matplotlib.pyplot as plt

import minor_loss as hmin
import utility as utl

from utility import unit

min_flow = 0
max_flow = 500
iteration = 1000

g = 32.174 #ft/s^2

#Pipe and network parameters
L = 100
Rough = 0.02 #ft
D = 0.1722 #ft
cross_area = np.pi*(D/2)**2 #square feet

#Crossflow heat exchangers (mixed-unmixed)
H_x = lambda Q: (0.0049*np.pow(Q,1.852)) # Q must be in gallons per minute.  Loss in ft*lbf/lbm
A_hx = 5000 #ft^2
U = lambda Q: (1/(1/(13*np.pow(Q,0.8))+0.047)) # Q in gpm.  Returns U in BTU/(hr*ft^2*degF)

#Minor loss factor
f_t = 0.3086/np.log10((Rough/(3.7*D))**1.11)**2
k_min = 10*hmin.fittings['elb90'](f_t) # Minor loss coefficient from elbows
k_min += 6*hmin.fittings['gate'](f_t) #minor loss coefficient from gates

# Air properties
T_in = 72 #Temperature in degF
T_out = 10
Air_Mass = 41.7 #lbm/sec
c_air = 0.240 #BTU/lbm/degF
capacity_air = Air_Mass*c_air #BTU/sec/degF
capacity_air *= unit['hr'] #BTU/hr/degF

# Water properties
Density_w = 62.4 #lbm/ft^3
Mu = 0.88e-3 #dynamic viscosity lbm/ft/s
Nu = 1.4e-5 #kinematic viscosity ft^2/s
c_w = 1.00 #BTU/lbm/degF
T_w = 50 #Guess temperature for water
T_w1 = [] #Iterated flow values
T_w2 = []
Freeze = []

h_maj =[]
h_min = []
h_hx = []
h_total = []
q1 = [] #BTU/hr
q2 = [] #BTU/hr

w_flow = np.linspace(min_flow,max_flow,iteration) #GPM

#Flow iteration
for i,q in enumerate(w_flow):

    u_w = q*(unit['gpm']/(unit['ft']**3))/cross_area #velocity in ft/s
    m = q*(unit['gpm']/unit['ft']**3)*Density_w

    Re = u_w*D/Nu

    ## Head losses
    #Major loss
    if Re < 1:
        f = 0
    elif Re < 2300:
        f = 64/Re
    else:
        f = 0.3086/(np.log10(6.9/Re+np.pow((Rough/(3.7*D)),1.11))**2)
    
    h_maj.append(f*(L/D)*(u_w**2/(2*utl.g_c)))

    #Minor loss
    h_min.append(k_min*(u_w**2/(2*utl.g_c)))

    #HX loss
    h_hx.append(utl.HX_HeadLoss(q))

    h_total.append(h_maj[i]+h_min[i]+h_hx[i])

    ## HX Rating    
    capacity_w = c_w*m*unit['hr']
    capacity = sorted([capacity_w, capacity_air])
    Cr = capacity[0]/capacity[1]
    NTU: float
    eff: float

    if capacity[0] < 1e-10:
        eff = 1
    else:
        NTU = U(q)*A_hx/capacity[0] #unitless.  capacity[0] is C_min

        if capacity_air > capacity_w:
            eff = utl.eff_crossflow(Cr,NTU,'max')
        else:
            eff = utl.eff_crossflow(Cr,NTU,'min')
    
    #q1 = eff*C_min*(T_1-T_out)
    #q1 = C_w*(T_1-T_2)
    #T_2 = T_1-eff*C_min*(T_1-T_out)/C_w

    #q2 = eff*C_min*(T_2-T_in)
    #q2 = C_w*(T_2-T_1)
    #T_1 = T_2-eff*C_min*(T_2-T_air)/C_w

    if capacity_w < 1e-10:
        T_w1.append(T_in)
        T_w2.append(T_out)

        q1.append(0)
        q2.append(0)
    else:
        T_w1.append(T_w) #First HX inlet, initial guess
        T_w2.append(T_w-eff*capacity[0]*(T_w-T_out)/capacity_w) #Second HX inlet, initial guess

        for j in range(1,int(iteration/10)):
            T_w1[i] = T_w2[i]-eff*capacity[0]*(T_w2[i]-T_in)/capacity_w #Output temperature of second HX
            T_w2[i] = T_w1[i]-eff*capacity[0]*(T_w1[i]-T_out)/capacity_w #Output temperature of first HX
    
    Freeze.append(32)

##Plot rendering
#Head loss
plt.plot(w_flow,h_maj)
plt.plot(w_flow,h_min)
plt.plot(w_flow,h_hx)
plt.plot(w_flow,h_total, lw=2)

plt.title("Head losses")
plt.xlabel("Flow rate (gpm)")
plt.ylabel("Head loss (ft*lbf/lbm)")

plt.legend([
    'major head loss',
    "minor head loss",
    "HX head loss",
    "total head loss"
])

plt.show()

#HX inlet temperatures
plt.plot(w_flow,T_w1,color='r')
plt.plot(w_flow,T_w2,color='b')
plt.plot(w_flow,Freeze,color='k',linestyle='--')

plt.title("Water Flow Temperatures")
plt.xlabel("Flow rate (gpm)")
plt.ylabel(f"Temperature (\u00B0F)")

plt.legend([
    "Water inlet of HX 1",
    "Water inlet of HX 2"
])

plt.show()