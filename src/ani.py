from src import sim
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers

plot_style = 'dark_background'  # variável de estilo de plot possível de ser alterada pelo usuário

# todo: trocar asserts por try ... except em amimar_aim()


def animar_sim(sim_data=None, fps=30, vel=1.0, salvar_em='',
               xlim=(-5, 5), ylim=(-5, 5), seguir=-42, **kwargs):
    """
    Plota animação 2D, opcionalmente salva, e a exibe, com base em matplotlib, tendo diversas opções de customização.
    .. warning:: Para salvar animações se faz necessário ter instalado ffmpeg.

    Parâmetros
    ----------
    sim_data : ndarray, ndarray
        Arrays 's_hist' e 't_hist' de sim.simular().
    fps : int ou float, padrão=30
    vel : int ou float, padrão=1.0
        Velocidade de reprodução
    salvar_em : string, opcional
        string com diretório do arquivo a ser salvado. Não alterando essa variável nada será salvo.
        .. warning:: O diretório deve incluir o nome do arquivo e ser no formato .mp4
    xlim : iterável de comprimento 2, padrão=(-5, 5)
        'Campo de visão' ou tamanho do enquadramento na direção x, em coordenadas do sistema.
    ylim : iterável de comprimento 2, padrão=(-5, 5)
        'Campo de visão' ou tamanho do enquadramento na direção y, em coordenadas do sistema.
    seguir : int, opcional
        Índice de objeto um objeto na lista '_objs' ou ordem em que ele foi criado, para a 'câmera' acompanhar
        e atualizar os limites.
    kwargs
        Ver Raises

    Raises
    ------
    Argumentos dos dados de simulação não preenchidos devidamente.
        animar_sim() necessita que se entre como argumentos, ou uma simulação sim.simular(),
        ou com uma lista de vetores posição em cada iteração \'s_hist=\' e uma lista de de instantes \'t_hist\'

    Exemplos
    --------
    Ver seção executável do módulo sim.py.

    Notas
    ------
    Até o momento 'animar_sim()' ainda depende da importação de sim.py e sua manipulação de objetos.

    O estilo deplotagem pode ser alterado pela variavel global 'plot_style'.
    Para mais informações visite a seção plot styles da biblioteca matplotlib.

    Ver também
    ----------
    sim.simular()

    """
    plt.style.use(plot_style)
    if sim_data is not None:  # essas condicionais servem para aceitar tanto a função simulate, como entrada quanto
        # os vetores posição e lista de iterações, separadamente
        s_hist, t_hist = sim_data
    else:
        assert ('s_hist' and 't_hist') in kwargs, 'Argumentos dos dados de simulação não preenchidos devidamente. \n' \
                      'animar_sim() necessita que se entre como argumentos, ou uma simulação sim.simular(),' \
                      'ou com uma lista de vetores posição em cada iteração \'s_hist=\'' \
                                                  'e uma lista de de instantes \'t_hist\''
        s_hist = kwargs['s_hist']
        t_hist = kwargs['t_hist']

    s_hist = np.array(s_hist)  # para garantir que é uma array
    t_hist = np.array(t_hist)
    h = t_hist[1] - t_hist[0]  # tamanho do passo
    t_total = t_hist[-1] + h  # retoma duração da simulação
    dt = 1/fps * vel  # intervalo entre frames
    print('Compilando vídeo. Duração: {}s, numero de frames: {}'.format(t_total / vel, int(t_total / dt)))

    def func_animar(f):  # gerador de função animar. f é o frame atual
        t = f * dt  # instante atual
        p = np.argmax(t_hist >= t)  # passo atual (primeiro instate após o frame atual)
        pos = s_hist[p]  # posições no passo atual

        plt.cla()  # limpa o plot anterior
        plt.axis('scaled')

        if seguir < 0:  # configurações de limite responsivo
            plt.xlim(xlim)  # limites fixos
            plt.ylim(ylim)
        else:
            assert seguir < len(sim._objs), 'Objeto não referenciado corretamente. \n' \
                                           'Deve-se colocar a ordem em que ele foi criado (ex: 0,1,2,3... etc)'
            plt.xlim(xlim + pos[seguir, 0])  # limite atualizado de acordo com a posição do objeto
            plt.ylim(ylim + pos[seguir, 1])

        plt.scatter(pos[:, 0], pos[:, 1])  # plota os pontos

        # todo: ajustar função para configurar plot por objeto (cores e raios próprios)
        # todo: adicionar acompanhar centro de massa

    anim = FuncAnimation(plt.gcf(), func_animar,
                         frames=int(t_total / dt), interval=1000 * dt)  # faz o loop de animação
    if salvar_em != '':
        print('Salvando vídeo em {}'.format(salvar_em))
        Escritor = writers['ffmpeg']
        escritor = Escritor(fps=fps)
        anim.save(salvar_em, escritor)  # salva a animação usando ffmpeg

    print('Exibindo...')
    plt.show()
    plt.close()
