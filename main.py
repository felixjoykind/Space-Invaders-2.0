import pygame
import os
import time
import random

# Initializing pygame
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders 0.2.0")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Laser class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window): # Drawing
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel): # Moving
        self.y += vel
    
    def off_screen(self, height): # Is off the screen
        return not (self.y <= height and self.y >= 0)
    
    def collision(self, obj): # Is colliding with something
        return collide(obj, self)

# Ship class (Player, Enemy, Boss)
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(WIN)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if obj.type == 'boss' and laser.collision(obj) and obj.health > 0:
                        obj.health -= 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                    elif laser.collision(obj) and obj.type != 'boss':
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.type = 'enemy'

    def move(self, vel):
        self.y += vel
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Boss(Ship):
    def __init__(self, x, y, health=1200):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(RED_SPACE_SHIP, (250, 200))
        self.laser_img = pygame.transform.scale(RED_LASER, (150, 150))
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel_y = 1.5
        self.vel_x = 1.5
        self.type = 'boss'
        self.max_health = health
        self.come = False

    def move(self, vel):
        self.y += self.vel_y

        if self.y >= 100 and not self.come:
            self.come = True

        if self.come:
            self.x += self.vel_x

        if self.health <= 0:
            self.vel_x = 0
            self.vel_y = 0

        if self.x + self.ship_img.get_width() >= WIDTH:
            self.vel_x = -random.randint(1, 3)
        elif self.x <= 0:
            self.vel_x = random.randint(1, 3)
        elif self.y + self.ship_img.get_height() >= HEIGHT:
            self.vel_y = -random.randint(1, 3)
        elif self.y <= 0 and self.come:
            self.vel_y = random.randint(1, 3)
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser1 = Laser(self.x+20, self.y, self.laser_img)
            laser2 = Laser(self.x+60, self.y, self.laser_img)
            laser3 = Laser(self.x+100, self.y, self.laser_img)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            self.lasers.append(laser3)
            self.cool_down_counter = 1
    
    def draw(self, window):
        super().draw(window)
        if self.come:
            self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (165, 10, WIDTH-165*2, 10))
        pygame.draw.rect(window, (0, 255, 0), (165, 10, (WIDTH-(165*2)) * (self.health/self.max_health), 10))

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

def main():
    run = True
    FPS = 60
    level = 0
    boss_spawned = False
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    dificulty = 5
    wave_length = dificulty
    enemy_vel = 1
    level_to_boss = dificulty - 2

    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))

        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0 and level < level_to_boss and not boss_spawned:
                level += 1
                wave_length += dificulty
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1300, -100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
        elif level == level_to_boss and not boss_spawned:
            enemies = [] # Removing all enemies
            enemies.append(Boss(WIDTH/2-130, -350)) # Spawning boss
            boss_spawned = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        pygame.init()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 4*60) == 1 and enemy.health > 0:
                enemy.shoot()

            if collide(enemy, player):
                if enemy.type == 'boss':
                    player.health -= 0.3
                else:
                    player.health -= 10
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2., 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    
    pygame.quit()

if __name__ == "__main__":
    # execute only if run as a script
    main_menu()
