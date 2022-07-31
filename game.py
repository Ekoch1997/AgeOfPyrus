import random
import math
from settings import *
import pygame
from itertools import cycle

#walls
#resource gatherer building
#barracks - creates units to run towards buldings / enemies
#bomb with countdown timer

class Resource():
    def __init__(self, resource, amount):
        self.resource = resource
        self.amount = amount

class Projectile():
    def __init__(self,symbol,img,speed,direction,damage,location):
        self.symbol = symbol
        self.img = img
        self.speed = speed
        self.direction = direction
        self.damage = damage
        self.location = location

class Tower():
    def __init__(self,towerType,health,damage,cooldown,location):
        self.towerType = towerType
        self.health = health
        self.damage = damage
        self.cooldown = cooldown
        self.location = location



class GameOverScene:

    def draw(self, screen):
        screen.fill(pygame.Color('lightblue'))
        screen.blit(font_gameOver.render("GAME OVER",1,"black"),(470,200))
        if player_info['p2']['health'] <= 0:
            screen.blit(font_gameOver.render("P1 WINS!",1,"blue"),(560,320))
        else:
            screen.blit(font_gameOver.render("P2 WINS!",1,"red"),(560,320))

class GameActiveScene:

    def draw(self,screen):

        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] != ' ':

                    if hasattr(map[i][j],'resource'):
                        if map[i][j].resource == 'G':
                            screen.blit(GOLD_IMG, (j * BLOCKSIZE, i * BLOCKSIZE))
                            screen.blit(font_block_info.render(str(map[i][j].amount),1,"black"),(j * BLOCKSIZE + BLOCKSIZE / 3, i * BLOCKSIZE + BLOCKSIZE / 3))
                        if map[i][j].resource == 'S':
                            screen.blit(STONE_IMG, (j * BLOCKSIZE, i * BLOCKSIZE))
                            screen.blit(font_block_info.render(str(map[i][j].amount),1,"black"),(j * BLOCKSIZE + BLOCKSIZE / 3, i * BLOCKSIZE + BLOCKSIZE / 3))
                        if map[i][j].resource == 'W':
                            screen.blit(TREE_IMG, (j * BLOCKSIZE, i * BLOCKSIZE))
                            screen.blit(font_block_info.render(str(map[i][j].amount),1,"black"),(j * BLOCKSIZE + BLOCKSIZE / 3, i * BLOCKSIZE + BLOCKSIZE / 3))

                    elif map[i][j] == 'P1':
                        screen.blit(PLAYER1_IMG, (j * BLOCKSIZE, i * BLOCKSIZE))
                    elif map[i][j] == 'P2':
                        screen.blit(PLAYER2_IMG, (j * BLOCKSIZE, i * BLOCKSIZE))

                    elif hasattr(map[i][j],'towerType'): #tower
                        if map[i][j].towerType == 'WizardTower':
                            screen.blit(WIZARDTOWER_IMG, (j * BLOCKSIZE, i * BLOCKSIZE))
                            screen.blit(font_block_info.render(str(map[i][j].health),1,"black"),(j * BLOCKSIZE + BLOCKSIZE / 3, i * BLOCKSIZE + BLOCKSIZE / 3))
                        if map[i][j].towerType == 'ArcherTower':
                            screen.blit(ARCHERTOWER_IMG, (j * BLOCKSIZE, i * BLOCKSIZE))
                            screen.blit(font_block_info.render(str(map[i][j].health),1,"black"),(j * BLOCKSIZE + BLOCKSIZE / 3, i * BLOCKSIZE + BLOCKSIZE / 3))
                    
                    elif hasattr(map[i][j],'symbol'): #projectile
                        rotated_image = pygame.transform.rotate(map[i][j].img, map[i][j].direction - 90)
                        new_rect = rotated_image.get_rect(center = FIREBALL_IMG.get_rect(topleft = (j * BLOCKSIZE, i * BLOCKSIZE)).center)
                        screen.blit(rotated_image, new_rect)


        #Stats
        screen.blit(font.render("Health: " + str(player_info['p1']['health']),1,"black"),(10,10))
        screen.blit(font.render("Wood: " + str(player_info['p1']['W']),1,"black"),(10,30))
        screen.blit(font.render("Stone: " + str(player_info['p1']['S']),1,"black"),(10,50))
        screen.blit(font.render("Gold: " + str(player_info['p1']['G']),1,"black"),(10,70))

        screen.blit(font.render("Health: " + str(player_info['p2']['health']),1,"black"),(1500,10))
        screen.blit(font.render("Wood: " + str(player_info['p2']['W']),1,"black"),(1500,30))
        screen.blit(font.render("Stone: " + str(player_info['p2']['S']),1,"black"),(1500,50))
        screen.blit(font.render("Gold: " + str(player_info['p2']['G']),1,"black"),(1500,70))

        #Controls
        screen.blit(UI_IMG, (0,HEIGHT - 100))


