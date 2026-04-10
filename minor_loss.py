hf_minor = lambda a,b,Q: a*Q-b

fittings = {
    'elbow45': lambda q: hf_minor(1,0,q),
    'elbow90': lambda q: hf_minor(1,0,q)
}