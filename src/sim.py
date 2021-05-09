import numpy as np

_objs = []  # lista global de objetos de todas as classes
G = 1  # 6.6708e-11  # constante da gravitação universal

# todo: documentação dos módulos


class Particula:
    """
    Classe base para todos os objetos da simulação em 2D.
    Contem apenas posição inicial, velocidade inicial e massa de modo que não há colisões.
    Um ponteiro no final da lista '_objs' é adicionado em toda instânciação, apontando para ele.

    Parâmetros
    ----------
    s : iterável (lista, tupla, ndarray, etc.) de formato (2,), padrão=[0,0]
        Posição da partícula no início da simulação.
        Independente do tipo de iterável, o código transforma em ndarray.
    v : iterável (lista, tupla, ndarray, etc.) de formato (2,), padrão=[0,0]
        Velocidade da partícula no início da simulação.
        Independente do tipo de iterável, o código transforma em ndarray.
    m : int ou float, padrão=1.0
        Massa da partícula.

    Atributos
    ---------
    s : ndarray
        Vetor posição da partícula.
    v : ndarray
        Vetor velocidade da partícula.
    m : int ou float
        Massa da partícula.
    index : int
        Indíce do objeto na lista _objs.

    """
    def __init__(self, s=[0, 0], v=[0, 0], m=1.0):
        self.s = np.array(s)  # vetor de posição
        self.v = np.array(v)  # vetor de velocidade
        self.m = m  # massa do objeto
        self.index = len(_objs)  # armazena o endereço do próprio objeto na lista _objs
        _objs.append(self)  # adiciona o objeto à lista de pointers

        # todo: adicionar opção de customizar cores

    def ar(self):  # método para retornar o vetor de acleração resultante
        """
        Calcula o vetor aceleração resultante. No momento apeans a aceleração gravitacional é calculada
        comparando, a partir da distância entre o objeto atual e todos os outros.

        Parâmetros
        ----------
        Nenhum

        Retorna
        -------
        ar : ndarray
            Vetor 2D com a aceleração resultante no objeto.

        Notas
        -----
        A equação usada para determinar a aceleração gravitacional de cada objeto é

        .. math:: g = GM/(x^2 + y^2) * [x,y]/|[x,y]|

        """
        ar = np.zeros(2)
        for n in _objs:
            if n != self:
                d = self.s - n.s  # vetor distancia
                ar += - np.array(G * n.m / (d[0] ** 2 + d[1] ** 2) * d / np.linalg.norm(d))
                # aceleração gravitacional, multiplicada pelo versor da distância
        return ar

        # todo: criar outros modelos de forças e formas de seleciona-los.
        #  note que funções também são objetos e podem ser armazenadas dentro de listas. Portanto, pode-se fazer com que
        #  ar retorne um dicionário com o nome de forças e strings como definições. Pode-se criar uma variável de forças
        #  ativas dentro da classe. Dentre outras opções a se verificar futuramente. O que for feito deve ser a nível
        #  desta classe. Objetos mais complexos que partículas devem herdar desta classe. Reformatar o projeto com isso
        #  em mente.

    def em_orbita(self, s, m=1.0, sentido=True):  # cria automaticamente um novo objeto em velocidade orbital
        """
        Cria um novo objeto da classe Particula com velocidade orbital em relação à instânia que chamou este método.

        Parâmeteros
        ----------
        s : iterável de formato (2,)
            Posição da partícula no início da simulação.
            Independente do tipo de iterável, o código transforma em ndarray.
        m : int o float, padrão=1.0
            Massa da partícula.
        sentido : bool, padrão=True
            True definido como sentido horáiro e False como anti-horário.

        Retorna
        -------
        Particula
            Retorna um objeto da classse partícula em velocidade orbital ao redor do objeto que chamou o método.

        """
        # sentido=True -> horário, sentido=False -> anti-horário
        s = np.array(s)
        d = s - self.s  # vetor distância
        mod_v = np.sqrt(G * self.m / abs(np.linalg.norm(d)))  # módulo da velocidade orbital
        angle = np.arccos(d[0] / abs(np.linalg.norm(d)))
        if sentido:
            angle -= np.pi / 2  # calcula a inclinação do vetor v
        else:
            angle += np.pi / 2  # no senitdo horáiro ou anti-horáio
        v = np.array([mod_v * np.cos(angle), mod_v * np.sin(angle)]) + self.v
        # a adição da velocidade do objeto principal serve para anular a velocidade relativa
        return Particula(s, v, m)


