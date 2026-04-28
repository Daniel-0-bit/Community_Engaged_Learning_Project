import numpy as np

import utility as utl
import minor_loss as hmin

from utility import unit

Density_w = 62.4 #lbm/ft^3
c_w = 1.0 #BTU/(lbm*degF)

Max_iter = 1000

HX_demand = [ #BTU/hr
    1925875, #McCain
    1924500, #Walker
    2549700  #Patterson
]
demand_total = sum(HX_demand)

Chiller_inlet = 47.8 #Fahrenheit
Chiller_outlet = 40.0 #Fahrenheit

#Q = c_w*m_flow*(T_in-T_out)  #Equation for heat removed by chiller

m_total = (demand_total/(60**2))/(c_w*(Chiller_inlet-Chiller_outlet)) #mass flow through chiller in lbm/s

v_total = m_total/Density_w #volumetric flow through chiller in ft^3/s
v_total_gpm = v_total*((unit['ft']**3)/unit['gpm'])

Pipes = [ #Pipes defined by (length (ft), diameter (in))
    [300, 8],
    [100,10],
    [300,8],
    [100,8],
    [300,10],
    [300,8],
    [300,8]
]

k1 = 4.727
n = 1.852
c = 130
ft = 0.014

K = []
for L,D in Pipes:
    K.append((k1*L)/((np.pow(c,n))*np.pow(D,4.8704)))

Network = [ #Loops arranged by building.  (Pipe, direction)
    [ #Loop 1
        [0,1],
        [1,1],
        [2,-1],
        [3,-1]
    ],
    [ #Loop 2
        [0,-1],
        [4,-1],
        [5,1],
        [6,1]
    ]
]

def thermal_simulation():
    print(f"Chiller inlet temperature: {Chiller_inlet} degF\nChiller outlet temperature: {Chiller_outlet} degF")

    print(f"\nTotal thermal load: {demand_total} BTU/hr")

    print(f"\nRequired chiller flow rate: {v_total_gpm} GPM")

def main():
    print('Running simulation for Step 1 of Part B')
    thermal_simulation()

if __name__ == "__main__":
    main()