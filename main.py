import pygame
import time
import math
import random

from actors import *

pygame.init()
pygame.font.init()

# Game properties
screenWidth = 1200
screenHeight = 1000
tickDelay = 0.01
gameTitle = "Epic Boss Fighter"

screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption(gameTitle)

# Game class
class Game:
    def __init__(self):
        self.gamePhase = 0
        """
        0: Main Menu
        1: Help
        2: Battle Screen
        3: Game Over
        4: Victory
        """

        # Fonts
        self.statFont = pygame.font.SysFont('Arial', 20)
        self.subtitleFont = pygame.font.SysFont('Arial', 25)
        self.headerFont = pygame.font.SysFont('Arial', 40)
        self.titleFont = pygame.font.SysFont('Arial', 50)

        # Gameplay
        self.difficulty = 1
        """
        0: Easy
        1: Normal
        2: Hard
        3: Impossible
        """

        # Text Buttons
        self.textButtons = []
        
        # Player
        self.player = Player(580, 850)
        self.playerProjectiles = []
        self.nextShot = 0
        self.nextShot2 = 0

        # Winning VS Boss
        self.won = False
        self.winDelay = 150

        # Main Menu
        self.rain = []
        self.nextDrop = 0

        # Main Menu - Lightning
        self.nextBolt = random.choice(range(50, 400))
        self.boltX = -1
        self.boltFlash = 0
        self.boltLife = 0
        self.boltDirection = 0

        # Boss
        self.boss = Boss(0)

        self.enemies = []
        self.enemyProjectiles = []

        self.makeBoss(10)

        # Boss 1
        self.I1BnextShot = 15

        # Boss 2
        self.I2BmoveTarget = [random.choice(range(100, 1100)), random.choice(range(100, 900))]
        self.I2BsummonTimer = 40

        # Boss 3
        self.I3BnextRain = 20
        self.I3BnextWall = 220

        # Boss 4
        self.I4Bshield = 0
        self.I4Bring = 0
        self.I4Bangle = 0
        self.I4Bspawn = 50

        # Boss 5
        self.I5BteleportDamage = 999999
        self.I5InitialTeleport = True

        # Boss 6
        self.I6BnextShot = 5
        self.I6walls = 200
        self.I6BmoveTarget = [random.choice(range(100, 1100)), random.choice(range(100, 900))]

        # Boss 7
        self.I7BmoveTarget = [-1, -1]
        self.I7BmoveRing = False

        # Boss 8
        self.I8BdecayTimer = 0

        # Boss 10
        self.I10BsideShot = 5
        self.I10BattackPattern = 3
        self.I10patternSwap = 0
        self.I10Bangle = 0

        # Boss 11
        self.I11Bstyle = random.choice([0, 1])
        self.I11BstyleSwitch = random.choice(range(400, 700))
        self.I11BmoveTarget = [-1, -1]
        self.I11BnextShot = 0

        self.I11Bdashing = False
        self.I11BnextDash = random.choice(range(100, 500))

    def reset(self):
        self.resetBosses()
        self.makeBoss(0)

        # Player
        self.player = Player(580, 850)
        self.playerProjectiles = []
        self.nextShot = 0
        self.nextShot2 = 0

        # Lightning Bolts
        self.nextBolt = random.choice(range(50, 400))
        self.boltX = -1
        self.boltFlash = 0
        self.boltLife = 0
        self.boltDirection = 0

        # Winning VS Boss
        self.won = False
        self.winDelay = 150

        # Main Menu
        self.rain = []
        self.nextDrop = 0

        self.enemies = []
        self.enemyProjectiles = []

        self.makeBoss(0)

        self.rain = []
    
    def resetBosses(self):
        self.won = False
        self.winDelay = 150
        
        self.enemies = []
        self.enemyProjectiles = []
        self.playerProjectiles = []

        # Boss 1
        self.I1BnextShot = 15

        # Boss 2
        self.I2BmoveTarget = [random.choice(range(100, 1100)), random.choice(range(100, 900))]
        self.I2BsummonTimer = 40

        # Boss 3
        self.I3BnextRain = 20
        self.I3BnextWall = 220

        # Boss 4
        self.I4Bshield = 0
        self.I4Bring = 0
        self.I4Bangle = 0
        self.I4Bspawn = 50

        # Boss 5
        self.I5BteleportDamage = 999999
        self.I5InitialTeleport = True

        # Boss 6
        self.I6BnextShot = 5
        self.I6walls = 200
        self.I6BmoveTarget = [random.choice(range(100, 1100)), random.choice(range(100, 900))]

        # Boss 7
        self.I7BmoveTarget = [-1, -1]
        self.I7BmoveRing = False

        # Boss 8
        self.I8BdecayTimer = 0

        # Boss 10
        self.I10BsideShot = 5
        self.I10BattackPattern = 3
        self.I10patternSwap = 0
        self.I10Bangle = 0

        # Boss 11
        self.I11Bstyle = random.choice([0, 1])
        self.I11BstyleSwitch = random.choice(range(400, 700))
        self.I11BmoveTarget = [-1, -1]
        self.I11BnextShot = 0

        self.I11Bdashing = False
        self.I11BnextDash = random.choice(range(100, 500))
    
    def moveBoss(self, speed):
        if self.boss.x + self.boss.size / 2 < self.player.x + 20:
            self.boss.x += speed
            #if self.boss.x + self.boss.size / 2 > self.player.x + 20:
                #self.boss.x = self.player.x - 20
                #print("Left")
        elif self.boss.x + self.boss.size / 2 > self.player.x + 20:
            self.boss.x -= speed
            #if self.boss.x + self.boss.size / 2 < self.player.x + 20:
                #self.boss.x = self.player.x - 20
                #print("Right")

        if self.boss.y + self.boss.size / 2 < self.player.y + 20:
            self.boss.y += speed
            #if self.boss.y + self.boss.size / 2 > self.player.y + 20:
                #self.boss.y = self.player.y - 20
                #print("Up")
        elif self.boss.y + self.boss.size / 2 > self.player.y + 20:
            self.boss.y -= speed
            #if self.boss.y + self.boss.size / 2 < self.player.y + 20:
                #self.boss.y = self.player.y - 20
                #print("Down")
    
    def makeBoss(self, bossID):
        self.boss = Boss(bossID)

        match self.difficulty:
            case 0:
                self.boss.health *= 0.5
                self.boss.maxHealth *= 0.5
                self.boss.collisionDamage *= 0.5
            case 2:
                self.boss.health *= 2
                self.boss.maxHealth *= 2
                self.boss.collisionDamage *= 2
            case 3:
                self.boss.health *= 3
                self.boss.maxHealth *= 3
                self.boss.collisionDamage *= 10

    def makeEnemy(self, enemy):
        match self.difficulty:
            case 0:
                enemy.health *= 0.5
                enemy.collisionDamage *= 0.5
                enemy.speed *= 0.5
            case 2:
                enemy.health *= 2
                enemy.collisionDamage *= 2
            case 3:
                enemy.health *= 3
                enemy.collisionDamage *= 5
                enemy.speed *= 2

        self.enemies.append(enemy)

    def makeEProjectile(self, projectile):
        match self.difficulty:
            case 0:
                projectile.velX *= 0.5
                projectile.velY *= 0.5
                projectile.damage *= 0.5
            case 2:
                projectile.damage *= 2
            case 3:
                projectile.velX *= 2
                projectile.velY *= 2
                projectile.damage *= 3
        
        self.enemyProjectiles.append(projectile)

    def shootAtPlayer(self, x, y, speed, damage):
        xDif = (self.player.x + 20) - x
        yDif = (self.player.y + 20) - y

        try:
            angle = math.atan(yDif / xDif)
        except ZeroDivisionError:
            angle = math.pi / 2 if (yDif > 0) else -(math.pi / 2)

        xSpeed = speed * math.cos(angle)
        ySpeed = speed * math.sin(angle)

        if xDif < 0:
            xSpeed *= -1
            ySpeed *= -1

        self.makeEProjectile(Projectile(1, xSpeed, ySpeed, x, y, damage))
    
    def drawText(self, text, colour, font, x, y, style): # For style: 0 = Left Anchor, 1 = Middle Anchor, 2 = Right Anchor
        global screen
        
        text = font.render(text, True, colour)

        text_rect = text.get_rect(center=(x, y))
        
        if style == 0:
            text_rect.left = x
        elif style == 2:
            text_rect = text.get_rect(center=(x, y))
            text_rect.right = x
        screen.blit(text, text_rect)

        return text_rect

    def inputs(self):
        global gameRunning
        
        match self.gamePhase:
            case 0:
                mouseX, mouseY = pygame.mouse.get_pos()

                pressed = pygame.mouse.get_pressed()

                if pressed[0]:
                    for button in self.textButtons:
                        if button.collidepoint(mouseX, mouseY):
                            match self.textButtons.index(button):
                                case 0:
                                    self.gamePhase = 2
                                    self.makeBoss(0)

                                case 1:
                                    self.gamePhase = 1

                                case 2:
                                    gameRunning = False

                                case 3:
                                    self.difficulty = 0

                                case 4:
                                    self.difficulty =1

                                case 5:
                                    self.difficulty = 2

                                case 6:
                                    self.difficulty = 3
            
            case 1:
                mouseX, mouseY = pygame.mouse.get_pos()

                pressed = pygame.mouse.get_pressed()

                if pressed[0]:
                    for button in self.textButtons:
                        if button.collidepoint(mouseX, mouseY):
                            self.gamePhase = 0
            
            case 2:
                # Movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.player.y = max(0, self.player.y - self.player.speed)
                elif keys[pygame.K_s]:
                    self.player.y = min(960, self.player.y + self.player.speed)

                if keys[pygame.K_a]:
                    self.player.x = max(0, self.player.x - self.player.speed)
                elif keys[pygame.K_d]:
                    self.player.x = min(1160, self.player.x + self.player.speed)

                # Shooting
                pressed = pygame.mouse.get_pressed()

                if pressed[0] and self.nextShot <= 0:
                    self.nextShot = self.player.fireRate
                    
                    mouseX, mouseY = pygame.mouse.get_pos()

                    xDif = mouseX - (self.player.x + 20)
                    yDif = mouseY - (self.player.y + 20)

                    try:
                        angle = math.atan(yDif / xDif)
                    except ZeroDivisionError:
                        angle = math.pi / 2 if (yDif > 0) else -(math.pi / 2)

                    xSpeed = 12 * math.cos(angle)
                    ySpeed = 12 * math.sin(angle)

                    if xDif < 0:
                        xSpeed *= -1
                        ySpeed *= -1

                    self.playerProjectiles.append(Projectile(0, xSpeed, ySpeed, self.player.x + 20, self.player.y + 20))

                elif pressed[2] and self.nextShot2 <= 0 and not pressed[0]:
                    self.nextShot2 = self.player.fireRate * 2

                    mouseX, mouseY = pygame.mouse.get_pos()
                    xDif = mouseX - (self.player.x + 20)
                    yDif = mouseY - (self.player.y + 20)

                    try:
                        angle = math.atan(yDif / xDif)
                    except ZeroDivisionError:
                        angle = math.pi / 2 if (yDif > 0) else -(math.pi / 2)

                    for i in range(0, 4):
                        alteration = random.uniform(-0.5, 0.5)
                        xSpeed = 12 * math.cos(angle + alteration)
                        ySpeed = 12 * math.sin(angle + alteration)
                    
                        if xDif < 0:
                            xSpeed *= -1
                            ySpeed *= -1

                        self.playerProjectiles.append(Projectile(0, xSpeed, ySpeed, self.player.x + 20, self.player.y + 20))

                # Dashing
                if keys[pygame.K_SPACE] and not self.player.isDashing and self.player.dash >= 100:
                    self.player.isDashing = True
                    self.player.speed = 16
            case 3:
                mouseX, mouseY = pygame.mouse.get_pos()

                pressed = pygame.mouse.get_pressed()

                if pressed[0]:
                    for button in self.textButtons:
                        if button.collidepoint(mouseX, mouseY):
                            self.reset()
                            self.gamePhase = 0
                        

            case 4:
                mouseX, mouseY = pygame.mouse.get_pos()

                pressed = pygame.mouse.get_pressed()

                if pressed[0]:
                    for button in self.textButtons:
                        if button.collidepoint(mouseX, mouseY):
                            self.reset()
                            self.gamePhase = 0
    
    def logic(self):
        match self.gamePhase:
            case 0:
                for rain in self.rain:
                    rain.update()

                for rain in self.rain:
                    if rain.y > random.choice(range(710, 1200)):
                        self.rain.remove(rain)
                
                self.nextDrop -= 1
                if self.nextDrop <= 0:
                    self.nextDrop = 0
                    self.rain.append(Rain(random.choice(range(0, 1350)), -100))
                    self.rain.append(Rain(random.choice(range(0, 1350)), -100))

                self.nextBolt -= 1

                if self.nextBolt <= 0:
                    self.nextBolt = random.choice(range(50, 400))
                    self.boltX = random.choice(range(0, 1200))
                    self.boltLife = random.choice(range(20, 50))
                    self.boltDirection = random.choice([-1, 1])
                    self.boltFlash = random.choice(range(100, 200))

                if self.boltX != -1:
                    self.boltLife -= 3
                    self.boltFlash = max(0, self.boltFlash - 5)
            
            case 1:
                for rain in self.rain:
                    rain.update()

                for rain in self.rain:
                    if rain.y > random.choice(range(710, 1200)):
                        self.rain.remove(rain)
                
                self.nextDrop -= 1
                if self.nextDrop <= 0:
                    self.nextDrop = 0
                    self.rain.append(Rain(random.choice(range(0, 1350)), -100))
                    self.rain.append(Rain(random.choice(range(0, 1350)), -100))

                self.nextBolt -= 1

                if self.nextBolt <= 0:
                    self.nextBolt = random.choice(range(50, 400))
                    self.boltX = random.choice(range(0, 1200))
                    self.boltLife = random.choice(range(20, 50))
                    self.boltDirection = random.choice([-1, 1])
                    self.boltFlash = random.choice(range(100, 200))

                if self.boltX != -1:
                    self.boltLife -= 3
                    self.boltFlash = max(0, self.boltFlash - 5)
            
            case 2:
                # Player movement and shooting
                self.nextShot -= 1
                self.nextShot2 -= 1

                if self.player.isDashing:
                    self.player.dash -= 6
                    if self.player.dash <= 0:
                        self.player.speed = 6
                        self.player.isDashing = False
                else:
                    self.player.dash = min(100, self.player.dash + 1)

                # Player projectiles
                for projectile in self.playerProjectiles:
                    projectile.update()

                    bossBox = pygame.Rect(self.boss.x, self.boss.y, self.boss.size, self.boss.size)
                    
                    if bossBox.collidepoint((projectile.x, projectile.y)) and not (self.I11Bdashing and self.boss.bossID == 10):
                        self.boss.health -= 1
                        projectile.x = 10000

                        if self.boss.bossID == 3 or self.boss.bossID == 8:
                            self.I4Bshield = max(0, self.I4Bshield - 8)

                    for enemy in self.enemies:
                        enemyBox = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)

                        if enemyBox.collidepoint((projectile.x, projectile.y)):
                            enemy.health -= 1
                            projectile.x = 10000

                for projectile in self.playerProjectiles:
                    if (not -100 <= projectile.x <= 1300) or (not -100 <= projectile.y <= 1100):
                        self.playerProjectiles.remove(projectile)

                # Victory VS Boss
                if self.boss.health <= 0:
                    self.won = True
                    self.boss.collisionDamage = 0
                    self.enemyProjectiles = []
                    self.enemies = []

                if self.won:
                    self.winDelay -= 1

                    if self.winDelay <= 0:
                        self.player.health = min(100, self.player.health + 60)

                        if self.boss.bossID == 9:
                            self.player.health = 100
                            if self.difficulty < 3:
                                self.gamePhase = 4

                        elif self.boss.bossID >= 10:
                            self.gamePhase = 4
                        
                        self.won = False
                        self.resetBosses()

                        if self.gamePhase != 4:
                            self.makeBoss(self.boss.bossID + 1)

                            self.player.x = 580
                            self.player.y = 850

                # Loss
                if self.player.health <= 0:
                    self.gamePhase = 3
                
                # Enemy projectiles
                for projectile in self.enemyProjectiles:
                    projectile.update()

                    playerBox = pygame.Rect(self.player.x, self.player.y, 40, 40)

                    if playerBox.collidepoint((projectile.x, projectile.y)) and not self.player.isDashing:
                        self.player.health -= projectile.damage
                        projectile.x = 10000

                for projectile in self.enemyProjectiles:
                    if (not -100 <= projectile.x <= 1300) or (not -100 <= projectile.y <= 1100):
                        self.enemyProjectiles.remove(projectile)

                # Enemies
                for enemy in self.enemies:
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)

                for enemy in self.enemies:
                    enemy.collisionTick -= 1
                    
                    playerBox = pygame.Rect(self.player.x, self.player.y, 40, 40)
                    enemyBox = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)

                    if playerBox.colliderect(enemyBox) and not self.player.isDashing and enemy.collisionTick <= 0:
                        enemy.collisionTick = 20
                        self.player.health -= enemy.collisionDamage

                    match enemy.uType:
                        case 0:
                            if enemy.x < self.player.x:
                                enemy.x += 1.5
                                if enemy.x > self.player.x:
                                    enemy.x = self.player.x
                            elif enemy.x > self.player.x:
                                enemy.x -= 1.5
                                if enemy.x < self.player.x:
                                    enemy.x = self.player.x

                            if enemy.y < self.player.y:
                                enemy.y += 1.5
                                if enemy.y > self.player.y:
                                    enemy.y = self.player.y
                            elif enemy.y > self.player.y:
                                enemy.y -= 1.5
                                if enemy.y < self.player.y:
                                    enemy.y = self.player.y

                        case 1:
                            if not (((self.player.x + 20 - enemy.x + enemy.size / 2)**2 + (self.player.y + 20 - enemy.y + enemy.size / 2)**2) <= 150000):
                                if enemy.x < self.player.x:
                                    enemy.x += 1.5
                                    if enemy.x > self.player.x:
                                        enemy.x = self.player.x
                                elif enemy.x > self.player.x:
                                    enemy.x -= 1.5
                                    if enemy.x < self.player.x:
                                        enemy.x = self.player.x

                                if enemy.y < self.player.y:
                                    enemy.y += 1.5
                                    if enemy.y > self.player.y:
                                        enemy.y = self.player.y
                                elif enemy.y > self.player.y:
                                    enemy.y -= 1.5
                                    if enemy.y < self.player.y:
                                        enemy.y = self.player.y

                            enemy.nextAttack -= 1
                            if enemy.nextAttack <= 0:
                                enemy.nextAttack = random.choice(range(50, 100))
                                self.shootAtPlayer(enemy.x + enemy.size / 2, enemy.y + enemy.size / 2, 5, 4)

                # Boss
                self.boss.collisionTick -= 1
                
                playerBox = pygame.Rect(self.player.x, self.player.y, 40, 40)
                bossBox = pygame.Rect(self.boss.x, self.boss.y, self.boss.size, self.boss.size)

                if playerBox.colliderect(bossBox) and not self.player.isDashing and self.boss.collisionTick <= 0:
                    self.player.health -= self.boss.collisionDamage
                    self.boss.collisionTick = 20

                if self.boss.health > 0:
                    match self.boss.bossID:
                        case 0:
                            self.I1BnextShot -= 1
                            
                            self.moveBoss(1.5)

                            if self.I1BnextShot <= 0 and self.difficulty > 0:
                                self.I1BnextShot = 30 if self.difficulty < 15 else 15
                                self.shootAtPlayer(self.boss.x + 40, self.boss.y + 40, 7, 5)

                                if self.difficulty >= 2:
                                    self.shootAtPlayer(self.boss.x, self.boss.y, 4, 5)
                                    self.shootAtPlayer(self.boss.x + 80, self.boss.y + 80, 4, 5)
                                    self.shootAtPlayer(self.boss.x, self.boss.y + 80, 4, 5)
                                    self.shootAtPlayer(self.boss.x + 80, self.boss.y, 4, 5)

                                if self.difficulty >= 3:
                                    self.shootAtPlayer(self.boss.x, self.boss.y, 0.5, 5)
                                    self.shootAtPlayer(self.boss.x + 80, self.boss.y + 80, 0.5, 5)
                                    self.shootAtPlayer(self.boss.x, self.boss.y + 80, 0.5, 5)
                                    self.shootAtPlayer(self.boss.x + 80, self.boss.y, 0.5, 5)
                        case 1:
                            self.I2BsummonTimer -= 1

                            if self.I2BsummonTimer <= 0 and len(self.enemies) < (4 if self.difficulty < 3 else 10):
                                self.I2BsummonTimer = (100 if self.difficulty < 2 else 50)

                                self.makeEnemy(Enemy(random.choice([0, 1160]), random.choice([0, 860]), 0))
                            elif self.I2BsummonTimer <= 0:
                                self.I2BsummonTimer = 20
                                
                            if self.boss.x < self.I2BmoveTarget[0]:
                                self.boss.x += 1.8
                                if self.boss.x > self.I2BmoveTarget[0]:
                                    self.boss.x = self.I2BmoveTarget[0]
                            elif self.boss.x > self.I2BmoveTarget[0]:
                                self.boss.x -= 1.8
                                if self.boss.x < self.I2BmoveTarget[0]:
                                    self.boss.x = self.I2BmoveTarget[0]

                            if self.boss.y < self.I2BmoveTarget[1]:
                                self.boss.y += 1.8
                                if self.boss.y > self.I2BmoveTarget[1]:
                                    self.boss.y = self.I2BmoveTarget[1]
                            elif self.boss.y > self.I2BmoveTarget[1]:
                                self.boss.y -= 1.8
                                if self.boss.y < self.I2BmoveTarget[1]:
                                    self.boss.y = self.I2BmoveTarget[1]

                            if self.boss.x == self.I2BmoveTarget[0] and self.boss.y == self.I2BmoveTarget[1]:
                                self.I2BmoveTarget = [random.choice(range(100, 1100)), random.choice(range(100, 900))]
                                if self.difficulty > 0:
                                    self.makeEProjectile(Projectile(1, (9 / (1 if self.difficulty < 3 else 2)), 0, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, 0, (9 / (1 if self.difficulty < 3 else 2)), self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, -(9 / (1 if self.difficulty < 3 else 2)), 0, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, 0, -(9 / (1 if self.difficulty < 3 else 2)), self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, (6.36 / (1 if self.difficulty < 3 else 2)), (6.36 / (1 if self.difficulty < 3 else 2)), self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, (6.36 / (1 if self.difficulty < 3 else 2)), -(6.36 / (1 if self.difficulty < 3 else 2)), self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, -(6.36 / (1 if self.difficulty < 3 else 2)), (6.36 / (1 if self.difficulty < 3 else 2)), self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, -(6.36 / (1 if self.difficulty < 3 else 2)), -(6.36 / (1 if self.difficulty < 3 else 2)), self.boss.x + 25, self.boss.y + 25, 6))

                                if self.difficulty >= 3:
                                    self.makeEProjectile(Projectile(1, 2, 0, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, 0, 2, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, -2, 0, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, 0, -2, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, 1.41, 1.41, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, 1.41, -1.41, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, -1.41, 1.41, self.boss.x + 25, self.boss.y + 25, 6))
                                    self.makeEProjectile(Projectile(1, -1.41, -1.41, self.boss.x + 25, self.boss.y + 25, 6))
                        case 2:
                            self.I3BnextRain -= 1
                            self.I3BnextWall -= 1

                            speed = [4, 2, 2, 1][self.difficulty]

                            if self.difficulty >= 3:
                                self.I3BnextRain -= 1
                                self.I3BnextWall -= 1
                            
                            self.moveBoss(1.5)

                            if self.I3BnextRain <= 0:
                                self.I3BnextRain = 50

                                rainBlast = []
                                for i in range(0, (4 if self.difficulty < 2 else 8)):
                                    rainBlast.append(random.choice(range(0, 1200)))

                                direction = random.choice([0, 1, 2, 3])
                                match direction:
                                    case 0:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, 2, 0, -10, rain, 5))
                                    case 1:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, -2, 0, 1210, rain, 5))
                                    case 2:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, 0, 2, rain, -10, 5))
                                    case 3:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, 0, -2, rain, 1010, 5))

                            if self.I3BnextWall <= 0:
                                self.I3BnextWall = 400

                                rainBlast = []
                                for i in range(0, 90):
                                    rainBlast.append(i * 20)

                                direction = random.choice([0, 1, 2, 3])
                                match direction:
                                    case 0:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, speed, 0, -10, rain, 5))
                                    case 1:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, -speed, 0, 1210, rain, 5))
                                    case 2:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, 0, speed, rain, -10, 5))
                                    case 3:
                                        for rain in rainBlast:
                                            self.makeEProjectile(Projectile(1, 0, -speed, rain, 1010, 5))
                        case 3:
                            self.I4Bshield += (1.5 if self.difficulty == 3 else 1)
                            self.I4Bangle += 1
                            if self.I4Bangle > 360:
                                self.I4Bangle = 0

                            self.I4Bring -= 1
                            self.I4Bspawn -= 1

                            if ((self.player.x + 20 - self.boss.x + self.boss.size / 2)**2 + (self.player.y+- 20 - self.boss.y + self.boss.size / 2)**2) <= self.I4Bshield**2:
                                self.player.health -= 1

                            if self.I4Bring <= 0:
                                self.I4Bring = random.choice(range(50, 150))
                                for i in range(0, (9 if self.difficulty < 2 else 18)):
                                    xSpeed = 3 * math.cos(math.radians(self.I4Bangle + i * (40 if self.difficulty < 2 else 20)))
                                    ySpeed = 3 * math.sin(math.radians(self.I4Bangle + i * (40 if self.difficulty < 2 else 20)))
                                    self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, 10))

                            enemyLimit = [0, 2, 4, 6]
                            if self.I4Bspawn <= 0 and len(self.enemies) < (enemyLimit[self.difficulty]):
                                self.I4Bspawn = (100 if self.difficulty < 2 else 50)
                                self.makeEnemy(Enemy(random.choice([0, 1160]), random.choice([0, 860]), 1))

                        case 4:
                            self.moveBoss(4 if self.difficulty < 2 else 5)

                            if self.I5BteleportDamage >= self.boss.health and not self.I5InitialTeleport:
                                self.I5BteleportDamage = self.boss.health - random.choice(range(5, 15))
                                chosenX = random.choice(range(0, 1200))
                                chosenY = random.choice(range(0, 1000))

                                while ((self.player.x + 20 - chosenX)**2 + (self.player.y+- 20 - chosenY)**2) <= (40000 if self.difficulty < 3 else 25000):
                                    chosenX = random.choice(range(0, 1200))
                                    chosenY = random.choice(range(0, 1000))

                                self.boss.x = chosenX
                                self.boss.y = chosenY

                                if self.difficulty >= 1:
                                    for i in range(0, (9 if self.difficulty < 2 else 18)):
                                        xSpeed = 3 * math.cos(math.radians(i * (40 if self.difficulty < 2 else 20)))
                                        ySpeed = 3 * math.sin(math.radians(i * (40 if self.difficulty < 2 else 20)))
                                        self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, (10 if self.difficulty < 3 else 6)))

                                if self.difficulty >= 2:
                                    self.enemies = []
                                    for i in range(0, (2 if self.difficulty < 3 else 4)):
                                        chosenX = random.choice(range(0, 1200))
                                        chosenY = random.choice(range(0, 1000))

                                        while not (70000 <= ((self.player.x + 20 - chosenX)**2 + (self.player.y+- 20 - chosenY)**2) <= 150000):
                                            chosenX = random.choice(range(0, 1200))
                                            chosenY = random.choice(range(0, 1000))

                                        self.makeEnemy(Enemy(chosenX, chosenY, (0 if self.difficulty < 3 else 1)))
                            elif self.I5BteleportDamage >= self.boss.health and  self.I5InitialTeleport:
                                self.I5BteleportDamage = self.boss.health - random.choice(range(5, 15))
                                self.I5InitialTeleport = False
                                self.boss.x = 600 - 15
                                self.boss.y = 0

                        case 5:
                            if self.boss.x < self.I6BmoveTarget[0]:
                                self.boss.x += 1.5
                                if self.boss.x > self.I6BmoveTarget[0]:
                                    self.boss.x = self.I6BmoveTarget[0]
                            elif self.boss.x > self.I6BmoveTarget[0]:
                                self.boss.x -= 1.5
                                if self.boss.x < self.I6BmoveTarget[0]:
                                    self.boss.x = self.I6BmoveTarget[0]

                            if self.boss.y < self.I6BmoveTarget[1]:
                                self.boss.y += 1.5
                                if self.boss.y > self.I6BmoveTarget[1]:
                                    self.boss.y = self.I6BmoveTarget[1]
                            elif self.boss.y > self.I6BmoveTarget[1]:
                                self.boss.y -= 1.5
                                if self.boss.y < self.I6BmoveTarget[1]:
                                    self.boss.y = self.I6BmoveTarget[1]

                            if self.boss.x == self.I6BmoveTarget[0] and self.boss.y == self.I6BmoveTarget[1]:
                                self.I6BmoveTarget = [random.choice(range(100, 1100)), random.choice(range(100, 900))]

                            self.I6BnextShot -= 1

                            if self.I6BnextShot <= 0:
                                self.I6BnextShot = [5, 3, 2, 0][self.difficulty]
                                self.shootAtPlayer(self.boss.x + 20, self.boss.y + 20, 7, (3 if self.difficulty == 0 else 1))

                                if self.difficulty >= 2:
                                    self.shootAtPlayer(self.boss.x, self.boss.y, 5, 1)
                                    self.shootAtPlayer(self.boss.x + 40, self.boss.y, 5, 1)

                                if self.difficulty >= 3:
                                    self.shootAtPlayer(self.boss.x, self.boss.y + 40, 5, 1)
                                    self.shootAtPlayer(self.boss.x + 40, self.boss.y + 40, 5, 1)

                            self.I6walls -= 1

                            speed = [4, 2, 2, 1][self.difficulty]

                            if self.I6walls <= 0 and self.difficulty >= 1:
                                self.I6walls = 800

                                rainBlast = []
                                for i in range(0, 90):
                                    rainBlast.append(i * 20)

                                for direction in [0, 1, 2, 3]:
                                    match direction:
                                        case 0:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, speed, 0, -10, rain, 1))
                                        case 1:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, -speed, 0, 1210, rain, 1))
                                        case 2:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, 0, speed, rain, -10, 1))
                                        case 3:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, 0, -speed, rain, 1010, 1))
                        case 6:
                            if self.I7BmoveTarget == [-1, -1]:
                                match random.choice([0, 1, 2, 3]):
                                    case 0:
                                        self.boss.x = -60
                                        self.boss.y = random.choice(range(0, 960))
                                        self.I7BmoveTarget = [1200, random.choice(range(0, 960))]

                                    case 1:
                                        self.boss.x = 1200
                                        self.boss.y = random.choice(range(0, 960))
                                        self.I7BmoveTarget = [-60, random.choice(range(0, 960))]

                                    case 2:
                                        self.boss.y = -60
                                        self.boss.x = random.choice(range(0, 1140))
                                        self.I7BmoveTarget = [random.choice(range(0, 1140)), 1000]

                                    case 3:
                                        self.boss.y = 1000
                                        self.boss.x = random.choice(range(0, 1140))
                                        self.I7BmoveTarget = [random.choice(range(0, 1140)), -60]

                                if self.difficulty >= 1:
                                    self.shootAtPlayer(self.boss.x, self.boss.y, 2, 10)
                                self.I7BmoveRing = False

                            if self.boss.x < self.I7BmoveTarget[0]:
                                self.boss.x += (5 if self.difficulty < 3 else 6)
                                if self.boss.x > self.I7BmoveTarget[0]:
                                    self.boss.x = self.I7BmoveTarget[0]
                            elif self.boss.x > self.I7BmoveTarget[0]:
                                self.boss.x -= (5 if self.difficulty < 3 else 6)
                                if self.boss.x < self.I7BmoveTarget[0]:
                                    self.boss.x = self.I7BmoveTarget[0]

                            if self.boss.y < self.I7BmoveTarget[1]:
                                self.boss.y += (5 if self.difficulty < 3 else 6)
                                if self.boss.y > self.I7BmoveTarget[1]:
                                    self.boss.y = self.I7BmoveTarget[1]
                            elif self.boss.y > self.I7BmoveTarget[1]:
                                self.boss.y -= (5 if self.difficulty < 3 else 6)
                                if self.boss.y < self.I7BmoveTarget[1]:
                                    self.boss.y = self.I7BmoveTarget[1]

                            if self.boss.x == self.I7BmoveTarget[0] and self.boss.y == self.I7BmoveTarget[1]:
                                self.I7BmoveTarget = [-1, -1]

                                self.shootAtPlayer(self.boss.x, self.boss.y, 2, 10)

                                if self.difficulty >= 2:
                                    for i in range(0, (9 if self.difficulty < 3 else 18)):
                                        xSpeed = 3 * math.cos(math.radians(i * (40 if self.difficulty < 3 else 20)))
                                        ySpeed = 3 * math.sin(math.radians(i * (40 if self.difficulty < 3 else 20)))
                                        self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, (10 if self.difficulty < 3 else 5)))

                            if (self.boss.y <= self.player.y <= self.boss.y + 60 or self.boss.x <= self.player.x <= self.boss.x + 60) and not self.I7BmoveRing:
                                self.I7BmoveRing = True

                                if self.difficulty == 0:
                                    self.shootAtPlayer(self.boss.x, self.boss.y, 2, 10)
                                else:
                                    for i in range(0, (9 if self.difficulty < 2 else 18)):
                                        xSpeed = 3 * math.cos(math.radians(i * (40 if self.difficulty < 2 else 20)))
                                        ySpeed = 3 * math.sin(math.radians(i * (40 if self.difficulty < 2 else 20)))
                                        self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, (10 if self.difficulty < 3 else 5)))
                        case 7:
                            self.moveBoss(((1 - (self.boss.health / self.boss.maxHealth)) * 4) + 1)

                            self.I8BdecayTimer -= 1

                            if self.I8BdecayTimer <= 0:
                                self.I8BdecayTimer = [8, 6, 4, 3][self.difficulty]

                                speed = random.uniform(1, 5)
                                angle = random.uniform(0, 360)
                                xSpeed = speed * math.cos(math.radians(angle))
                                ySpeed = speed * math.sin(math.radians(angle))
                                self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, 5))

                        case 8:
                            self.moveBoss(1)
                            
                            self.boss.colour = (random.choice(range(0, 50)), random.choice(range(0, 50)), random.choice(range(0, 50)))

                            self.I1BnextShot -= 1

                            if self.I1BnextShot <= 0 and self.difficulty > 0:
                                self.I1BnextShot = 50 if self.difficulty < 3 else 30
                                self.shootAtPlayer(self.boss.x + 40, self.boss.y + 40, 7, 5)

                            self.I2BsummonTimer -= 1

                            if self.I2BsummonTimer <= 0 and len(self.enemies) < [2, 3, 4, 6][self.difficulty]:
                                self.I2BsummonTimer = (150 if self.difficulty < 2 else 100)

                                self.makeEnemy(Enemy(random.choice([0, 1160]), random.choice([0, 860]), random.choice([0, 1])))
                            elif self.I2BsummonTimer <= 0:
                                self.I2BsummonTimer = 20

                            self.I3BnextWall -= 1
                            
                            if self.I3BnextWall <= 0:
                                self.I3BnextWall = 600

                                rainBlast = []
                                for i in range(0, 90):
                                    rainBlast.append(i * 20)

                                directions = [0, 1, 2, 3]

                                speed = [4, 2, 2, 1][self.difficulty]

                                for i in range(0, 2):
                                    direction = random.choice(directions)
                                    match direction:
                                        case 0:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, speed, 0, -10, rain, 5))
                                        case 1:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, -speed, 0, 1210, rain, 5))
                                        case 2:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, 0, speed, rain, -10, 5))
                                        case 3:
                                            for rain in rainBlast:
                                                self.makeEProjectile(Projectile(1, 0, -speed, rain, 1010, 5))

                                    directions.remove(direction)

                            self.I4Bshield += 0.8
                            if ((self.player.x + 20 - self.boss.x + self.boss.size / 2)**2 + (self.player.y+- 20 - self.boss.y + self.boss.size / 2)**2) <= self.I4Bshield**2:
                                self.player.health -= 1

                            self.I4Bangle += 1
                            if self.I4Bangle > 360:
                                self.I4Bangle = 0

                            self.I4Bring -= 1

                            if self.I4Bring <= 0:
                                self.I4Bring = random.choice(range(150, 200))
                                for i in range(0, (9 if self.difficulty < 2 else 18)):
                                    xSpeed = 3 * math.cos(math.radians(self.I4Bangle + i * (40 if self.difficulty < 2 else 20)))
                                    ySpeed = 3 * math.sin(math.radians(self.I4Bangle + i * (40 if self.difficulty < 2 else 20)))
                                    self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, 10))

                            self.I8BdecayTimer -= 1

                            if self.I8BdecayTimer <= 0:
                                self.I8BdecayTimer = [30, 20, 15, 10][self.difficulty]

                                speed = random.uniform(1, 5)
                                angle = random.uniform(0, 360)
                                xSpeed = speed * math.cos(math.radians(angle))
                                ySpeed = speed * math.sin(math.radians(angle))
                                self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, 5))

                        case 9:
                            self.I10BsideShot -= 1
                            self.I10patternSwap -= 1

                            self.I10Bangle += 1
                            if self.I10Bangle > 360:
                                self.I10Bangle = 0

                            if self.I10patternSwap <= 0:
                                if len(self.enemyProjectiles) <= 0:
                                    self.I10BattackPattern = random.choice([0, 1, 2])
                                    self.I10BsideShot = 0
                                    self.I10patternSwap = random.choice(range(400, 800))

                                    if self.I10BattackPattern == 2 and self.difficulty < 2:
                                        self.I10BattackPattern = random.choice([0, 1])

                                    if self.difficulty < 1:
                                        self.I10BattackPattern = 0
                                else:
                                    self.I10BattackPattern = 5

                            if self.I10BsideShot <= 0:
                                match self.I10BattackPattern:
                                    case 0:
                                        self.I10BsideShot = [12, 8, 6, 4][self.difficulty]

                                        direction = random.choice([0, 1, 2, 3])
                                        speed = [2, 1, 1, 1][self.difficulty]
                                        match direction:
                                            case 0:
                                                self.makeEProjectile(Projectile(1, speed, 0, -10, random.choice(range(0, 1000)), 3))
                                            case 1:
                                                self.makeEProjectile(Projectile(1, -speed, 0, 1210, random.choice(range(0, 1000)), 3))
                                            case 2:
                                                self.makeEProjectile(Projectile(1, 0, speed, random.choice(range(0, 1200)), -10, 3))
                                            case 3:
                                                self.makeEProjectile(Projectile(1, 0, -speed, random.choice(range(0, 1200)), 1010, 3))

                                    case 1:
                                        self.I10BsideShot = [50, 30, 20, 15][self.difficulty]
                                        
                                        for i in range(0, 18):
                                            xSpeed = 3 * math.cos(math.radians(self.I10Bangle + i * 20))
                                            ySpeed = 3 * math.sin(math.radians(self.I10Bangle + i * 20))
                                            self.makeEProjectile(Projectile(1, xSpeed, ySpeed, self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2, 8))

                                    case 2:
                                        self.I10BsideShot = [15, 12, 10, 8][self.difficulty]
                                        self.shootAtPlayer(0, 0, 1, 3)
                                        self.shootAtPlayer(1200, 1000, 1, 3)
                                        self.shootAtPlayer(0, 1000, 1, 3)
                                        self.shootAtPlayer(1200, 0, 1, 3)

                                        self.shootAtPlayer(600, 0, 1, 3)
                                        self.shootAtPlayer(600, 1000, 1, 3)
                                        self.shootAtPlayer(0, 500, 1, 3)
                                        self.shootAtPlayer(1200, 500, 1, 3)

                        case 10:
                            if self.I11BmoveTarget == [-1, -1]:
                                hasSpot = False

                                while not hasSpot:
                                    self.I11BmoveTarget = [random.choice(range(0, 1160)), random.choice(range(0, 960))]
                                    distance = (self.I11BmoveTarget[0] - self.player.x)**2 + (self.I11BmoveTarget[1] - self.player.y)**2
                                    butterZone = (100)**2
                                    
                                    if (distance > butterZone and self.I11Bstyle == 0) or (distance < butterZone and self.I11Bstyle == 1):
                                        hasSpot = True

                            if self.boss.x < self.I11BmoveTarget[0]:
                                self.boss.x += (16 if self.I11Bdashing else 6)
                                if self.boss.x > self.I11BmoveTarget[0]:
                                    self.boss.x = self.I11BmoveTarget[0]
                            elif self.boss.x > self.I11BmoveTarget[0]:
                                self.boss.x -= (16 if self.I11Bdashing else 6)
                                if self.boss.x < self.I11BmoveTarget[0]:
                                    self.boss.x = self.I11BmoveTarget[0]

                            if self.boss.y < self.I11BmoveTarget[1]:
                                self.boss.y += (16 if self.I11Bdashing else 6)
                                if self.boss.y > self.I11BmoveTarget[1]:
                                    self.boss.y = self.I11BmoveTarget[1]
                            elif self.boss.y > self.I11BmoveTarget[1]:
                                self.boss.y -= (16 if self.I11Bdashing else 6)
                                if self.boss.y < self.I11BmoveTarget[1]:
                                    self.boss.y = self.I11BmoveTarget[1]

                            if self.boss.x == self.I11BmoveTarget[0] and self.boss.y == self.I11BmoveTarget[1]:
                                self.I11BmoveTarget = [-1, -1]

                                self.I11BstyleSwitch -= random.choice(range(1, 100))

                                if self.I11BstyleSwitch <= 0:
                                    self.I11Bstyle = (0 if self.I11Bstyle == 1 else 1)
                                    
                                    self.I11BstyleSwitch = random.choice(range(400, 700))

                            self.I11BnextDash -= 1

                            if self.I11BnextDash <= 0:
                                if self.I11Bdashing:
                                    self.I11Bdashing = False
                                    self.I11BnextDash = random.choice(range(100, 500))

                                else:
                                    self.I11Bdashing = True
                                    self.I11BnextDash = 16

                            shotType = -1

                            self.I11BnextShot -= 1

                            if self.I11BnextShot <= 0:
                                self.I11BnextShot = 5
                                
                                shotType = random.choice([0, 0, 0, 0, 1])

                                if (self.I11BmoveTarget[0] - self.player.x)**2 + (self.I11BmoveTarget[1] - self.player.y)**2 < (150)**2:
                                    shotType = random.choice([1, 1, 1, 1, 0])

                            if shotType == 0:
                                self.shootAtPlayer(self.boss.x + 20, self.boss.y + 20, 6, 3)

                            elif shotType == 1:
                                self.I11BnextShot = 10
                                
                                mouseX = self.player.x + 20
                                mouseY = self.player.y + 20
                                xDif = mouseX - (self.boss.x + 20)
                                yDif = mouseY - (self.boss.y + 20)

                                try:
                                    angle = math.atan(yDif / xDif)
                                except ZeroDivisionError:
                                    angle = math.pi / 2 if (yDif > 0) else -(math.pi / 2)

                                for i in range(0, 4):
                                    alteration = random.uniform(-0.5, 0.5)
                                    xSpeed = 12 * math.cos(angle + alteration)
                                    ySpeed = 12 * math.sin(angle + alteration)
                                
                                    if xDif < 0:
                                        xSpeed *= -1
                                        ySpeed *= -1

                                    self.enemyProjectiles.append(Projectile(1, xSpeed, ySpeed, self.boss.x + 20, self.boss.y + 20, 3))
                                
            case 3:
                pass

            case 4:
                pass

    def draw(self):
        global screen

        self.textButtons = []
        
        match self.gamePhase:
            case 0:
                screen.fill((53,25,49))

                # Water - Back
                pygame.draw.rect(screen, (5, 15, 80), pygame.Rect(0, 730, 1200, 500))

                # The Sun
                pygame.draw.circle(screen, (240, 255, 25), (600, 700), 200)

                # Water - Front
                s = pygame.Surface((1200, 500))
                s.set_alpha(240)
                s.fill((5, 15, 80))
                screen.blit(s, (0, 730))

                # Rain
                for rain in self.rain:
                    pygame.draw.line(screen, (255, 255, 255), (rain.x, rain.y), (rain.x - 5, rain.y + 20))

                # Lightning - Flash
                if self.boltFlash >= 0:
                    s = pygame.Surface((2200, 2000))
                    s.set_alpha(self.boltFlash)
                    s.fill((255, 255, 255))
                    screen.blit(s, (0, 0))

                # Lightning - Bolt
                if self.boltLife >= 0:
                    pygame.draw.line(screen, (255, 255, 255), (self.boltX, 0), (self.boltX + 50 * self.boltDirection, 600))
                    pygame.draw.line(screen, (255, 255, 255), (self.boltX - 50, 600), (self.boltX + 70 * self.boltDirection, 500))
                    pygame.draw.line(screen, (255, 255, 255), (self.boltX - 70, 500), (self.boltX + 80 * self.boltDirection, 1000))

                # Window
                s = pygame.Surface((2200, 2000))
                s.set_alpha(110)
                s.fill((20, 20, 20))
                screen.blit(s, (0, 0))

                # Window Frame
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 0, 1200, 20))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 980, 1200, 20))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 0, 20, 1000))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(1180, 0, 20, 1000))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(590, 0, 20, 1000))

                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 315, 1200, 10))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 635, 1200, 10))

                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(295, 0, 10, 1000))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(895, 0, 10, 1000))

                # Text
                self.drawText("Epic Boss Fighter", (255, 255, 255), self.titleFont, 600, 50, 1)

                # Buttons
                self.textButtons.append(self.drawText("> Play <", (255, 255, 255), self.headerFont, 760, 380, 1))
                self.textButtons.append(self.drawText("> Help <", (255, 255, 255), self.headerFont, 760, 480, 1))
                self.textButtons.append(self.drawText("> Quit <", (255, 255, 255), self.headerFont, 760, 580, 1))

                # Difficulties
                self.textButtons.append(self.drawText("> Easy <", ((255, 255, 255) if self.difficulty == 0 else (100, 100, 100)), self.headerFont, 450, 360, 1))
                self.textButtons.append(self.drawText("> Normal <", ((255, 255, 255) if self.difficulty == 1 else (100, 100, 100)), self.headerFont, 450, 440, 1))
                self.textButtons.append(self.drawText("> Hard <", ((255, 255, 255) if self.difficulty == 2 else (100, 100, 100)), self.headerFont, 450, 520, 1))
                self.textButtons.append(self.drawText("> Impossible <", ((255, 255, 255) if self.difficulty == 3 else (100, 100, 100)), self.headerFont, 450, 600, 1))
            
            case 1:
                screen.fill((53,25,49))

                # Water - Back
                pygame.draw.rect(screen, (5, 15, 80), pygame.Rect(0, 730, 1200, 500))

                # The Sun
                pygame.draw.circle(screen, (240, 255, 25), (600, 700), 200)

                # Water - Front
                s = pygame.Surface((1200, 500))
                s.set_alpha(240)
                s.fill((5, 15, 80))
                screen.blit(s, (0, 730))

                # Rain
                for rain in self.rain:
                    pygame.draw.line(screen, (255, 255, 255), (rain.x, rain.y), (rain.x - 5, rain.y + 20))

                # Lightning - Flash
                if self.boltFlash >= 0:
                    s = pygame.Surface((2200, 2000))
                    s.set_alpha(self.boltFlash)
                    s.fill((255, 255, 255))
                    screen.blit(s, (0, 0))

                # Lightning - Bolt
                if self.boltLife >= 0:
                    pygame.draw.line(screen, (255, 255, 255), (self.boltX, 0), (self.boltX + 50 * self.boltDirection, 600))
                    pygame.draw.line(screen, (255, 255, 255), (self.boltX - 50, 600), (self.boltX + 70 * self.boltDirection, 500))
                    pygame.draw.line(screen, (255, 255, 255), (self.boltX - 70, 500), (self.boltX + 80 * self.boltDirection, 1000))

                # Window
                s = pygame.Surface((2200, 2000))
                s.set_alpha(110)
                s.fill((20, 20, 20))
                screen.blit(s, (0, 0))

                # Window Frame
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 0, 1200, 20))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 980, 1200, 20))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 0, 20, 1000))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(1180, 0, 20, 1000))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(590, 0, 20, 1000))

                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 315, 1200, 10))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(0, 635, 1200, 10))

                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(295, 0, 10, 1000))
                pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(895, 0, 10, 1000))

                # Text
                self.drawText("Epic Boss Fighter", (255, 255, 255), self.titleFont, 600, 50, 1)

                self.drawText("Defeat every boss.", (255, 255, 255), self.headerFont, 760, 380, 1)
                self.drawText("Dash to move", (255, 255, 255), self.headerFont, 760, 460, 1)
                self.drawText("through damage.", (255, 255, 255), self.headerFont, 760, 500, 1)
                self.drawText("Don't die", (255, 255, 255), self.headerFont, 760, 580, 1)

                self.drawText("WASD: Move", (255, 255, 255), self.subtitleFont, 450, 360, 1)
                self.drawText("Left Click: Fire", (255, 255, 255), self.subtitleFont, 450, 440, 1)
                self.drawText("Right Click: Shotgun", (255, 255, 255), self.subtitleFont, 450, 520, 1)
                self.drawText("Space: Dash", (255, 255, 255), self.subtitleFont, 450, 600, 1)

                self.textButtons.append(self.drawText("> Back <", (255, 255, 255), self.headerFont, 450, 900, 1))
                self.textButtons.append(self.drawText("> Back <", (255, 255, 255), self.headerFont, 760, 900, 1))
            
            case 2:
                # Clear screen
                screen.fill((0, 0, 0))

                if self.won and self.winDelay > 100:
                    if self.winDelay >= 125:
                        screen.fill((0, 3*(150 - self.winDelay), 0))
                    else:
                        screen.fill((0, 3*(self.winDelay - 100), 0))

                # Boss Shield
                if self.boss.bossID == 3 or self.boss.bossID == 8:
                    pygame.draw.circle(screen, (20, 170, 150), (self.boss.x + self.boss.size / 2, self.boss.y + self.boss.size / 2), int(self.I4Bshield))
                
                # Player Projectiles
                for projectile in self.playerProjectiles:
                    pygame.draw.circle(screen, (200, 200, 0), (projectile.x, projectile.y), 10)

                # Enemy Projectiles
                for projectile in self.enemyProjectiles:
                    pygame.draw.circle(screen, (200, 0, 0), (int(projectile.x), int(projectile.y)), 10)
                
                # Player
                pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(self.player.x, self.player.y, 40, 40))

                # Enemies
                for enemy in self.enemies:
                    pygame.draw.rect(screen, enemy.colour, pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size))

                # Boss
                pygame.draw.rect(screen, self.boss.colour, pygame.Rect(self.boss.x, self.boss.y, self.boss.size, self.boss.size))

                # Statistics
                self.drawText("Health: " + str(math.ceil(self.player.health)) + "%", (255, 255, 255), self.statFont, 20, 950, 0)
                self.drawText("Dash: " + str(self.player.dash) + "%", (255, 255, 255), self.statFont, 20, 975, 0)
                
                # Boss Bar
                pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(5, 5, 1190, 30))
                pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(10, 10, 1180, 20))
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, (1180 * (self.boss.health / self.boss.maxHealth)), 20))

                # Health Bar
                pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(0, 940, 300, 60))
                pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(10, 950, 280, 40))
                pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(10, 950, 280, 30))
                pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(10, 950, (280 * (self.player.health / 100)), 30))
                pygame.draw.rect(screen, (0, 0, 200), pygame.Rect(10, 980, (280 * (self.player.dash / 100)), 10))
                
            case 3:
                screen.fill((200, 0, 0))
                
                self.drawText("Defeat...", (255, 255, 255), self.headerFont, 600, 30, 1)

                self.drawText("Difficulty: " + ["Easy", "Normal", "Hard", "Impossible"][self.difficulty], (255, 255, 255), self.subtitleFont, 600, 70, 1)

                match self.boss.bossID:
                    case 0:
                        self.drawText(["Wha-?! This is the easiest boss on the EASIEST difficulty! HOW DID YOU LOSE?!",
                                       "This is the first boss! If you lost here, what about the others?!",
                                       "Good effort, although maybe you need a bit more practice. Try Normal first.",
                                       "...Well... We don't call it \"Impossible\" for no reason..."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 1:
                        self.drawText(["At least it wasn't the first boss... Try gunning down the enemies to clear space.",
                                       "Second boss, not bad. Don't hyper-focus on anything, it'll cause your death.",
                                       "Second boss... Be wary of those ring attacks, they're a killer.",
                                       "Hey, at least you made it past the first boss..."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 2:
                        self.drawText(["Okay, this one is a bit difficult. Use your dash to bypass the projectile walls with ease.",
                                       "Be wary of those walls and save your dash if you can. You may need it.",
                                       "Okay, this boss is kind of difficult. Use your shotgun when close-up to the boss, it'll speed things up.",
                                       "This boss is just stupid. I have nothing else to say."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 3:
                        self.drawText(["Keep an eye on the boss' shield, it'll kill you if you're in it. Shoot the boss to weaken the shield.",
                                       "Keep an eye on where those rings are going. You should be able to shimmey to evade them.",
                                       "Lots of projectiles, huh? You have more time than you think to handle the shield, it grows slowly.",
                                       "My only advice: Always attack the boss. If you don't, you risk losing to the shield."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 4:
                        self.drawText(["This boss is like a ninja. It's going to keep teleporting to try and flank you.",
                                       "Use your dash to put distance between you and the boss, giving you more time to weaken it.",
                                       "You can probably just ignore any enemies that spawn around you. They won't catch you.",
                                       "Stay in the centre if you can help it, and use your dash to evade the boss. It'll kill you quickly."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 5:
                        self.drawText(["Just circle the boss and don't let it flank you. You should do fine.",
                                       "Those walls can be tricky to dodge. Try to leap through a horizontal and vertical wall at a time.",
                                       "The walls don't do loads of damage, so don't worry if you need your dash to evade the boss.",
                                       "All I can really say is focus. Try to save your dash and be ready at a moment's notice to dodge."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 6:
                        self.drawText(["Stay in the middle of the screen. It'll give you the most time to dodge its rushes.",
                                       "Be wary of those slow-moving projectiles. Always be aware where they're headed.",
                                       "Try not to stay directly above, below, left, or right of it. That's when it launches extra projectiles.",
                                       "Don't get greedy with that shotgun if you can help it. Your main weapon will keep you safe."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 7:
                        self.drawText(["This boss is really unstable. Try to stay away from it and let the projectiles spread out more.",
                                       "The boss speeds up the more you damage it. Use your dash when it's low on health to keep your distance.",
                                       "You can try to circle it while it's in the middle of the screen to keep it locked there.",
                                       "Honestly, focus completely on survival if this boss gets close. Don't take any risks."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 8:
                        self.drawText(["Alright, this boss is tough. It's a combination of previous bosses, so counter them the same way you did before.",
                                       "You'll want to use your shotgun to bring down the boss as fast as you can.",
                                       "Try to group the enemies together to get them out of your hair, leaving you with just the boss.",
                                       "I'll be honest with you right now - This is the hardest boss in the game."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 9:
                        self.drawText(["Damn, so close! Oh well, you win some, you lose some I guess.",
                                       "The boss leaves itself open to an attack each time it finishes an attack. Take that opportunity to attack it!",
                                       "Be wary of what attack the boss is using next. Always be ready to dodge.",
                                       "It's probably your nerves that got you killed... Calm yourself and be ready when this boss arrives again."][self.difficulty],(255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 10:
                        self.drawText("Once you've bested everyone else, the only person who can defeat you is yourself.", (255, 255, 255), self.subtitleFont, 600, 500, 1)
                        
                self.textButtons.append(self.drawText("> Back <", (255, 255, 255), self.subtitleFont, 600, 970, 1))

            case 4:
                screen.fill((0, 200, 0))

                self.drawText("! VICTORY !", (255, 255, 255), self.headerFont, 600, 30, 1)

                self.drawText("Difficulty: " + ["Easy", "Normal", "Hard", "Impossible"][self.difficulty], (255, 255, 255), self.subtitleFont, 600, 70, 1)

                match self.difficulty:
                    case 0:
                        self.drawText("Easy? That's it? Come on, try a harder difficulty!", (255, 255, 255), self.subtitleFont, 600, 500, 1)
                        self.drawText("wimp", (255, 255, 255), self.statFont, 600, 525, 1)

                    case 1:
                        self.drawText("Normal. Not bad, not great. You're in the middle. Good job.", (255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 2:
                        self.drawText("Hard mode, huh? Now that's pretty impressive. Well done! Now, try Impossible if you're up for it...", (255, 255, 255), self.subtitleFont, 600, 500, 1)

                    case 3:
                        self.drawText("...Welp... Guess I gotta go make a harder difficulty now...", (255, 255, 255), self.subtitleFont, 600, 500, 1)

                self.textButtons.append(self.drawText("> Back <", (255, 255, 255), self.subtitleFont, 600, 970, 1))
        
        pygame.display.flip() # Display drawn objects on screen

# Run the actual game
game = Game() # Game object

gameRunning = True
while gameRunning:
    ev = pygame.event.get()
    
    for event in ev:
        if event.type == pygame.QUIT:
            gameRunning = False
    
    # Run game functions
    game.inputs()
    game.logic()
    game.draw()

    time.sleep(tickDelay)

pygame.quit()
