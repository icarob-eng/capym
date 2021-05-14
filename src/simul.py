from src import coisas as csa
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers


class Sim:
    def __init__(self, herdar=None):
        if isinstance(herdar, Sim):  # possibilita herdar as configurações de outra sdimulação
            self.objs = herdar.objs
            self.dados = herdar.dados
            self.tempos = herdar.tempos
            self.configs = herdar.configs
            self.h = herdar.h
        else:
            self.objs = []  # lista de objetos inclusos na simulação
            self.dados = np.empty()  # dados gerados
            self.tempos = np.empty()  # insatantes de cada passo
            self.h = 0.01  # passo da simulação (padrão como 0.01)
            self.configs = {'estilo': 'dark_barckground', 'xlim': (-5, 5), 'ylim': (-5, 5)}
            # dicionário de configurações da simulação
        self.extra_configs(config=self.configs)

    def add_obj(self, *args):
        classes = [csa.Particula] + csa.Particula.__subclasses__()  # litsa de todas as classes suportadas na simulação
        try:  # isso serve para determinar se entreram com uma lista (ou iterável) no argumento, ou apenas um objeto
            a, = args
            iter(a)  # isso levanta um erro de tipo se o argumento não for iterável
            for obj in a:
                for c in classes:
                    if isinstance(obj, c):  # checa se o objeto é suportado na simulação
                        self.objs.append(obj)
                    else:
                        print('{}, não é um objeto simulável'.format(obj))
        except TypeError:
            for a in args:
                for c in classes:  # se o argumento não for um iterável,
                    # então deve ser um objeto ou lista de objetos da simulação
                    if isinstance(a, c):  # checa se o objeto é siumlável
                        self.objs.append(a)
                    else:
                        print('{}, não é um objeto simulável'.format(a))

    def extra_configs(self, **kwargs):  # função para configurar detalhes da simulação
        pass
        # todo: função extra_configs

    def iterar(self):
        h = self.h
        s_list = []  # lista com posição dos objetos em cada iteração
        for i in self.objs:  # calcula os estados para cada objeto
            # atualiza o valor das variáveis do objeto i:
            i.s = i.s + h * i.v
            i.v = i.v + h * i.ar()  # todo: trazer a funçaõ ar() para esta classe
            s_list.append(i.s)
        return np.array(s_list)

    def simular(self, t, h=0.01):
        self.tempos = np.arange(0, t, h)  # cria uma lista de instantes no intervalo e passo definido
        t_hist = self.tempos
        self.h = h  # atualiza o valor de passo utilizado
        print('Calculando {} iterações e {} interações.'.format(len(t_hist), len(t_hist) * len(self.objs) ** 2))
        s_hist = []  # lista com as posições dos objetos durante toda a simulação
        for tn in t_hist:  # loop de iterações em cada instante
            s_hist.append(self.iterar())  # adiciona as posições do frame à lista de iterações
        self.dados = np.array(s_hist)

    def animar(self, fps=30, vel=1.0, salvar_em='', seguir=-42):
        plt.style.use(self.estilo)
        xlim = self.xlim
        ylim = self.ylim
        s_hist = self.dados
        h = self.h
        t_hist = self.tempos
        t_total = t_hist[-1] + h  # retoma duração da simulação
        dt = 1 / fps * vel  # intervalo entre frames
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
            elif seguir > len(self.objs):
                raise IndexError('Objeto selecionado para seguir fora da lista de objetos. '
                                 'Lembre-se que o índice começa em 0.')
            else:
                plt.xlim(xlim + pos[seguir, 0])  # limite atualizado de acordo com a posição do objeto
                plt.ylim(ylim + pos[seguir, 1])

            plt.scatter(pos[:, 0], pos[:, 1])  # plota os pontos

            # todo: ajustar função para configurar plot por objeto (cores e raios próprios)
            # todo: adicionar acompanhar centro de massa
            # todo: criar limites adaptáveis

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

    def reset(self):  # reseta a simulação, apagando dados e objetos
        self.dados = np.empty()
        self.tempos = np.empty()
        self.configs = {'estilo': 'dark_barckground', 'xlim': (-5, 5), 'ylim': (-5, 5)}  # configurações padrão
        # não esquecer de atualizar
        self.h = 0.01
        for o in self.objs:
            del o
        self.extra_configs(config=self.configs)
