import pygame
import serial
import time
import random
import math
from pygame import mixer

#arduino serial setup. Get COM from arduino IDE
arduinoSerialData = serial.Serial('COM5', 9600)

#initialise pygame
pygame.init()
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
backgroundSpeed = 50
black = (0, 0, 0)
white = (255, 255, 255)

#create the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Star Wars Level 1")
starWarsLogoImg = pygame.image.load('StarWarsLogo.png')

#background properties
rock1Img = pygame.image.load('Rock1.png')
rock2Img = pygame.image.load('Rock2.png')
groundDirt1Img = pygame.image.load('groundDirt.png')
groundDirt2Img = pygame.image.load('groundDirt.png')
groundDirt3Img = pygame.image.load('groundDirt.png')
groundDirt4Img = pygame.image.load('groundDirt.png')
groundDirt5Img = pygame.image.load('groundDirt.png')
groundDirt6Img = pygame.image.load('groundDirt.png')
groundDirt7Img = pygame.image.load('groundDirt.png')
groundDirt8Img = pygame.image.load('groundDirt.png')

#startin positions for background graphics
rock1Y = 0
rock1X = 50
rock2Y = -200
rock2X = 750
groundDirt1Y = random.randrange(-300, 600)
groundDirt1X = random.randrange(100, 700)
groundDirt2Y = random.randrange(-300, 600)
groundDirt2X = random.randrange(100, 700)
groundDirt3Y = random.randrange(-300, 600)
groundDirt3X = random.randrange(100, 700)
groundDirt4Y = random.randrange(-300, 600)
groundDirt4X = random.randrange(100, 700)
groundDirt5Y = random.randrange(-300, 600)
groundDirt5X = random.randrange(100, 700)
groundDirt6Y = random.randrange(-300, 600)
groundDirt6X = random.randrange(100, 700)
groundDirt7Y = random.randrange(-300, 600)
groundDirt7X = random.randrange(100, 700)
groundDirt8Y = random.randrange(-300, 600)
groundDirt8X = random.randrange(100, 700)

#player properties
playerImg = pygame.image.load('Racer.png')
playerX = 325
playerY = 450

#jawa properties
jawaX = random.randrange(50, 650)
jawaY = -300
jawaYChange = 2
jawaState = "ready"

#bullet properties
bulletImg = pygame.image.load('Fireball.png')
bulletY = 450
bulletX = 0
bulletYChange = 50
bulletState = "ready"

#Main screen function
def gameIntro():
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    mixer.music.load('StarWarsIntroTheme.wav')
    mixer.music.play()
    intro = True
    while intro:
        #get Arduino data
        arduinoString = arduinoSerialData.readline()
        string_n = arduinoString.decode()
        arduinoDataArray = string_n.rstrip().split(',')
        btn1 = int(arduinoDataArray[0])
        btn2 = int(arduinoDataArray[1])
        FSR = int(arduinoDataArray[2])
        #Open right hand to start game
        if FSR < 100:
            screen.blit(starWarsLogoImg, (115, 0))
            introMessage = font.render("Open Your Right Hand to Start the Game", True, white)
            screen.blit(introMessage, (75, 450))
            pygame.display.update()
            clock.tick(60)
        else:
            intro = False

#instructions for jawa stage screen
def beforeJawaStageClip():
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    mixer.music.load('BetweenStageSound.wav')
    mixer.music.play()
    countdown = 8
    while countdown > 0:
        JawaInfoMessage = font.render("Get Ready to Kill Some Jawas", True, white)
        JawaInfoMessage2 = font.render("Open Your Right Hand to Shoot", True, white)
        screen.blit(JawaInfoMessage, (75, 150))
        screen.blit(JawaInfoMessage2, (75, 200))
        pygame.display.update()
        countdown -= 1
        time.sleep(0.5)

#function to display score
def showScore(x, y):
    score = font.render("Score: " + str(scoreValue), True, black)
    screen.blit(score, (x, y))

#function to display player
def racer():
    screen.blit(playerImg, (playerX, playerY))

#function to display jawa
def jawa(jawaX, jawaY):
    jawaImg = pygame.image.load('Jawa.png')
    jawaImg = pygame.transform.scale(jawaImg, (50, 75))
    screen.blit(jawaImg, (jawaX, jawaY))

#function to display bullet
def bullet(bulletX, bulletY):
    global bulletState
    screen.blit(bulletImg, (bulletX, bulletY))
    if bulletY > 300:
        bulletSound = mixer.Sound('BulletSound.wav')
        bulletSound.play()

#update score and jawa when collision between bullet and jawa occurs
def shot(jawaX, jawaY, bulletX, bulletY):
    distance = math.sqrt(math.pow(jawaX - bulletX, 2) + (math.pow(jawaY - bulletY, 2)))
    if distance <= 35 and distance > 15:
        JawaSound = mixer.Sound('JawaSound.wav')
        JawaSound.play()
        return True
    else:
        return False

