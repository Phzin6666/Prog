import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definindo algumas cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)  # Cor da pele
RED = (255, 0, 0)  # Cor da camisa e das caixas vermelhas
BLUE = (0, 0, 255)  # Cor do short
BROWN = (139, 69, 19)  # Cor da madeira das caixas
DARK_BROWN = (101, 67, 33)
GRAY = (169, 169, 169)
ASPHALT_GRAY = (50, 50, 50)  # Cor do cenário (asfalto)
BLACK_BOMB = (0, 0, 0)  # Cor da bomba

# Configurações da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Food Drop Inspired by Pou")

# Configurações do jogador (pessoa)
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 7

# Configurações da comida
food_width = 30
food_height = 30
food_x = random.randint(0, SCREEN_WIDTH - food_width)
food_y = 0
food_speed = 3

# Configurações das caixas vermelhas (que causam dano)
red_box_x = random.randint(0, SCREEN_WIDTH - food_width)
red_box_y = -random.randint(100, 500)  # Caixas vermelhas aparecem mais tarde
red_box_speed = 3

# Configurações da bomba
bomb_width = 20
bomb_height = 20
bomb_x = random.randint(0, SCREEN_WIDTH - bomb_width)
bomb_y = -random.randint(100, 500)  # A bomba aparece aleatoriamente acima da tela
bomb_speed = 3
bomb_spawn_time = random.randint(1500, 5000)  # Tempo aleatório para gerar uma nova bomba
last_bomb_spawn_time = pygame.time.get_ticks()  # Tempo em que a última bomba foi gerada

# Variáveis do jogo
score = 0
lives = 3  # O jogador começa com 3 vidas
clock = pygame.time.Clock()
running = True
ticks_per_second = 30  # Ticks iniciais

# Função para desenhar uma pessoa com camisa vermelha, short azul, cabelo e olhos
def draw_person(x, y, leg_animation_offset):
    # Cabeça (bege com olhos e cabelo preto)
    pygame.draw.circle(screen, BEIGE, (x + 25, y + 10), 10)  # Cabeça
    pygame.draw.rect(screen, BLACK, (x + 15, y, 20, 5))  # Cabelo
    pygame.draw.circle(screen, BLACK, (x + 20, y + 10), 2)  # Olho esquerdo
    pygame.draw.circle(screen, BLACK, (x + 30, y + 10), 2)  # Olho direito

    # Corpo (camisa vermelha)
    pygame.draw.rect(screen, RED, (x + 15, y + 20, 20, 20))  # Camisa

    # Short (azul)
    pygame.draw.rect(screen, BLUE, (x + 15, y + 40, 20, 10))  # Short

    # Braços levantados (cor de pele - bege)
    pygame.draw.line(screen, BEIGE, (x + 15, y + 20), (x - 5, y + 5), 5)  # Braço esquerdo
    pygame.draw.line(screen, BEIGE, (x + 35, y + 20), (x + 55, y + 5), 5)  # Braço direito

    # Pernas (com animação)
    pygame.draw.line(screen, BEIGE, (x + 20, y + 50 + leg_animation_offset), (x + 20, y + 70), 5)  # Perna esquerda
    pygame.draw.line(screen, BEIGE, (x + 30, y + 50 - leg_animation_offset), (x + 30, y + 70), 5)  # Perna direita

# Função para desenhar corações de vida (com formato real)
def draw_heart(x, y):
    heart_color = RED
    pygame.draw.circle(screen, heart_color, (x - 10, y), 10)  # Lado esquerdo do coração
    pygame.draw.circle(screen, heart_color, (x + 10, y), 10)  # Lado direito do coração
    pygame.draw.polygon(screen, heart_color, [(x - 20, y), (x + 20, y), (x, y + 30)])  # Parte inferior

# Função para desenhar as vidas do jogador
def draw_hearts(lives):
    for i in range(lives):
        draw_heart(30 + i * 40, 40)

# Função para desenhar uma "caixa" de madeira 3D com paraquedas
def draw_wooden_box_with_parachute(x, y, width, height):
    # Caixa de madeira
    pygame.draw.rect(screen, BROWN, (x, y, width, height))

    # Detalhes da caixa
    pygame.draw.line(screen, DARK_BROWN, (x, y + 5), (x + width, y + height - 5), 2)
    pygame.draw.line(screen, DARK_BROWN, (x, y + height - 5), (x + width, y + 5), 2)

    # Paraquedas
    pygame.draw.arc(screen, GRAY, (x - 10, y - 30, width + 20, 40), 0, 3.14, 2)  # Parte superior
    pygame.draw.line(screen, GRAY, (x, y), (x + 5, y - 20), 2)  # Corda esquerda
    pygame.draw.line(screen, GRAY, (x + width, y), (x + width - 5, y - 20), 2)  # Corda direita

