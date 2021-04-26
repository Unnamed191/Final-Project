import random
from attributes import *
import pygame


class GameSprite(pygame.sprite.Sprite):
     def __init__(self, image_name, speed=1):
         super().__init__()                             # Initialization
         self.image = pygame.image.load(image_name)     # Define the attributes of the object (image)
         self.rect = self.image.get_rect()              # Define the attributes (position) of the object
         self.speed = speed                             # define speed
         self.speed_x = speed                           # Define the horizontal speed of your own aircraft
         self.speed_y = speed                           # Define the vertical speed of your own aircraft

     def update(self):
         self.rect.y += self.speed                      # Move in the vertical direction of the screen

     def updateObliqueLeft(self):                       # Move diagonally to the left on the screen
         self.rect.x += self.speed
         self.rect.y += self.speed

     def updateObliqueRight(self):                      # Move diagonally on the screen
         self.rect.x -= self.speed
         self.rect.y += self.speed


class BackGround(GameSprite):
    def update(self):
        super().update()
        if self.rect.y >= self.rect.height:             # If the y of the background image exceeds the height of the screen, the y value becomes the negative value of the height
            self.rect.y = -self.rect.height

    # noinspection PyPep8Naming
    # Own aircraft subclass


class Own(GameSprite):
    def __init__(self):
        super().__init__(OWN_IMAGE, 0)                  # Define the image and initial speed of your own aircraft
        self.rect.centerx = SCREEN_RECT.centerx         # Set the position of the Player, centerx refers to the x value of the center of the image
        self.rect.y = SCREEN_RECT.height - self.rect.height
        self.bullets = pygame.sprite.Group()            # Create bullet group

    def update(self):
        """ Player moves in the horizontal direction """
        self.rect.x += self.speed_x                     # The offset of the movement is the value of the speed
        if self.rect.x < 0:                             # Control the Player cannot leave the screen
            self.rect.x = 0
        elif self.rect.x > SCREEN_RECT.width - self.rect.width:
            self.rect.x = SCREEN_RECT.width - self.rect.width
        """ Player moves in the vertical direction """
        self.rect.y += self.speed_y
        if self.rect.y < 0:                             # Control the Player cannot leave the screen
            self.rect.y = 0
        elif self.rect.y > SCREEN_RECT.height - self.rect.height:
            self.rect.y = SCREEN_RECT.height - self.rect.height

    """Bullet levels"""

    def fireOne(self):
        """ Create bullet-1 capsule """
        bullet = Bullet()
        bullet.rect.centerx = self.rect.centerx  # Specify the initial position of the bullet
        bullet.rect.y = self.rect.y - 30  # The y value displayed by the bullet is above the plane
        self.bullets.add(bullet)  # Add bullet to bullet group
        return bullet

    def fireTwo(self):
        """ Create bullets-2 capsules """
        bullet_l = Bullet()
        bullet_l.rect.centerx = self.rect.centerx - self.rect.width / 2     # Specify the initial position of the left bullet
        bullet_l.rect.y = self.rect.y - 30                                  # The y value displayed by the bullet is above the plane
        bullet_r = Bullet()
        bullet_r.rect.centerx = self.rect.centerx + self.rect.width / 2     # Specify the initial position of the right bullet
        bullet_r.rect.y = self.rect.y - 30                                  # The y value displayed by the bullet is above the plane
        self.bullets.add(bullet_l, bullet_r)                                # add bullet to bullet group
        return bullet_l, bullet_r

    def fireThree(self):
        """ Create bullets-3 grains """
        bullet_one = self.fireOne()
        bullet_two_l, bullet_two_r = self.fireTwo()
        self.bullets.add(bullet_one, bullet_two_l, bullet_two_r)            # add bullet to bullet group
        return bullet_one, bullet_two_l, bullet_two_r

    def fireFour(self):
        """ Create bullet-4 capsules """
        bullet_one, bullet_two_l, bullet_two_r = self.fireThree()
        bullet_ol = Bullet('LEFT')
        bullet_ol.rect.centerx = self.rect.centerx - self.rect.width / 2    # Specify the initial position of the left tilted bullet
        bullet_ol.rect.y = self.rect.y - 30                                 # The y value displayed by the bullet is above the plane
        bullet_or = Bullet('RIGHT')
        bullet_or.rect.centerx = self.rect.centerx + self.rect.width / 2    # Specify the initial position of the right tilted bullet
        bullet_or.rect.y = self.rect.y - 30                                 # The y value displayed by the bullet is above the plane
        self.bullets.add(bullet_one, bullet_two_l, bullet_two_r, bullet_ol, bullet_or)  # add bullet to bullet group


