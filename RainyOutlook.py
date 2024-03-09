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
gameTitle = "A Rainy Outlook"

screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption(gameTitle)

# Game class
class Game:
    def __init__(self):
        self.gamePhase = 0

        # Fonts
        self.statFont = pygame.font.SysFont('Arial', 20)
        self.subtitleFont = pygame.font.SysFont('Arial', 25)
        self.headerFont = pygame.font.SysFont('Arial', 40)
        self.titleFont = pygame.font.SysFont('Arial', 50)

        # Lightning Bolts
        self.nextBolt = random.choice(range(50, 400))
        self.boltX = -1
        self.boltFlash = 0
        self.boltLife = 0
        self.boltDirection = 0

        # Main Menu
        self.rain = []
        self.nextDrop = 0
    
    def logic(self):
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

    def draw(self):
        global screen
        
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
    game.logic()
    game.draw()

    time.sleep(tickDelay)

pygame.quit()
