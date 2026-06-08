import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    BRANCO,
)
from src.funcoes import (
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)


def criar_jogador(posicao_inicial, cor):
    rect = pygame.Rect(posicao_inicial[0], posicao_inicial[1], 40, 40)
    return {
        "rect": rect,
        "cor": cor,
        "vidas": 3,
        "direcao": pygame.Vector2(0, -1),
        "velocidade": 5,
    }


def criar_tiro(posicao, direcao, cor):
    rect = pygame.Rect(posicao[0], posicao[1], 8, 8)
    return {
        "rect": rect,
        "direcao": direcao.normalize() if direcao.length_squared() > 0 else pygame.Vector2(0, -1),
        "velocidade": 8,
        "cor": cor,
    }


def desenhar_jogador(tela, jogador):
    pygame.draw.rect(tela, jogador["cor"], jogador["rect"])


def desenhar_obstaculos(tela, obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, BRANCO, obstaculo)


def atualizar_tiros(tiros):
    tiros_para_remover = []
    for tiro in tiros:
        tiro["rect"].x += int(tiro["direcao"].x * tiro["velocidade"])
        tiro["rect"].y += int(tiro["direcao"].y * tiro["velocidade"])

        if (
            tiro["rect"].right < 0
            or tiro["rect"].left > LARGURA_TELA
            or tiro["rect"].bottom < 0
            or tiro["rect"].top > ALTURA_TELA
        ):
            tiros_para_remover.append(tiro)

    for tiro in tiros_para_remover:
        tiros.remove(tiro)


def desenhar_tiros(tela, tiros):
    for tiro in tiros:
        pygame.draw.rect(tela, tiro["cor"], tiro["rect"])


def mover_jogador(jogador, direcao):
    jogador["rect"].x += int(direcao[0] * jogador["velocidade"])
    jogador["rect"].y += int(direcao[1] * jogador["velocidade"])

    jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
    jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)


def impedir_movimento_por_obstaculos(jogador, obstaculos, ultimo_rect):
    for obstaculo in obstaculos:
        if jogador["rect"].colliderect(obstaculo):
            jogador["rect"].x = ultimo_rect.x
            jogador["rect"].y = ultimo_rect.y
            break


def processar_disparo(evento, jogador, tiros):
    if evento.type != pygame.KEYDOWN:
        return

    if evento.key in (pygame.K_e, pygame.K_p):
        origem = jogador["rect"].center
        tiro = criar_tiro(origem, jogador["direcao"], jogador["cor"])
        tiros.append(tiro)


def exibir_texto(tela, fonte, texto, posicao, cor=BRANCO):
    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, posicao)


def executar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 28)
    fonte_titulo = pygame.font.SysFont(None, 42, bold=True)

    jogador1 = criar_jogador((100, 100), (200, 50, 50))
    jogador2 = criar_jogador((LARGURA_TELA - 140, ALTURA_TELA - 140), (50, 50, 200))

    obstaculos = [
        pygame.Rect(300, 180, 40, 160),
        pygame.Rect(460, 260, 40, 160),
    ]

    tiros = []
    rodando = True
    jogo_ativo = True
    vencedor = None

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                jogo_ativo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                    jogo_ativo = False
                elif not jogo_ativo and evento.key == pygame.K_SPACE:
                    jogador1 = criar_jogador((100, 100), (200, 50, 50))
                    jogador2 = criar_jogador((LARGURA_TELA - 140, ALTURA_TELA - 140), (50, 50, 200))
                    tiros.clear()
                    jogo_ativo = True
                    vencedor = None
                else:
                    processar_disparo(evento, jogador1, tiros)
                    processar_disparo(evento, jogador2, tiros)

        if jogo_ativo:
            teclas = pygame.key.get_pressed()

            direcao1 = pygame.Vector2(0, 0)
            if teclas[pygame.K_a]:
                direcao1.x = -1
            if teclas[pygame.K_d]:
                direcao1.x = 1
            if teclas[pygame.K_w]:
                direcao1.y = -1
            if teclas[pygame.K_s]:
                direcao1.y = 1
            if direcao1.length_squared() > 0:
                jogador1["direcao"] = direcao1.normalize()

            direcao2 = pygame.Vector2(0, 0)
            if teclas[pygame.K_LEFT]:
                direcao2.x = -1
            if teclas[pygame.K_RIGHT]:
                direcao2.x = 1
            if teclas[pygame.K_UP]:
                direcao2.y = -1
            if teclas[pygame.K_DOWN]:
                direcao2.y = 1
            if direcao2.length_squared() > 0:
                jogador2["direcao"] = direcao2.normalize()

            ultimo_rect1 = jogador1["rect"].copy()
            mover_jogador(jogador1, direcao1)
            impedir_movimento_por_obstaculos(jogador1, obstaculos, ultimo_rect1)

            ultimo_rect2 = jogador2["rect"].copy()
            mover_jogador(jogador2, direcao2)
            impedir_movimento_por_obstaculos(jogador2, obstaculos, ultimo_rect2)

            atualizar_tiros(tiros)

            tiros_para_remover = []
            for tiro in tiros:
                if tiro["rect"].colliderect(jogador1["rect"]) and tiro["cor"] != jogador1["cor"]:
                    jogador1["vidas"] = tomar_dano(jogador1["vidas"], 1)
                    tiros_para_remover.append(tiro)
                elif tiro["rect"].colliderect(jogador2["rect"]) and tiro["cor"] != jogador2["cor"]:
                    jogador2["vidas"] = tomar_dano(jogador2["vidas"], 1)
                    tiros_para_remover.append(tiro)
                else:
                    for obstaculo in obstaculos:
                        if tiro["rect"].colliderect(obstaculo):
                            tiros_para_remover.append(tiro)
                            break

            for tiro in tiros_para_remover:
                if tiro in tiros:
                    tiros.remove(tiro)

            if jogador_perdeu(jogador1["vidas"]):
                jogo_ativo = False
                vencedor = "Jogador 2 venceu!"
            elif jogador_perdeu(jogador2["vidas"]):
                jogo_ativo = False
                vencedor = "Jogador 1 venceu!"

        tela.fill(CINZA)
        desenhar_obstaculos(tela, obstaculos)
        desenhar_jogador(tela, jogador1)
        desenhar_jogador(tela, jogador2)
        desenhar_tiros(tela, tiros)

        exibir_texto(tela, fonte, f"Jogador 1 vidas: {jogador1['vidas']}", (10, 10))
        exibir_texto(tela, fonte, f"Jogador 2 vidas: {jogador2['vidas']}", (LARGURA_TELA - 190, 10))
        exibir_texto(tela, fonte, "WASD + E: Jogador 1", (10, ALTURA_TELA - 60))
        exibir_texto(tela, fonte, "Setas + P: Jogador 2", (10, ALTURA_TELA - 30))

        if not jogo_ativo:
            titulo = fonte_titulo.render("Fim de jogo", True, BRANCO)
            tela.blit(titulo, ((LARGURA_TELA - titulo.get_width()) // 2, ALTURA_TELA // 2 - 40))
            resultado = fonte.render(vencedor or "Pressione Espaço para reiniciar", True, BRANCO)
            tela.blit(resultado, ((LARGURA_TELA - resultado.get_width()) // 2, ALTURA_TELA // 2 + 10))
            aviso = fonte.render("Pressione Espaço para jogar novamente ou ESC para sair", True, BRANCO)
            tela.blit(aviso, ((LARGURA_TELA - aviso.get_width()) // 2, ALTURA_TELA // 2 + 40))

        pygame.display.flip()

    pygame.quit()
