import pygame
import random

LARGURA = 1000
ALTURA = 600
FPS = 60

FASES = [
    ("Floresta", "Colete os resíduos e proteja a floresta."),
    ("Rio", "Ajude a manter o rio limpo."),
    ("Cidade", "Recicle corretamente os resíduos."),
    ("Energia", "Economize energia e evite desperdícios."),
    ("Planeta", "Complete a missão final pelo planeta."),
]

class EcoQuest:
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("EcoQuest - A Missão do Planeta")
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("arial", 28)
        self.fonte_grande = pygame.font.SysFont("arial", 48, bold=True)
        self.estado = "menu"
        self.fase = 0
        self.pontos = 0
        self.vidas = 3
        self.nome = "Jogador"
        self.jogador = pygame.Rect(100, 450, 45, 55)
        self.vel_y = 0
        self.no_chao = True
        self.itens = []
        self.obstaculos = []
        self.respostas = [
            ("Qual atitude ajuda o meio ambiente?", ["Jogar lixo no rio", "Reciclar resíduos", "Desperdiçar água"], 1),
            ("Qual recurso devemos economizar?", ["Água", "Lixo", "Poluição"], 0),
            ("O que pode ser reciclado?", ["Papel", "Fumaça", "Esgoto"], 0),
        ]
        self.pergunta_atual = 0
        self.mensagem = ""
        self.tempo_mensagem = 0

    def texto(self, texto, x, y, grande=False):
        fonte = self.fonte_grande if grande else self.fonte
        img = fonte.render(texto, True, (255, 255, 255))
        self.tela.blit(img, (x, y))

    def novo_cenario(self):
        self.jogador.x = 100
        self.jogador.y = 450
        self.vel_y = 0
        self.itens.clear()
        self.obstaculos.clear()

        for _ in range(7):
            x = random.randint(300, 900)
            y = random.randint(390, 500)
            self.itens.append(pygame.Rect(x, y, 30, 30))

        for _ in range(4):
            x = random.randint(400, 950)
            self.obstaculos.append(pygame.Rect(x, 485, 40, 35))

    def iniciar(self):
        self.estado = "jogo"
        self.fase = 0
        self.pontos = 0
        self.vidas = 3
        self.novo_cenario()

    def desenhar_fundo(self):
        fundos = [
            (50, 130, 70),
            (40, 130, 180),
            (120, 120, 120),
            (210, 170, 60),
            (70, 160, 100),
        ]
        self.tela.fill(fundos[self.fase])

        pygame.draw.rect(self.tela, (70, 50, 30), (0, 520, LARGURA, 80))

        # elementos simples do cenário
        if self.fase == 0:
            for x in range(50, LARGURA, 180):
                pygame.draw.rect(self.tela, (90, 55, 25), (x, 300, 35, 220))
                pygame.draw.circle(self.tela, (20, 100, 40), (x+18, 285), 70)
        elif self.fase == 1:
            pygame.draw.rect(self.tela, (30, 100, 190), (0, 430, LARGURA, 90))
        elif self.fase == 2:
            for x in range(20, LARGURA, 150):
                pygame.draw.rect(self.tela, (60, 60, 65), (x, 260, 100, 260))
        elif self.fase == 3:
            for x in range(80, LARGURA, 180):
                pygame.draw.rect(self.tela, (230, 230, 230), (x, 180, 70, 340))
        else:
            pygame.draw.circle(self.tela, (50, 180, 80), (800, 170), 120)

    def desenhar_hud(self):
        self.texto(f"Fase: {self.fase+1}/5 - {FASES[self.fase][0]}", 20, 15)
        self.texto(f"Pontos: {self.pontos}", 20, 50)
        self.texto(f"Vidas: {self.vidas}", 20, 85)

    def desenhar_jogo(self):
        self.desenhar_fundo()
        self.desenhar_hud()

        pygame.draw.rect(self.tela, (40, 90, 220), self.jogador)
        pygame.draw.circle(self.tela, (255, 220, 170),
                           (self.jogador.centerx, self.jogador.top - 10), 15)

        for item in self.itens:
            pygame.draw.rect(self.tela, (40, 220, 80), item)
            pygame.draw.rect(self.tela, (255, 255, 255), (item.x+8, item.y+5, 14, 20), 2)

        for obstaculo in self.obstaculos:
            pygame.draw.rect(self.tela, (200, 50, 50), obstaculo)

        self.texto(FASES[self.fase][1], 300, 20)

        if self.mensagem and self.tempo_mensagem > 0:
            self.texto(self.mensagem, 300, 550)

    def atualizar_jogo(self):
        teclas = pygame.key.get_pressed()
        velocidade = 5

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.jogador.x -= velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.jogador.x += velocidade

        self.jogador.x = max(0, min(LARGURA - self.jogador.width, self.jogador.x))

        self.vel_y += 1
        self.jogador.y += self.vel_y

        if self.jogador.bottom >= 520:
            self.jogador.bottom = 520
            self.vel_y = 0
            self.no_chao = True

        for item in self.itens[:]:
            if self.jogador.colliderect(item):
                self.itens.remove(item)
                self.pontos += 10
                self.mensagem = "+10 pontos! Resíduo coletado."
                self.tempo_mensagem = 90

        for obstaculo in self.obstaculos:
            if self.jogador.colliderect(obstaculo):
                self.jogador.x -= 25
                self.vidas -= 1
                self.mensagem = "Cuidado! Você perdeu uma vida."
                self.tempo_mensagem = 90
                if self.vidas <= 0:
                    self.estado = "fim"

        if self.tempo_mensagem > 0:
            self.tempo_mensagem -= 1

        if not self.itens:
            self.estado = "pergunta"

    def desenhar_menu(self):
        self.tela.fill((30, 120, 70))
        self.texto("ECOQUEST", 320, 130, True)
        self.texto("A Missão do Planeta", 325, 195)
        self.texto("ENTER - Começar", 350, 300)
        self.texto("ESC - Sair", 390, 350)

    def desenhar_pergunta(self):
        self.tela.fill((35, 90, 130))
        pergunta, alternativas, _ = self.respostas[self.pergunta_atual]
        self.texto("PERGUNTA AMBIENTAL", 300, 70, True)
        self.texto(pergunta, 180, 180)

        for i, alternativa in enumerate(alternativas):
            self.texto(f"{i+1} - {alternativa}", 230, 270 + i * 60)

    def responder(self, indice):
        _, _, correta = self.respostas[self.pergunta_atual]
        if indice == correta:
            self.pontos += 50
            self.mensagem = "Resposta correta! +50 pontos."
        else:
            self.vidas -= 1
            self.mensagem = "Resposta incorreta. Você perdeu uma vida."

        if self.vidas <= 0:
            self.estado = "fim"
            return

        self.pergunta_atual = (self.pergunta_atual + 1) % len(self.respostas)

        if self.fase == len(FASES) - 1:
            self.estado = "vitoria"
        else:
            self.fase += 1
            self.novo_cenario()
            self.estado = "jogo"

    def desenhar_fim(self):
        self.tela.fill((100, 35, 35))
        self.texto("FIM DE JOGO", 340, 150, True)
        self.texto(f"Pontuação: {self.pontos}", 370, 240)
        self.texto("ENTER - Jogar novamente", 300, 330)
        self.texto("ESC - Sair", 400, 390)

    def desenhar_vitoria(self):
        self.tela.fill((35, 130, 75))
        self.texto("PARABÉNS!", 350, 130, True)
        self.texto("Você completou a missão pelo planeta!", 220, 220)
        self.texto(f"Pontuação final: {self.pontos}", 330, 290)
        self.texto("ENTER - Jogar novamente", 300, 380)
        self.texto("ESC - Sair", 400, 430)

    def executar(self):
        rodando = True

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False

                    if self.estado == "menu" and evento.key == pygame.K_RETURN:
                        self.iniciar()

                    elif self.estado == "jogo" and evento.key == pygame.K_SPACE and self.no_chao:
                        self.vel_y = -17
                        self.no_chao = False

                    elif self.estado == "pergunta":
                        if evento.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                            self.responder(evento.key - pygame.K_1)

                    elif self.estado in ("fim", "vitoria") and evento.key == pygame.K_RETURN:
                        self.iniciar()

            if self.estado == "jogo":
                self.atualizar_jogo()

            if self.estado == "menu":
                self.desenhar_menu()
            elif self.estado == "jogo":
                self.desenhar_jogo()
            elif self.estado == "pergunta":
                self.desenhar_pergunta()
            elif self.estado == "fim":
                self.desenhar_fim()
            elif self.estado == "vitoria":
                self.desenhar_vitoria()

            pygame.display.flip()
            self.clock.tick(FPS)
