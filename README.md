# CaPyM: Capy, Python, Mecânica.

## Descrição
Projeto simples de simulador de interações físicas, feito com base em numpy e matplotlib para plotagem. Para salvar animações feitas, se necessita de ffmpeg.

No momento ele apenas trata de interações gravitacionais bidimensionais de pariculas pontiformes e não tem GUI, mas futuramente prentendo adicionar corpos contínuos, simulações tridimensionais, geometria de corpos rígidos, talvez até GUI. É um projeto pessoal, tenho aprendido bastante no desenvolvimento dele, mas não é pra ser grande coisa.

## Funcionamento
Para usar este projeto você precisa fazer mão de duas classes importantes: `coisas.Particula` e `sim.Sim`. A primeira nos dá um objeto a ser simulado e a segunda nos dá uma simulação. Para criar uma partícula e uma simulação novas com as configurações padrão, basta fazer:
```{python}
from src import *

minha_particula = coisas.Particula()
minha_sim = sim.Sim()
```
### Sua primeira partícula
Para criar uma partícula com massa, velocidade e posição definidas, é necessário definir estas características quando ela for criado. Por ex. uma partícula nas coordenadas (0,3), com um vetor velocidade (1,1) e massa 3 é criada fazedno `coisas.Particula((0,3), (1,1), 3)`. Com argumentos de palavras-chave temos:
`coisas.Particula(s=(0,3), v=(1,1), m=3)`.

O objeto que determina os vetores velocidade e posição podem ser qualquer iterável suportado pelo numpy.

O padrão para partícula com dados não alterados é s=(0,0), v=(0,0), m=1.

### Minha primeira simulação
É nas simulações que a física acontece, e também onde se é possível gerar e animar dados. Mas primeiro é preciso adicionar um objeto à simulação (caso contrários teremos erros) usando o método `sim.add_obj()`:
```{python}
from src import *

a = coisas.Particula(s=(1,0), v=(1,0), m=10)
b = coisas.Particula(s=(-1,0), v=(-1,0), m=10)
# criar duas partículas em posições quaisquer

simul = sim.Sim()  # cria uma simulação

simul.add_obj(a, b)  # adiciona as partículas à simulação
```
Depois podemos simular o movimento das partículas adicioandas, digamos, por 2s:
```{python}
simul.simular(2)
```
Por fim, vamos exibir o que fizemos:
```{python}
simul.animar()
```

![sis](https://user-images.githubusercontent.com/54824248/117578154-52407780-b0c3-11eb-83c5-2b106a286364.gif)

Um dos parametros do método de animação é `salvar_em=''`, você pode substituir a string pelo caminho de um arquivo em que você queira salvar a animação (com o nome do arquivo e extensão inclusas), se você tiver ffmpeg funcionado. Há uma lista de formatos que devem ser suportados, em `sim.py`: '3g2', '3pg', 'amv', 'asf', 'avi', 'dirac', 'drc', 'flv', 'gif', 'm4v', 'mp2', 'mp3', 'mp4', 'mjpeg', 'mpeg', 'mpegets', 'mov', 'mkv', 'mxf', 'mxf_d10', 'mxf_opatom', 'nsv', 'null', 'ogg', 'ogv', 'rm', 'roq', 'vob', 'webm'. Ourtos formatos podem ser suportados (de acordo com ffmpeg), mas não garanto que vão.

É possível alterar o estilo do gráfico de plotagem pelo artributo `Sim.configs['estilo']` substituindo o padrão por qualquer outro [estio da matplolib](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html).

Na verdade, o dicionário `Sim.configs` tem diversas configurações relevantes que podem ser alteradas para simples

## Exemplos
Aqui outras simulações que já fiz. Esta primeira está em `example.py`.
```{python}
# Condições iniciais:
a = 0.3471128135672417
b = 0.532726851767674

lis = []  # lista de partícualas

# cira partículas
lis.apppend(coisas.Particula(s=[-1, 0], v=[a, b]))
lis.apppend(coisas.Particula(s=[1, 0], v=[a, b]))
lis.apppend(coisas.Particula(s=[0, 0], v=[-2 * a, -2 * b]))

minhaSim = sim.Sim()  # cria simulação
minhaSim.configs['xlim'] = (-2, 2)  #  altera o tamanho do enquadramento da simulação
minhaSim.configs['ylim'] = (-2, 2)
minhaSim.add_obj(lis)  # adiciona a lista de objetos
minhaSim.simular(10, 0.01)  # faz uma simulação de 10s com passo h=0.01s
minhaSim.animar(salvar_em='C:/Users/Ícaro/Desktop/animação.gif')  # salva a animação num diretório específico

```
Resultado:
![animação](https://user-images.githubusercontent.com/54824248/117578528-2cb46d80-b0c5-11eb-8134-7cece530f3ad.gif)
---
```{python}
# Condições iniciais:
sol = coisas.Particula(s=(0, 0), m=1000)
planeta = sol.em_orbita(s=(10, 0), m=50)  # cria partícula em velocidade orbital na posição especificada
lua = planeta.em_orbita(s=(11, 0), m=1)

simul = sim.Sim()
simul.add_obj(sol, planeta, lua)  # adiciona os objetos à simulação
simul.simular(t=10, h=0.0001)  # cria uma simulação de duração t e passo h

simul.configs['xlim'] = (-15, 15)  #  altera o tamanho do enquadramento da animação
simul.configs['ylim'] = (-15, 15)

simul.amimar(salvar_em='C:/Users/Ícaro/Desktop/sla.gif')
```
Note que esta animação tem bem mais iterações por segundo (10000) e também usa um método da classe partícula, o .em_orbita, que cria um novo objeto em órbita da instância que chamou o método.

Em ambos os exemplos temos alterações de bordas do enquadramento da animação

Resultado:
![sla](https://user-images.githubusercontent.com/54824248/117578722-0fcc6a00-b0c6-11eb-95f0-764fef71c11c.gif)
---
