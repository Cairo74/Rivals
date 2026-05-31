# Rivals

Projeto final da disciplina de Introducao a Algoritmos/Programacao, desenvolvido com Python e Pygame.

Rivals e um jogo de tiro competitivo local para dois jogadores. Os jogadores se enfrentam em uma arena, controlam personagens armados, desviam dos disparos do adversario e tentam acertar tiros para reduzir as vidas do oponente.

## Integrantes do grupo

- Cairo Rodrigues Rezende
- Pedro Aguiar
- Ruan Montoya

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicacao.
- `src/`: codigo-fonte principal do jogo.
- `src/config.py`: configuracoes como tamanho da tela, cores, caminhos de arquivos, velocidade e valores gerais.
- `src/jogo.py`: loop principal, controle de eventos, atualizacao dos objetos e regras da partida.
- `src/sprites.py`: funcoes auxiliares para carregar e recortar sprites.
- `src/dados.py`: funcoes para carregar e salvar dados persistentes.
- `src/funcoes.py`: funcoes de apoio para pontuacao, colisao, limites e dano.
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes, como recorde ou dados de progresso.
- `tests/`: testes unitarios com `pytest`.
- `docs/`: documentacao do projeto, incluindo a proposta inicial.

## Descrição do jogo

Rivals coloca dois jogadores na mesma tela, cada um iniciando em um lado diferente da arena. Durante a partida, os jogadores precisam se movimentar, mirar na direcao em que estao virados e disparar contra o adversario.

A tela exibe a arena, os personagens, os tiros em movimento e a quantidade de vidas restante de cada jogador. O desafio principal e atacar o oponente sem ser atingido.

## Objetivo do jogador

O objetivo de cada jogador e acertar tiros no adversario ate fazer com que ele perca todas as suas vidas. Vence quem conseguir reduzir as 3 vidas do oponente a 0 primeiro.

## Regras do jogo

- Cada jogador comeca a partida com 3 vidas.
- Cada tiro que acerta o adversario remove 1 vida dele.
- Os jogadores podem se movimentar pela arena para atacar e desviar dos tiros.
- Os tiros seguem em linha reta na direcao em que o jogador esta virado.
- Os personagens nao podem sair dos limites da arena.
- A partida termina quando um dos jogadores fica com 0 vidas.
- Ao fim da partida, o jogo mostra qual jogador venceu.

## Condicoes de vitoria e derrota

Um jogador vence quando faz o adversario perder todas as 3 vidas. Um jogador perde quando sua propria quantidade de vidas chega a 0. Nesse momento, a partida e encerrada.

## Elementos do jogo

- Jogador 1: personagem que inicia na parte de cima da arena.
- Jogador 2: personagem que inicia na parte de baixo da arena.
- Arena: espaco onde os jogadores se movimentam e se enfrentam.
- Tiros: projeteis disparados pelos jogadores, capazes de colidir com o adversario.
- Vidas: indicador de resistencia dos jogadores durante a partida.
- Limites da arena: impedem que os jogadores saiam da tela.

## Controles

- W, A, S, D: mover o Jogador 1
- E: atirar com o Jogador 1
- Setas do teclado: mover o Jogador 2
- P: atirar com o Jogador 2
- ESC: sair do jogo

## Escopo minimo

A versao minima do jogo deve conter:

- dois jogadores na mesma tela;
- movimentacao por teclado;
- sistema de tiros;
- colisao entre tiro e adversario;
- 3 vidas para cada jogador;
- fim de jogo indicando o vencedor.

## Possiveis melhorias

- Criar uma tela inicial para comecar a partida.
- Adicionar sons para tiros, acertos e fim de jogo.
- Adicionar obstaculos na arena para os jogadores se protegerem.
- Criar diferentes personagens ou cores para personalizacao.
- Adicionar menu de pausa e opcao de reiniciar a partida.

## Como executar o projeto

### 1. Clonar o repositorio

```bash
git clone LINK_DO_REPOSITORIO
cd Rivals
```

### 2. Instalar as dependencias

```bash
pip install -r requirements.txt
```

### 3. Executar o jogo

```bash
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Tecnologias utilizadas

- Python
- Pygame
- Pytest

## Documentacao

A proposta inicial do projeto esta em `docs/proposta.MD`.
