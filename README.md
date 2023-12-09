# CaPyM: Capy, Python, Mecânica.

## Descrição
Projeto simples de simulador de interações físicas, feito com base em numpy e matplotlib para plotagem. Para salvar animações feitas, se necessita de ffmpeg. [Link para download do ffmpeg](https://www.ffmpeg.org/) ~~Não fiz nenhum teste de versões então, boa sorte.~~

No momento ele apenas trata de interações gravitacionais bidimensionais de pariculas pontiformes e não tem GUI, mas futuramente prentendo adicionar corpos extensos, simulações tridimensionais, física de corpos rígidos, talvez até GUI. É um projeto pessoal, tenho aprendido bastante no desenvolvimento dele, mas não é para ser grande coisa.

## Funcionamento
Para usar este projeto precisa-se fazer mão de duas classes importantes: `coisas.Particula` e `sim.Sim`. A primeira nos dá um objeto a ser simulado e a segunda nos dá uma simulação. Para criar uma partícula e uma simulação novas com as configurações padrão, basta fazer:
```python
from src.capym import *

minha_particula = coisas.Particula()
minha_sim = sim.Sim()
```
### Sua primeira partícula
Para criar uma partícula com massa, velocidade e posição definidas, é necessário definir estas características quando ela for criado. Por ex. uma partícula nas coordenadas (0,3), com um vetor velocidade (1,1) e massa 3 é criada fazedno `coisas.Particula((0,3), (1,1), 3)`. Com argumentos de palavras-chave temos:
`coisas.Particula(s=(0,3), v=(1,1), m=3)`.

O objeto que determina os vetores velocidade e posição podem ser qualquer iterável suportado pelo numpy.

O padrão para partícula com dados não alterados é s=(0,0), v=(0,0), m=1.

### Criando uma simulação
É nas simulações que a física acontece, e também onde se é possível gerar e animar dados. Todavia primeiro é preciso adicionar um objeto à simulação (caso contrários teremos erros) usando o método `sim.add_obj()`:

```python
from src.capym import *

a = coisas.Particula(s=(1, 0), v=(1, 0), m=10)
b = coisas.Particula(s=(-1, 0), v=(-1, 0), m=10)
# criar duas partículas em posições quaisquer

simul = sim.Sim()  # cria uma simulação

simul.add_object(a, b)  # adiciona as partículas à simulação
```
Depois podemos simular o movimento das partículas adicioandas, digamos, por 2s:
```python
simul.simular(2)
```
Por fim, vamos exibir o que fizemos:
```python
simul.animar()
```

![sis](https://user-images.githubusercontent.com/54824248/117578154-52407780-b0c3-11eb-83c5-2b106a286364.gif)

Um dos parametros do método de animação é `salvar_em=''`, pode-se substituir a `string` pelo caminho de um arquivo em que queira salvar a animação (com o nome do arquivo e extensão inclusas), se tiver ffmpeg funcionado. Há uma lista de formatos que devem ser suportados, em `sim.py`: `'3g2', '3pg', 'amv', 'asf', 'avi', 'dirac', 'drc', 'flv', 'gif', 'm4v', 'mp2', 'mp3', 'mp4', 'mjpeg', 'mpeg', 'mpegets', 'mov', 'mkv', 'mxf', 'mxf_d10', 'mxf_opatom', 'nsv', 'null', 'ogg', 'ogv', 'rm', 'roq', 'vob', 'webm'`. Ourtos formatos podem ser suportados (de acordo com ffmpeg), mas não garanto que vão.

É possível alterar o estilo do gráfico de plotagem pelo artributo `Sim.configs['estilo']` substituindo o padrão por qualquer outro [estilo da matplolib](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html).

Na verdade, o dicionário `Sim.configs` tem diversas configurações relevantes que podem ser alteradas simplesmente substituindo o valor por outro válido.

### Ilustrações extras
Outras coisas podem ser adiocinadas à simulação que não tenhma nenhum efeito físico. Por exemplo, é possível ver o caminho que dois objetos de excentricidades diferentes percorrem com este código:

```python
from src.capym import *

c = coisas.Particula(m=100)
a = c.em_orbita([0, -1], m=0, e=0, cor='tab:green')
b = c.em_orbita([0, -1], m=0, e=0.7)
s = sim.Sim()

s.add_object(a, b, c)

s.simular(10)

s.rastro(a)
s.rastro(b)

s.configs['lims'] = ((-3, 3), (-3, 3))
s.animar(target_path='ani.gif')
```

![ani](https://user-images.githubusercontent.com/54824248/120056650-13dc0f80-c014-11eb-81f2-7075222cb400.gif)

Estes objetos extras são o que chamados de objetos gráficos. São todos adicionados em métodos de `sim.Sim` após ter executado a simulação. Por hora os objetos gráficos disponíveis são:

- `rastro()`
- `area_kepler()`
- `texto()`
- `seta()`

Para mais detalhes sobre cada um, consulte a documentação.

### Estrutura recomendada de uma simulação
Em linhas gerais é possível estabelecer alguns passos para exeutar uma simulação:

1. Definir os objetos simuláveis;
2. Criar um objeto de simulação (instância de `sim.Sim`);
3. Configurar a simulação usando o dicionário `Sim.congifs`;
4. Adicionar objetos usando `Sim.add_obj()`;
5. Executar a simulação com `Sim.simular()`;
6. Por os objetos gráficos extras como `Sim.rastro()`;
7. Compilar tudo e animar com `Sim.animar()`; 

## Exemplos
Aqui outras simulações que já fiz. Esta primeira está é uma versão anterior da que está em `example.py`.

```python
from src.capym import *

# Condições iniciais:
a = 0.3471128135672417
b = 0.532726851767674

lis = []  # lista de partícualas

# cria partículas
lis.append(coisas.Particula(s=[-1, 0], v=[a, b]))
lis.append(coisas.Particula(s=[1, 0], v=[a, b]))
lis.append(coisas.Particula(s=[0, 0], v=[-2 * a, -2 * b]))

minhaSim = sim.Sim()  # cria simulação
minhaSim.configs['xlim'] = (-2, 2)  # altera o tamanho do enquadramento da simulação
minhaSim.configs['ylim'] = (-2, 2)
minhaSim.add_object(lis)  # adiciona a lista de objetos
minhaSim.simular(10, 0.01)  # faz uma simulação de 10s com passo h=0.01s
minhaSim.animar(target_path='C:/Users/Ícaro/Desktop/animação.gif')  # salva a animação num diretório específico

```

Resultado:

![animação](https://user-images.githubusercontent.com/54824248/117578528-2cb46d80-b0c5-11eb-8134-7cece530f3ad.gif)
---

```python
from src.capym import *

# Condições iniciais:
sol = coisas.Particula(s=(0, 0), m=1000)
planeta = sol.em_orbita(s=(10, 0), m=50)  # cria partícula em velocidade orbital na posição especificada
lua = planeta.em_orbita(s=(11, 0), m=1)

simul = sim.Sim()
simul.add_object(sol, planeta, lua)  # adiciona os objetos à simulação
simul.simular(t=10, h=0.0001)  # cria uma simulação de duração t e passo h

simul.configs['xlim'] = (-15, 15)  # altera o tamanho do enquadramento da animação
simul.configs['ylim'] = (-15, 15)

simul.animar(target_path='C:/Users/Ícaro/Desktop/sla.gif')
```

Note que esta animação tem bem mais iterações por segundo (10 000) e também usa um método da classe partícula, o `.em_orbita`, que cria um objeto em órbita da instância que chamou o método.

Em ambos exemplos temos alterações de bordas do enquadramento da animação.

Resultado:

![sla](https://user-images.githubusercontent.com/54824248/117578722-0fcc6a00-b0c6-11eb-95f0-764fef71c11c.gif)
---
