#! /usr/bin/env python
import sys , os , math , random
import pygame
from pygame. locals import *
from random import randint

pygame.init();

# Settings
base_path, filename = os.path.split(os.path.abspath(__file__))

# Classe Minion - Personagem minion
class Minion(pygame.sprite.Sprite):
    def __init__ (self, position):
        self.image = pygame.image.load( base_path + '/img/minion.png' )
        self.image.set_clip(pygame.Rect(0, 0, c_width, c_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = position


# Classe Minion - Personagem minion
class Box(pygame.sprite.Sprite):
    def __init__ (self, position):
        self.image = pygame.image.load( base_path + '/img/box.jpg' )
        self.image.set_clip(pygame.Rect(0, 0, 48, 48))
        self.rect = self.image.get_rect()
        self.rect.topleft = position


# Musica de fundo
#pygame.mixer.music.load( base_path + '/sound/music.m4a' )
#pygame.mixer.music.play(0)

# Equations
equations = [
    {"label": "1 + 1", "result": 2},
    {"label": "2 x 5", "result": 10},
    {"label": "3 x 6", "result": 18},
    {"label": "4 x 5", "result": 20}
]

# texto do box
box_font = pygame.font.SysFont("Comic Sans MS", 23)

box_list = [
    {"name": "box1", "position": 25, "value": randint(0, 99), "element": None},
    {"name": "box2", "position": 98, "value": randint(0, 99), "element": None},
    {"name": "box3", "position": 173, "value": randint(0, 99), "element": None},
    {"name": "box4", "position": 246, "value": randint(0, 99), "element": None}
]

def start():
    print("Starting...")

    global move
    global filename
    global s_width
    global s_height
    global c_width
    global c_height
    global title_font
    global title_label
    global box_list
    global eq_key
    global res_key
    global colisao
    global v_ini_pos
    global h_ini_pos

    # Screen dimensions
    s_width = 320
    s_height = 500

    # Character dimensions
    c_width = 30
    c_height = 43

    # Controle de movimento horizontal do personagem
    move = 0 #(0 => stop, 1 => left, 2 => right)

    v_ini_pos = 0 # Initial vertical position
    h_ini_pos = randint(0, (s_width - c_width)) #Initial horizontal position

    colisao = False

    # Sroteio da equacao
    eq_key = randint(0, (len(equations)-1))
    
    print(equations[eq_key]["label"])
    print(equations[eq_key]["result"])  

    # Atualiza o label do titulo
    title_font = pygame.font.SysFont("Comic Sans MS", 50)
    title_label = title_font.render(equations[eq_key]["label"], 1, (0,0,0))

    # Box que tera a resposta
    res_key = randint(0, (len(box_list)-1))

    # Sorteando os valores do box
    cur_box_key = 0        
    for box in box_list:
        if cur_box_key == res_key:
            box_list[cur_box_key]["value"] = equations[eq_key]["result"]
        else:
            box_list[cur_box_key]["value"] = randint(0, 99)
        cur_box_key = cur_box_key+1

# Staring the game
start()
running = 1
screen = pygame.display.set_mode((s_width, s_height))

# palco
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    # Tela
    screen.fill((155, 227, 251))
    screen.blit(title_label, (100, 0))

    # desenho do personagem na tela
    player = Minion((h_ini_pos, v_ini_pos))
    screen.blit(player.image, player.rect)

    for box in box_list:
        box["element"] = Box((box["position"], (s_height - (48 + 25) ))) # current box
        screen.blit(box["element"].image, box["element"].rect)
        
        # labels dos box
        box_label = box_font.render(str(box["value"]), 48, (255,255,255))
        screen.blit(box_label, ((box["position"] + 11), 435))

        if(player.rect.colliderect(box["element"].rect)):
            if(box["value"] == equations[eq_key]["result"]):
                if(colisao == False):
                    print("Voce acertou!")
            else:
                if(colisao == False):
                    print("Voce errou!")

            if(colisao == False):
                print("Colidiu com: " + box["name"])                
                colisao = True
                start()

    if(not colisao):
        v_ini_pos = v_ini_pos + 0.22

    # Controle do personagem:
    if move == 1:
        h_ini_pos-=0.25
    elif move == 2:
        h_ini_pos+=0.25
    else:
        h_ini_pos = h_ini_pos

    if event.type == KEYDOWN:
        if (event.key == K_LEFT):
            move = 1
        elif (event.key == K_RIGHT):
            move = 2
    elif event.type == KEYUP:
        move = 0

    chao = pygame.draw.rect(screen, (98, 168, 80), (0,475,s_width,25))
    # Atualizacao da tela
    pygame.display.update()