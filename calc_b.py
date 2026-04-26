import numpy as np

import minor_loss as hmin
import utility as utl
from utility import unit

## =========================================================
## GLOBAL CONSTANTS / FLUID PROPERTIES
## =========================================================
g = 32.174
Density_w = 62.4
c_w = 1.0
Nu = 1.4e-5

## =========================================================
## HARDY-CROSS PARAMETERS
## =========================================================
n = 1.852
C = 130
max_iter = 100
precision = 5e-5

## =========================================================
## PIPE NETWORK DEFINITION
## =========================================================
pipes = [
    (2000,12),
    (2000,6),
    (3000,6),
    (4000,6),
    (1000,8),
    (3000,8),
    (2000,8)
]

## Resistance coefficients (Hazen-Williams)
K = []
for length, diameter in pipes:
    K.append((4.727 * length) / ((C**n) * (diameter**4.8704)))

## Initial flow guesses (must be continuous)
flows_init = [0.8, 0.2, 1.2, 1.2, 1, 1, 1]

## Loop definitions
loops = [
    [[1,1],[2,-1],[3,-1],[4,-1]],
    [[1,-1],[5,1],[6,1],[7,-1]]
]

## =========================================================
## HEAT EXCHANGER SYSTEM
## =========================================================

## Parallel HX energy demands (BTU/hr)
HX_demand = [50000, 40000, 30000]

## Return HX parameters
A_hx = 5000

U = lambda Q: (1/(1/(13*np.pow(Q,0.8))+0.047))

## Air side
T_air_in = unit
T_air_out = unit
Air_Mass = 25
c_air = 0.240
capacity_air = Air_Mass * c_air * unit['hr']

## =========================================================
## HARDY-CROSS SOLVER
## =========================================================
def solve_flows(flows):

    for I in range(max_iter):
        max_delta = 0

        for loop in loops:
            top = 0
            bot = 0

            for pipe, direction in loop:
                pipe -= 1
                Q = flows[pipe]

                top += K[pipe]*(abs(Q)**(n-1))*Q*direction
                bot += K[pipe]*(abs(Q)**(n-1))

            bot *= n

            if bot == 0:
                continue

            deltaQ = -top / bot
            max_delta = max(max_delta, abs(deltaQ))

            for pipe, direction in loop:
                pipe -= 1
                flows[pipe] += deltaQ * direction

        if max_delta < precision:
            break

    return flows

## =========================================================
## THERMAL SIMULATION
## =========================================================
def simulate_thermal(flows):

    ## Convert total flow
    total_flow = sum(flows)
    w_mass = total_flow * Density_w   # lbm/s

    ## Initial water temp
    T_water = unit

    ## ---------------------------------------------
    ## PARALLEL HEAT EXCHANGERS
    ## ---------------------------------------------
    HX_out_temps = []

    for demand in HX_demand:

        if w_mass <= 1e-10:
            HX_out_temps.append(T_water)
            continue

        deltaT = demand / (w_mass * c_w * unit['hr'])
        HX_out_temps.append(T_water - deltaT)

    ## Mixed temperature after parallel HX bank
    T_mixed = sum(HX_out_temps) / len(HX_out_temps)

    ## ---------------------------------------------
    ## RETURN HEAT EXCHANGER (NTU METHOD)
    ## ---------------------------------------------
    w_flow = total_flow / Density_w             # ft^3/s
    w_flow_gpm = w_flow*(unit['ft']**3/unit['gpm'])

    capacity_w = c_w * w_mass * unit['hr']
    capacity = sorted([capacity_w, capacity_air])

    if capacity[0] < 1e-10:
        eff = 1
    else:
        Cr = capacity[0] / capacity[1]
        NTU = U(w_flow_gpm) * A_hx / capacity[0]

        if capacity_air > capacity_w:
            eff = utl.eff_crossflow(Cr, NTU, 'max')
        else:
            eff = utl.eff_crossflow(Cr, NTU, 'min')

    T_out = T_mixed - eff * capacity[0] * (T_mixed - T_air_out) / capacity_w

    return {
        "T_parallel_out": unit['R>F'](T_mixed),
        "T_final": unit['R>F'](T_out)
    }

## =========================================================
## HEAD LOSS CALCULATION (OPTIONAL INTEGRATION POINT)
## =========================================================
def compute_head_losses(flow):

    ## Example single-pipe evaluation using your original logic
    Rough = 0.02
    D = 0.1722
    L = 100
    cross_area = np.pi*(D/2)**2

    f_t = 0.3086/np.log10((Rough/(3.7*D))**1.11)**2
    k_min = 10*hmin.fittings['elb90'](f_t)
    k_min += 6*hmin.fittings['gate'](f_t)

    w_flow = flow / Density_w
    u_w = w_flow / cross_area

    Re = u_w * D / Nu

    if Re <= 1e-8:
        f = 0
    elif Re < 2300:
        f = 64/Re
    else:
        f = 0.3086/(np.log10(6.9/Re+np.pow((Rough/(3.7*D)),1.11))**2)

    h_maj = f*(L/D)*(u_w**2/(2*utl.g_c))
    h_min = k_min*(u_w**2/(2*utl.g_c))
    h_hx = utl.HX_HeadLoss(w_flow)

    return h_maj + h_min + h_hx

## =========================================================
## MAIN EXECUTION
## =========================================================
def main():

    print("## Solving hydraulic network...")
    flows = solve_flows(flows_init.copy())

    print("\n## Final flows:")
    for i, Q in enumerate(flows):
        print(f"Pipe {i+1}: {Q:.5f}")

    print("\n## Running thermal simulation...")
    thermal = simulate_thermal(flows)

    print("\n## Thermal Results:")
    print(f"After parallel HX: {thermal['T_parallel_out']:.2f} F")
    print(f"After return HX: {thermal['T_final']:.2f} F")

    ## Example: evaluate head loss for total flow
    total_flow = sum(flows)
    head_loss = compute_head_losses(total_flow)

    print("\n## Estimated system head loss:")
    print(f"{head_loss:.3f} ft")


if __name__ == "__main__":
    main()