#function to read Arduino data
def arduinoCall():
    global playerX
    global bulletY
    global bulletX
    global bulletState
    global scoreValue
    global jawaX
    global jawaY
    arduinoString = arduinoSerialData.readline()
    string_n = arduinoString.decode()
    arduinoDataArray = string_n.rstrip().split(',')
    btn1 = int(arduinoDataArray[0])
    btn2 = int(arduinoDataArray[1])
    FSR = int(arduinoDataArray[2])
    print(btn1, btn2, FSR)
    
    #logic to move left and right and fire bullets
    if btn1 == 1:
        playerX -= 10
    if playerX < 0:
        playerX = 0
    if btn2 == 1:
        playerX += 10
    if playerX > 650:
        playerX = 650
    if FSR < 150:
        bulletX = playerX + 70
        bulletState = "fire"
    if bulletState is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletYChange
    if bulletY <= 0:
        bulletY = 450
        bulletState = "ready"

    #Logic when jawa is shot
    hit = shot(jawaX, jawaY, bulletX, bulletY)
    if hit:
        JawaSound = mixer.Sound('JawaSound.wav')
        JawaSound.play()
        bulletY = 450
        scoreValue += 1
        jawaY = -100
        jawaX = random.randrange(50, 750)
        
#Draw background and simulate movement
def background():
    rock1Img = pygame.image.load('Rock1.png')
    rock2Img = pygame.image.load('Rock2.png')
    groundDirt1Img = pygame.image.load('GroundDirt.png')
    groundDirt2Img = pygame.image.load('GroundDirt.png')
    groundDirt3Img = pygame.image.load('GroundDirt.png')
    groundDirt4Img = pygame.image.load('GroundDirt.png')
    groundDirt5Img = pygame.image.load('GroundDirt.png')
    groundDirt6Img = pygame.image.load('GroundDirt.png')
    groundDirt7Img = pygame.image.load('GroundDirt.png')
    groundDirt8Img = pygame.image.load('GroundDirt.png')

    screen.blit(rock1Img, (rock1X, rock1Y))
    screen.blit(rock2Img, (rock2X, rock2Y))
    screen.blit(groundDirt1Img, (groundDirt1X, groundDirt1Y))
    screen.blit(groundDirt2Img, (groundDirt2X, groundDirt2Y))
    screen.blit(groundDirt3Img, (groundDirt3X, groundDirt3Y))
    screen.blit(groundDirt4Img, (groundDirt4X, groundDirt4Y))
    screen.blit(groundDirt5Img, (groundDirt5X, groundDirt5Y))
    screen.blit(groundDirt6Img, (groundDirt6X, groundDirt6Y))
    screen.blit(groundDirt7Img, (groundDirt7X, groundDirt7Y))
    screen.blit(groundDirt8Img, (groundDirt8X, groundDirt8Y))

#End of stage screen
def gameOver():
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    gameOver = True
    while gameOver is True:
        gameOverMessage = font.render("Well Done!!! You Killed All the Jawas", True, white)
        screen.blit(gameOverMessage, (75, 150))
        pygame.display.update()
        clock.tick(60)

#game loop
clock = pygame.time.Clock()
gameIntro()
beforeJawaStageClip()
mixer.music.load('RacerStage.wav')
mixer.music.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #screen color
    screen.fill((252, 169, 3))
    background()
    #Logic to simulate background movement
    rock1Y += backgroundSpeed
    rock2Y += backgroundSpeed
    groundDirt1Y += backgroundSpeed
    groundDirt2Y += backgroundSpeed
    groundDirt3Y += backgroundSpeed
    groundDirt4Y += backgroundSpeed
    groundDirt5Y += backgroundSpeed
    groundDirt6Y += backgroundSpeed
    groundDirt7Y += backgroundSpeed
    groundDirt8Y += backgroundSpeed

    if rock1Y >= 600:
        rock1Y = -100
    if rock2Y >= 600:
        rock2Y = -100
    if groundDirt1Y >= 600:
        groundDirt1Y = -100
    if groundDirt2Y >= 600:
        groundDirt2Y = -100
    if groundDirt3Y >= 600:
        groundDirt3Y = -100
    if groundDirt4Y >= 600:
        groundDirt4Y = -100
    if groundDirt5Y >= 600:
        groundDirt5Y = -100
    if groundDirt6Y >= 600:
        groundDirt6Y = -100
    if groundDirt7Y >= 600:
        groundDirt7Y = -100
    if groundDirt8Y >= 600:
        groundDirt8Y = -100

    racer()
    arduinoCall()
    jawa(jawaX, jawaY)
    jawaY += 3
    showScore(textX, textY)

    if scoreValue >= 10:
        gameOver()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
    