# Função para desenhar a caixa vermelha (mais realista) com paraquedas
def draw_red_box_with_parachute(x, y, width, height):
    # Caixa vermelha
    pygame.draw.rect(screen, RED, (x, y, width, height))

    # Paraquedas
    pygame.draw.arc(screen, GRAY, (x - 10, y - 30, width + 20, 40), 0, 3.14, 2)  # Parte superior
    pygame.draw.line(screen, GRAY, (x, y), (x + 5, y - 20), 2)  # Corda esquerda
    pygame.draw.line(screen, GRAY, (x + width, y), (x + width - 5, y - 20), 2)  # Corda direita

# Função para desenhar a bomba com paraquedas
def draw_bomb(x, y):
    # Paraquedas da bomba
    pygame.draw.arc(screen, GRAY, (x - 10, y - 30, bomb_width + 20, 40), 0, 3.14, 2)  # Parte superior do paraquedas
    pygame.draw.line(screen, GRAY, (x, y), (x + 5, y - 20), 2)  # Corda esquerda
    pygame.draw.line(screen, GRAY, (x + bomb_width, y), (x + bomb_width - 5, y - 20), 2)  # Corda direita

    # Bomba
    pygame.draw.rect(screen, BLACK_BOMB, (x, y, bomb_width, bomb_height))  # Bomba
    pygame.draw.circle(screen, (255, 255, 0), (x + bomb_width // 2, y + bomb_height // 2), 5)  # Detalhe da bomba

# Loop principal do jogo
leg_animation_offset = 0  # Offset para a animação das pernas
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_j]:  # Aumenta a pontuação ao pressionar "J"
        score += 1

    # Movimentação da comida
    food_y += food_speed

    # Verifica se a comida caiu
    if food_y > SCREEN_HEIGHT:
        food_x = random.randint(0, SCREEN_WIDTH - food_width)
        food_y = 0

    # Movimentação da caixa vermelha
    red_box_y += red_box_speed

    # Verifica se a caixa vermelha caiu
    if red_box_y > SCREEN_HEIGHT:
        red_box_x = random.randint(0, SCREEN_WIDTH - food_width)
        red_box_y = -random.randint(100, 500)  # Reaparece em posição aleatória

    # Movimentação da bomba
    bomb_y += bomb_speed
    current_time = pygame.time.get_ticks()

    # Gera nova bomba em intervalos aleatórios
    if current_time - last_bomb_spawn_time > bomb_spawn_time:
        bomb_x = random.randint(0, SCREEN_WIDTH - bomb_width)
        bomb_y = -random.randint(100, 500)  # A bomba aparece aleatoriamente acima da tela
        last_bomb_spawn_time = current_time  # Atualiza o tempo da última bomba
        bomb_spawn_time = random.randint(1500, 5000)  # Gera um novo tempo aleatório para a próxima bomba

    # Verifica se o jogador pegou a comida
    if (player_x < food_x + food_width and
            player_x + player_width > food_x and
            player_y < food_y + food_height and
            player_y + player_height > food_y):
        score += 1
        food_x = random.randint(0, SCREEN_WIDTH - food_width)
        food_y = 0

    # Verifica se o jogador pegou a caixa vermelha
    if (player_x < red_box_x + food_width and
            player_x + player_width > red_box_x and
            player_y < red_box_y + food_height and
            player_y + player_height > red_box_y):
        lives -= 1  # Tira 1 de vida
        red_box_x = random.randint(0, SCREEN_WIDTH - food_width)
        red_box_y = -random.randint(100, 500)  # Reaparece em posição aleatória

    # Verifica se o jogador pegou a bomba
    if (player_x < bomb_x + bomb_width and
            player_x + player_width > bomb_x and
            player_y < bomb_y + bomb_height and
            player_y + player_height > bomb_y):
        lives -= 3  # Tira 3 de vida
        bomb_x = random.randint(0, SCREEN_WIDTH - bomb_width)
        bomb_y = -random.randint(100, 500)  # Reaparece em posição aleatória

    # Aumenta os ticks a cada 4 pontos
    if score % 4 == 0 and score > 0:
        ticks_per_second = int(30 * (1 + (score // 4) * 0.2))  # Aumenta a velocidade em 20% a cada 4 pontos

    # Verifica se o jogador ficou sem vidas
    if lives <= 0:
        running = False  # Encerra o jogo

    # Preencher a tela com a cor do asfalto (cenário de rua)
    screen.fill(ASPHALT_GRAY)

    # Desenhar o jogador (pessoa com roupas, cabelo e olhos) e animação das pernas
    leg_animation_offset = 5 if (pygame.time.get_ticks() // 100) % 2 == 0 else -5  # Alterna o offset para a animação
    draw_person(player_x, player_y, leg_animation_offset)

    # Desenhar a comida (caixas de madeira com paraquedas)
    draw_wooden_box_with_parachute(food_x, food_y, food_width, food_height)

    # Desenhar a caixa vermelha (mais realista) com paraquedas
    draw_red_box_with_parachute(red_box_x, red_box_y, food_width, food_height)

    # Desenhar a bomba com paraquedas
    draw_bomb(bomb_x, bomb_y)

    # Desenhar os corações de vida
    draw_hearts(lives)

    # Exibir a pontuação
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a velocidade do jogo
    clock.tick(ticks_per_second)  # Controla os ticks por segundo

# Encerrar o Pygame
pygame.quit()
