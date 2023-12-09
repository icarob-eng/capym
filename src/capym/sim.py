import sys
import copy
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from collections.abc import Iterable
from collections import OrderedDict

from src.config.background_style_config import BackgroundStyle
from src.config.simulation_config import SimulationConfig
from src.objects.object import Object

"""
Módulo com classe Sim para simulações.

Classes
-------
Sim
    Classe na qual ficam salvos os dados e configurações de simulação.

Variáveis
---------
formatos_suportados = ('3g2', '3pg', 'amv', 'asf', 'avi', 'dirac', 'drc', 'flv', 'gif', 'm4v', 'mp2', 'mp3', 'mp4',
                       'mjpeg', 'mpeg', 'mpegets', 'mov', 'mkv', 'mxf', 'mxf_d10', 'mxf_opatom', 'nsv', 'null', 'ogg',
                       'ogv', 'rm', 'roq', 'vob', 'webm')
    Lista de formatos suportados para serem salvos. Outros podem funcionar mas não garanto.
"""


supported_formats = ('3g2', '3pg', 'amv', 'asf', 'avi', 'dirac', 'drc', 'flv', 'gif', 'm4v', 'mp2', 'mp3', 'mp4',
                     'mjpeg', 'mpeg', 'mpegets', 'mov', 'mkv', 'mxf', 'mxf_d10', 'mxf_opatom', 'nsv', 'null', 'ogg',
                     'ogv', 'rm', 'roq', 'vob', 'webm')