class Fader:

    def __init__(self, scenes):
        self.scenes = cycle(scenes)
        self.scene = next(self.scenes)
        self.fading = None
        self.alpha = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)
        self.veil.fill((0, 0, 0))

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self, screen):
        self.scene.draw(screen)
        if self.fading:
            self.veil.set_alpha(self.alpha)
            screen.blit(self.veil, (0, 0))

    def update(self):

        if self.fading == 'OUT':
            self.alpha += 16
            if self.alpha >= 255:
                self.fading = 'IN'
                self.scene = next(self.scenes)
        else:
            self.alpha -= 16
            if self.alpha <= 0:
                self.fading = None

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Age of Pyrus")

TREE_IMG = pygame.image.load('Tree.png').convert_alpha()
STONE_IMG = pygame.image.load('Stone.png').convert_alpha()
GOLD_IMG = pygame.image.load('Gold.png').convert_alpha()
PLAYER1_IMG = pygame.image.load('Player1.png').convert_alpha()
PLAYER2_IMG = pygame.image.load('Player2.png').convert_alpha()
WIZARDTOWER_IMG = pygame.image.load('wizardTower.png').convert_alpha()
FIREBALL_IMG = pygame.image.load('Fireball.png').convert_alpha()
ARCHERTOWER_IMG = pygame.image.load('archerTower.png').convert_alpha()
ARROW_IMG = pygame.image.load('Arrow.png').convert_alpha()
UI_IMG = pygame.image.load('UI.png').convert_alpha()

towerSettings = {
    'WizardTower':{
        'cost':{
            'gold': 0,
            'stone':100,
            'wood': 50
        },
        'health':100,
        'damage':10,
        'speed':1,
        'build_cooldown':10,
        'attack_cooldown': 25,
        'attack_sprite':FIREBALL_IMG,
        'attack_symbol':'FB'
    },
    'ArcherTower':{
        'cost':{
            'gold': 0,
            'stone':50,
            'wood': 150
        },
        'health':100,
        'damage':5,
        'speed':1,
        'build_cooldown':10,
        'attack_cooldown': 15,
        'attack_sprite':ARROW_IMG,
        'attack_symbol':'AW'
    }

}


font_block_info = pygame.font.SysFont("Arial",14, bold = True)
font = pygame.font.SysFont("Arial" , 18 , bold = True)
font_gameOver = pygame.font.SysFont('Arial', 120, bold = True)

player_info = {
    'p1':{
        'health': 100,
        'W': 0,
        'S':0,
        'G':0,
        'cooldown':0,
        'towers':[]
    },
    'p2':{
        'health': 100,
        'W': 0,
        'S':0,
        'G':0,
        'cooldown':0,
        'towers':[]
    }
}

projectileList = []

map = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
]

tc = "X"

def resource_gen (origin, size, letter):

    options = [origin]
    while size > 0 and len(options) > 0:

        new_loc = options.pop(random.randint(0,len(options)-1))
        map[new_loc[0]][new_loc[1]] = letter
        size -= 1

        for i in range(-1,2):
            for j in range(-1,2):
                if (i != 0 and j == 0) or (i == 0 and j != 0):
                    if new_loc[0] + i >= 0 and new_loc[0] + i < len(map) and new_loc[1] + j >= 0 and new_loc[1] + j < len(map[0]):
                        if map[new_loc[0] + i][new_loc[1] + j] == ' ':
                            options.append((new_loc[0] + i,new_loc[1] + j))

