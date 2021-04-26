import threading
from group import *
from attributes import *


class PlaneGame(object):
    def __init__(self):
        self.score = 0
        self.bullet_grade = 1   # Initial bullet level
        self.boss_flag = 0      # Determine whether the BOSS appears
        self.ready_time = pygame.time.get_ticks()   # Used to control the clock that displays the ready screen
        self.star_enemy_life = STAR_ENEMY_LIFE      # Star enemy aircraft needs how many bullets
        self.boss_enemy_life = BOSS_ENEMY_LIFE      # BOSS enemy aircraft needs how many bullets
        self.bullet_type = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four'}
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        logo = pygame.image.load(LOGO_IMAGE)        # Logo
        pygame.display.set_icon(logo)
        pygame.display.set_caption(GAME_NAME)       # Game name

        self.clock = pygame.time.Clock()  # Clock
        self.__createSprite()  # Create group

        pygame.time.set_timer(CREATE_ENEMY_EVENT, ENEMY_TIMER)  # Time set
        pygame.time.set_timer(OWN_FIRE_EVENT, BULLET_TIMER)
        pygame.time.set_timer(BONUS_ENEMY_EVENT, BONUS_TIMER)
        pygame.time.set_timer(STAR_ENEMY_EVENT, START_TIMER)
        pygame.time.set_timer(BOSS_ENEMY_EVENT, BOSS_TIMER)
        pygame.time.set_timer(BULLET_BOSS_EVENT, BULLET_BOSS_TIMER)
        self.life_num = LIFE_NUMS

    def __createSprite(self):
        bg1 = BackGround(BACKGROUND)                    # Create background and group
        bg2 = BackGround(BACKGROUND)
        bg2.rect.y = -bg2.rect.height
        self.back_group = pygame.sprite.Group(bg1, bg2)

        self.ready_go_group = pygame.sprite.Group()     # Create ready group
        self.ready_go_group.add(ReadyGo())
        self.enemy_red_group = pygame.sprite.Group()    # Create a red enemy unit
        self.enemy_down_group = pygame.sprite.Group()   # Create the enemy unit that was hit
        self.bonus_enemy_group = pygame.sprite.Group()  # Create bonus fraction enemy
        self.gold_coin_group = pygame.sprite.Group()    #Create gold group
        self.star_enemy_group = pygame.sprite.Group()   # Create star enemy unit

        self.boss_enemy = EnemyBoss()
        self.boss_enemy_group = pygame.sprite.Group()   # Create boss enemy unit
        self.bullet_boss_group = pygame.sprite.Group()  # Create boss enemy bullet

        self.star_coin_group = pygame.sprite.Group()    # Create star unit
        self.own_died_group = pygame.sprite.Group()     # Create player death
        self.__resetOwn()                               # Create player

    def start(self):
        """ Game start """
        while True:
            self.clock.tick(FPS)        # Refresh frame rate
            self.__eventHandler()       # Event monitoring
            self.__checkCollide()       # Impact checking
            self.__updateSprites()      # Update/draw the picture

            pygame.display.update()     # Update screen display
            self.__gameOver()           # Game over

    def __eventHandler(self):
        """ Event type """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           # Determine whether to exit the game
                PlaneGame.quit()
            elif event.type == CREATE_ENEMY_EVENT:  # When the event value is equal to CREATE_ENEMY_EVENT, add the enemy aircraft to the group
                enemy = EnemyRed()
                self.enemy_red_group.add(enemy)
            elif event.type == BONUS_ENEMY_EVENT:   # When the event value is equal to CREATE_ENEMY_EVENT, add the bonus fraction enemy aircraft to the group
                bonus_enemy = EnemyRed()
                self.bonus_enemy_group.add(bonus_enemy)
            elif event.type == STAR_ENEMY_EVENT:    # When the event value is equal to CREATE_ENEMY_EVENT, add the star enemy aircraft to the group
                self.star_enemy_life = STAR_ENEMY_LIFE  # Gives new star enemy aircraft health
                star_enemy = EnemyBlue()
                self.star_enemy_group.add(star_enemy)

            elif event.type == BOSS_ENEMY_EVENT:    # When the event value is equal to BOSS_ENEMY_EVENT, add the BOSS enemy aircraft to the group
                self.boss_enemy_life = BOSS_ENEMY_LIFE  # Gives new BOSS enemy aircraft health
                self.boss_enemy = EnemyBoss()
                self.boss_enemy_group.add(self.boss_enemy)
                self.boss_flag = 1                  # Change BOSS flag

            elif event.type == OWN_FIRE_EVENT:      # When the event value is equal to OWN_FIRE_EVENT, fire according to the bullet level
                for n in self.bullet_type:
                    grade = 4 if self.bullet_grade > 4 else self.bullet_grade
                    if grade == n:
                        exec('self.own.fire{}()'.format(self.bullet_type[n]))

            if self.boss_flag == 1:                 # If the BOSS appears, shoot bullet
                if event.type == BULLET_BOSS_EVENT:
                    self.boss_enemy.fire()

        keys_pressed = pygame.key.get_pressed()     # Key pressed
        if keys_pressed[pygame.K_RIGHT]:
            self.own.speed_y = 0
            self.own.speed_x = MOVE_SPEED
        elif keys_pressed[pygame.K_LEFT]:
            self.own.speed_y = 0
            self.own.speed_x = -MOVE_SPEED
        elif keys_pressed[pygame.K_UP]:
            self.own.speed_x = 0
            self.own.speed_y = -MOVE_SPEED
        elif keys_pressed[pygame.K_DOWN]:
            self.own.speed_x = 0
            self.own.speed_y = MOVE_SPEED
        elif keys_pressed[pygame.K_SPACE]:          # Space to pause game
            self.__gamePause(True)
        else:  # else doesn't move
            self.own.speed_x = 0
            self.own.speed_y = 0

    def __checkCollide(self):
        """ Impact checking """
        # When the bullet collides with the enemy plane and the enemy plane explodes, the score is increased by 1
        killers = pygame.sprite.groupcollide(self.own.bullets, self.enemy_red_group, True, True)
        if len(killers) > 0:
            self.score += 1
            enemy_down = SpriteDown(ENEMY_DOWN_IMAGE, list(killers.keys())[0].rect, 0)
            self.enemy_down_group.add(enemy_down)

        # When an enemy plane collides with an already existing plane, the number of planes will be reduced by 1, and one plane will be displayed again after 1 second
        died_1 = pygame.sprite.groupcollide(self.enemy_red_group, self.own_group, True, True)
        died_2 = pygame.sprite.groupcollide(self.bonus_enemy_group, self.own_group, True, True)
        died_3 = pygame.sprite.groupcollide(self.star_enemy_group, self.own_group, True, True)
        died_4 = pygame.sprite.groupcollide(self.boss_enemy.bullets, self.own_group, True, True)
        died_5 = pygame.sprite.groupcollide(self.boss_enemy_group, self.own_group, True, True)
        died_owns = {**died_1, **died_2, **died_3, **died_4, **died_5}
        if len(died_owns) > 0:
            self.life_num -= 1
            own_died = SpriteDown(OWN_DOWN_IMAGE, list(died_owns.keys())[0].rect, 0)
            self.own_died_group.add(own_died)
            self.s = threading.Timer(1, self.__resetOwn)
            self.s.start()

        # When the bullet collides with the bonus enemy aircraft, gold coins appear and continue to fall
        bonus_enemies = pygame.sprite.groupcollide(self.own.bullets, self.bonus_enemy_group, True, True)
        if len(bonus_enemies) > 0:
            self.score += 1
            gold_coin = SpriteDown(GOLD_COIN_IMAGE, list(bonus_enemies.keys())[0].rect, 1)
            self.gold_coin_group.add(gold_coin)

        # When the machine collides with the coin, the score is +5, and the gold coin disappears
        gold = pygame.sprite.groupcollide(self.gold_coin_group, self.own_group, True, False)
        if len(gold) > 0:
            self.score += 5

        # When the bullet collides with the star enemy aircraft, the bullet disappears, and the stars continue to fall after more than n bullets.
        if self.star_enemy_life <= 0:
            star_enemy = pygame.sprite.groupcollide(self.own.bullets, self.star_enemy_group, True, True)
            if len(star_enemy) > 0:
                self.score += 5
                star_coin = SpriteDown(STAR_IMAGE, list(star_enemy.keys())[0].rect, 1)
                self.star_coin_group.add(star_coin)
        else:
            star_enemies = pygame.sprite.groupcollide(self.own.bullets, self.star_enemy_group, True, False)
            if len(star_enemies) > 0:
                self.star_enemy_life -= 1

        # When the bullet collides with the boss enemy plane, the bullet disappears, and the boss enemy plane explodes after more than n bullets
        if self.boss_enemy_life <= 0:
            boss_enemy = pygame.sprite.groupcollide(self.own.bullets, self.boss_enemy_group, True, True)
            if len(boss_enemy) > 0:
                self.score += 300
                enemy_down = SpriteDown(ENEMY_DOWN_IMAGE, list(boss_enemy.keys())[0].rect, 1)
                self.enemy_down_group.add(enemy_down)
                self.boss_flag = 0
        else:
            boss_enemies = pygame.sprite.groupcollide(self.own.bullets, self.boss_enemy_group, True, False)
            if len(boss_enemies) > 0:
                self.boss_enemy_life -= 1

        # When the machine collides with the stars, score +10, bullet level +1
        star = pygame.sprite.groupcollide(self.star_coin_group, self.own_group, True, False)
        if len(star) > 0:
            self.score += 10
            self.bullet_grade += 1

    def __resetOwn(self):
        """ Rebirth """
        self.own = Own()
        self.own_group = pygame.sprite.Group(self.own)
        self.bullet_grade = 1  # Initial bullet level

    def __infoDisplay(self, text, position, angle):
        """
        -- Display game
        text: Text content
        position: position[x, y]
        angle: Angle used for positioning
        """
        score_font = pygame.font.Font(SYS_FONT, 24)
        score_text = score_font.render(text, True, (255, 255, 255))
        text_rect = score_text.get_rect()
        exec('text_rect.{}={}'.format(angle, position))
        self.screen.blit(score_text, text_rect)

    def __updateSprites(self):
        """ update group """
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.__infoDisplay('score ' + str(self.score), [20, 10], 'topleft')
        self.__infoDisplay('level 01', [492, 10], 'topright')
        self.__infoDisplay('life ' + str(self.life_num), [230, 10], 'topleft')

        if pygame.time.get_ticks() < self.ready_time + 3000:    # Display the ready screen for 3 seconds
            self.ready_go_group.update()
            self.ready_go_group.draw(self.screen)

        if pygame.time.get_ticks() > self.ready_time + 4000:    # The ready screen starts to display game elements after 1 second
            self.enemy_red_group.update()
            self.enemy_red_group.draw(self.screen)    # Show enemy aircraft
            self.bonus_enemy_group.update()
            self.bonus_enemy_group.draw(self.screen)  # Show bonus fraction enemy aircraft
            self.star_enemy_group.update()
            self.star_enemy_group.draw(self.screen)  # Show star enemy aircraft
            self.boss_enemy_group.update()
            self.boss_enemy_group.draw(self.screen)  # Show boss enemy aircraft
            self.enemy_down_group.update()
            self.enemy_down_group.draw(self.screen)  # Show the enemy plane exploded
            self.own.bullets.update()
            self.own.bullets.draw(self.screen)      # Show the bullet

            self.boss_enemy.bullets.update()
            self.boss_enemy.bullets.draw(self.screen)  # Show boss bullets

            self.own_died_group.update()
            self.own_died_group.draw(self.screen)  # Shows that the plane has exploded
            self.gold_coin_group.update()
            self.gold_coin_group.draw(self.screen)  # Show gold coins
            self.star_coin_group.update()
            self.star_coin_group.draw(self.screen)  # Show star
            self.own_group.update()
            self.own_group.draw(self.screen)  # Show player aircraft

    def __gamePause(self, pause=False):
        """ Pause the game, press any key to exit"""
        self.__infoDisplay('Any key to continue...', SCREEN_CENTER, 'center')
        pygame.display.update()  # Update screen display
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    PlaneGame.quit()
                elif event.type == pygame.KEYDOWN:
                    pause = False

    def __gameOver(self):
        """ The game is over, press ESC to restart """
        if self.life_num == 0:  # If the number of aircraft is 0, exit the game
            game_over = pygame.image.load(GAME_OVER)  # Show GAMEOVER picture
            self.screen.blit(game_over, (50, 150))
            self.__infoDisplay('press ESC play again...', SCREEN_CENTER, 'center')
            pygame.display.update()
            flag = True
            while flag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        PlaneGame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Press SPACE to restart the game
                            flag = False
                            PlaneGame().start()

    @staticmethod
    def quit():
        pygame.quit()
        exit()