class SpriteDown(GameSprite):
    def __init__(self, image, pos, flag):
        super().__init__(image)
        self.killed_pos = pos
        self.rect.x = self.killed_pos[0]
        self.rect.y = self.killed_pos[1]
        self.flag = flag

    def update(self):
        super().update()
        if self.flag == 1:      # If it is a item, judge whether it will fly off the screen and delete it in time to free up memory space
            if self.rect.y >= SCREEN_RECT.height:
                self.kill()
        else:                   # If it’s not an item, delete it after a certain distance
            if self.rect.y > self.killed_pos[1] + self.rect.height:
                self.kill()


class Bullet(GameSprite):
    def __init__(self, flag='VERTICAL'):
        super().__init__(BULLET_IMAGE, -6)      # Define the image and initial velocity of the bullet
        self.flag = flag

    def update(self):
        if self.flag == 'LEFT':                 # According to the value of flag, choose which bullet's trajectory to call
            super().updateObliqueLeft()
        elif self.flag == 'RIGHT':
            super().updateObliqueRight()
        else:
            super().update()
        if self.rect.y < 0 or SCREEN_RECT.width < self.rect.x < 0:
            self.kill()


class BulletBoss(GameSprite):
    def __init__(self):
        super().__init__(BULLET_BOSS_IMAGE, 4)

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.kill()


# Blue enemy plane, the flight path is different from red
class EnemyBlue(GameSprite):
    def __init__(self):
        super().__init__(ENEMY_BLUE_IMAGE)              # Define the bandit image and initial speed
        self.x = [-1, 1]                                # The direction of movement of the blue enemy aircraft is random
        self.speed = 1                                  # The speed of the blue enemy aircraft is 1, divided into the speed of the xy axis
        self.speed_x = random.choice(self.x)
        self.rect.y = -self.rect.height                 # The y value when the enemy aircraft appears
        max_x = SCREEN_RECT.width - self.rect.width     # The maximum x value when the enemy aircraft appears
        self.rect.x = random.randint(0, max_x)          # Randomly generate the x value when the enemy aircraft appears

    def update(self):
        super().update()
        if self.rect.x <= 0 or self.rect.x >= SCREEN_RECT.width - self.rect.width:  # Take the reverse speed when x exceeds the screen
            self.speed_x = -self.speed_x
        self.rect.x += self.speed_x
        if self.rect.y >= SCREEN_RECT.height:           # Determine whether the enemy plane flies off the screen, delete it in time to free up memory space
            self.kill()


# 红色敌机子类
class EnemyRed(GameSprite):
    def __init__(self):
        super().__init__(ENEMY_RED_IMAGE)               # Define the bandit image and initial speed
        self.speed = random.randint(2, 5)               # Randomly define the speed of the enemy aircraft, if it is 1, it will be displayed on the screen without moving
        self.rect.y = -self.rect.height                 # The y value when the enemy aircraft appears
        max_x = SCREEN_RECT.width - self.rect.width     # The maximum x value when the enemy aircraft appears
        self.rect.x = random.randint(0, max_x)          # Randomly generate the x value when the enemy aircraft appears

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:           # Determine whether the enemy plane flies off the screen, delete it in time to free up memory space
            self.kill()


# boss敌机子类
class EnemyBoss(GameSprite):
    def __init__(self):
        super().__init__(BOSS_IMAGE)                    # Define BOSS enemy aircraft image and initial speed
        self.x = [-1, 1]                                # The direction of movement of the BOSS enemy aircraft is random
        self.speed_x = random.choice(self.x)
        self.rect.y = -self.rect.height                 # The y value when the BOSS enemy aircraft appears
        max_x = SCREEN_RECT.width - self.rect.width     # The maximum x value when the BOSS enemy aircraft appears
        self.rect.x = random.randint(0, max_x)          # Randomly generate the x value of BOSS when the enemy aircraft appears
        self.bullets = pygame.sprite.Group()            # Create bullet group

    def update(self):
        super().update()
        if self.rect.y >= 200:                          # Control the boss enemy aircraft at the top of the window
            self.speed = 0
        if self.rect.x <= 0 or self.rect.x >= SCREEN_RECT.width - self.rect.width:  # 当x超过屏幕时取反向速度
            self.speed_x = -self.speed_x
        self.rect.x += self.speed_x

    def fire(self):
        bullet = BulletBoss()
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.y = self.rect.y + self.rect.height + 30
        self.bullets.add(bullet)



class ReadyGo(GameSprite):
    def __init__(self):
        super().__init__(READY_IMAGE, 0)               # Define preparation image
        self.rect.x = 128
        self.rect.y = 200

    def update(self):
        super().update()
