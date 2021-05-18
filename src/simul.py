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
            self.dados = []  # dados gerados
            self.tempos = []  # insatantes de cada passo
            self.h = 0.01  # passo da simulação (padrão como 0.01)
            self.configs = {'estilo': 'dark_background',  # estilo de fundo
                            'seguir': -1,  # objeto seguido (negativo para nenhum)
                            'xlim': (-5, 5), 'ylim': (-5, 5),  # limites de enquadramento
                            'G': 1}  # Constante da gravitação universal; real = 6.6708e-11; 0 para sem gravidade
            # dicionário de configurações da simulação

    def configurar(self, **kwargs):  # função para configurar detalhes da simulação
        pass  # todo: função de configurar

    def add_obj(self, *args):
        classes = [csa.Particula] + csa.Particula.__subclasses__()  # litsa de todas as classes suportadas na simulação
        try:  # isso serve para determinar se entreram com uma lista (ou iterável) no argumento, ou apenas um objeto
            for a in args:
                iter(a)  # isso levanta um erro de tipo se o argumento não for iterável
                for obj in a:
                    for c in classes:
                        if isinstance(obj, c):  # checa se o objeto é suportado na simulação
                            self.objs.append(obj)
                        else:
                            print(f'{obj}, não é um objeto simulável')
        except TypeError:
            for a in args:
                for c in classes:  # se o argumento não for um iterável,
                    # então deve ser um objeto ou lista de objetos da simulação
                    if isinstance(a, c):  # checa se o objeto é siumlável
                        self.objs.append(a)
                    else:
                        print(f'{a}, não é um objeto simulável')

    def _ar(self, obj):
        gc = self.configs['G']  # pega o valor da constante da gravitação universal
        ar = np.zeros(2)
        for n in self.objs:
            if n is not obj:
                d = obj.s - n.s  # vetor distancia
                ar += - np.array(gc * n.m / (d[0] ** 2 + d[1] ** 2) * d / np.linalg.norm(d))
                # aceleração gravitacional, multiplicada pelo versor da distância
        return ar
        # todo: criar outros modelos de forças e formas de seleciona-los.
        #  note que funções também são objetos e podem ser armazenadas dentro de listas. Portanto, pode-se fazer com que
        #  ar retorne um dicionário com o nome de forças e strings como definições. Pode-se criar uma variável de forças
        #  ativas dentro da classe. Dentre outras opções a se verificar futuramente. O que for feito deve ser a nível
        #  desta classe. Objetos mais complexos que partículas devem herdar desta classe. Reformatar o projeto com isso
        #  em mente.

    def iterar(self):
        h = self.h
        s_list = []  # lista com posição dos objetos em cada iteração
        for o in self.objs:  # calcula os estados para cada objeto
            # atualiza o valor das variáveis do objeto o:
            o.s = o.s + h * o.v
            o.v = o.v + h * self._ar(o)
            s_list.append(o.s)
        return np.array(s_list)

    def simular(self, t, h=0.01):
        if len(self.objs) == 0:
            raise ValueError('Nenhum objeto adicionado a simulação atual.')
        t_hist = np.arange(0, t, h)  # cria uma lista de instantes no intervalo e passo definido
        if self.tempos == []:  # se a lista tempos era vazia, sobscreve ela com t_hist
            self.tempos = t_hist
        else:  # senão, adiciona t_hist ao final de tempos
            np.append(self.tempos, t_hist)
        self.h = h  # atualiza o valor de passo utilizado

        print('Calculando {} iterações e {} interações.'.format(len(t_hist), len(t_hist) * len(self.objs) ** 2))
        s_hist = []  # lista com as posições dos objetos durante toda a simulação
        for _ in t_hist:  # loop de iterações em cada instante
            s_hist.append(self.iterar())  # adiciona as posições do frame à lista de iterações

        if self.dados == []:  # se a lista dados era vazia, sobrescreve ela com s_hist
            self.dados = np.array(s_hist)
        else:  # senão, adicona s_hist ao final de dados
            dados = self.dados.tolist()  # transforma em lista para não perder o formato
            dados.append(s_hist)
            self.dados = np.array(dados)

    def animar(self, fps=30, vel=1.0, salvar_em=''):
        s_hist = self.dados
        h = self.h
        t_hist = self.tempos
        t_total = t_hist[-1] + h  # retoma duração da simulação
        dt = (1 / fps) * vel  # intervalo entre frames
        print('Compilando vídeo. Duração: {}s, numero de frames: {}'.format(t_total / vel, int(t_total / dt)))

        # configurações extras
        plt.style.use(self.configs['estilo'])
        xlim = self.configs['xlim']
        ylim = self.configs['ylim']
        seguir = self.configs['seguir']

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

            # todo: ajustar função para configurar de plot por objeto (cores e raios próprios)
            # todo: adicionar acompanhar centro de massa
            # todo: criar limites adaptáveis

        anim = FuncAnimation(plt.gcf(), func_animar,
                             frames=int(t_total / dt), interval=1000 * dt)  # faz o loop de animação
        if salvar_em != '':
            print(f'Salvando vídeo em {salvar_em}')
            writer = writers['ffmpeg']
            escritor = writer(fps=fps)
            anim.save(salvar_em, escritor)  # salva a animação usando ffmpeg

        print('Exibindo...')
        plt.show()
        plt.close()

    def reset(self):  # reseta a simulação, apagando dados e objetos
        self.dados = []
        self.tempos = []
        self.objs = []
        self.configs = {'estilo': 'dark_barckground', 'seguir': -1,
                        'xlim': (-5, 5), 'ylim': (-5, 5)}  # não esquecer de atualizar
        self.h = 0.01
