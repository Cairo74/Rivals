# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

Rivals

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Nome 1: Cairo Rodrigues Rezende
- Nome 2: Pedro Aguiar
- Nome 3: Ruan Montoya

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Jogo de tiro competitivo local para dois jogadores.

## 4. Descrição geral do jogo

Descrição:

> Rivals será um jogo feito em Python com Pygame em que dois jogadores se enfrentam em uma arena simples. Cada jogador começa em um lado diferente do campo e controla um personagem armado. O objetivo é se movimentar, desviar dos tiros do adversário e acertar disparos para tirar vidas do oponente.
>
> A tela mostrará a arena, os dois personagens, os tiros em movimento e a quantidade de vidas de cada jogador. O desafio principal será acertar o adversário sem ser atingido.

## 5. Objetivo do jogador

Objetivo:

> O objetivo principal de cada jogador é acertar tiros no adversário até fazer com que ele perca todas as suas vidas.

## 6. Regras principais

Regras do grupo:

- Regra 1: Cada jogador começa a partida com 3 vidas.
- Regra 2: Cada tiro que acertar o adversário remove 1 vida dele.
- Regra 3: Os jogadores podem se movimentar pela arena para atacar e desviar dos tiros.
- Regra 4: Os tiros seguem em linha reta na direção em que o jogador está virado.
- Regra 5: A partida termina quando um dos jogadores fica com 0 vidas.

## 7. Condição de vitória

Condição de vitória:

> Um jogador vence quando consegue fazer o adversário perder as 3 vidas.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> O jogador perde quando fica com 0 vidas. A partida é encerrada nesse momento e o jogo mostra qual jogador venceu.

## 9. Elementos previstos no jogo

Descreva os principais elementos que farão parte do jogo.

## Jogador ou elemento principal

Descrição:

> O jogo terá dois personagens principais. O Jogador 1 começará no lado esquerdo da arena e será controlado pelas teclas WASD. O Jogador 2 começará no lado direito da arena e será controlado pelas setas do teclado.

## Obstáculos, inimigos ou desafios

Descrição:

> O principal desafio será o outro jogador, que tentará acertar tiros e desviar dos disparos. Também poderão existir limites da arena para impedir que os personagens saiam da tela.

## Itens, alvos ou objetos de interação

Descrição:

> Os principais objetos de interação serão os tiros disparados pelos jogadores. Cada tiro se moverá pela tela e poderá colidir com o adversário ou sair da arena.

## Pontuação, vidas, tempo ou progresso

Descrição:

> Cada jogador começará com 3 vidas. A interface mostrará as vidas restantes dos dois jogadores durante a partida. Quando um jogador chegar a 0 vidas, a partida terminará.

## 10. Controles previstos

Controles do grupo:

- W, A, S, D: mover o Jogador 1
- E: atirar com o Jogador 1
- Setas do teclado: mover o Jogador 2
- P: atirar com o Jogador 2
- ESC: sair do jogo

## 11. Organização inicial do código

Organização planejada:

> A organização inicial do código será simples, para facilitar o desenvolvimento:
>
> - `main.py`: inicia o jogo e chama o loop principal;
> - `src/config.py`: guarda configurações como tamanho da tela, cores, velocidade dos jogadores e quantidade de vidas;
> - `src/jogador.py`: contém a classe dos jogadores, com movimentação, vidas e desenho na tela;
> - `src/tiro.py`: contém a classe dos tiros, com movimentação e colisão;
> - `src/jogo.py`: contém o loop principal, controle dos eventos, atualização dos objetos e condição de vitória.

## 12. Recursos externos previstos

Recursos previstos:

> Inicialmente, pretendemos usar formas simples desenhadas pelo próprio Pygame, como retângulos ou círculos para os jogadores e tiros. Caso haja tempo, poderemos utilizar sons gratuitos para os disparos e imagens simples para os personagens ou cenário.

## 13. Principais dificuldades esperadas

Dificuldades previstas:

- Dificuldade 1: Fazer a movimentação dos dois jogadores ao mesmo tempo.
- Dificuldade 2: Implementar a colisão entre tiros e jogadores corretamente.
- Dificuldade 3: Controlar o sistema de vidas, fim de jogo e reinício da partida.

## 14. Escopo mínimo para a entrega final

Escopo mínimo:

> A versão mínima do jogo terá dois jogadores na mesma tela, movimentação por teclado, sistema de tiros, colisão entre tiro e adversário, 3 vidas para cada jogador e tela de fim de jogo indicando o vencedor.

## 15. Possíveis melhorias, caso haja tempo

Melhorias possíveis:

- Melhoria 1: Criar uma tela inicial com botão ou tecla para começar a partida.
- Melhoria 2: Adicionar sons para tiros, acertos e fim de jogo.
- Melhoria 3: Adicionar obstáculos na arena para os jogadores se protegerem.
- Melhoria 4: Criar diferentes personagens ou cores para personalização.
- Melhoria 5: Adicionar um menu de pausa e opção de reiniciar a partida.