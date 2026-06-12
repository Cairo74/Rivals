import pygame
import tkinter as tk
from tkinter import filedialog

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
        "imagem": None,
        "max_municao": 20,
        "municao": 20,
        "gun_side": "right",
        "nick": "",
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
    if jogador.get("imagem"):
        tela.blit(jogador["imagem"], jogador["rect"].topleft)
    else:
        pygame.draw.rect(tela, jogador["cor"], jogador["rect"])
    # desenha arma mais parecida: corpo + cano
    side = jogador.get("gun_side", "right")
    base_w, base_h = 10, 6
    barrel_w, barrel_h = 18, 4
    if side == "right":
        base = pygame.Rect(jogador["rect"].right - 2, jogador["rect"].centery - base_h // 2, base_w, base_h)
        barrel = pygame.Rect(base.right, jogador["rect"].centery - barrel_h // 2, barrel_w, barrel_h)
    else:
        base = pygame.Rect(jogador["rect"].left - base_w + 2, jogador["rect"].centery - base_h // 2, base_w, base_h)
        barrel = pygame.Rect(base.left - barrel_w, jogador["rect"].centery - barrel_h // 2, barrel_w, barrel_h)
    pygame.draw.rect(tela, (30, 30, 30), base)
    pygame.draw.rect(tela, (50, 50, 50), barrel)


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
        if tiro in tiros:
            tiros.remove(tiro)


def desenhar_tiros(tela, tiros):
    for tiro in tiros:
        pygame.draw.rect(tela, tiro["cor"], tiro["rect"])
def desenhar_nick_above(tela, jogador, fonte):
    nick = jogador.get("nick", "")
    if not nick:
        return
    cor = BRANCO
    superficie = fonte.render(nick, True, cor)
    x = jogador["rect"].centerx - superficie.get_width() // 2
    y = jogador["rect"].top - 22
    tela.blit(superficie, (x, y))

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

    if evento.key == jogador.get("tecla_disparo"):
        # verifica munição
        if jogador.get("municao", 0) <= 0:
            return
        jogador["municao"] = max(0, jogador.get("municao", 0) - 1)
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

    # atribui teclas de disparo separadas
    jogador1["tecla_disparo"] = pygame.K_e
    jogador2["tecla_disparo"] = pygame.K_p
    # teclas de recarga
    jogador1["tecla_recarregar"] = pygame.K_r
    jogador2["tecla_recarregar"] = pygame.K_m
    # lados da arma
    jogador1["gun_side"] = "right"
    jogador2["gun_side"] = "left"

    obstaculos = [
        pygame.Rect(300, 180, 40, 160),
        pygame.Rect(460, 260, 40, 160),
    ]

    tiros = []
    rodando = True
    jogo_ativo = False
    vencedor = None

    # variáveis de skin
    skin1 = None
    skin2 = None

    def carregar_imagem_por_dialogo():
        root = tk.Tk()
        root.withdraw()
        caminho = filedialog.askopenfilename(
            title="Escolha uma imagem",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
        )
        root.destroy()
        if not caminho:
            return None
        try:
            img = pygame.image.load(caminho).convert_alpha()
            img = pygame.transform.scale(img, (40, 40))
            return img
        except Exception:
            return None
    # função reaproveitável: tela inicial simples para escolher skins
    def mostrar_menu(skin1, skin2, nick1, nick2):
        nonlocal rodando
        inicio = True
        ativo = None  # 1 para nick1, 2 para nick2
        while inicio and rodando:
            relogio.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    inicio = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                        inicio = False
                    elif ativo == 1:
                        if evento.key == pygame.K_BACKSPACE:
                            nick1 = nick1[:-1]
                        elif evento.key == pygame.K_RETURN:
                            ativo = None
                        else:
                            char = evento.unicode
                            if char.isprintable() and len(nick1) < 16:
                                nick1 += char
                    elif ativo == 2:
                        if evento.key == pygame.K_BACKSPACE:
                            nick2 = nick2[:-1]
                        elif evento.key == pygame.K_RETURN:
                            ativo = None
                        else:
                            char = evento.unicode
                            if char.isprintable() and len(nick2) < 16:
                                nick2 += char
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mx, my = evento.pos
                    botao1 = pygame.Rect(LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 - 20, 120, 40)
                    botao2 = pygame.Rect(3 * LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 - 20, 120, 40)
                    botao_jogar = pygame.Rect((LARGURA_TELA - 160) // 2, ALTURA_TELA // 2 + 120, 160, 50)
                    caixa_nick1 = pygame.Rect(LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 + 30, 180, 30)
                    caixa_nick2 = pygame.Rect(3 * LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 + 30, 180, 30)
                    if botao1.collidepoint(mx, my):
                        img = carregar_imagem_por_dialogo()
                        if img:
                            skin1 = img
                    elif botao2.collidepoint(mx, my):
                        img = carregar_imagem_por_dialogo()
                        if img:
                            skin2 = img
                    elif botao_jogar.collidepoint(mx, my):
                        inicio = False
                    elif caixa_nick1.collidepoint(mx, my):
                        ativo = 1
                    elif caixa_nick2.collidepoint(mx, my):
                        ativo = 2

            tela.fill(CINZA)
            exibir_texto(tela, fonte_titulo, "Seleção de Skins e Nicks", (LARGURA_TELA // 2 - 180, 40))

            botao1 = pygame.Rect(LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 - 20, 120, 40)
            botao2 = pygame.Rect(3 * LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 - 20, 120, 40)
            botao_jogar = pygame.Rect((LARGURA_TELA - 160) // 2, ALTURA_TELA // 2 + 120, 160, 50)
            caixa_nick1 = pygame.Rect(LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 + 30, 180, 30)
            caixa_nick2 = pygame.Rect(3 * LARGURA_TELA // 4 - 60, ALTURA_TELA // 2 + 30, 180, 30)

            pygame.draw.rect(tela, jogador1["cor"], botao1)
            pygame.draw.rect(tela, jogador2["cor"], botao2)
            pygame.draw.rect(tela, BRANCO, botao_jogar)

            exibir_texto(tela, fonte, "Escolher skin Jogador 1 (E)", (botao1.x + 6, botao1.y + 10))
            exibir_texto(tela, fonte, "Escolher skin Jogador 2 (P)", (botao2.x + 6, botao2.y + 10))
            exibir_texto(tela, fonte, "Jogar", (botao_jogar.x + 60, botao_jogar.y + 14), cor=(0, 0, 0))

            # previews
            if skin1:
                tela.blit(skin1, (LARGURA_TELA // 4 - 20, ALTURA_TELA // 2 - 80))
            if skin2:
                tela.blit(skin2, (3 * LARGURA_TELA // 4 - 20, ALTURA_TELA // 2 - 80))

            # caixas de nick
            pygame.draw.rect(tela, (40, 40, 40), caixa_nick1)
            pygame.draw.rect(tela, (40, 40, 40), caixa_nick2)
            cor_ativo = (220, 220, 220) if ativo == 1 else BRANCO
            exibir_texto(tela, fonte, nick1 or "Nick 1", (caixa_nick1.x + 6, caixa_nick1.y + 6), cor=cor_ativo)
            cor_ativo = (220, 220, 220) if ativo == 2 else BRANCO
            exibir_texto(tela, fonte, nick2 or "Nick 2", (caixa_nick2.x + 6, caixa_nick2.y + 6), cor=cor_ativo)

            # mostra munição disponível na interface
            exibir_texto(tela, fonte, f"Municao: {jogador1.get('max_municao', 0)}", (LARGURA_TELA // 4 - 40, ALTURA_TELA // 2 + 70))
            exibir_texto(tela, fonte, f"Municao: {jogador2.get('max_municao', 0)}", (3 * LARGURA_TELA // 4 - 40, ALTURA_TELA // 2 + 70))

            pygame.display.flip()

        return skin1, skin2, nick1, nick2

    # mostrar menu inicial antes de começar (skins + nicks)
    nick1 = jogador1.get("nick", "")
    nick2 = jogador2.get("nick", "")
    skin1, skin2, nick1, nick2 = mostrar_menu(skin1, skin2, nick1, nick2)
    if skin1:
        jogador1["imagem"] = skin1
    if skin2:
        jogador2["imagem"] = skin2
    jogador1["nick"] = nick1
    jogador2["nick"] = nick2

    # loop principal do jogo
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
                    # reinicia posições e vidas mantendo skins
                    jogador1["rect"].topleft = (100, 100)
                    jogador2["rect"].topleft = (LARGURA_TELA - 140, ALTURA_TELA - 140)
                    jogador1["vidas"] = 3
                    jogador2["vidas"] = 3
                    jogador1["municao"] = jogador1.get("max_municao", 20)
                    jogador2["municao"] = jogador2.get("max_municao", 20)
                    jogador1["tecla_disparo"] = pygame.K_e
                    jogador2["tecla_disparo"] = pygame.K_p
                    tiros.clear()
                    jogo_ativo = True
                    vencedor = None
                else:
                    # recarga
                    if evento.key == jogador1.get("tecla_recarregar"):
                        jogador1["municao"] = jogador1.get("max_municao", 20)
                    elif evento.key == jogador2.get("tecla_recarregar"):
                        jogador2["municao"] = jogador2.get("max_municao", 20)
                    # disparo
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
                # volta para o menu sem perder as skins (permite editar nicks)
                skin1 = jogador1.get("imagem")
                skin2 = jogador2.get("imagem")
                nick1 = jogador1.get("nick", "")
                nick2 = jogador2.get("nick", "")
                skin1, skin2, nick1, nick2 = mostrar_menu(skin1, skin2, nick1, nick2)
                if skin1:
                    jogador1["imagem"] = skin1
                if skin2:
                    jogador2["imagem"] = skin2
                jogador1["nick"] = nick1
                jogador2["nick"] = nick2
                # resetar posições, vidas e munição mantendo skins
                jogador1["rect"].topleft = (100, 100)
                jogador2["rect"].topleft = (LARGURA_TELA - 140, ALTURA_TELA - 140)
                jogador1["vidas"] = 3
                jogador2["vidas"] = 3
                jogador1["municao"] = jogador1.get("max_municao", 20)
                jogador2["municao"] = jogador2.get("max_municao", 20)
                jogador1["tecla_disparo"] = pygame.K_e
                jogador2["tecla_disparo"] = pygame.K_p
                tiros.clear()
                jogo_ativo = True
            elif jogador_perdeu(jogador2["vidas"]):
                jogo_ativo = False
                vencedor = "Jogador 1 venceu!"
                skin1 = jogador1.get("imagem")
                skin2 = jogador2.get("imagem")
                nick1 = jogador1.get("nick", "")
                nick2 = jogador2.get("nick", "")
                skin1, skin2, nick1, nick2 = mostrar_menu(skin1, skin2, nick1, nick2)
                if skin1:
                    jogador1["imagem"] = skin1
                if skin2:
                    jogador2["imagem"] = skin2
                jogador1["nick"] = nick1
                jogador2["nick"] = nick2
                jogador1["rect"].topleft = (100, 100)
                jogador2["rect"].topleft = (LARGURA_TELA - 140, ALTURA_TELA - 140)
                jogador1["vidas"] = 3
                jogador1["vidas"] = 3
                jogador2["vidas"] = 3
                jogador1["municao"] = jogador1.get("max_municao", 20)
                jogador2["municao"] = jogador2.get("max_municao", 20)
                jogador1["tecla_disparo"] = pygame.K_e
                jogador2["tecla_disparo"] = pygame.K_p
                jogador2["tecla_disparo"] = pygame.K_p
                tiros.clear()
                jogo_ativo = True

        # fundo da arena: preto
        tela.fill((0, 0, 0))
        desenhar_obstaculos(tela, obstaculos)
        desenhar_jogador(tela, jogador1)
        desenhar_jogador(tela, jogador2)
        desenhar_nick_above(tela, jogador1, fonte)
        desenhar_nick_above(tela, jogador2, fonte)
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
