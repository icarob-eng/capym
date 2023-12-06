"""
Script com exemplos de simulações.

Quando executado roda uma lista de exemplos  disponíveis:

1 - Uma solução para o problema de 3 corpos [1] formando um 'infinito'. Também demonstra o recurso de alterar passo da
simulação e limites de enquadramento;

2 - Outra solução ao problema de 3 corpos [1]. A simulação exemplifica o uso do recurso de cores, alteração do tamanho
 do passo, texto na animação e velocidade de reprodução alterada;

3 - Um mini sistema solar, demonstrando os recursos de criar objeto em orbita, cores dos objetos, referencia à objetos
usando nomes, alteração dos limites de enquadramento da simulação e também o desenho de uma seta;

4 - Exemplo de órbita elíptica, com cores custumizadas, enquadramento de simulação móvel, duas áreas para demonstração
da lei das áreas de Kepler e um rastro orbital;

Ver comentários ao longo do código para mais detalhes.

Referências
-----------
[1] QUARESMA, Luciano J. B.; RODRIGUES, Manuel E. Coreografias no Problema de Três Corpos Restrito. Revista Brasileira
de Ensino de Física, [S.L.], v. 41, n. 2, 1 nov. 2018. FapUNIFESP (SciELO). Disponível em:
http://dx.doi.org/10.1590/1806-9126-rbef-2017-0401. Acesso em: 28 maio 2021.
"""


from src.capym import *

sis = input('Selecione sistema de 3 corpos de exemplo: \n'
            '1 - Infinito \n'
            '2 - Com órbita externa \n'
            '3 - Sistema palentário \n'
            '4 - Órbita elíptica \n'
            '-> ')
if sis == '1':
    # sistema de 3 corpos formato infinito;
    a = 0.3471128135672417  # parâmetros necessários para fazer o sistema estável, de acordo com a referência [1]
    b = 0.532726851767674

    lis = [coisas.Particula(s=[-1, 0], v=[a, b]),
           coisas.Particula(s=[1, 0], v=[a, b]),
           coisas.Particula(s=[0, 0], v=[-2 * a, -2 * b])]
    # cria os objetos dentro de uma lista para facilitar o manuzeio

    minhaSim = sim.Sim()  # cria um objeto simulação
    minhaSim.add_obj(lis)  # adiciona todos os objetos da lista a uma simulação
    minhaSim.simular(5, h=0.0001)  # simula as interações num intervalo de 5s e um passo de 0.0001s

    minhaSim.configs['lims'] = ((-1.5, 1.5), (-1, 1))  # alterando enquadamento

    minhaSim.animar()  # compila e mostra a animação

elif sis == '2':
    # um sistema de 3 corpos;
    # estes valores específicos são necessários para fazer o sistema estável, de acordo com a referência [1]
    lis = [coisas.Particula(s=[-1, 0], v=[0, -0.3660350371], m=2, cor='orchid'),
           coisas.Particula(s=[1.254953728, 0], v=[0, 0.4593570344], m=0.5, cor='purple'),
           coisas.Particula(s=[2.745046272, 0], v=[0, 1.004783114], m=0.5, cor='lime')]
    # cria os objetos dentro de uma lista para facilitar o manuzeio

    minhaSim = sim.Sim()  # cria um objeto simulação
    minhaSim.add_obj(lis)  # adiciona todos os objetos da lista a uma simulação
    minhaSim.simular(10, 0.0001)  # simula as interações num intervalo de 10s e um passo de 0.0001s

    minhaSim.texto('Olha só, texto', (0.5, 0.5), obj=0)  # cria um texto na tela que acopanha o objeto de índice 0
    minhaSim.configs['vel'] = 2  # faz com que a animação seja duas vezes mais rápida

    minhaSim.animar()  # compila e mostra a animação

elif sis == '3':
    estrela = coisas.Particula(m=1_000_000, nome='Sol', cor='yellow')
    # cria um objeto central massivo apelidado de Sol com cor amarela
    planeta = estrela.em_orbita(s=[200, 0], m=10000, nome='marte', cor='tomato')
    # cria um objeto orbitando o Sol, apelidado de marte e com cor de tomate
    lua = planeta.em_orbita(s=[205, 0], m=0, nome='phobos', cor='silver')
    # cria um satélite sem massa em órbita de marte, tendo um apelido de phobos e uma cor de prata
    # Nota: a phobos da vida real tem massa, obviamente, mas esta simulação trabalha com a acelração gravitacional,
    #  fazendo com que isso seja possível

    sistema = sim.Sim()  # cria um objeto de simulação
    sistema.add_obj(estrela, planeta, lua)  # adicona os astros criados à simulação

    sistema.configs['lims'] = ((-250, 250), (-250, 250))  # altera o enquadramento da simulação
    # (veja que os obejtos estão bem distantes)

    sistema.simular(20)  # executa a simulação or 20s usando o passo padrão de h=0.01s

    sistema.seta(ref_a='marte', ref_b='Sol', largura=5)  # cria uma seta (bem feia) de largura especificada partindo
    #  de marte ao Sol

    sistema.animar()  # compila e mostra a animação

elif sis == '4':
    a = coisas.Particula(v=(0, 1), cor='lightpink', m=10)
    # cria uma particula com cor rosa leve e massa 10
    b = a.em_orbita(s=(0, 2.5), m=1, cor='g', e=0.9)
    # cria uma particula em órbita, com cor verde. A excentricidade orbital é 0.9

    s = sim.Sim()  # cria um objeto de simulação
    s.add_obj(a, b)  # adiciona os objetos criados à simulação

    s.simular(20)  # executa a simulação or 20s usando o passo padrão de h=0.01s

    s.configs['seguir'] = a  # faz com que o vídeo acompanhe o objeto `a` no centro da imagem
    s.area_kepler(a, b, inicio=2, parar=4)  # cria uma área de Kepler de 2 a 4 segundos
    #  e permanece exibindo até o fim da simulação
    s.area_kepler(a, b, inicio=6, parar=8, fechar=10)  # cria uma área de Kepler de 2 a 4 segundos
    #  e apra de exibir em t=10
    s.rastro(b, ref=a)  # faz com que o objeto b deixe um rastro

    s.animar()  # compila e mostra a animação

else:
    raise ValueError('Número inválido >:v')