def limpar_objetos():  # função para limpar a lista de objetos (reiniciar simulações)
    """
    Limpa a lista '_objs' apagando todos os objetos.

    Notas
    -----
    Útil apenas para mais de uma simulação no mesmo código.

    """
    global _objs
    for n in _objs:
        del n


def colisao():
    pass  # função que terá as colisões entre objetos


def iterar(h=1/30):  # padrão definido para 30 FPS
    """
    Iteração básica de uma simulação usando método de Euler. Atualiza todos os valores dos objetos um a um.

    Parâmetros
    ----------
    h: float, padrão= 1/30
        Tamanho do passo entre cada iteração em segundos.

    Retorna
    -------
    ndarray
        Lista de vetores com posições de cada objeto. A ordem dos vetores correpsonde ao índice do objeto em '_objs'.

    Notas
    -----
    Quanto menor o valor de h maior precisão/reslução da simulação.
    Um h negativo implica em uma simulação voltando no tempo, teoricamente.

    """
    s_list = []  # lista com posição dos objetos em cada iteração
    for i in _objs:  # calcula os estados para cada objeto
        # atualiza o valor das variáveis do objeto i:
        i.s = i.s + h * i.v
        i.v = i.v + h * i.ar()
        s_list.append(i.s)
        colisao()
    return np.array(s_list)


def simular(t, h=1/30):  # função com as iterações em loop do sistema. Padrão definido para 30 FPS
    """
    Executa diversas iterações e retorna um histórico delas.

    Parâmetros
    ----------
    t : int ou float
        Tempo total da simulação em segundos.
    h: float, padrão= 1/30
        Tamanho do passo entre cada iteração em segundos.

    Retorna
    -------
    s_hist : ndarray
        Vetor com cada elemento sendo vetores posições de cada objeto em cada iteração
    t_hist : ndarray
        Vetor com o instante de cada iteração.

    Notas
    -----
    Essa função retorna uma matriz de ranque três, sendo a primeira coordenada uma lista com cada iteração;
    a segunda, uma lista de vetores posição de cada objeto por iteração; e a terceira a devida coordenada x ou y.
    Assim, em 's_hist[i,o,d]' temos que 'i' é o índice de cada Iteração;
    'o', o índice de cada Objeto na dada iteração; e 'd' a Direção/coordenada de cada objeto em cada iteração.

    Ver também
    ----------
    iterar()

    """
    t_hist = np.arange(0, t, h)  # cria uma lista de instantes no intervalo e passo definido
    print('Calculando {} iterações e {} interações.' .format(len(t_hist), len(t_hist) * len(_objs) ** 2))
    s_hist = []  # lista com as posições dos objetos durante toda a simulação
    for tn in t_hist:  # loop de iterações em cada instante
        s_hist.append(iterar(h))  # adiciona as posições do frame à lista de iterações
    return np.array(s_hist), t_hist


if __name__ == '__main__':
    from capym import ani

    sis = input('Selecione sistema de 3 corpos de exemplo: \n 1 - Infinito \n 2 - Com órbita externa \n')
    if sis == '1':
        # sistema de 3 corpos formato infinito; G = 1
        a = 0.3471128135672417
        b = 0.532726851767674
        Particula(s=[-1, 0], v=[a, b])
        Particula(s=[1, 0], v=[a, b])
        Particula(s=[0, 0], v=[-2 * a, -2 * b])
    elif sis == '2':
        # um sistema de 3 corpos; G = 1
        Particula(s=[-1, 0], v=[0, -0.3660350371], m=2)
        Particula(s=[1.254953728, 0], v=[0, 0.4593570344], m=0.5)
        Particula(s=[2.745046272, 0], v=[0, 1.004783114], m=0.5)
    else:
        raise ValueError('Poxa! Era 1 ou 2, não tinha muita margem para erro, o que você botou aqui?')

    ani.animar_sim(simular(10, 0.01), xlim=(-2, 2), ylim=(-2, 2), vel=1)


# todo: criar função de delta-v numa determinada direção, bem como função de teleporte de objeto
# todo: criar nova classe Esfera, adicionado orientação, torque, raio e colisões aos objetos
