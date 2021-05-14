import numpy as np

G = 1  # 6.6708e-11  # constante da gravitação universal


class Particula:
    """
    Classe base para todos os objetos da simulação em 2D.
    Contem apenas posição inicial, velocidade inicial e massa de modo que não há colisões.
    Um ponteiro no final da lista `_objs` é adicionado em toda instânciação, apontando para ele.

    Atributos
    ---------
    s : ndarray
        Vetor posição da partícula.
    v : ndarray
        Vetor velocidade da partícula.
    m : int ou float
        Massa da partícula.
    index : int
        Indíce do objeto na lista `_objs`.

    Métodos
    -------
    ar()
        Retorna vetor aceleração resutante.
    em_orbita(s, m=1.0, sentido=True)
        Retorna uma partícula em órbita na posição e massa especificada.

    """
    def __init__(self, s=(0, 0), v=(0, 0), m=1.0):
        """
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
        """
        self.s = np.array(s)  # vetor de posição
        self.v = np.array(v)  # vetor de velocidade
        self.m = m  # massa do objeto
        self.index = 0  # índice do objeto na simulação
        self.sim = None  # simulação a qual o objeto foi atrelado
        # todo: adicionar opção de customizar cores
        # todo: configurar indíces de acordo com a classe simulação, bem como `sim`

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
        for n in self.sim.objs:
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
        # todo: passar esse método para simulação

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
