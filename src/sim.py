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
    Classe na qual ficam salvos os dados e configurações de simulação. É possível herdar valores já configurados, copiar
    uma simulação simplesmente passando a instância da qual vai ser herdada os valores como parâmetro no construtor da
    classe.

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
        lims: limites de enquadramento;
        fps: fps;
        vel: velocidade de reprodução;
        G: constante da gravitação universal (0 para sem gravidade);

    Métodos
    -------
    add_obj(*args)
        Adicionar objetos ou listan de objetos à simulação.
        (automaticamente atualiza a velociade orbital dos objetos em órbita)
    iterar()
        Iteração simples usando método de Euler.
    simulaar(t, h=0.01)
        Executa diversas iterações e rotorna uma lista de passos.
    animar(salvar_em='')
        Anima, exibe e salva simulações.
    reset()
        Reinicia configurações e dados da simulação (limpa objetos).

    Outros métodos
    --------------
    rastro(obj, inicio=0, parar=None, fechar=none, cor='tab:gray', ref=None)
        Faz com que o objeto `obj` exiba o rastro simulado.
    area_kepler(obj_central, satelite, inicio=0, parar=None, fechar=None,
                cor='tab:cyan', opacidade=0.25, cor_borda='tab:blue')
        Faz com que o objeto `satelite` forme uma setor para ilustrar a segunda lei de Kepler.
    texto(texto, local=(0, 0), inicio=0, fechar=None, obj=None, cor='w', fonte='serif')
        Cria um texto que pode ficar estático ou acompanhar um objeto `obj`.
    seta(self, pos0=(0, 0), pos1=(0, 0), ref0=None, ref1=None, inicio=0, fechar=None, largura=0.1,
         cor='tab:cyan', opacidade=1, cor_borda='tab:blue')
        Cria uma seta que pode ser entre dois pontos estáticos ou relativos a objetos.

    Exemplos
    --------
    Aqui um exemplo da estrutura do uso dessa classe e da simulação no geral:

    # cria-se os objetos simuláveis

    # cria-se um objeto de simulação

    # configura a simulação usando o `.configs`

    # adiciona-se os objetos pelo `.add_obj()`

    # executa a simulação com `.simular()`

    # põe-se objetos gráficos e plots extras

    # compila e anima tudo com `.animar()`

    Notas
    -----
    O atributo `.configs` é essencial para configurar parâmetros de simulação e animação, então deve ser configurado
    o quanto antes, já que não adianta alterar `G` depois que a simulação já foi feita, embora os parâmetros estéticos
    só precisam ser configurados após a animaçaõ mesmo.

    Os métodos em 'Outros métodos' são todos 'plots extras', ou seja, objetos geometricos e meramente gráficos que não
    tem nenhum efeito físico. Devem ser configuradas depois de feita a simulação, mas antes de feita a animação.
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
            self.h = herdar.h
            self.configs = herdar.configs
            self._extra_plots = []
        else:
            self.objs = []  # lista de objetos inclusos na simulação
            self.dados = []  # dados gerados
            self.tempos = []  # insatantes de cada passo
            self.h = 0.01  # passo da simulação (padrão como 0.01)
            self.configs = {'estilo': 'dark_background',  # estilo de fundo
                            'seguir': None,  # objeto seguido
                            'lims': ((-5, 5), (-5, 5)),  # limites de enquadramento
                            'fps': 30, 'vel': 1,
                            'G': 1}  # Constante da gravitação universal; real = 6.6708e-11; 0 para sem gravidade
            # dicionário de configurações da simulação

            self._extra_plots = []  # lisat de funções plotando certas estruturas (como rastros)

            # todo: ver como faz para centro de massa (função que retorna um CM com todos os objetos?)

    def add_obj(self, *args):
        """
        Método para adicionar objetos a uma simulação.

        Parametros
        ----------
        args
            Objeto ou lista de objetos (suporta vários argumentos ou um iterável). O objeto precisa ser simulável.

        Notas
        -----
        Se o argumento não for de uma classe simulável suportada, será printada uma mensagem avisando isto e ele
        não será adicionado.

        Se o objeto tiver satélites com velocidade orbital não configurada, ela será cnfigurada automaticamente
        usando o G da simulação, então altere o G antes de adicionar objetos, por favor.
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
                # todo: fazer com que cada calculo de força específico seja opcional
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

        Raise
        -----
        NameError
            Não há nenhum objeto nesta simulação. Tente adicionar objetos usando o método `.add_obj()`.

        Notas
        -----
        Quanto menor o valor de `h` maior precisão/reslução da simulação.
        Um `h` negativo implica em uma simulação voltando no tempo *(teoricamente)*.
        """
        if len(self.objs) == 0:
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
        Executa diversas iterações e retorna um histórico delas. Ao final atualiza as listas `.dados` e `.tempos`.

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

        Raise
        -----
        ValueError
            Nenhum objeto adicionado a simulação atual.

        Ver também
        ----------
        iterar()
        """
        if len(self.objs) == 0:
            raise ValueError('Nenhum objeto adicionado a simulação atual.')
        t_hist = np.arange(0, t, h)  # cria uma lista de instantes no intervalo e passo definido
        if len(self.tempos) == 0:  # se a lista tempos era vazia, sobscreve ela com t_hist
            self.tempos = t_hist
        else:  # senão, adiciona t_hist ao final de tempos
            np.append(self.tempos, t_hist)
        self.h = h  # atualiza o valor de passo utilizado

        print('Calculando {} iterações e {} interações.'.format(len(t_hist), len(t_hist) * len(self.objs) ** 2))
        s_hist = []  # lista com as posições dos objetos durante toda a simulação
        for _ in t_hist:  # loop de iterações em cada instante
            s_hist.append(self.iterar())  # adiciona as posições do frame à lista de iterações

        if len(self.dados) == 0:  # se a lista dados era vazia, sobrescreve ela com s_hist
            self.dados = np.array(s_hist)
        else:  # senão, adicona s_hist ao final de dados
            dados = self.dados.tolist()  # transforma em lista para não perder o formato
            dados.append(s_hist)
            self.dados = np.array(dados)

    def animar(self, salvar_em=''):
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
        plt.style.use(self.configs['estilo'])
        xlim = self.configs['lims'][0]
        ylim = self.configs['lims'][1]
        seguir = self.configs['seguir']
        vel = self.configs['vel']
        fps = self.configs['fps']

        if len(self.tempos) == 0:  # se uma simulação não tiver sido feita ele levanta esse erro
            raise NameError('Não há dados de simulação neste objeto.'
                            ' Tente fazer uma simulação usando o método `.simular()`.')
        else:
            dados = self.dados
            tempos = self.tempos

        h = self.h
        t_max = tempos[-1] + h  # retoma duração da simulação
        dt = (1 / fps)  # intervalo entre frames
        print('Compilando vídeo. Duração: {}s, numero de frames: {}'.format(t_max / vel, int(t_max / dt)))

        cores = []
        for o in self.objs:
            cores.append(o.cor)

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

            # todo: adicionar acompanhar centro de massa
            # todo: criar limites adaptáveis

        anim = FuncAnimation(plt.gcf(), func_animar,
                             frames=int(t_max / dt), interval=1000 / (vel * fps))  # faz o loop de animação
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
