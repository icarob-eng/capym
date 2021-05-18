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

from src import coisas as csa
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers

formatos_suportados = ('3g2', '3pg', 'amv', 'asf', 'avi', 'dirac', 'drc', 'flv', 'gif', 'm4v', 'mp2', 'mp3', 'mp4',
                       'mjpeg', 'mpeg', 'mpegets', 'mov', 'mkv', 'mxf', 'mxf_d10', 'mxf_opatom', 'nsv', 'null', 'ogg',
                       'ogv', 'rm', 'roq', 'vob', 'webm')


class Sim:
    """
    Classe na qual ficam salvos os dados e configurações de simulação.
    Atributos
    ---------
    objs : list, padrão=[]
        Lista com objetos adiconados à simulação.
    dados : list, padrão=[]
        Lista com posições dos objetos a cada iteração.
    tempos : list, padrão=[]
        Lista com instantes de cada iteração.
    h : float, padrão=0.01
        Passo entre ieterações (em segundos).
    configs : dict, padrão={'estilo': 'dark_background', 'seguir': -1, 'xlim': (-5, 5), 'ylim': (-5, 5), 'fps': 30,
                            'vel': 1, 'G': 1}
        Configurações extras da simulação. Sendo elas:
        estilo: estilo de plot da matplotlib;
        seguir: ínidce do objeto que se o enquadramento irá seguir (negativo para nenhum);
        xlim/ylim: limites de enquadramento;
        fps: fps;
        vel: velocidade de reprodução;
        G: constante da gravitação universal (0 para sem gravidade);

    Métodos
    -------
    add_obj(*args)
        Adicionar objetos ou listan de objetos à simulação.
        (automaticamente atualiza a velociade orbital dos objetos em órbita)
    iterar()
        Iteração simples usando método de Euler
    simulaar(t, h=0.01)
        Executa diversas iterações e rotorna uma lista de passos.
    animar(salvar_em='')
        Anima, mostra e salva simulações.
    reset()
        Reinicia configurações e dados da simulação (limpa objetos).
    """
    def __init__(self, herdar=None):
        """
        Parametros
        ----------
        herdar
            Pode herdar dados e configurações de outras simulações, bastando colocar a oujtra instãncia aqui quando
            for criar esta.
        """
        if isinstance(herdar, Sim):  # possibilita herdar as configurações de outra simulação
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
                            # todo: criar forma de seguir ponteiro, além de índice
                            'xlim': (-5, 5), 'ylim': (-5, 5),
                            'fps': 30, 'vel': 1,  # limites de enquadramento
                            'G': 1}  # Constante da gravitação universal; real = 6.6708e-11; 0 para sem gravidade
            # dicionário de configurações da simulação

    def add_obj(self, *args):
        """
        Método para adiconar objetos a uma simulação.

        Parametros
        ----------
        args
            Objeto ou lista de objetos (suporta vários argumentos ou um iterável). O objeto precisa ser simulável.

        Notas
        -----
        Se o argumento não for de uma classe simulável suportada, será printada uma mensagem avisando isto e ele
        não será adicionado.
        Se o objeto tiver satélites com velocidade orbital não configurada, ela será cnfigurada automaticamente
        usando o G da simulação.
        """
        classes = [csa.Particula] + csa.Particula.__subclasses__()  # litsa de todas as classes suportadas na simulação
        add = []  # lista que reune todos os objetos que serão adicionados
        for a in args:
            try:  # testa se o argumento é iterável ou um objeto
                iter(a)
                for obj in a:  # adiciona todos os objetos do iterável à lista `add`
                    add.append(obj)
            except TypeError:
                add.append(a)  # adiciona o objeto à lista `add`

        for obj in add:  # testa e adiciona todos os objetos reunidos
            for c in classes:
                if isinstance(obj, c):  # checa se o objeto é de uma classe suportada
                    self.objs.append(obj)
                    obj._sim = self
                    obj._def_sats()
                else:
                    print(f'{obj}, não é um objeto simulável')

    def _ar(self, obj):
        gc = self.configs['G']  # pega o valor da constante da gravitação universal
        ar = np.zeros(2)
        for n in self.objs:
            if n is not obj:
                d = obj.s - n.s  # vetor distancia
                ar += - np.array(gc * n.m / (d[0] ** 2 + d[1] ** 2) * d / np.linalg.norm(d))
                # aceleração gravitacional, multiplicada pelo versor da distância
                # aqui se colocaria outras forças a serem adicionadas a `ar`
        return ar

    def iterar(self):
        """
        Iteração básica de uma simulação usando método de Euler. Atualiza todos os valores dos objetos um a um.
        O tamanho do passo é o atributo `h` da simulação

        Retorna
        -------
        ndarray
            Lista de vetores com posições de cada objeto. A ordem dos vetores correpsonde a ordem em que o objeto foi
            adicionado.

        Raises
        ------
        NameError
            Não há nenhum objeto nesta simulação. Tente adicionar objetos usando o método `.add_obj()`.

        Notas
        -----
        Quanto menor o valor de `h` maior precisão/reslução da simulação.
        Um `h` negativo implica em uma simulação voltando no tempo *(teoricamente)*.
        """
        if not self.objs:
            raise NameError('Não há nenhum objeto nesta simulação.'
                            ' Tente adicionar objetos usando o método `.add_obj()`.')
        h = self.h
        s_list = []  # lista com posição dos objetos em cada iteração
        for o in self.objs:  # calcula os estados para cada objeto
            # atualiza o valor das variáveis do objeto o:
            o.s = o.s + h * o.v
            o.v = o.v + h * self._ar(o)
            s_list.append(o.s)
        return np.array(s_list)

    def simular(self, t, h=0.01):
        """
        Executa diversas iterações e retorna um histórico delas. Ao final atualiza as listas `dados` e `tempos`.

        Parâmetros
        ----------
        t : int ou float
            Tempo total da simulação em segundos.
        h: float, padrão= 1/30
            Tamanho do passo entre cada iteração em segundos.

        Notas
        -----
        Essa função transforma `dados` em uma matriz de três dimensões,
        sendo a primeira coordenada uma lista com cada iteração;
        a segunda, uma lista de vetores posição de cada objeto por iteração;
        e a terceira a devida coordenada `x` ou `y`.
        Assim, em `dados[i,o,d]` temos que `i` é o índice de cada Iteração;
        `o`, o índice de cada Objeto na dada iteração;
        e `d` a Direção/coordenada de cada objeto em cada iteração.

        Ver também
        ----------
        iterar()
        """
        if len(self.objs) == 0:
            raise ValueError('Nenhum objeto adicionado a simulação atual.')
        t_hist = np.arange(0, t, h)  # cria uma lista de instantes no intervalo e passo definido
        if not self.tempos:  # se a lista tempos era vazia, sobscreve ela com t_hist
            self.tempos = t_hist
        else:  # senão, adiciona t_hist ao final de tempos
            np.append(self.tempos, t_hist)
        self.h = h  # atualiza o valor de passo utilizado

        print('Calculando {} iterações e {} interações.'.format(len(t_hist), len(t_hist) * len(self.objs) ** 2))
        s_hist = []  # lista com as posições dos objetos durante toda a simulação
        for _ in t_hist:  # loop de iterações em cada instante
            s_hist.append(self.iterar())  # adiciona as posições do frame à lista de iterações

        if not self.dados:  # se a lista dados era vazia, sobrescreve ela com s_hist
            self.dados = np.array(s_hist)
        else:  # senão, adicona s_hist ao final de dados
            dados = self.dados.tolist()  # transforma em lista para não perder o formato
            dados.append(s_hist)
            self.dados = np.array(dados)

    def animar(self, salvar_em=''):
        """
        Plota animação 2D, opcionalmente salva, e a exibe, com base em matplotlib,
        tendo diversas opções de customização, no dicionário ´configs´.
        .. warning:: Para salvar animações se faz necessário ter instalado ffmpeg.

        Parâmetros
        ----------
        salvar_em : string, opcional
            string com diretório do arquivo a ser salvado. Não alterando essa variável nada será salvo.
            .. warning:: O diretório deve incluir o nome do arquivo e ser num fomrato suportado
            Ver variável `formatos_suportados`

        Raises
        ------
        NameError
            Não há dados de simulação neste objeto. Tente fazer uma simulação usando o método `.simular()`.
        UserWarnig
            Este formato de vídeo não é suportado.
            Tente acessar simul.formatos_suportados para ver uma série de opções.
            Sugerido: .mp4
            Erro levantado para substuir o erro da matplolib de quando o formato de vídeo a ser salvo não é supoirtado.


        Exemplos
        --------
        Ver seção executável do script `example.py`.

        Notas
        -----
        Para configurações de animação/vídeo, ver `Sim.configs()`.

        Ver também
        ----------
        Sim.simular()
        Sim.configs
        """
        # configurações
        plt.style.use(self.configs['estilo'])
        xlim = self.configs['xlim']
        ylim = self.configs['ylim']
        seguir = self.configs['seguir']
        vel = self.configs['vel']
        fps = self.configs['fps']

        if not self.tempos:  # se uma simulação não tiver sido feita ele levanta esse erro
            raise NameError('Não há dados de simulação neste objeto.'
                            ' Tente fazer uma simulação usando o método `.simular()`.')
        else:
            s_hist = self.dados
            t_hist = self.tempos
        h = self.h
        t_total = t_hist[-1] + h  # retoma duração da simulação
        dt = (1 / fps) * vel  # intervalo entre frames
        print('Compilando vídeo. Duração: {}s, numero de frames: {}'.format(t_total / vel, int(t_total / dt)))

        def func_animar(f):  # gerador de função animar. f é o frame atual
            t = f * dt  # instante atual
            p = np.argmax(t_hist >= t)  # passo atual (primeiro instate após o frame atual)
            pos = np.array(s_hist[p])  # posições no passo atual

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
            formato = salvar_em.split('.')[-1]  # retorna o texto após o último ponto do diretório
            salvar = True
            if formato not in formatos_suportados:  # checa se o formato está na lista de suportados
                r = input(f'Este formato de vídeo, \'.{formato}\' pode não ser suportado.'
                          f' Tentar mesmo assim? [S/N]\n->')
                if r != 'S':
                    print('Ok, então o vídeo não será salvo.')
                    salvar = False

            try:
                if salvar:  # não tenta salvar a animação se o usuário esitir, acima
                    writer = writers['ffmpeg']
                    escritor = writer(fps=fps)
                    anim.save(salvar_em, escritor)  # salva a animação usando ffmpeg
                    print(f'Vídeo salvo em {salvar_em}')
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
