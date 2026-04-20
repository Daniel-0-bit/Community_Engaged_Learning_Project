gate = {
    1: 0.17,
    0.75: 0.9,
    0.5: 4.5,
    0.25: 24
}

fittings = {
    'elb90_standard': 0.75,
    'gate': lambda o: gate[o]
}