# Aprendizado em Mundo Digital com Redes Neurais e Algoritmo Genético

#### Aluno: [Adriano Lyrio](https://github.com/adrianolyrio)
#### Orientadora: [Manoela Kohler](https://github.com/manoelakohler).

---

Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

- [Link para o código](https://github.com/adrianolyrio/ann_ga). 

---

### Resumo

Este trabalho tem como objetivo apresentar a aplicação de um modelo de Inteligência Artificial em um jogo digital, com o intuito de aprender a interagir com este ambiente complexo para atingir um objetivo.
No estudo, foi utilizado Algoritmo Genético junto com a aplicação de Redes Neurais como modelo de Inteligência Artificial. Ambos os modelos são inspirados na biologia animal, onde as Redes Neurais são baseadas no modelo de neurônios do cérebro biológico e o Algoritmo Genético é baseado na biologia evolutiva cromossomática como hereditariedade, mutação, seleção natural e recombinação.
O ambiente digital que foi criado e utilizado para treinar o modelo de Inteligência Artificial é um jogo de Corrida, no qual o jogador deve completar o circuito de maneira rápida e se mantendo na pista de corrida, sem colidir o veículo. Este ambiente digital pode representar inclusive, de maneira simples, um ambiente real, no qual um robô deverá atingir um objetivo, evitando danos e colisões pelo percurso que deverá percorrer.

---

### Algorítmos Genéticos

Algorítimos Genéticos são algorítimos inspirados no processo evolutivo biológico genético, onde os genes são passados de uma geração para a outra. Estes algorítimos realizam uma busca aleatória da melhor solução para um problema e aplica técnicas como seleção, reprodução e mutação para criar indivíduos melhores, reptindo estas técnicas através de gerações, para se encontrar o melhor resultado.

---

### Redes Neurais Artificiais

Redes Neurais Artificiais são modelos computacionais inspirados na estrutura neural biológica de organismos inteligentes. As Redes Neurais biológicas são compostas de células chamadas neurônios, que se comunicam através de conexões chamadas sinapses.
As Redes Neurais Artificiais são compostas por diversos neurônios, que também são chamados de unidades de processamento ou nós. Os neurônios se conectam uns aos outros e cada conexão contém um peso. A eficácia de uma Rede Neural Artificial se dá pela interação destes neurônios e pelo ajuste destes pesos.

---

### Jogo de Corrida

O Jogo Digital foi criado em Python com a blibioteca PyGame, que permite a criação de interfaces gráficas animadas para o usuário. O objetivo do jogo consiste em guiar um veículo através de uma pista de corrida, sem sair da pista e completando voltas no menor tempo possível. Sair da pista de corrida é considerado derrota e finaliza o jogo.
 
O veículo utilizado contém diversos atributos, que são:
•	Velocidade do Veículo
•	Ângulo do Veículo em relação ao Mapa
•	Ângulo das Rodas, para cálculo de curvas
•	Doze (12) sensores de distância, que identificam obstáculos ao redor do veículo

O conjunto destes atributos em um determinado tempo t é chamado de estado do veículo. Os estados serão gerados 15 vezes por segundo e serão disponibilizados ao sistema que irá controlar o veículo.
O controle do veículo irá consistir em 4 ações distintas que são:
•	Acelerar
•	Frear
•	Virar à direita
•	Virar à esquerda

---

Matrícula: 182.477.014

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
