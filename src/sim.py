import numpy as np

_inicio = 0  # variável para estimar tempo de computação
objs = []  # lista global de objetos de todas as classes
G = 1  # 6.6708e-11  # constante da gravitação universal

# todo: documentação


class Particula:
    def __init__(self, s=[0, 0], v=[0, 0], m=1.0):
        self.s = np.array(s)  # vetor de posição
        self.v = np.array(v)  # vetor de velocidade
        self.m = m  # massa do objeto
        self.index = len(objs)  # armazena o endereço do próprio objeto na lista objs
        objs.append(self)  # adiciona o objeto à lista de pointers

        # todo: adicionar opção de customizar cores

    def ar(self):  # método para retornar o vetor de acleração resultante
        ar = np.zeros(2)
        for n in objs:
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
    global objs
    for n in objs:
        del n


def colisao():
    pass  # função que terá as colisões entre objetos


def iterar(h=1/30):  # padrão definido para 30 FPS
    s_list = []  # lista com posição dos objetos em cada iteração
    for i in objs:  # calcula os estados para cada objeto
        # atualiza o valor das variáveis do objeto i:
        i.s = i.s + h * i.v
        i.v = i.v + h * i.ar()
        s_list.append(i.s)
        colisao()
    return np.array(s_list)


def simular(t, h=1/30):  # função com as iterações em loop do sistema. Padrão definido para 30 FPS
    t_hist = np.arange(0, t, h)  # cria uma lista de instantes no intervalo e passo definido
    print('Calculando {} iterações e {} interações.' .format(len(t_hist), len(t_hist) * len(objs) ** 2))
    s_hist = []  # lista com as posições dos objetos durante toda a simulação

    global _inicio
    for tn in t_hist:  # loop de iterações em cada instante
        s_hist.append(iterar(h))  # adiciona as posições do frame à lista de iterações
    return np.array(s_hist), t_hist


# --------------------- testes do código ---------------------
if __name__ == '__main__':
    from capym import ani
    # # um sistema de 3 corpos; G = 1
    # Particula(s=[-1, 0], v=[0, -0.3660350371], m=2)
    # Particula(s=[1.254953728, 0], v=[0, 0.4593570344], m=0.5)
    # Particula(s=[2.745046272, 0], v=[0, 1.004783114], m=0.5)

    # sistema de 3 corpos formato infinito; G = 1
    a = 0.3471128135672417
    b = 0.532726851767674
    Particula(s=[-1, 0], v=[a, b])
    Particula(s=[1, 0], v=[a, b])
    Particula(s=[0, 0], v=[-2 * a, -2 * b])
    ani.animar_sim(simular(10, 0.01), xlim=(-2, 2), ylim=(-2, 2), vel=1, salvar_em='C:/Users/Ícaro/Desktop/foo.mp4')

# todo: criar função de delta-v numa determinada direção, bem como função de teleporte de objeto
# todo: criar nova classe Esfera, adicionado orientação, torque, raio e colisões aos objetos
