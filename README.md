# CaPyM: Capy, Python, Mecânica.

## Descrição
Projeto simples de simulador de interações físicas, feito com base em numpy e matplotlib para plotagem. Para salvar animações feitas, por enquanto se necessita de ffmpeg.

No momento ele apenas trata de interações gravitacionais bidimensionais de pariculas pontiformes e não tem GUI, mas futuramente prentendo adicionar corpos contínuos, simulações tridimensionais, geometria de corpos rígidos, talvez até GUI. É um projeto pessoal, tenho aprendido bastante coisa no desenvolvimento dele, mas não é pra ser grande coisa.

## Funcionamento
### Sua primeira partícula
O sistema é todo orientado a objetos, cuja classe base (na verdade, a única classe por enquanto) é `sim.Particula`. Desta forma, para adicionar uma partícula a simulação basta fazer: `sim.Particula()`, as definições padrão criam uma partícula na posição (0,0), velocidade nula e massa 1. Para criar uma partícula com os valores certos basta fazer: `sim.Particula(s=(1, 1), v=(0, 2), m=1)`. Dessa forma o sistema salva automaticmaente o objeto na lista `_objs`, não sendo necesário por numa variável. Para saber saber o índice nesta lista é só acesar a variável `.index` da instância.

A classe suporta qualquer itérável como argumento e os elemntos podem ser `int` ou `float`, assim como a massa.
### Fazendo uma simulação
Uma simulação apenas executa as iterações do sistema usando o método de Euler. A função `sim.simular()` retorna um vetor com vários vetores dentr (representando o estado das partículas em cada iteração), cujos elemntos por sua vez também são vetores, que dão a posição de cada partícula na dad iteração. Assim o primeiro valor de retorno da função `sim.simular()` é organizado assim:

| Primeiro índice | Segundo ínidice | Terceiro índice 
| --------------- | --------------- | --------------- 
| Iteração        | Partícula       | Direção         
| 1               | 1               | x1              
|                 |                 | y1              
|                 | 2               | x2              
|                 |                 | y2              
| 2               | 1               | x1              
|                 |                 | y1              
|                 | 2               | x2              
|                 |                 | y2              

O número da partícula nada mais é que a ordem que ela foi cirada, ou o ídice na lista `_objs`. O segundo valor de retorno é um vetor com o instante de cada iteração.

Para fazer uma simulação você só precisa antes ter delcarado as partículas e então por o tempo total de simulação e o tamanho do passo entre cada iteração:
```{python}
sim.Particula(s=[1,0], v=[1,0], m=10)
sim.Particula(s=[-1,0], v=[-1,0], m=10)

sim.simular(t=2, h=0.01)
```
Onde `t=10`é a duração e `h=10`o passo.

A constante da gravitação universla está definida como: `sim.G = 1`, mas caso queira trabalhar em escalas reais sinta-se livre para alterar isso. 

### Visualizando
Aqui vamos fazer uso da função de animação da matplotlib, mas tudo de forma integrada, bastando apenas por `sim.simular()` dentro da função `ani.animar_sim()` e por alguns parâmetros adicionais, como fps, velocidade de reprodução, limites de enquadramento e outras coisas (que constam na documentação). De qualquer forma, basta fazer:
```{python}
sim.Particula(s=[1,0], v=[1,0], m=10)
sim.Particula(s=[-1,0], v=[-1,0], m=10)

ani.animar_sim(sim.simular(t=2, h=0.01))
```
Para ter como resultado:

![sis](https://user-images.githubusercontent.com/54824248/117578154-52407780-b0c3-11eb-83c5-2b106a286364.gif)

Um dos parametros da funçaõ de animação é `salvar_em=' '`, você pode substituir a string pelo caminho de um arquivo em que você queira salvar a animação (com o nome do arquivo e extensão inclusas), se você tiver ffmpeg funcionado. Já testei salvar em Gif e mp4, não me responsabilizo por outros formatos.

É possível alterar o estilo do gráfico de plotagem pela variável `ani.plot_style='dark_background'`, substituindo o padrão por qualquer outro [estio da matplolib](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html).

## Exemplos
Aqui outras simulações que já fiz. Algumas inclusas quandos e executa `sim.py`.
```{python}
# Condições iniciais:
a = 0.3471128135672417
b = 0.532726851767674
sim.Particula(s=[-1, 0], v=[a, b])
sim.Particula(s=[1, 0], v=[a, b])
sim.Particula(s=[0, 0], v=[-2 * a, -2 * b])

# Simulação:
ani.animar_sim(sim.simular(10, 0.01), xlim=(-2, 2), ylim=(-2, 2), vel=1, salvar_em='C:/Users/Ícaro/Desktop/animação.gif')
```
Resultado:
![animação](https://user-images.githubusercontent.com/54824248/117578528-2cb46d80-b0c5-11eb-8134-7cece530f3ad.gif)
---
```{python}
# Condições iniciais:
sol = sim.Particula(s=(0, 0), m=1000)
planeta = sol.em_orbita(s=(10, 0), m=50)
lua = planeta.em_orbita(s=(11, 0), m=1)

# Simulação:
ani.animar_sim(sim.simular(10, 0.0001), xlim=(-15, 15), ylim=(-15, 15), vel=1, salvar_em='C:/Users/Ícaro/Desktop/sla.gif')
```
Note que esta animação tem bem mais iterações por segundo (10000) e também usa um método da classe partícula, o .em_orbita, que cira um novo objeto em órbita da instância que chamou o método.

Resultado:
![sla](https://user-images.githubusercontent.com/54824248/117578722-0fcc6a00-b0c6-11eb-95f0-764fef71c11c.gif)
---
