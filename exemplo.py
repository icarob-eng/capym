from src import *

l = []

sis = input('Selecione sistema de 3 corpos de exemplo: \n1 - Infinito \n2 - Com órbita externa \n->')
if sis == '1':
    # sistema de 3 corpos formato infinito; G = 1
    a = 0.3471128135672417
    b = 0.532726851767674
    l.append(coisas.Particula(s=[-1, 0], v=[a, b]))
    l.append(coisas.Particula(s=[1, 0], v=[a, b]))
    l.append(coisas.Particula(s=[0, 0], v=[-2 * a, -2 * b]))
elif sis == '2':
    # um sistema de 3 corpos; G = 1
    l.append(coisas.Particula(s=[-1, 0], v=[0, -0.3660350371], m=2))
    l.append(coisas.Particula(s=[1.254953728, 0], v=[0, 0.4593570344], m=0.5))
    l.append(coisas.Particula(s=[2.745046272, 0], v=[0, 1.004783114], m=0.5))
else:
    raise ValueError('Poxa! Era 1 ou 2, não tinha muita margem para erro, o que você botou aqui?')

minhaSim = sim.Sim()
minhaSim.add_obj(l)
minhaSim.configs['vel'] = 3
minhaSim.configs['fps'] = 90
minhaSim.simular(10)
minhaSim.animar()
