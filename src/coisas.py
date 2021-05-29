"""
Módulo com os objetos simuláveis.

Classes
-------
Partícula
    Classe base para todos os objetos da simulação em 2D.
"""

import numpy as np


class Particula:
    """
    Classe base para todos os objetos da simulação em 2D.
    Contem apenas posição inicial, velocidade inicial e massa, de modo que não há colisões.
    Para simular e animar o objeto, precisa ser adicionado a uma animação do módulo `sim.py`.

    Atributos
    ---------
    s : array_like
        Vetor posição da partícula.
    v : array_like
        Vetor velocidade da partícula.
    m : int ou float
        Massa da partícula.
    nome : str
        Nome dado a particula. Uma opção para se referir a cada objeto ao invés de indice na simulação ou variaável.
    cor : str
        Cor em formato suportado pela Matplotlib. Ver padrões de especificação de cores:
        https://matplotlib.org/stable/tutorials/colors/colors.html.
        Ver cores nomeadas disponíveis pelo Matplotlib:
        https://matplotlib.org/stable/gallery/color/named_colors.html

    Métodos
    -------
    em_orbita(s, m=1.0, tipo='particula', sentido=True, e=0.0, nome='', cor='tab:blue')
        Retorna um objeto de classe especificada em órbita na posição especificada.

    Ver também
    ----------
    sim.Sim

    """
    def __init__(self, s=(0, 0), v=(0, 0), m=1.0, nome='', cor='tab:blue'):
        """
        Parâmetros
        ----------
        s : array_like de formato (2,), padrão=[0,0]
            Posição da partícula no início da simulação.
            Independente do tipo de iterável, o código transforma em array_like.
        v : array_like de formato (2,), padrão=[0,0]
            Velocidade da partícula no início da simulação.
            Independente do tipo de iterável, o código transforma em ndarray.
        m : int ou float, padrão=1.0
            Massa da partícula.
        nome : str, padrão=''
            Nome dado a particula. Uma opção para se referir a cada objeto ao invés de indice na simulação ou variaável.
        cor : str, padrão='tab:blue'
            Cor em formato suportado pela Matplotlib. Ver padrões de especificação de cores:
            https://matplotlib.org/stable/tutorials/colors/colors.html.
            Ver cores nomeadas disponíveis pelo Matplotlib:
            https://matplotlib.org/stable/gallery/color/named_colors.html
        """
        self.s = np.array(s)  # vetor de posição
        self.v = np.array(v)  # vetor de velocidade
        self.m = m  # massa do objeto

        self.nome = nome
        self.cor = cor

        self._sim = None  # simulação a que o objeto se relaciona
        self._sats = []  # lista de satélites,
        # para o caso de o objeto não ter sido adicionado a uma simulação ainda,
        # eles são colocados em óbita só depois que for definida a simlação (e G)

    def em_orbita(self, s, m=1.0, tipo='particula', sentido=True, e=0.0, nome='', cor='tab:blue'):
        # todo: checar se passar kwargs para os argumentos do novo objeto seja uma melhor ideia
        # cria automaticamente um novo objeto em velocidade orbital da classe especificada
        """
        Cria um novo objeto de classe selecionada com velocidade orbital em relação à instânia que chamou este método.

        Parâmeteros
        ----------
        s : array_like de formato (2,)
            Posição do objeto no início da simulação.
            Independente do tipo de iterável, o código transforma em ndarray.
        m : int o float, padrão=1.0
            Massa do objeto.
        tipo : string, padrão='particula'
            Escolhe a classe da instância retornada pela função (no momento apenas partícula)
        sentido : bool, padrão=True
            True definido como sentido horáiro e False como anti-horário.
        e : excentricidade orbital, padrão=0.0
            Altera a excentrcidade da orbita. A posição inicial sempre é o periastro.
        nome : str, padrão=''
            Ver coisas.Particula
        cor : str, padrão='tab:blue'
            Ver cisas.Particula

        Retorna
        -------
        Particula
            Retorna um objeto da classse partícula em velocidade orbital ao redor do objeto que chamou o método.

        Raise
        -----
        NotImplementedError
            Tipo não suportado para por em órbita
            Se for colocado uma classe não reconhecida, o programa levanda este erro.

        Ver também
        ----------
        coisas.Particula.__init__()

        Notas
        -----
        Se este método for chamado sem a instância atual estar adiconada a uma simulação, a velocidade orbital do objeto
        que retorna será configuranda automaticamente quando a instância for adicionada. Isto ocrre pois a velocidade
        orbital depende da constante da gavitação universal (configurada na simulação).

        A equação da velocidade orbital é: v = sqrt(G * M ( 2 / dist - 1 /a)
        Onde o semi-eixo maior a = r_p - e * r_p, sendo r_p o raio do periastro (posição inicial).
        """
        # sentido=True -> horário, sentido=False -> anti-horário
        if self._sim is not None:  # se ainda não se sabe o valor de G da simulação, apenas retorna como true
            gc = self._sim.configs['G']  # pega o valor da constante G da simulação
            v = self._v_orbital(s, gc, sentido, e)

            if tipo == 'particula':
                return Particula(s, v, m, nome, cor)
            else:
                raise NotImplementedError('Tipo não suportado para por em órbita')
        else:  # se o objeto central não estiver em uma simulação, isto será adicionado depois
            if tipo == 'particula':
                sat = Particula(s=s, m=m, nome=nome, cor=cor)
                self._sats.append((sat, sentido, e))  # adiciona o objeto (sem velocidade) e o sentido de rotação como
                # pares ordenados na _sats
                print('Simulação não definida, a velocidade será configurada depois, automaticamente')
                return sat
            else:
                raise NotImplementedError('Tipo não suportado para por em órbita')

    def _v_orbital(self, s, g, sent, e):  # função para calcular a velociadde orbital de um objeto tendo a posição
        s = np.array(s)
        d = s - self.s  # vetor distância
        mod_rp = abs(np.linalg.norm(d))  # módulo do raio do perigeu
        mod_v = np.sqrt(g * self.m * (2 / mod_rp - 1 / ((1 + e) * mod_rp)))  # módulo da velocidade orbital
        angle = np.arccos(d[0] / mod_rp)
        if sent:
            angle -= np.pi / 2  # calcula a inclinação do vetor v
        else:
            angle += np.pi / 2  # no senitdo horáiro ou anti-horáio
        v = np.array([mod_v * np.cos(angle), mod_v * np.sin(angle)]) + self.v
        # a adição da velocidade do objeto principal serve para anular a velocidade relativa
        return v

    def _def_sats(self):  # atualiza a velocidade orbital dos satéites levando em conta o G da simulação isntanciada
        g = self._sim.configs['G']
        for sat in self._sats:
            sat[0].v = self._v_orbital(sat[0].s, g, sent=sat[1], e=sat[2])
            # define a velocidade orbital do satélite (sat[0] é o objeto e sat[1] o sentido de rotação)
        del self._sats

# tarefas organizadas em ordem de prioridade de execução
# todo: transformar configuração de limites como uma função extra na lista de funções exectuada por sim.Sim.animar(),
#  permitindo configurar enquadramento dinâmico futuramente
# todo: criar opção de customizar pontos exibidos das partículas
# todo: módulo com calculos. Ex: período orbital (pegar dados da primeira posição da simulação)
# todo: Sim.simular_objs(): função com toda a rotina de simulação simplificada
# todo: criar propriedades elétricas
# todo: classe circulo, com simulações de gases (não optimizado)
# todo: criar objetos continuos estáticos colidíveis
# todo: criar arrasto
# todo: módulo com operações optimizadas, como ditsâncias, colisões, etc.
# todo: física de corpos contínuos
# todo: aerodinâmica
# todo: complementar versão orientada a objetos, com funcional (simulação local ao invês de objeto, como opção), fazer
#  isso com objetos locais automáticos
