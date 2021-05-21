from src import *

sis = input('Selecione sistema de 3 corpos de exemplo: \n'
            '1 - Infinito \n'
            '2 - Com órbita externa \n'
            '3 - Sistema palentário \n'
            '4 - Órbita elíptica \n'
            '-> ')
if sis == '1':
    # sistema de 3 corpos formato infinito;
    # os valores desta e da simulação seguinte são retirados do artigo Coreografias no Problema de Três Corpos Restrito,
    # link: https://doi.org/10.1590/1806-9126-rbef-2017-0401
    a = 0.3471128135672417
    b = 0.532726851767674
    lis = [coisas.Particula(s=[-1, 0], v=[a, b]),
           coisas.Particula(s=[1, 0], v=[a, b]),
           coisas.Particula(s=[0, 0], v=[-2 * a, -2 * b])]
    # crio os objetos dentro de uma lista para facilitar o manuzeio

    minhaSim = sim.Sim()
    minhaSim.add_obj(lis)
    minhaSim.simular(5, h=0.0001)

    minhaSim.configs['lims'] = ((-1.5, 1.5), (-1, 1))  # alterando enquadamento

    minhaSim.animar()
elif sis == '2':
    # um sistema de 3 corpos;
    lis = [coisas.Particula(s=[-1, 0], v=[0, -0.3660350371], m=2, cor='orchid'),
           coisas.Particula(s=[1.254953728, 0], v=[0, 0.4593570344], m=0.5, cor='purple'),
           coisas.Particula(s=[2.745046272, 0], v=[0, 1.004783114], m=0.5, cor='lime')]
    # crio os objetos dentro de uma lista para facilitar o manuzeio

    minhaSim = sim.Sim()
    minhaSim.add_obj(lis)
    minhaSim.simular(10)

    minhaSim.texto((0.5, 0.5), 'Olha só, texto', obj=0)
    minhaSim.configs['vel'] = 2

    minhaSim.animar()

elif sis == '3':
    estrela = coisas.Particula(m=1_000_000, nome='Sol', cor='yellow')
    planeta = estrela.em_orbita(s=[200, 0], m=10000, nome='marte', cor='tomato')
    lua = planeta.em_orbita(s=[205, 0], m=0, nome='phobos', cor='silver')

    sistema = sim.Sim()
    sistema.add_obj(estrela, planeta, lua)

    sistema.configs['lims'] = ((-250, 250), (-250, 250))

    sistema.simular(20)

    sistema.seta(ref0=planeta, ref1=estrela, largura=5)

    sistema.animar()
elif sis == '4':
    a = coisas.Particula(v=(0, 1), cor='lightpink', m=10)
    b = a.em_orbita(s=(0, 2.5), m=1, cor='g', e=0.9)

    s = sim.Sim()
    s.add_obj(a, b)

    s.simular(20)

    s.configs['seguir'] = a
    s.configs['vel'] = 1
    s.area_kepler(a, b, t0=2, t1=4)
    s.area_kepler(a, b, t0=6, t1=8)
    s.rastro(b, ref=a)

    s.animar()
else:
    raise ValueError('Número inválido >:v')