class Simulation(SimulationConfig):

    def __init__(self, interval: float, objects: list[Object],
                 background_config: BackgroundStyle, final_moment: float, limits: tuple[tuple, tuple],  *args):
        super().__init__(interval, objects, background_config, final_moment, limits)
        self.__objects: list[Object] = []
        self.add_object(args)

        self.__historic: OrderedDict[tuple[float, float], list[Object]] = OrderedDict({
            (self.initial_moment, self.interval): copy.copy(self.__objects)
        })

    @property
    def objects(self) -> list:
        return self.__objects

    def add_object(self, *args):
        if isinstance(args, Iterable):
            for obj in args:
                if obj is not None and isinstance(obj, Object):
                    self.__objects.append(obj)
                else:
                    print(f"{obj} is not a valid argument.", file=sys.stderr)

        elif isinstance(args, Object):
            self.__objects.append(args)

        else:
            print(f"{args} is not a valid argument.", file=sys.stderr)

    def repeated(self) -> None:
        if len(self.__objects) == 0:
            raise NameError("This simulation does not contains any object.")

        with next(reversed(self.__historic)) as ((frame_moment, frame_interval), objects):
            new_frame_moment = frame_moment + frame_interval

            objects_with_new_accelerations: list[Object] = []

            for outer_object in objects:
                for inner_object in objects:
                    if outer_object.uuid != inner_object.uuid:
                        outer_object.acceleration += outer_object.gravitational_acceleration(inner_object,
                                                                                             self.constant_of_gravitation)
                objects_with_new_accelerations.append(outer_object)

            temp_historic = OrderedDict({(new_frame_moment, frame_interval): []})

            for obj in objects_with_new_accelerations:
                obj.velocity += obj.acceleration * frame_interval
                obj.position += obj.velocity * frame_interval
                temp_historic[(new_frame_moment, frame_interval)] += obj

            self.__historic += temp_historic

    def simular(self):
        if len(self.objs) == 0:
            raise ValueError('No objects added to the current simulation.')
        print(f"Simulating {len(self.objs)}")
        for instant in np.arange(0, self.initial_moment, self.interval):
            if instant < self.final_moment:
                print(f"Simulating instant {instant}.")
                self.repeated()
            else:
                break

    def animar(self, target_path=''):
        """
        Plota animação 2D, salva (opcionalmente) e a exibe, com base em matplotlib,
        tendo diversas opções de customização, no dicionário ´configs´.

        .. warning:: Para salvar animações se faz necessário ter instalado ffmpeg.

        Parâmetros
        ----------
        salvar_em : string, opcional
            string com diretório do arquivo a ser salvado. Não alterando essa variável nada será salvo.

            .. warning:: O diretório deve incluir o nome do arquivo e ser num fomrato suportado

            Ver variável `formatos_suportados`

        Raise
        -----
        NameError
            Não há dados de simulação neste objeto. Tente fazer uma simulação usando o método `.simular()`.
        UserWarnig
            Este formato de vídeo não é suportado.
            Tente acessar simul.formatos_suportados para ver uma série de opções.
            Sugerido: .mp4

            Erro levantado para substuir o erro da matplolib de quando o formato de vídeo a ser salvo não é supoirtado.


        Exemplos
        --------
        Ver script `example.py`.

        Notas
        -----
        Para configurações de animação/vídeo, ver `Sim.configs`.

        Ver também
        ----------
        Sim.simular()
        Sim.configs
        """
        # configurações
        plt.style.use(str(self.background_config))
        xlim = self.limits[0]
        ylim = self.limits[1]

        if len(self.__historic) == 0:
            raise NameError('Não há dados de simulação neste objeto.Tente fazer uma simulação usando o método '
                            '`.simular()`.')

        cores = []
        for o in self.objects:
            cores.append(object)

        def func_animar(f):  # gerador de função animar. f é o frame atual
            t = f * dt * vel  # instante atual
            p = np.argmax(tempos >= t)  # passo atual (primeiro instate após o frame atual)
            pos = np.array(dados[p])  # posições no passo atual

            plt.cla()  # limpa o plot anterior
            plt.axis('scaled')

            for func in self._extra_plots:
                func(p)

            if seguir is None:  # configurações de limite responsivo
                plt.xlim(xlim)  # limites fixos
                plt.ylim(ylim)
            elif seguir in self.objs:  # se seguir é objeto da simulação
                ind = self.objs.index(seguir)  # pega o índice do objeto na lista `objs`
                plt.xlim(xlim + pos[ind, 0])  # limite atualizado de acordo com a posição do objeto
                plt.ylim(ylim + pos[ind, 1])
            elif isinstance(seguir, int) and seguir < len(self.objs):  # se for um índice de um objeto
                plt.xlim(xlim + pos[seguir, 0])  # limite atualizado de acordo com a posição do objeto
                plt.ylim(ylim + pos[seguir, 1])

            plt.scatter(pos[:, 0], pos[:, 1], c=cores)  # plota os pontos

        anim = FuncAnimation(plt.gcf(), func_animar,
                             frames=int(t_max / dt), interval=1000 / (vel * fps))  # faz o loop de animação
        if target_path != '':
            formato = target_path.split('.')[-1]  # retorna o texto após o último ponto do diretório
            salvar = True
            if formato not in supported_formats:  # checa se o formato está na lista de suportados
                r = input(f'Este formato de vídeo, \'.{formato}\' pode não ser suportado.'
                          f' Tentar mesmo assim? [S/N]\n->')
                if r != 'S':
                    print('Ok, então o vídeo não será salvo.')
                    salvar = False

            try:
                if salvar:  # não tenta salvar a animação se o usuário esitir, acima
                    writer = writers['ffmpeg']
                    escritor = writer(fps=fps)
                    anim.save(target_path, escritor)  # salva a animação usando ffmpeg
                    print(f'Vídeo salvo em {target_path}')
            except UnicodeDecodeError:
                raise UserWarning('Este formato de vídeo não é suportado.'
                                  '\nTente acessar simul.formatos_suportados para ver uma série de opções.'
                                  '\nSugerido: .mp4')
                # isto serve apenas para substuir o erro do matplolib que é ilegível

        print('Exibindo...')
        plt.show()
        plt.close()

    def reset(self):  # reseta a simulação, apagando dados e objetos
        """Método para limpar dados da simulação e reiniciar configs"""
        self.dados = []
        self.tempos = []
        self.objs = []
        self.configs = {'estilo': 'dark_background',  # estilo de fundo
                        'seguir': -1,  # objeto seguido (negativo para nenhum)
                        'xlim': (-5, 5), 'ylim': (-5, 5),
                        'fps': 30, 'vel': 1,  # limites de enquadramento
                        'G': 1}  # Constante da gravitação universal; real = 6.6708e-11; 0 para sem gravidade
        self.h = 0.01

    def _get_index(self, o):  # função interna que retorna um ínidice de objeto mesmo independente da input
        # assim, serve como tratamento de input para funções aplicadas sobre objetos na simulação
        if o in self.objs:  # se for um objeto propriamente adicionado basta pegar o índice
            ind = self.objs.index(o)  # pega o índice do objeto na lista `objs`
        elif isinstance(o, int) and o < len(self.objs) or o is None:
            ind = o  # ser for um índice ou None, basta retornar isto
        elif isinstance(o, str):  # se for uma string, compara com o nome de todos os objetos da simulação e retorna
            # o primeiro de nome igual
            ind = None
            for i in self.objs:
                if i.nome == o:
                    ind = self.objs.index(i)
                    break
            if ind is None:
                raise ValueError('Nome de objeto não corresponde a nenhum da simulação')
        else:
            raise ValueError('Objeto selecionado não foi adicionado à simulação')
        return ind

    def _extra_plot_time_params(self, inicio, parar, fechar):
        # função que prepara as inputs de tempo das funções de plots extras

        if len(self.tempos) == 0:  # se uma simulação não tiver sido feita ele levanta esse erro
            raise NameError('É necessário executar a simulação antes de adicionar objetos extras de plot.'
                            ' Tente fazer uma simulação usando o método `.simular()`.')

        t0 = inicio
        t1 = parar
        t_max = fechar

        # testam se o objeto é None ou inteiro
        if fechar is None:
            t_max = self.tempos[-1]
            if parar is None:
                t1 = self.tempos[-1]
        else:
            if parar is None:
                t1 = self.tempos[-1]
            elif t1 > t_max:
                t_max = t1

        if t0 == t1 or t0 == t_max:
            print('Objeto de plot com tempo de animação 0')
        elif t1 > self.tempos[-1] or t_max > self.tempos[-1]:
            raise ValueError('Tempos de plotagem do objeto extra fora do intervalo da simulação.')

        return t0, t1, t_max

    def rastro(self, obj, inicio=0, parar=None, fechar=None, cor='tab:gray', ref=None):
        """
        Método que cria objeto gráfico de rastro. Como um percurso feito pela partícula, que altera ao longo do tempo.

        Ele começa a ser exibido em t=`inicio`, para de se atualizar em t=`parar` e deixa de ser exibido em t=`fechar`.

        Se `parar` for None, a animação só irá pausar em t=`fechar`.
        Se `fechar` for None, o objeto só deixará de ser exibido no final da simulação.

        Parâmetros
        ----------
        obj : objeto de classe simulável, int ou str
            Objeto, índice ou nome do objeto que irá deixar o rastro.
        inicio : int ou float, padrão=0
            Instante em que a animação deste objeto gráfico começa.
        parar : int, float ou None, padrão=None
            Instante em que a animação deste objeto gráfico pausa, ou seja, 'congela'.
        fechar : int, float ou None, padrão=None
            Instante em que este objeto gráfico para de ser exibido.
        cor : string, padrão='tab:gray'
            Cor do rastro. Padrão de cores da matplotlib. Ver `coisas.Particula`.
        ref : objeto de classe simulável, int ou str, padrão=None
            Objeto, índice ou nome do objeto que servirá de referencial para as posições do rastro.

        Raise
        -----
        ValueError
            Nome de objeto não corresponde a nenhum da simulação

            Levantado quando se passa uma string inválida como objeto.
        ValueError
            Objeto selecionado não foi adicionado à simulação

            Levantado quando se passa um objeto que não foi adicionado à simulação.
        NameError
            É necessário executar a simulação antes de adicionar objetos extras de plot.
            Tente fazer uma simulação usando o método `.simular()`.

            Levantado quando se chama este método antes de `.simular()`.
        ValueError
            Tempos de plotagem do objeto extra fora do intervalo da simulação.

            Levantado quando se entra com `parar` ou `fechar` maiores que o tamanho da simulação.


        Notas
        -----
        As inputs de tempo e de objetos são todas tratadas pelos mesmos métodos internos `._get_index(o)` e
        `._extra_plot_time_params(inicio, parar, fechar)`.
        O que significa que todas tratam da mesma forma as suas inputs de objetos e tempos:
        pode entrar com qualuqer objeto de classe reconhecida, índice deste objeto na simulação ou `.nome` do objeto e
        estes serão reconhecidos da mesma forma (internamente trabalhamos com índice);
        de forma similar, os tratmentos para `inicio`, `parar` e `fechar` são sempre os mesmos que o descrito (quando
        o método não usa `parar` isto é simplesmente ignorado.

        Este e os ourtos métodos que criam objetos gráficos adicionam uma função a uma lista de funções de plot extras,
        executada cada frame em `.animar()`.

        Ver também
        ----------
        .simular()
        .animar()
        coisas.Particula
        """
        # método que cria função de plotagem de rastro
        ind = self._get_index(obj)  # objeto a deixar rastro
        ref = self._get_index(ref)  # objeto de referencial para o rastro
        t0, t1, t_max = self._extra_plot_time_params(inicio, parar, fechar)

        # funções de tratamento de inputs

        def _plotar_rastro(p):  # função que plota o gráfico do rastro do momento inicial t0 até o atual t
            t = self.tempos[p]  # vê o segundo da iteração atual
            if t0 < t < t_max and p > 0:  # se o intervalo já tiver passado do t_max, não o plota
                # em i == 0 pode surgir um erro de lista vazia
                tempos = np.array(self.tempos)
                dados = np.array(self.dados)  # transforma os dados em array para melhor manipulação
                p0 = np.argmax(tempos >= t0)  # primeiro passo a exibir o plot
                p1 = np.argmax(tempos >= t1)  # ultimo passo a ser animado
                ref_pos_atual = np.zeros(2)
                if ref is not None:
                    ref_pos_atual = dados[p, ref]  # posiçao atual do referencial

                if t > t1:  # se o tempo da animação parou  o rastro apra de ser atualizado
                    p = p1

                abs_pos = dados[p0:p, ind]  # posições do objeto até o momento atual
                if ref is not None:
                    ref_pos = dados[p0:p, ref]  # se o referencial não é nulo, retorna as posições do referencial até
                    # o frame atual
                else:
                    ref_pos = np.zeros(2)  # se o referencial é nulo, não retorna nada

                dists = abs_pos - ref_pos + ref_pos_atual  # calcula as posições em relação a ref e põe junto
                # a posição atual de ref

                x = dists[:, 0]  # separa os valores x e y de dists
                y = dists[:, 1]

                linha = plt.Line2D(x, y, c=cor)  # retorna uma linha com o rastro do objeto
                plt.gca().add_line(linha)  # plota a linha

        self._extra_plots.append(_plotar_rastro)  # retorna a função de plotagem

    def area_kepler(self, foco, satelite, inicio=0, parar=None, fechar=None,
                    cor='tab:cyan', opacidade=0.25, cor_borda='tab:blue'):
        """
        Método que cria um polígono de muitos lados para parecer um setor de elipse que começa no inicio do rastro do
        satélite e termina no foco do setor, e então fechando o polígono.

        Para mais detalhes dos parâmetros, ver `.rastro()`.

        Parâmetros
        ----------
        foco :  objeto de classe simulável, int ou str
            Objeto, índice ou nome do objeto que servirá como foco para o setor de elíptica gerado.
        satelite : objeto de classe simulável, int ou str
            Objeto, índice ou nome do objeto que atuará como 'planeta' orbitando o foco.
        inicio : int ou float, padrão=0
            Instante em que a animação deste objeto gráfico começa.
        parar : int, float ou None, padrão=None
            Instante em que a animação deste objeto gráfico pausa, ou seja, 'congela'.
        fechar : int, float ou None, padrão=None
            Instante em que este objeto gráfico para de ser exibido.
        cor : string, padrão='tab:cyan'
            Cor da área. Padrão de cores da matplotlib. Ver `coisas.Particula`.
        opacidade : float, padrão=0.25
            O 'alpha', a intensidade, da cor. 0 para mais opaco e 1 para mais sólido. Detalhes especificados em
            `coisas.Particula`.
        cor_borda : string, padrão'tab:blue'
            Cor da borda da área exibida. Padrão de cores da matplotlib. Ver `coisas.Particula`.

        Raise
        -----
        ValueError
            Nome de objeto não corresponde a nenhum da simulação

            Levantado quando se passa uma string inválida como objeto.
        ValueError
            Objeto selecionado não foi adicionado à simulação

            Levantado quando se passa um objeto que não foi adicionado à simulação.
        NameError
            É necessário executar a simulação antes de adicionar objetos extras de plot.
            Tente fazer uma simulação usando o método `.simular()`.

            Levantado quando se chama este método antes de `.simular()`.
        ValueError
            Tempos de plotagem do objeto extra fora do intervalo da simulação.

            Levantado quando se entra com `parar` ou `fechar` maiores que o tamanho da simulação.

        Notas
        -----
        Vale lembrar a segunda lei de Kepler: o vetor que liga um planeta e o Sol varre áreas iguais em tempos iguais.
        Ou seja, para uma mesma órbita, qualquer setor de elipse com um mesmo delta_t terá a mesma área.

        Ver também
        ----------
        .rastro()
            Com todos os detalhes dos funcionamentos de métodos de animação de objetos gráficos.
        """
        centro = self._get_index(foco)
        sat = self._get_index(satelite)
        t0, t1, t_max = self._extra_plot_time_params(inicio, parar, fechar)

        # funções para tratar input

        def _plotar_area(p):
            t = self.tempos[p]  # vê o segundo da iteração atual
            if t0 < t < t_max and p > 0:  # se o intervalo já tiver passado, não plota o gráfico
                tempos = np.array(self.tempos)
                dados = np.array(self.dados)  # transforma os dados em array para melhor manipulação
                p0 = np.argmax(tempos >= t0)  # primeiro passo a ser exibido
                p1 = np.argmax(tempos >= t1)  # ultimo passo a ser animado
                centro_pos_atual = dados[p, centro]  # posição atual do centro (para referencial)

                if t > t1:  # se o tempo da animação parou para de atualizar o passo para o polígono
                    p = p1
                sat_pos = dados[p0:p, sat]
                centro_pos = dados[p0:p, centro]  # posições do satélite e centro até o momento atual

                sat_dists = sat_pos - centro_pos + centro_pos_atual  # calcula o rastro do satélite

                pos = sat_dists.tolist()
                pos.append(centro_pos_atual)  # adiciona o centro ao rastro fechando o polígono

                poligono = plt.Polygon(pos, facecolor=cor, alpha=opacidade, edgecolor=cor_borda)  # cria o polígono
                plt.gca().add_patch(poligono)  # plota o polígono

        self._extra_plots.append(_plotar_area)  # retornaa função de plotagem

    def texto(self, texto, local=(0, 0), inicio=0, fechar=None, obj=None,
              cor='w', fonte='serif'):
        """
        Cria um texto estático na animação. No entanto, se um `obj` for definido, o texto tomará esse novo objeto como
        referencial para sua posição.

        Para mais detalhes dos parâmetros, ver `.rastro()`.

        Parâmetros
        ----------
        texto : string
            Texto que será exibido. Tem suporte para formatação LaTex (entretanto use daus barras invertidas ao invés de
            apenas uma). A tipografia não será necessariamente igual a do LaTeX, infelizmente :(
        local : array_like, padrão=(0, 0)
            Posição relativa do texto.
        inicio : int ou float, padrão=0
            Instante em que a animação deste objeto gráfico começa.
        fechar : int, float ou None, padrão=None
            Instante em que este objeto gráfico para de ser exibido.
        obj : objeto de classe simulável, int ou str, padrão=None
            Objeto, índice ou nome do objeto que pode servir de referencial para o movimento do texto.
        cor : string, padrão='w'
            Cor do rastro. Padrão de cores da matplotlib. Ver `coisas.Particula`.
        fonte : string, padrão='serif'
            Padrão de fonte do matplotlib. Detalhes em: https://matplotlib.org/stable/tutorials/text/text_props.html

        Raise
        -----
        ValueError
            Nome de objeto não corresponde a nenhum da simulação

            Levantado quando se passa uma string inválida como objeto.
        ValueError
            Objeto selecionado não foi adicionado à simulação

            Levantado quando se passa um objeto que não foi adicionado à simulação.
        NameError
            É necessário executar a simulação antes de adicionar objetos extras de plot.
            Tente fazer uma simulação usando o método `.simular()`.

            Levantado quando se chama este método antes de `.simular()`.
        ValueError
            Tempos de plotagem do objeto extra fora do intervalo da simulação.

            Levantado quando se entra com `fechar` maior que o tamanho da simulação.

        Ver também
        ----------
        .rastro()
            Com todos os detalhes dos funcionamentos de métodos de animação de objetos gráficos.
        """
        ref_ind = self._get_index(obj)
        rel_pos = np.array(local)  # posição relativa (se tiver objeto como referencial)
        t0, _, t_max = self._extra_plot_time_params(inicio, None, fechar)

        # funções para tratar input

        def _plotar_texto(p):
            t = self.tempos[p]  # vê o segundo da iteração atual
            if t0 < t < t_max and p > 0:  # se o intervalo já tiver passado, não plota o gráfico
                dados = np.array(self.dados)  # transforma em array para facilitar manipulação
                np.argmax(self.tempos >= t0)  # primeiro passo a exibir o plot
                if ref_ind is None:
                    ref = np.zeros(2)  # se não tiver um objeto, não faz anda
                else:
                    ref = dados[p, ref_ind]  # posição atual do objeto

                p = rel_pos + ref  # calcula a posição do texto em relação ao objeto
                plt.text(p[0], p[1], texto, color=cor, fontfamily=fonte)  # plota o texto

        self._extra_plots.append(_plotar_texto)  # retorna a função de plotagem

    def seta(self, pos_a=(0, 0), pos_b=(0, 0), ref_a=None, ref_b=None, inicio=0, fechar=None,
             largura=0.1, cor='tab:cyan', opacidade=1, cor_borda='tab:blue'):
        """
        Cria uma seta do ponto `a` ao ponto `b`. O ponto pode ser apenas `pos_a` ou, se `ref_a` for definido,
        a = pos_a + pos_a

        A seta pode ter cor, cor da borda, opacidade e largura (em relação ao comprimento) alteradas.

        Parâmetros
        ----------
        pos_a : array_like, padrão=(0, 0)
            Posição relativa do ponto a.
        pos_b : array_like, padrão=(0, 0)
            Posição relativa do ponto b.
        ref_a : objeto de classe simulável, int ou str, padrão=None
            Objeto, índice ou nome do objeto que servirá de referência para o ponto a.
        ref_b : objeto de classe simulável, int ou str, padrão=None
            Objeto, índice ou nome do objeto que servirá de referência para o ponto b.
        inicio : int ou float, padrão=0
            Instante em que a animação deste objeto gráfico começa.
        fechar : int, float ou None, padrão=None
            Instante em que este objeto gráfico para de ser exibido.
        largura : int ou float, padrão=0.1
            Largura da seta. Para mais detalhes, ver:
            https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.arrow.html
        cor : string, padrão='tab:cyan'
            Cor da área. Padrão de cores da matplotlib. Ver `coisas.Particula`.
        opacidade : float, padrão=1
            O 'alpha', a intensidade, da cor. 0 para mais opaco e 1 para mais sólido. Detalhes especificados em
            `coisas.Particula`.
        cor_borda : string, padrão'tab:blue'
            Cor da borda da área exibida. Padrão de cores da matplotlib. Ver `coisas.Particula`.

        Raise
        -----
        ValueError
            Nome de objeto não corresponde a nenhum da simulação

            Levantado quando se passa uma string inválida como objeto.
        ValueError
            Objeto selecionado não foi adicionado à simulação

            Levantado quando se passa um objeto que não foi adicionado à simulação.
        NameError
            É necessário executar a simulação antes de adicionar objetos extras de plot.
            Tente fazer uma simulação usando o método `.simular()`.

            Levantado quando se chama este método antes de `.simular()`.
        ValueError
            Tempos de plotagem do objeto extra fora do intervalo da simulação.

            Levantado quando se entra com `fechar` maior que o tamanho da simulação.

        Ver também
        ----------
        .rastro()
            Com todos os detalhes dos funcionamentos de métodos de animação de objetos gráficos.
        """
        pos_a = np.array(pos_a)
        pos_b = np.array(pos_b)
        oa_ind = self._get_index(ref_a)
        ob_ind = self._get_index(ref_b)
        t0, _, t_max = self._extra_plot_time_params(inicio, None, fechar)

        def _plotar_seta(p):
            t = self.tempos[p]  # vê o segundo da iteração atual
            if t0 < t < t_max and p > 0:  # se o intervalo já tiver passado, não plota o gráfico
                dados = np.array(self.dados)  # transforma os dados em array para melhor manipulação
                if ref_a is None:  # se ref0 é None, o referencial é 0
                    obj_a = np.zeros(2)
                else:  # senão, o referencial é a posição atual
                    obj_a = np.array(dados[p, oa_ind])
                if ref_b is None:  # idem do sobrescrito
                    obj_b = np.zeros(2)
                else:  # bis in idem
                    obj_b = np.array(dados[p, ob_ind])

                p = pos_a + obj_a  # calcula a posição de partida do vetor somado ao referencial
                delta_p = pos_b + obj_b - p  # o vetor em se partindo de p com referencial a outro objeto

                plt.arrow(p[0], p[1], delta_p[0], delta_p[1],
                          facecolor=cor, alpha=opacidade, edgecolor=cor_borda, width=largura)
                # plota o a seta

        self._extra_plots.append(_plotar_seta)  # retorna a função de plotagem
