import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    BRANCO,
    FUNDO,
    FUNDO_GRADE,
    COR_BORDA_ARENA,
    COR_JOGADOR1,
    COR_JOGADOR2,
    COR_OBSTACULO,
    COR_OBSTACULO_BORDA,
    COR_TEXTO,
    COR_TEXTO_SUAVE,
    COR_OVERLAY,
)
from src.funcoes import (
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)


def escurecer(cor, fator=0.55):
    """Retorna uma versão mais escura da cor informada."""
    return (int(cor[0] * fator), int(cor[1] * fator), int(cor[2] * fator))


def clarear(cor, fator=0.45):
    """Retorna uma versão mais clara da cor informada."""
    return (
        int(cor[0] + (255 - cor[0]) * fator),
        int(cor[1] + (255 - cor[1]) * fator),
        int(cor[2] + (255 - cor[2]) * fator),
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


def desenhar_fundo(tela):
    """Desenha a arena: fundo escuro, grade sutil, divisória central e borda."""
    tela.fill(FUNDO)

    espacamento = 40
    for x in range(0, LARGURA_TELA, espacamento):
        pygame.draw.line(tela, FUNDO_GRADE, (x, 0), (x, ALTURA_TELA))
    for y in range(0, ALTURA_TELA, espacamento):
        pygame.draw.line(tela, FUNDO_GRADE, (0, y), (LARGURA_TELA, y))

    # Linha divisória central na diagonal entre os cantos dos jogadores.
    pygame.draw.line(
        tela, COR_BORDA_ARENA, (LARGURA_TELA, 0), (0, ALTURA_TELA), 1
    )

    # Borda da arena.
    pygame.draw.rect(tela, COR_BORDA_ARENA, (0, 0, LARGURA_TELA, ALTURA_TELA), 4)


def desenhar_jogador(tela, jogador):
    """Desenha o jogador com sombra, corpo arredondado e indicador de mira."""
    rect = jogador["rect"]
    cor = jogador["cor"]

    # Sombra projetada no chão.
    sombra = pygame.Rect(0, 0, rect.width, 10)
    sombra.center = (rect.centerx, rect.bottom + 2)
    superficie_sombra = pygame.Surface(sombra.size, pygame.SRCALPHA)
    pygame.draw.ellipse(superficie_sombra, (0, 0, 0, 90), superficie_sombra.get_rect())
    tela.blit(superficie_sombra, sombra)

    # Indicador de mira (cano) apontando na direção atual.
    centro = pygame.Vector2(rect.center)
    ponta = centro + jogador["direcao"] * (rect.width / 2 + 8)
    pygame.draw.line(tela, escurecer(cor), centro, ponta, 7)
    pygame.draw.circle(tela, clarear(cor, 0.2), (int(ponta.x), int(ponta.y)), 5)

    # Corpo arredondado com borda.
    pygame.draw.rect(tela, escurecer(cor), rect, border_radius=10)
    corpo = rect.inflate(-6, -6)
    pygame.draw.rect(tela, cor, corpo, border_radius=8)

    # Brilho superior para dar volume.
    brilho = pygame.Rect(corpo.x + 4, corpo.y + 4, corpo.width - 8, corpo.height // 3)
    pygame.draw.rect(tela, clarear(cor, 0.35), brilho, border_radius=6)


def desenhar_obstaculos(tela, obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, COR_OBSTACULO, obstaculo, border_radius=6)
        pygame.draw.rect(tela, COR_OBSTACULO_BORDA, obstaculo, width=2, border_radius=6)


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
    """Desenha cada tiro como um círculo com brilho central."""
    for tiro in tiros:
        centro = tiro["rect"].center
        raio = max(tiro["rect"].width, tiro["rect"].height) // 2 + 1
        pygame.draw.circle(tela, escurecer(tiro["cor"], 0.7), centro, raio + 2)
        pygame.draw.circle(tela, tiro["cor"], centro, raio)
        pygame.draw.circle(tela, clarear(tiro["cor"], 0.6), centro, max(1, raio - 2))


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


def processar_disparo(evento, jogador, tiros, tecla_tiro):
    """Cria um tiro do jogador quando a sua tecla de disparo específica é pressionada."""
    if evento.type != pygame.KEYDOWN:
        return

    if evento.key == tecla_tiro:
        origem = jogador["rect"].center
        tiro = criar_tiro(origem, jogador["direcao"], jogador["cor"])
        tiros.append(tiro)


def exibir_texto(tela, fonte, texto, posicao, cor=COR_TEXTO):
    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, posicao)


def desenhar_vidas(tela, x, y, vidas, cor, alinhar_direita=False):
    """Desenha a quantidade de vidas como pequenos quadrados coloridos."""
    tamanho = 16
    espaco = 6
    for i in range(vidas):
        deslocamento = i * (tamanho + espaco)
        if alinhar_direita:
            px = x - deslocamento - tamanho
        else:
            px = x + deslocamento
        bloco = pygame.Rect(px, y, tamanho, tamanho)
        pygame.draw.rect(tela, escurecer(cor), bloco, border_radius=4)
        pygame.draw.rect(tela, cor, bloco.inflate(-4, -4), border_radius=3)


def desenhar_hud(tela, fonte, jogador1, jogador2):
    """Desenha placar de vidas e legendas de controles."""
    exibir_texto(tela, fonte, "Jogador 1", (16, 12), COR_JOGADOR1)
    desenhar_vidas(tela, 16, 38, jogador1["vidas"], jogador1["cor"])

    texto_j2 = "Jogador 2"
    largura_j2 = fonte.size(texto_j2)[0]
    exibir_texto(tela, fonte, texto_j2, (LARGURA_TELA - 16 - largura_j2, 12), COR_JOGADOR2)
    desenhar_vidas(tela, LARGURA_TELA - 16, 38, jogador2["vidas"], jogador2["cor"], alinhar_direita=True)

    exibir_texto(tela, fonte, "WASD + E", (16, ALTURA_TELA - 30), COR_TEXTO_SUAVE)
    texto_ctrl2 = "Setas + P"
    largura_ctrl2 = fonte.size(texto_ctrl2)[0]
    exibir_texto(tela, fonte, texto_ctrl2, (LARGURA_TELA - 16 - largura_ctrl2, ALTURA_TELA - 30), COR_TEXTO_SUAVE)


def desenhar_tela_fim(tela, fonte, fonte_titulo, vencedor):
    """Desenha o overlay de fim de jogo com o vencedor e instruções."""
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((COR_OVERLAY[0], COR_OVERLAY[1], COR_OVERLAY[2], 200))
    tela.blit(overlay, (0, 0))

    painel = pygame.Rect(0, 0, 460, 220)
    painel.center = (LARGURA_TELA // 2, ALTURA_TELA // 2)
    pygame.draw.rect(tela, FUNDO, painel, border_radius=16)
    pygame.draw.rect(tela, COR_BORDA_ARENA, painel, width=3, border_radius=16)

    titulo = fonte_titulo.render("Fim de jogo", True, BRANCO)
    tela.blit(titulo, ((LARGURA_TELA - titulo.get_width()) // 2, painel.top + 30))

    resultado = fonte.render(vencedor or "Empate", True, COR_TEXTO)
    tela.blit(resultado, ((LARGURA_TELA - resultado.get_width()) // 2, painel.centery - 5))

    aviso = fonte.render("Espaço: jogar de novo    ESC: sair", True, COR_TEXTO_SUAVE)
    tela.blit(aviso, ((LARGURA_TELA - aviso.get_width()) // 2, painel.bottom - 45))


def ler_direcao(teclas, mapa_teclas):
    """Lê a direção a partir do mapa de teclas de movimento de um jogador."""
    direcao = pygame.Vector2(0, 0)
    if teclas[mapa_teclas["esquerda"]]:
        direcao.x = -1
    if teclas[mapa_teclas["direita"]]:
        direcao.x = 1
    if teclas[mapa_teclas["cima"]]:
        direcao.y = -1
    if teclas[mapa_teclas["baixo"]]:
        direcao.y = 1
    return direcao


def executar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 28)
    fonte_titulo = pygame.font.SysFont(None, 42, bold=True)

    posicao_inicial_1 = (100, 100)
    posicao_inicial_2 = (LARGURA_TELA - 140, ALTURA_TELA - 140)

    jogador1 = criar_jogador(posicao_inicial_1, COR_JOGADOR1)
    jogador2 = criar_jogador(posicao_inicial_2, COR_JOGADOR2)

    teclas_jogador1 = {
        "esquerda": pygame.K_a,
        "direita": pygame.K_d,
        "cima": pygame.K_w,
        "baixo": pygame.K_s,
    }
    teclas_jogador2 = {
        "esquerda": pygame.K_LEFT,
        "direita": pygame.K_RIGHT,
        "cima": pygame.K_UP,
        "baixo": pygame.K_DOWN,
    }

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
                    jogador1 = criar_jogador(posicao_inicial_1, COR_JOGADOR1)
                    jogador2 = criar_jogador(posicao_inicial_2, COR_JOGADOR2)
                    tiros.clear()
                    jogo_ativo = True
                    vencedor = None
                elif jogo_ativo:
                    # E dispara apenas o Jogador 1; P dispara apenas o Jogador 2.
                    processar_disparo(evento, jogador1, tiros, pygame.K_e)
                    processar_disparo(evento, jogador2, tiros, pygame.K_p)

        if jogo_ativo:
            teclas = pygame.key.get_pressed()

            direcao1 = ler_direcao(teclas, teclas_jogador1)
            if direcao1.length_squared() > 0:
                jogador1["direcao"] = direcao1.normalize()

            direcao2 = ler_direcao(teclas, teclas_jogador2)
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
                if verificar_colisao(tiro["rect"], jogador1["rect"]) and tiro["cor"] != jogador1["cor"]:
                    jogador1["vidas"] = tomar_dano(jogador1["vidas"], 1)
                    tiros_para_remover.append(tiro)
                elif verificar_colisao(tiro["rect"], jogador2["rect"]) and tiro["cor"] != jogador2["cor"]:
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

        desenhar_fundo(tela)
        desenhar_obstaculos(tela, obstaculos)
        desenhar_jogador(tela, jogador1)
        desenhar_jogador(tela, jogador2)
        desenhar_tiros(tela, tiros)
        desenhar_hud(tela, fonte, jogador1, jogador2)

        if not jogo_ativo:
            desenhar_tela_fim(tela, fonte, fonte_titulo, vencedor)

        pygame.display.flip()

    pygame.quit()