tc_loc = (math.floor(len(map) * random.randint(20,80) / 100),math.floor(len(map[0]) * random.randint(20,80) / 100))

for i in range(GOLDPILES):

    # Check for valid placement
    while True:
        dir = random.randint(0,359)
        start = (round((math.cos(math.radians(dir)) * (5 + 3*i)) + tc_loc[0]),round(math.sin(math.radians(dir)) * (5 + 3*i) + tc_loc[1]))
        if start[0] >= 0 and start[0] < len(map) and start[1] >= 0 and start[1] < len(map[0]):
            if map[start[0]][start[1]] == ' ':
                break

    resource_gen(start, GOLDSIZE, "G")

for i in range(STONEPILES):

    # Check for valid placement
    while True:
        dir = random.randint(0,359)
        start = (round((math.cos(math.radians(dir)) * (5 + 3*i)) + tc_loc[0]),round(math.sin(math.radians(dir)) * (5 + 3*i) + tc_loc[1]))
        if start[0] >= 0 and start[0] < len(map) and start[1] >= 0 and start[1] < len(map[0]):
            if map[start[0]][start[1]] == ' ':
                break

    resource_gen(start, STONESIZE, "S")

for i in range(WOODPILES):

    # Check for valid placement
    attempts = 0
    valid_start = False
    while attempts < 10:
        dir = random.randint(0,359)
        start = (round((math.cos(math.radians(dir)) * (5 + 3*i)) + tc_loc[0]),round(math.sin(math.radians(dir)) * (5 + 3*i) + tc_loc[1]))
        if start[0] >= 0 and start[0] < len(map) and start[1] >= 0 and start[1] < len(map[0]):
            if map[start[0]][start[1]] == ' ':
                valid_start = True
                break
        attempts += 1
    if valid_start:
        resource_gen(start, WOODSIZE, "W")


map[tc_loc[0]][tc_loc[1]] = "P1"


# Flip, rotate, extend board (symetry)
temp=[]
for i in range(len(map)):
    temprow = []
    for j in range(len(map[i])):
        if map[len(map)-1-i][len(map)-1-j] == 'P1':
            temprow.append('P2')
        else:
            temprow.append(map[len(map)-1-i][len(map)-1-j])
    temp.append(temprow)

for i in range(len(map)):
    map[i].extend(temp[i])

for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == 'P1':
            player_info['p1']['loc'] = (i,j)
        if map[i][j] == 'P2':
            player_info['p2']['loc'] = (i,j)
        if map[i][j] == 'G':
            map[i][j] = Resource('G',GOLDAMOUNT)
        if map[i][j] == 'S':
            map[i][j] = Resource('S',STONEAMOUNT)
        if map[i][j] == 'W':
            map[i][j] = Resource('W',WOODAMOUNT)

        

def move(player,p_loc,direction):

    if direction == 'UP':
        if p_loc[0] - 1 >= 0:
            if map[p_loc[0] - 1][p_loc[1]] == ' ':
                map[p_loc[0]][p_loc[1]] = ' '
                map[p_loc[0] - 1][p_loc[1]] = player
                return (p_loc[0] - 1,p_loc[1])
        
    
    if direction == 'DOWN':
        if p_loc[0] + 1 < len(map):
            if map[p_loc[0] + 1][p_loc[1]] == ' ':
                map[p_loc[0]][p_loc[1]] = ' '
                map[p_loc[0] + 1][p_loc[1]] = player
                return (p_loc[0] + 1,p_loc[1])

    if direction == 'LEFT':
        if p_loc[1] - 1 >= 0:
            if map[p_loc[0]][p_loc[1] - 1] == ' ':
                map[p_loc[0]][p_loc[1]] = ' '
                map[p_loc[0]][p_loc[1] - 1] = player
                return (p_loc[0],p_loc[1] - 1)

    if direction == 'RIGHT':
        if p_loc[1] + 1 < len(map[0]):
            if map[p_loc[0]][p_loc[1] + 1] == ' ':
                map[p_loc[0]][p_loc[1]] = ' '
                map[p_loc[0]][p_loc[1] + 1] = player
                return (p_loc[0],p_loc[1] + 1)
    
    return (p_loc[0],p_loc[1])

