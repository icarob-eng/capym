from capym import sim
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers

plot_style = 'dark_background'  # variável de estilo de plot possível de ser alterada pelo usuário


def animar_sim(sim_data=None, xlim=(-5, 5), ylim=(-5, 5), seguir=-42,
               vel=1.0, fps=30, salvar_em='', **kwargs):
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
            assert seguir < len(sim.objs), 'Objeto não referenciado corretamente. \n' \
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


if __name__ == '__main__':
    part = sim.Particula(m=1)
    part.em_orbita(s=[-1, 0], m=0.1)
    animar_sim(sim.simular(10, 0.01), xlim=(-2, 2), ylim=(-2, 2), vel=1,
               salvar_em='C:/Users/Ícaro/Desktop/zoo.mp4')
