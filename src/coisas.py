import numpy as np


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
        self.sim = None  # simulação a que o objeto se relaciona
        self.sats = []  # lista de satélites,
        # para o caso de o objeto não ter sido adicionado a uma simulação ainda,
        # eles são colocados em óbita só depois que for definida a simlação (e G)
        # todo: adicionar opção de customizar cores

    def em_orbita(self, s, m=1.0, tipo='particula', sentido=True):
        # cria automaticamente um novo objeto em velocidade orbital da classe especificada
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
        if self.sim is not None:  # se ainda não se sabe o valor de G da simulação, apenas retorna como true
            gc = self.sim.configs['G']  # pega o valor da constante G da simulação
            v = self._v_orbital(s, gc, sentido)

            if tipo == 'particula':
                return Particula(s, v, m)
            else:
                raise NotImplementedError('Tipo não suportado para por em órbita')
        else:  # se o objeto central não estiver em uma simulação, isto será adicionado depois
            if tipo == 'particula':
                sat = Particula(s=s, m=m)
                self.sats.append((sat, sentido))  # adiciona o objeto (sem velocidade) e o sentido de rotação como
                # pares ordenados na sats
                print('Simulação não definida, a velocidade será configurada depois, automaticamente')
                return sat
            else:
                raise NotImplementedError('Tipo não suportado para por em órbita')

    def _v_orbital(self, s, g, sent):  # função para calcular a velociadde orbital de um objeto tendo a posição
        s = np.array(s)
        d = s - self.s  # vetor distância
        mod_v = np.sqrt(g * self.m / abs(np.linalg.norm(d)))  # módulo da velocidade orbital
        angle = np.arccos(d[0] / abs(np.linalg.norm(d)))
        if sent:
            angle -= np.pi / 2  # calcula a inclinação do vetor v
        else:
            angle += np.pi / 2  # no senitdo horáiro ou anti-horáio
        v = np.array([mod_v * np.cos(angle), mod_v * np.sin(angle)]) + self.v
        # a adição da velocidade do objeto principal serve para anular a velocidade relativa
        return v

    def _def_sats(self):  # atualiza a velocidade orbital dos satéites levando em conta o G da simulação isntanciada
        g = self.sim.configs['G']
        for sat in self.sats:
            sat[0].v = self._v_orbital(sat[0].s, g, sat[1])
            # define a velocidade orbital do satélite (sat[0] é o objeto e sat[1] o sentido de rotação)
        del self.sats

# todo: criar opção de deixar rastro para partícula
# todo: classe circulo, com simulações de gases
# todo: criar propriedades elétricas
# todo: criar delta v e tp
# todo: criar legenda temporária
# todo: linhas (entre objetos e colisivas)
# todo: atualizar documentação
