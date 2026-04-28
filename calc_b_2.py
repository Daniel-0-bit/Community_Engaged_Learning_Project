import numpy as np

import utility as utl
import minor_loss as hmin

from utility import unit

Pipes = [ #Pipes defined by (length (ft), diameter (in))
    [300, 8],
    [100,10],
    [300,8],
    [100,8],
    [300,10],
    [300,8],
    [300,8]
]

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


k1 = 4.727
n = 1.852
c = 130
ft = 0.014

K = []
for L,D in Pipes:
    K.append((k1*L)/((np.pow(c,n))*np.pow(D,4.8704)))

def Hardy_Cross(
    flows_init=None,
    max_iter=100,
    precision=5e-5,
    dampen=1.0,
    verbose=True
):
    """
    Solve flows using Hardy-Cross method.

    Uses global:
        - Pipes
        - Network
        - K
        - n
    """

    num_pipes = len(Pipes)

    # Default initial guess
    if flows_init is None:
        flows = [1.0 for _ in range(num_pipes)]
    else:
        flows = flows_init.copy()

    history = []

    for I in range(max_iter):

        max_delta = 0.0

        if verbose:
            print(f"Iteration {I}")

        for i, loop in enumerate(Network):

            top = 0.0
            bot = 0.0

            for pipe, direction in loop:
                Q = flows[pipe]

                term = K[pipe] * (abs(Q)**(n - 1))
                top += term * Q * direction
                bot += term

                if verbose:
                    print(f"\tQ{pipe} = {Q}")

            bot *= n

            if abs(bot) < 1e-12:
                if verbose:
                    print("\tSkipping loop (zero denominator)")
                continue

            deltaQ = -top / bot
            max_delta = max(max_delta, abs(deltaQ))

            if verbose:
                print(f"\t\tdeltaQ{i} = {deltaQ}\n")

            for pipe, direction in loop:
                flows[pipe] += deltaQ * dampen * direction

        history.append(max_delta)

        if max_delta < precision:
            if verbose:
                print(f"Converged in {I+1} iterations.\n")
            break

    return flows, history

def main():
    print("Part B Step 2 Simulation")

    flows, history = Hardy_Cross(verbose=True)

    print("Final flows:")
    for i, Q in enumerate(flows):
        print(f"Pipe {i}: {Q:.5f}")

if __name__=="__main__":
    main()