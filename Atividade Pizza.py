import pygame
import sys
import math

# Inicializar pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zone Defense")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonte
FONT = pygame.font.Font(None, 30)

# Imagens
BACKGROUND_IMG = pygame.image.load("images/background.png")
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

TOWER_IMAGES = [
    pygame.transform.scale(pygame.image.load("images/tower1.png"), (30, 30)),
    pygame.transform.scale(pygame.image.load("images/tower2.png"), (30, 30)),
    pygame.transform.scale(pygame.image.load("images/tower3.png"), (30, 30)),
]

ENEMY_IMAGE = pygame.transform.scale(pygame.image.load("images/enemy.png"), (20, 20))
PROJECTILE_IMAGE = pygame.transform.scale(pygame.image.load("images/projectile.png"), (10, 10))

# Configurações gerais
TOWER_COSTS = [100, 200, 250]  # Custo de construção
UPGRADE_COSTS = [100, 200, 250]  # Custo de upgrade correspondente ao tipo
ZONE_POSITION = (100, 500)
ZONE_RADIUS = 30
PATH_POINTS = [
    (0, 150), (100, 150), (200, 200), (300, 250),
    (400, 250), (500, 300), (600, 350), (700, 400), (750, 500)
]


### Funções utilitárias de desenho ###

def draw_path(win):
    """Desenha o caminho dos inimigos."""
    for i in range(len(PATH_POINTS) - 1):
        pygame.draw.line(win, BLACK, PATH_POINTS[i], PATH_POINTS[i + 1], 5)
        pygame.draw.circle(win, YELLOW, PATH_POINTS[i], 5)


def draw_background(win):
    """Desenha o fundo da tela."""
    win.blit(BACKGROUND_IMG, (0, 0))


