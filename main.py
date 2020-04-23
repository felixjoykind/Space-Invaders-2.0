import pygame
import os
import time
import random
from settings import *
from classes.laser import Laser
from classes.ship import Ship
from classes.player import Player
from classes.enemy import Enemy
from classes.boss import Boss

# Initializing pygame
pygame.init()
pygame.font.init()

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
    dificulty = 4
    wave_length = dificulty
    enemy_vel = 1
    level_to_boss = 5

    killed_bosses = 0

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

        WIN.blit(lives_label, (10, 10)) # Displaying lives
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10)) # Displaying level

        for enemy in enemies: # Drawing all enemies
            enemy.draw(WIN)

        player.draw(WIN) # Drawi player

        if lost: # If layer lost
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0: # That means that player lost
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0 and level < level_to_boss and not boss_spawned: # If player killed all enemies
                level += 1
                wave_length += dificulty
                for i in range(wave_length): # Adding new enemies
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1300, -100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
        elif level == level_to_boss and not boss_spawned: # If it is the boss level
            enemies = [] # Removing all enemies
            enemies.append(Boss(WIDTH/2-130, -350, killed_bosses, 100*(killed_bosses+1))) # Spawning boss
            boss_spawned = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

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

            if collide(enemy, player): # If enemy colliding with player
                if enemy.type == 'boss':
                    player.health -= 0.3
                else:
                    player.health -= 10
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT and enemy.type != 'boss':
                lives -= 1
                enemies.remove(enemy)
            elif enemy.type == 'boss' and enemy.killed:
                enemies = []
                boss_spawned = False
                level_to_boss += 3
                killed_bosses += 1

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
