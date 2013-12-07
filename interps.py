def lin(a, b, c, d, t):
    e = []
    for i in range(len(a)):
        e.append((b[i] - a[i])*(t - c)/(d - c) + a[i])
#        if e[i]<d < c: e[i]=max(d,e[i])
#        if e[i]>d > c: e[i]=min(d,e[i])
    return e