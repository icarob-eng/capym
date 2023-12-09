"""Código do autor usado para gerar algumas animações para aulas"""

from src.capym import *

r = int(input('Número da apresentação: '))
dire = 'C:/Users/Ícaro/Desktop/ani.gif'  # + str(r) + '.mp4'

if r == 1:
    a = coisas.Particula((-2, 0))
    b = coisas.Particula((2, 0))

    s = sim.Sim()
    s.add_object(a, b)
    s.configs['lims'] = ((-5, 5), (-1, 1))

    s.simular(7.5)
    s.animar(target_path=dire)
elif r == 2:
    a = coisas.Particula((-4.5, 0))
    b = coisas.Particula((4.5, 0))

    s = sim.Sim()
    s.add_object(a, b)
    s.configs['lims'] = ((-5, 5), (-1, 1))

    s.simular(20)
    s.animar(target_path=dire)
elif r == 3:
    a = coisas.Particula((-4.5, 0), m=10)
    b = coisas.Particula((4.5, 0), m=10)

    s = sim.Sim()
    s.add_object(a, b)
    s.configs['lims'] = ((-5, 5), (-1, 1))

    s.simular(10)
    s.animar(target_path=dire)
elif r == 4:
    a = coisas.Particula(m=10)
    b = coisas.Particula(s=(2, 0), v=(0, 2), cor='tab:green')

    s = sim.Sim()
    s.add_object(a, b)

    s.simular(10)
    s.animar(target_path=dire)
elif r == 5:
    c = coisas.Particula(m=100)
    a = c.em_orbita([0, -1], m=0, e=0, cor='tab:green')
    b = c.em_orbita([0, -1], m=0, e=0.7)
    s = sim.Sim()

    s.add_object(a, b, c)

    s.simular(10)

    s.rastro(a)
    s.rastro(b)

    s.configs['lims'] = ((-3, 3), (-3, 3))
    s.animar(target_path=dire)
elif r == 6:
    c = coisas.Particula(m=10)
    a = c.em_orbita(s=(-1, 0), m=0, e=0.8)

    s = sim.Sim()
    s.add_object(c, a)
    s.simular(20)
    s.configs['lims'] = ((-3, 3), (-3, 3))

    s.rastro(a)
    s.area_kepler(c, a, inicio=6, parar=7)
    s.area_kepler(c, a, inicio=9, parar=10)

    s.animar(target_path=dire)
elif r == 7:
    a = coisas.Particula()
    b = coisas.Particula(s=(1, 0), v=(0, 1), cor='tab:green')

    s = sim.Sim()
    s.add_object(a, b)

    s.simular(10)
    s.animar(target_path=dire)
elif r == 8:
    a = coisas.Particula()
    b = coisas.Particula(s=(1, 0), v=(0, 1), cor='tab:green')

    s = sim.Sim()
    s.add_object(a, b)

    s.configs['lims'] = ((-2, 2), (-2, 2))
    s.configs['seguir'] = a

    s.simular(10)
    s.animar(target_path=dire)
elif r == 9:
    a = coisas.Particula(m=10)
    b = coisas.Particula(s=(1, 0), v=(0, 2), cor='tab:green')

    s = sim.Sim()
    s.add_object(a, b)

    s.simular(10)
    s.animar(target_path=dire)