def gather(player):
    for i in range(-1,2):
            for j in range(-1,2):
                if (i != 0 and j == 0) or (i == 0 and j != 0):
                    if player['loc'][0] + i >= 0 and player['loc'][0] + i < len(map) and player['loc'][1] + j >= 0 and player['loc'][1] + j < len(map[0]):
                        if hasattr(map[player['loc'][0] + i][player['loc'][1] + j],'resource'):
                            player[map[player['loc'][0] + i][player['loc'][1] + j].resource] += 1
                            map[player['loc'][0] + i][player['loc'][1] + j].amount -= 1

                            if map[player['loc'][0] + i][player['loc'][1] + j].amount <= 0:
                                map[player['loc'][0] + i][player['loc'][1] + j] = ' '

def build(player,tower,direction):
    if player['W'] >= towerSettings[tower]['cost']['wood'] and player['G'] >= towerSettings[tower]['cost']['gold'] and player['S'] >= towerSettings[tower]['cost']['stone']:
        #place tower
        if direction == 'UP':
            if player['loc'][0] - 1 >= 0:
                if map[player['loc'][0] - 1][player['loc'][1]] == ' ':
                    map[player['loc'][0] - 1][player['loc'][1]] = Tower(tower,towerSettings[tower]['health'],towerSettings[tower]['damage'],towerSettings[tower]['attack_cooldown'],(player['loc'][0] - 1,player['loc'][1]))
                    player['towers'].append(map[player['loc'][0] - 1][player['loc'][1]])
                    player['W'] -= towerSettings[tower]['cost']['wood']
                    player['G'] -= towerSettings[tower]['cost']['gold']
                    player['S'] -= towerSettings[tower]['cost']['stone']
        
        if direction == 'DOWN':
            if player['loc'][0] + 1 < len(map):
                if map[player['loc'][0] + 1][player['loc'][1]] == ' ':
                    map[player['loc'][0] + 1][player['loc'][1]] = Tower(tower,towerSettings[tower]['health'],towerSettings[tower]['damage'],towerSettings[tower]['attack_cooldown'],(player['loc'][0] + 1,player['loc'][1]))
                    player['towers'].append(map[player['loc'][0] + 1][player['loc'][1]])
                    player['W'] -= towerSettings[tower]['cost']['wood']
                    player['G'] -= towerSettings[tower]['cost']['gold']
                    player['S'] -= towerSettings[tower]['cost']['stone']

        if direction == 'LEFT':
            if player['loc'][1] - 1 >= 0:
                if map[player['loc'][0]][player['loc'][1] - 1] == ' ':
                    map[player['loc'][0]][player['loc'][1] - 1] = Tower(tower,towerSettings[tower]['health'],towerSettings[tower]['damage'],towerSettings[tower]['attack_cooldown'],(player['loc'][0],player['loc'][1] - 1))
                    player['towers'].append(map[player['loc'][0]][player['loc'][1] - 1])
                    player['W'] -= towerSettings[tower]['cost']['wood']
                    player['G'] -= towerSettings[tower]['cost']['gold']
                    player['S'] -= towerSettings[tower]['cost']['stone']

        if direction == 'RIGHT':
            if player['loc'][1] + 1 < len(map[0]):
                if map[player['loc'][0]][player['loc'][1] + 1] == ' ':
                    map[player['loc'][0]][player['loc'][1] + 1] = Tower(tower,towerSettings[tower]['health'],towerSettings[tower]['damage'],towerSettings[tower]['attack_cooldown'],(player['loc'][0],player['loc'][1] + 1))
                    player['towers'].append(map[player['loc'][0]][player['loc'][1] + 1])
                    player['W'] -= towerSettings[tower]['cost']['wood']
                    player['G'] -= towerSettings[tower]['cost']['gold']
                    player['S'] -= towerSettings[tower]['cost']['stone']


