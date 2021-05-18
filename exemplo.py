from src import *

p = coisas.Particula(v=(5, 0))
q = coisas.Particula(s=(0, 1), v=(5, 0))
s = simul.Sim()

s.add_obj(p, q)

s.simular(5)
s.animar()
