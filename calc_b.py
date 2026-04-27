import numpy as np

import minor_loss as hmin
import utility as utl
from utility import unit

## =========================================================
## CONSTANTS (FLUID PROPERTIES)
## =========================================================

Density_w = 62.4  
# Density of water (lbm/ft^3)
# Used to convert volumetric flow (ft^3/s) → mass flow (lbm/s)

c_w = 1.0  
# Specific heat capacity of water (BTU/lbm·°F)
# Used in energy balance: Q = m*c_p*ΔT

## =========================================================
## HARDY-CROSS PARAMETERS
## =========================================================

n = 1.852  
# Exponent in Hazen-Williams / empirical head loss model
# Governs nonlinearity of flow resistance

C = 130  
# Hazen-Williams roughness coefficient
# Higher = smoother pipes → lower head loss

max_iter = 100  
# Maximum iterations allowed for Hardy-Cross solver

precision = 5e-5  
# Convergence tolerance for loop flow correction (ΔQ threshold)

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
# Each tuple = (length ft, diameter in)
# Defines physical layout of network segments

K = [
    (4.727 * L) / ((C**n) * (D**4.8704))
    for L, D in pipes
]
# Hydraulic resistance coefficient for each pipe
# Used in Hardy-Cross: h = K * Q^n

flows_init = [0.8, 0.2, 1.2, 1.2, 1, 1, 1]
# Initial guesses for flow in each pipe (ft^3/s)
# Must satisfy continuity roughly but will be corrected

loops = [
    [[1,1],[2,-1],[3,-1],[4,-1]],
    [[1,-1],[5,1],[6,1],[7,-1]]
]
# Hardy-Cross loop definitions
# Each entry = (pipe index, direction sign)
# direction: +1 = loop direction, -1 = opposite

## =========================================================
## HEAT DEMANDS (BUILDINGS)
## =========================================================

HX_demand = [50000, 40000, 30000]
# Heat required by each building (BTU/hr)
# These are fixed energy sinks in the system

HX_branches = [0, 3, 5]
# Mapping: which pipe supplies each building HX
# Each demand corresponds to a branch flow

c_p = 1.0
# Heat capacity of water (BTU/lbm·°F)
# Used for ΔT calculations in each building

## =========================================================
## SUPPLY CONDITIONS (GIVEN SYSTEM BOUNDARY)
## =========================================================

T_supply_in = unit
# Temperature entering supply HX (Rankine)

T_supply_out = unit
# Temperature leaving supply HX (Rankine)
# Defines total energy added to system

Q_total_demand = sum(HX_demand)
# Total thermal load of all buildings (BTU/hr)

m_dot_total = Q_total_demand / (c_p * (T_supply_in - T_supply_out))
# Required total mass flow rate (lbm/s)
# Derived from energy balance: Q = m*c_p*ΔT

Q_vol_total = m_dot_total / Density_w
# Total volumetric flow rate (ft^3/s)
# This is what Hardy-Cross distributes across pipes

## =========================================================
## HARDY-CROSS SOLVER (HYDRAULIC NETWORK)
## =========================================================

def solve_flows(flows):

    for _ in range(max_iter):
        max_delta = 0

        for loop in loops:
            top = 0  
            # Loop head loss imbalance numerator

            bot = 0  
            # Sensitivity denominator (derivative term)

            for pipe, direction in loop:
                pipe -= 1
                Q = flows[pipe]
                # Current flow in pipe (ft^3/s)

                top += K[pipe] * (abs(Q)**(n-1)) * Q * direction
                # Sum of signed head losses around loop

                bot += K[pipe] * (abs(Q)**(n-1))
                # Sum of derivatives dH/dQ approximation

            bot *= n
            # Completes derivative scaling for power law

            if abs(bot) < 1e-12:
                continue

            deltaQ = -top / bot
            # Flow correction for loop

            max_delta = max(max_delta, abs(deltaQ))

            for pipe, direction in loop:
                pipe -= 1
                flows[pipe] += deltaQ * direction
                # Update pipe flows based on loop correction

        if max_delta < precision:
            break

    return flows

## =========================================================
## THERMAL MODEL (PURE ENERGY BALANCE)
## =========================================================

def simulate_thermal(flows):

    HX_out_temps = []
    # Outlet temperature of each building HX

    m_flows = []
    # Mass flow in each HX branch (lbm/s)

    T_supply = T_supply_in
    # Fixed supply temperature entering distribution system

    ## ----------------------------
    ## BUILDING HEAT EXCHANGERS
    ## ----------------------------
    for i, Q in enumerate(HX_demand):

        Q_branch = flows[HX_branches[i]]
        # Volumetric flow in branch supplying building i (ft^3/s)

        m_dot = Q_branch * Density_w
        # Mass flow rate in branch (lbm/s)

        m_flows.append(m_dot)

        if abs(m_dot) < 1e-10:
            HX_out_temps.append(T_supply)
            continue

        deltaT = Q / (m_dot * c_p)
        # Temperature drop required to satisfy building demand

        HX_out_temps.append(T_supply - deltaT)

    ## ----------------------------
    ## MIXING NODE (RETURN LINE)
    ## ----------------------------
    total_m = sum(m_flows)
    # Total mass returning from all branches

    if total_m < 1e-10:
        T_return = T_supply
    else:
        T_return = sum(m*T for m, T in zip(m_flows, HX_out_temps)) / total_m
        # Mass-weighted mixing temperature

    ## ----------------------------
    ## ENERGY CHECK (DIAGNOSTIC)
    ## ----------------------------
    Q_delivered = sum(HX_demand)
    # Total heat extracted by buildings

    return {
        "T_supply_F": unit['R>F'](T_supply),
        "T_return_F": unit['R>F'](T_return),
        "Q_total_BTU_hr": Q_delivered
    }

## =========================================================
## MAIN EXECUTION
## =========================================================

def main():

    print("Solving hydraulic network...")

    flows = solve_flows(flows_init.copy())

    print("\nFinal pipe flows:")
    for i, Q in enumerate(flows):
        print(f"Pipe {i+1}: {Q:.5f} ft^3/s")

    print("\nTotal system flow (from energy balance):")
    print(f"{Q_vol_total:.5f} ft^3/s")

    print("\nRunning thermal model...")

    thermal = simulate_thermal(flows)

    print("\nThermal results:")
    print(f"Supply temperature: {thermal['T_supply_F']:.2f} °F")
    print(f"Return temperature: {thermal['T_return_F']:.2f} °F")
    print(f"Total demand: {thermal['Q_total_BTU_hr']:.1f} BTU/hr")


if __name__ == "__main__":
    main()