def tower_attack(player, tower):
    if player == 'P1':
        target = 'p2'
    else:
        target = 'p1'
    
    targetList = []
    targetList.append(player_info[target]['loc'])

    for targetTower in player_info[target]['towers']:
        targetList.append(targetTower.location)

    # Logic for tower types
    if tower.towerType == 'WizardTower':
        closestDistance = math.inf
        for targetLoc in targetList:
            if math.sqrt(((tower.location[0]-targetLoc[0])**2)+((tower.location[1]-targetLoc[1])**2)) < closestDistance:
                closestDistance = math.sqrt(((tower.location[0]-targetLoc[0])**2)+((tower.location[1]-targetLoc[1])**2))
                closestTargetDirection = math.degrees(math.atan2((targetLoc[1] - tower.location[1]),(targetLoc[0] - tower.location[0])))

    elif tower.towerType == 'ArcherTower':
        closestTargetDirection = math.degrees(math.atan2((player_info[target]['loc'][1] - tower.location[1]),(player_info[target]['loc'][0] - tower.location[0])))

    projectileLocation = (tower.location[0] + (math.cos(math.radians(closestTargetDirection)) * towerSettings[tower.towerType]['speed']),tower.location[1] + (math.sin(math.radians(closestTargetDirection)) * towerSettings[tower.towerType]['speed']))
    
    new_projectile = Projectile(towerSettings[tower.towerType]['attack_symbol'],towerSettings[tower.towerType]['attack_sprite'],towerSettings[tower.towerType]['speed'],closestTargetDirection,towerSettings[tower.towerType]['damage'],projectileLocation)
    
    if map[round(projectileLocation[0])][round(projectileLocation[1])] == ' ':
        map[round(projectileLocation[0])][round(projectileLocation[1])] = new_projectile
        projectileList.append(new_projectile)
    else:
        projectile_hit(new_projectile,projectileLocation)
    tower.cooldown = towerSettings[tower.towerType]['attack_cooldown']

def destroy_projectile(projectile):
    map[round(projectile.location[0])][round(projectile.location[1])] = ' '
    if projectile in projectileList: projectileList.remove(projectile)

def projectile_hit(projectile,target_loc):
    # Deal Damage
    if map[round(target_loc[0])][round(target_loc[1])] == 'P1':
        player_info['p1']['health'] -= projectile.damage
    if map[round(target_loc[0])][round(target_loc[1])] == 'P2':
        player_info['p2']['health'] -= projectile.damage
    
    if hasattr(map[round(target_loc[0])][round(target_loc[1])],'resource'):
        map[round(target_loc[0])][round(target_loc[1])].amount -= projectile.damage
        if map[round(target_loc[0])][round(target_loc[1])].amount <= 0:
            map[round(target_loc[0])][round(target_loc[1])] = ' '

    if hasattr(map[round(target_loc[0])][round(target_loc[1])],'towerType'):
        map[round(target_loc[0])][round(target_loc[1])].health -= projectile.damage
        if map[round(target_loc[0])][round(target_loc[1])].health <= 0:
            if map[round(target_loc[0])][round(target_loc[1])] in player_info['p1']['towers']: player_info['p1']['towers'].remove(map[round(target_loc[0])][round(target_loc[1])])
            if map[round(target_loc[0])][round(target_loc[1])] in player_info['p2']['towers']: player_info['p2']['towers'].remove(map[round(target_loc[0])][round(target_loc[1])])
            map[round(target_loc[0])][round(target_loc[1])] = ' '

def update_projectile(projectile):
    new_loc = (projectile.location[0] + (math.cos(math.radians(projectile.direction)) * projectile.speed),projectile.location[1] + (math.sin(math.radians(projectile.direction)) * projectile.speed))
    
    if round(new_loc[0]) >= 0 and round(new_loc[0]) < len(map) and round(new_loc[1]) >= 0 and round(new_loc[1]) < len(map[0]):

        if map[round(new_loc[0])][round(new_loc[1])] == ' ' or map[round(new_loc[0])][round(new_loc[1])] == projectile:
            map[round(projectile.location[0])][round(projectile.location[1])] = ' '
            map[round(new_loc[0])][round(new_loc[1])] = projectile
            projectile.location = new_loc
        
        else:
            if hasattr(map[round(new_loc[0])][round(new_loc[1])],'symbol'):
                destroy_projectile(map[round(new_loc[0])][round(new_loc[1])])
            projectile_hit(projectile,new_loc)

            destroy_projectile(projectile)

    else:
        map[round(projectile.location[0])][round(projectile.location[1])] = ' '
        projectileList.remove(projectile)


