# problem specification for q1

from bnetbase import *

a = Variable('a', [1, 0])
b = Variable('b', [1, 0])
c = Variable('c', [1, 0])
d = Variable('d', [1, 0])
e = Variable('e', [1, 0])
f = Variable('f', [1, 0])
g = Variable('g', [1, 0])
h = Variable('h', [1, 0])
i = Variable('i', [1, 0])

Fa = Factor('P(a)', [a])
Fa.add_values([[1, 0.9],
               [0, 0.1]])

Fbah = Factor('P(b|ah)', [b, a, h])
Fbah.add_values([[1, 1, 1, 1.0],
                 [1, 1, 0, 0.0],
                 [1, 0, 1, 0.5],
                 [1, 0, 0, 0.6],
                 [0, 1, 1, 0.0],
                 [0, 1, 0, 1.0],
                 [0, 0, 1, 0.5],
                 [0, 0, 0, 0.4]])

Fcbg = Factor('P(c|bg)', [c, b, g])
Fcbg.add_values([[1, 1, 1, 0.9],
                 [1, 1, 0, 0.9],
                 [1, 0, 1, 0.1],
                 [1, 0, 0, 1.0],
                 [0, 1, 1, 0.1],
                 [0, 1, 0, 0.1],
                 [0, 0, 1, 0.9],
                 [0, 0, 0, 0.0]])

Fdcf = Factor('P(d|cf)', [d, c, f])
Fdcf.add_values([[1, 1, 1, 0.0],
                 [1, 1, 0, 1.0],
                 [1, 0, 1, 0.7],
                 [1, 0, 0, 0.2],
                 [0, 1, 1, 1.0],
                 [0, 1, 0, 0.0],
                 [0, 0, 1, 0.3],
                 [0, 0, 0, 0.8]])

Fec = Factor('P(e|c)', [e, c])
Fec.add_values([[1, 1, 0.2],
                [1, 0, 0.4],
                [0, 1, 0.8],
                [0, 0, 0.6]])

Ff = Factor('P(f)', [f])
Ff.add_values([[1, 0.1],
               [0, 0.9]])

Fg = Factor('P(g)', [g])
Fg.add_values([[1, 1.0],
               [0, 0.0]])

Fh = Factor('P(h)', [h])
Fh.add_values([[1, 0.5],
               [0, 0.5]])

Fib = Factor('P(i|b)', [i, b])
Fib.add_values([[1, 1, 0.3],
                [1, 0, 0.9],
                [0, 1, 0.7],
                [0, 0, 0.1]])


net = BN('q1 net',
         [a, b, c, d, e, f, g, h, i],
         [Fa, Fbah, Fcbg, Fdcf, Fec, Ff, Fg, Fh, Fib])

a.set_evidence(1)
q1a = VE(net, b, [a])
print('a) ', q1a[0])

a.set_evidence(1)
q1b = VE(net, c, [a])
print('b) ', q1b[0])

a.set_evidence(1)
e.set_evidence(0)
q1c = VE(net, c, [a, e])
print('c) ', q1c[0])

a.set_evidence(1)
f.set_evidence(0)
q1d = VE(net, c, [a, f])
print('d) ', q1d[0])