def draw_zone(win, zone_health):
    """Desenha a zona de defesa."""
    pygame.draw.circle(win, GREEN if zone_health > 0 else RED, ZONE_POSITION, ZONE_RADIUS)
    health_text = FONT.render(f"{zone_health} HP", True, BLACK)
    win.blit(health_text, (ZONE_POSITION[0] - health_text.get_width() // 2, ZONE_POSITION[1] - 50))


def draw_interface(win, coins, score, wave, zone_health):
    """Exibe informações como moedas, pontuação, onda e saúde da zona."""
    text = FONT.render(f"Moedas: {coins} | Pontuação: {score} | Onda: {wave}", True, BLACK)
    win.blit(text, (10, 10))


### Classes ###

class Enemy:
    def __init__(self, path, speed, health):
        self.path = path
        self.speed = speed
        self.max_health = health
        self.health = health
        self.current_point = 0
        self.x, self.y = self.path[self.current_point]

    def move(self):
        """Move o inimigo pelo caminho. Retorna True se ele alcançar o final."""
        if self.current_point < len(self.path) - 1:
            target_x, target_y = self.path[self.current_point + 1]
            direction_x, direction_y = target_x - self.x, target_y - self.y
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

            if distance < self.speed:
                self.x, self.y = target_x, target_y
                self.current_point += 1
            else:
                self.x += self.speed * (direction_x / distance)
                self.y += self.speed * (direction_y / distance)
        return self.current_point == len(self.path) - 1

    def draw(self, win):
        """Desenha o inimigo usando imagem."""
        win.blit(ENEMY_IMAGE, (int(self.x) - 10, int(self.y) - 10))
        health_bar_width = 30
        health_ratio = self.health / self.max_health
        pygame.draw.rect(win, BLACK, (self.x - health_bar_width // 2, self.y - 15, health_bar_width, 5))
        pygame.draw.rect(win, GREEN, (self.x - health_bar_width // 2, self.y - 15, int(health_bar_width * health_ratio), 5))


class TowerStatus:
    def __init__(self, range, damage, cooldown, color):
        self.base_range = range
        self.base_damage = damage
        self.base_cooldown = cooldown
        self.color = color

    def get_stats(self, level):
        """Retorna as estatísticas ajustadas com base no nível da torre."""
        return {
            "range": self.base_range + (level - 1) * 20,
            "damage": self.base_damage + (level - 1) * 10,
            "cooldown": max(5, self.base_cooldown - (level - 1) * 2)
        }


class Tower:
    def __init__(self, x, y, status: TowerStatus, level=1):
        self.x = x
        self.y = y
        self.status = status
        self.level = level
        self.cooldown_timer = 0
        self.update_stats()

    def update_stats(self):
        """Atualiza as estatísticas da torre com base no nível."""
        stats = self.status.get_stats(self.level)
        self.range = stats["range"]
        self.damage = stats["damage"]
        self.cooldown = stats["cooldown"]

    def attack(self, enemies, projectiles):
        """Ataca os inimigos dentro do alcance."""
        if self.cooldown_timer == 0:
            for enemy in enemies:
                distance = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
                if distance <= self.range:
                    projectiles.append(Projectile(self.x, self.y, enemy, 5, self.damage))
                    self.cooldown_timer = self.cooldown
                    break

    def update(self):
        """Atualiza o cooldown da torre."""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def level_up(self):
        """Aumenta o nível da torre."""
        if self.level < 3:
            self.level += 1
            self.update_stats()

    def draw(self, win):
        """Desenha a torre com a imagem correspondente."""
        win.blit(TOWER_IMAGES[self.status.color], (self.x - 15, self.y - 15))
        pygame.draw.circle(win, BLACK, (self.x, self.y), self.range, 1)
        level_text = FONT.render(f"Lv{self.level}", True, BLACK)
        win.blit(level_text, (self.x - level_text.get_width() // 2, self.y - 30))


class Projectile:
    def __init__(self, x, y, target, speed, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.damage = damage

    def move(self):
        """Move o projétil em direção ao alvo. Retorna True se atingir o alvo."""
        direction_x, direction_y = self.target.x - self.x, self.target.y - self.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance < self.speed:
            return True
        self.x += self.speed * (direction_x / distance)
        self.y += self.speed * (direction_y / distance)
        return False

    def draw(self, win):
        """Desenha o projétil com a imagem correspondente."""
        win.blit(PROJECTILE_IMAGE, (int(self.x) - 5, int(self.y) - 5))


# A função principal permanece inalterada, exceto pela integração com as novas imagens.



### Função principal ###

def main():
    run = True
    clock = pygame.time.Clock()

    # Variáveis do jogo
    enemies, towers, projectiles = [], [], []
    wave, coins, score, zone_health = 1, 200, 0, 100
    spawn_timer, enemies_spawned, enemy_speed, enemy_health = 0, 0, 1, 50
    selected_tower_type = 0
    tower_types = [
        TowerStatus(100, 10, 15, GREEN),
        TowerStatus(90, 40, 60, YELLOW),
        TowerStatus(160, 27, 40, RED)
    ]

    # Loop principal
    while run:
        clock.tick(60)
        draw_background(win)
        draw_zone(win, zone_health)
        draw_interface(win, coins, score, wave, zone_health)
        draw_path(win)

        # Gerenciamento do jogo
        spawn_timer += 1
        if spawn_timer >= 90 and enemies_spawned < 10:
            spawn_timer, enemies_spawned = 0, enemies_spawned + 1
            enemies.append(Enemy(PATH_POINTS, enemy_speed, enemy_health))
        elif enemies_spawned >= 10:
            wave += 1
            enemies_spawned, enemy_speed, enemy_health = 0, enemy_speed + 0.2, enemy_health + 10

        # Atualização de inimigos, torres e projéteis
        for enemy in enemies[:]:
            if enemy.move():
                zone_health -= 10
                enemies.remove(enemy)
            elif enemy.health <= 0:
                enemies.remove(enemy)
                coins += 10
                score += 20

        for tower in towers:
            tower.update()
            tower.attack(enemies, projectiles)

        for projectile in projectiles[:]:
            if projectile.move():
                projectile.target.health -= projectile.damage
                projectiles.remove(projectile)

        # Desenha elementos
        for enemy in enemies:
            enemy.draw(win)
        for tower in towers:
            tower.draw(win)
        for projectile in projectiles:
            projectile.draw(win)

        pygame.display.update()

        # Eventos do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    for tower in towers:
                        if math.sqrt((tower.x - mouse_x) ** 2 + (tower.y - mouse_y) ** 2) <= 15 and coins >= UPGRADE_COSTS[selected_tower_type]:
                            coins -= UPGRADE_COSTS[selected_tower_type]
                            tower.level_up()
                elif event.button == 3 and coins >= TOWER_COSTS[selected_tower_type]:
                    coins -= TOWER_COSTS[selected_tower_type]
                    towers.append(Tower(mouse_x, mouse_y, tower_types[selected_tower_type]))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_tower_type = 0
                elif event.key == pygame.K_2:
                    selected_tower_type = 1
                elif event.key == pygame.K_3:
                    selected_tower_type = 2

    pygame.quit()


if __name__ == "__main__":
    main()
