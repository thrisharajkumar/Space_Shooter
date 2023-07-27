import pygame
import random
pygame.init()

#Screen height and display
SIZE = WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode(SIZE)

#rgb color code
WHITE = 255, 255, 255
RED = 255,0,0
BLUE = 0,0,255
BLACK = 0,0,0

bulletSound = pygame.mixer.Sound("assets/sounds/laser-gun-72558.mp3")
EnemySound = pygame.mixer.Sound("assets/sounds/shoot02wav-14562.mp3")

def HomeScreen():
    font_1 = pygame.font.Font("assets/Fonts/LoveGlitchPersonalUseRegular-vmEyA.ttf", 100)
    text_1= font_1.render("Space Shooter!", True, WHITE)

    font_2 = pygame.font.SysFont(None, 50)
    text_2 = font_2.render("Press Space to Start Game_", True, WHITE)
    while True:
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
        SCREEN.blit(text_1, (275, 200))
        SCREEN.blit(text_2, (300, 350))
        pygame.display.flip()
def playerHealth(Count):
    #to display a text
    font = pygame.font.SysFont(None, 20) #font style , fontsize
    text = font.render(f"Health : {Count}", True, BLUE)
    SCREEN.blit(text, (10, 500))

def GameOver():
    font = pygame.font.SysFont(None, 80)
    text = font.render("GAME OVER!", True, BLUE)
    while True:
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.blit(text, (300, 300))
        pygame.display.flip()
def main():
    # changing the backgorund color of screen

    SCREEN.fill(BLACK)
    move_x =0
    move_y =0

    ship = pygame.image.load("assets/images/MySpaceship-removebg-preview.png")

    ship_w =ship.get_width()

    ship_h = ship.get_height()
    #will place the ship in center bottom
    ship_x = WIDTH //2 - ship_w//2
    ship_y = HEIGHT -ship_h

    #ENEMY SHIP
    enemyShip = pygame.image.load("assets/images/SpaceShipEnemy.png")
    eship_w =enemyShip.get_width()
    eship_h = enemyShip.get_height()
    #will place the ship in center bottom

    enemyList =[]
    nrows = 2
    ncols = WIDTH // eship_w

    # bullet code
    #bullet_x = ship_x + ship_w //2 - 2.5 # half of bullet width
    bullet_y = ship_y
    bullet_w = 5
    bullet_h = 10

    moveBullet =0

    for i in range(nrows):
        for j in range(ncols):
            enemyX = eship_w * j
            enemyY = eship_h * i
            enemyRect = pygame.Rect(enemyX, enemyY, eship_w, eship_h)
            enemyList.append(enemyRect)
            #enemyList.append([enemyX, enemyY])

    random_enemy = random.choice(enemyList)
    enemy_bullet_w = 5
    enemy_bullet_h = 10
    enemy_bullet_x = random_enemy.x + eship_w //2#toget the bullet in center of the eship
    enemy_bullet_y = random_enemy.bottom -10

    #Player health counter
    playerHealthCount = 100

    while True:

        bullet_x = ship_x + ship_w // 2 - 2
        #solution for hanging problem
        #this line runs parellely in the background to
        # manage the events actions performed
        eventList = pygame.event.get()
        for event in eventList:
            # print(event)
            if event.type == pygame.QUIT:
                # quit the pygame
                pygame.quit()
                #quit python
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move_x = 2
                elif event.key == pygame.K_LEFT:
                    move_x = -2
                #as you enter space bar the bullet moves upward
                elif event.key == pygame.K_SPACE:
                    #this number contros how fast the bullet moves
                    moveBullet = -7
                    bulletSound.play()

            else:
                move_x =0

        SCREEN.fill(BLACK)

        #Bullet
        bullet_rect = pygame.draw.rect(SCREEN, RED, [bullet_x, bullet_y, bullet_w, bullet_h])
        bullet_y += moveBullet

        # to render an image
        # blit is a method
        SCREEN.blit(ship, (ship_x, ship_y))
        ship_x += move_x

        #need a rectangle for our spaceship as well
        ship_rect = pygame.Rect(ship_x, ship_y, ship_w, ship_h)

        #enemybullet
        enemyBullet = pygame.draw.rect(SCREEN, BLUE, [enemy_bullet_x, enemy_bullet_y, enemy_bullet_w, enemy_bullet_h])
        enemy_bullet_y += 8

        for i in range(len(enemyList)):
            #SCREEN.blit(enemyShip, ( enemyList[i][0], enemyList[i][1]))
            SCREEN.blit(enemyShip, (enemyList[i].x, enemyList[i].y))


        #When our spaceship collides with enemy
        for i in range(len(enemyList)):
            #predefined methos colliderect()
            if bullet_rect.colliderect(enemyList[i]):
                del enemyList[i]
                #as it cancels the whole column
                #bringing back the bullet to the spaceship
                bullet_y = ship_y
                #stop bullet after
                moveBullet =0
                break
        #after the bullet reaches the top of the screen it has to come back
        #now you have infite bullets
        if bullet_y <0:
            bullet_y = ship_y
            moveBullet= 0

        #this part of if statement will make a bullet rain
        if enemy_bullet_y > HEIGHT:
            random_enemy = random.choice(enemyList)
            enemy_bullet_x = random_enemy.x + eship_w // 2  # toget the bullet in center of the eship
            enemy_bullet_y = random_enemy.bottom - 10
            EnemySound.play()

        if enemyBullet.colliderect(ship_rect):
            playerHealthCount -=1

        if playerHealthCount ==0:
            GameOver()

        playerHealth(playerHealthCount)

        # Should always be in the last as it updates the screen
        #this line always updates the screen
        pygame.display.flip()

#main()
HomeScreen()