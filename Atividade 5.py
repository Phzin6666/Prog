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

# Adicionar custos das torres
TOWER_COSTS = [100, 200, 250]  # Custo de construção
UPGRADE_COSTS = [100, 200, 250]  # Custo de upgrade correspondente ao tipo

# Configuração da zona
ZONE_POSITION = (100, 500)
ZONE_RADIUS = 30

# Caminho dos inimigos
PATH_POINTS = [
    (0, 150), (100, 150), (200, 200), (300, 250),
    (400, 250), (500, 300), (600, 350), (700, 400),
    (750, 500)
]

# Função para desenhar o caminho
def draw_path(win):
    if len(PATH_POINTS) < 2:
        return
    for i in range(len(PATH_POINTS) - 1):
        pygame.draw.line(win, BLACK, PATH_POINTS[i], PATH_POINTS[i + 1], 5)
        pygame.draw.circle(win, YELLOW, PATH_POINTS[i], 5)

# Função para desenhar o fundo
def draw_background(win):
    win.fill(WHITE)

# Função para desenhar a zona de defesa
def draw_zone(win, zone_health):
    pygame.draw.circle(win, GREEN if zone_health > 0 else RED, ZONE_POSITION, ZONE_RADIUS)
    health_text = FONT.render(f"{zone_health} HP", True, BLACK)
    win.blit(health_text, (ZONE_POSITION[0] - health_text.get_width() // 2, ZONE_POSITION[1] - 50))

# Função para desenhar a interface
def draw_interface(win, coins, score, wave, zone_health):
    text = FONT.render(f"Moedas: {coins} | Pontuação: {score} | Onda: {wave}", True, BLACK)
    win.blit(text, (10, 10))

# Classe para representar inimigos
class Enemy:
    def __init__(self, path, speed, health):
        self.path = path
        self.speed = speed
        self.max_health = health
        self.health = health
        self.current_point = 0
        self.x, self.y = self.path[self.current_point]

    def move(self):
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
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), 10)
        health_bar_width = 30
        health_ratio = self.health / self.max_health
        pygame.draw.rect(win, BLACK, (self.x - health_bar_width // 2, self.y - 15, health_bar_width, 5))
        pygame.draw.rect(win, GREEN, (self.x - health_bar_width // 2, self.y - 15, int(health_bar_width * health_ratio), 5))

# Classe para representar torres
class Tower:
    def __init__(self, x, y, range, damage, cooldown, color, level=1, tower_type=0):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.cooldown_timer = 0
        self.color = color
        self.level = level
        self.tower_type = tower_type

    def attack(self, enemies, projectiles):
        if self.cooldown_timer == 0:
            for enemy in enemies:
                distance = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
                if distance <= self.range:
                    projectiles.append(Projectile(self.x, self.y, enemy, 5, self.damage))
                    self.cooldown_timer = self.cooldown
                    break

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def level_up(self):
        if self.level < 3:
            if self.tower_type == 0:  # Torre tipo 1
                self.range += 20
                self.damage += 10
            elif self.tower_type == 1:  # Torre tipo 2
                self.damage += 25
            elif self.tower_type == 2:  # Torre tipo 3
                self.cooldown = max(5, self.cooldown - 2)
                self.range += 15
            self.level += 1

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), 15)
        pygame.draw.circle(win, BLACK, (self.x, self.y), self.range, 1)
        level_text = FONT.render(f"Lv{self.level}", True, BLACK)
        win.blit(level_text, (self.x - level_text.get_width() // 2, self.y - 30))

# Classe para representar projéteis
class Projectile:
    def __init__(self, x, y, target, speed, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.damage = damage

    def move(self):
        direction_x, direction_y = self.target.x - self.x, self.target.y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)
        if distance < self.speed:
            return True
        self.x += self.speed * (direction_x / distance)
        self.y += self.speed * (direction_y / distance)
        return False

    def draw(self, win):
        pygame.draw.circle(win, BLACK, (int(self.x), int(self.y)), 5)

# Função principal
def main():
    run = True
    clock = pygame.time.Clock()
    enemies = []
    towers = []
    projectiles = []
    wave = 1
    coins = 200
    score = 0
    zone_health = 100
    spawn_timer = 0
    enemies_spawned = 0
    enemy_speed = 1
    enemy_health = 50
    selected_tower_type = 0
    tower_colors = [GREEN, YELLOW, RED]

    while run:
        clock.tick(60)
        draw_background(win)
        draw_zone(win, zone_health)
        draw_interface(win, coins, score, wave, zone_health)
        draw_path(win)

        spawn_timer += 1
        if spawn_timer >= 90:
            spawn_timer = 0
            if enemies_spawned < 10:
                enemies.append(Enemy(PATH_POINTS, enemy_speed, enemy_health))
                enemies_spawned += 1
            else:
                wave += 1
                enemies_spawned = 0
                enemy_speed += 0.2
                enemy_health += 10

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

        if zone_health <= 0:
            print("A base foi destruída! Você perdeu!")
            run = False

        for enemy in enemies:
            enemy.draw(win)
        for tower in towers:
            tower.draw(win)
        for projectile in projectiles:
            projectile.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    for tower in towers:
                        if math.sqrt((tower.x - mouse_x) ** 2 + (tower.y - mouse_y) ** 2) <= 15:
                            if coins >= UPGRADE_COSTS[tower.tower_type]:
                                coins -= UPGRADE_COSTS[tower.tower_type]
                                tower.level_up()
                elif event.button == 3:
                    if coins >= TOWER_COSTS[selected_tower_type]:
                        coins -= TOWER_COSTS[selected_tower_type]
                        towers.append(Tower(mouse_x, mouse_y, 100, 10, 50, tower_colors[selected_tower_type], tower_type=selected_tower_type))
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