running = True
GameActive = True
clock = pygame.time.Clock()
fader = Fader([GameActiveScene(),GameOverScene()])
dt = 0
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
        
    keys = pygame.key.get_pressed()

    # Check if a player won
    if (player_info['p1']['health'] <= 0 or player_info['p2']['health'] <= 0) and GameActive == True:
        GameActive = False
        fader.next()

    if GameActive:
        for projectile in projectileList:
            update_projectile(projectile)

        #build wizard tower
        if keys[pygame.K_c]:
            if keys[pygame.K_w]:
                build(player_info['p1'],'WizardTower','UP')
            elif keys[pygame.K_s]:
                build(player_info['p1'],'WizardTower','DOWN')
            elif keys[pygame.K_a]:
                build(player_info['p1'],'WizardTower','LEFT')
            elif keys[pygame.K_d]:
                build(player_info['p1'],'WizardTower','RIGHT')
        elif keys[pygame.K_v]:
            if keys[pygame.K_w]:
                build(player_info['p1'],'ArcherTower','UP')
            elif keys[pygame.K_s]:
                build(player_info['p1'],'ArcherTower','DOWN')
            elif keys[pygame.K_a]:
                build(player_info['p1'],'ArcherTower','LEFT')
            elif keys[pygame.K_d]:
                build(player_info['p1'],'ArcherTower','RIGHT')

        elif keys[pygame.K_w]:
            player_info['p1']['loc'] = move('P1',player_info['p1']['loc'],'UP')
        elif keys[pygame.K_s]:
            player_info['p1']['loc'] = move('P1',player_info['p1']['loc'],'DOWN')
        elif keys[pygame.K_a]:
            player_info['p1']['loc'] = move('P1',player_info['p1']['loc'],'LEFT')
        elif keys[pygame.K_d]:
            player_info['p1']['loc'] = move('P1',player_info['p1']['loc'],'RIGHT')
        elif keys[pygame.K_SPACE]:
            gather(player_info['p1'])

        for tower in player_info['p1']['towers']:
            if tower.cooldown <= 0:
                tower_attack('P1',tower)
            
            tower.cooldown -= 1
        
        
        #build wizard tower
        if keys[pygame.K_0]:
            if keys[pygame.K_UP]:
                build(player_info['p2'],'WizardTower','UP')
            elif keys[pygame.K_DOWN]:
                build(player_info['p2'],'WizardTower','DOWN')
            elif keys[pygame.K_LEFT]:
                build(player_info['p2'],'WizardTower','LEFT')
            elif keys[pygame.K_RIGHT]:
                build(player_info['p2'],'WizardTower','RIGHT')
        elif keys[pygame.K_9]:
            if keys[pygame.K_UP]:
                build(player_info['p2'],'ArcherTower','UP')
            elif keys[pygame.K_DOWN]:
                build(player_info['p2'],'ArcherTower','DOWN')
            elif keys[pygame.K_LEFT]:
                build(player_info['p2'],'ArcherTower','LEFT')
            elif keys[pygame.K_RIGHT]:
                build(player_info['p2'],'ArcherTower','RIGHT')

        elif keys[pygame.K_UP]:
            player_info['p2']['loc'] = move('P2',player_info['p2']['loc'],'UP')
        elif keys[pygame.K_DOWN]:
            player_info['p2']['loc'] = move('P2',player_info['p2']['loc'],'DOWN')
        elif keys[pygame.K_LEFT]:
            player_info['p2']['loc'] = move('P2',player_info['p2']['loc'],'LEFT')
        elif keys[pygame.K_RIGHT]:
            player_info['p2']['loc'] = move('P2',player_info['p2']['loc'],'RIGHT')
        elif keys[pygame.K_RCTRL]:
            gather(player_info['p2'])

        for tower in player_info['p2']['towers']:
            if tower.cooldown <= 0:
                tower_attack('P2',tower)
            
            tower.cooldown -= 1


    screen.fill((173,255,47))
    fader.draw(screen)
    fader.update()
    dt = clock.tick(10)
    pygame.display.update()