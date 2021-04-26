import pygame


SCREEN_RECT = pygame.Rect (0, 0, 512, 768)  # Use a constant to store the position and size of the screen, and the constant is expressed in all uppercase
SCREEN_CENTER = [SCREEN_RECT.width / 2, SCREEN_RECT.height / 2]

CREATE_ENEMY_EVENT = pygame.USEREVENT       # The constant value of the enemy aircraft event timer
OWN_FIRE_EVENT = pygame.USEREVENT + 1       # The constant value of the firing bullet timer
BONUS_ENEMY_EVENT = pygame.USEREVENT + 2    # The timer constant value of bonus points for enemy aircraft
STAR_ENEMY_EVENT = pygame.USEREVENT + 3     # The timer constant value of the star enemy aircraft
BOSS_ENEMY_EVENT = pygame.USEREVENT + 4     # BOSS enemy’s timer constant value
BULLET_BOSS_EVENT = pygame.USEREVENT + 5    # The bullet timer constant value of the BOSS enemy aircraft

ENEMY_TIMER = 600                           # The time frequency of enemy aircraft appearance
BULLET_TIMER = 400                          # The time frequency of bullets
BONUS_TIMER = 5000                          # Bonus points to the time and frequency of enemy aircraft appearance
START_TIMER = 20000                         # The time frequency of the appearance of the enemy aircraft
BOSS_TIMER = 120000                         # The time frequency of BOSS enemy aircraft appearance
BULLET_BOSS_TIMER = 1500                    # The time frequency of BOSS enemy bullets

LIFE_NUMS = 3                               # HP
MOVE_SPEED = 5                              # The moving speed of the aircraft
STAR_ENEMY_LIFE = 6                         # The bullets needed to destroy the star enemy aircraft
BOSS_ENEMY_LIFE = 100                       # The bullet needed to destroy the BOSS enemy aircraft

# Picture
BACKGROUND = r'.\images\background.png'
GAME_OVER = r'.\images\gameover.png'
OWN_IMAGE = r'.\images\own.png'
OWN_DOWN_IMAGE = r'.\images\own_died.png'
ENEMY_RED_IMAGE = r'.\images\enemy_red.png'
ENEMY_BLUE_IMAGE = r'.\images\enemy_blue.png'
ENEMY_DOWN_IMAGE = r'.\images\enemy_down.png'
BULLET_IMAGE = r'.\images\bullet.png'
BULLET_BOSS_IMAGE = r'.\images\bullet_boss.png'
LIFE_IMAGE = r'.\images\life.png'
GOLD_COIN_IMAGE = r'.\images\bonus.png'
STAR_IMAGE = r'.\images\star.png'
READY_IMAGE = r'.\images\ready.png'
BOSS_IMAGE = r'.\images\boss.png'
LOGO_IMAGE = r'.\images\logo.ico'

SYS_FONT = r'.\fonts\BOLDER.ttf'
GAME_NAME = 'Aircraft war'

FPS = 60            # Screen refresh rate
