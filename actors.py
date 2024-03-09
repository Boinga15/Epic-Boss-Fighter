import math
import copy
import random

class Rain:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.x -= 2.4
        self.y += 20

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 6

        self.fireRate = 5

        self.health = 100
        self.dash = 100
        self.isDashing = False

class Projectile:
    def __init__(self, team, xSpeed, ySpeed, x, y, damage = 1):
        self.velX = xSpeed
        self.velY = ySpeed

        self.x = x
        self.y = y

        self.damage = damage

    def update(self):
        self.x += self.velX
        self.y += self.velY

class Boss:
    def __init__(self, bossID):
        self.bossID = bossID
        
        self.health = [200, 120, 240, 250, 100, 120, 160, 300, 260, 500, 34][bossID]
        self.maxHealth = copy.deepcopy(self.health)
        
        self.size = [80, 50, 70, 100, 30, 40, 60, 50, 100, 200, 40][bossID]
        self.colour = [(150, 0, 0), (200, 90, 0), (150, 150, 150), (150, 200, 50), (20, 20, 20), (70, 10, 70), (110, 45, 0), (20, 65, 10), (0, 0, 0), (255, 255, 255), (255, 0, 0)][bossID]

        self.x = 600 - self.size / 2
        self.y = 500 - self.size / 2
        self.collisionDamage = [15, 12, 20, 15, 5, 20, 15, 30, 10, 100, 0][bossID]

        self.collisionTick = 0

class Enemy:
    def __init__(self, x, y, uType):
        self.x = x
        self.y = y
        self.uType = uType

        self.health = [10, 8][uType]
        self.colour = [(255, 0, 0), (120, 30, 10)][uType]
        self.size = [40, 40][uType]
        self.collisionDamage = [5, 2][uType]
        self.speed = [3, 2][uType]

        self.collisionTick = 0

        self.nextAttack = [0, 50][uType]
