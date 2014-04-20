#! /usr/bin/env python
import sys , os , math , random
import pygame
from pygame. locals import *
from random import randint
import equations

pygame.init();

# Settings
base_path, filename = os.path.split(os.path.abspath(__file__))

# Equations object
eq = equations.Equations()
equations = eq.equations_list 
#eq.run()

# Classe Minion - Personagem minion
class Minion(pygame.sprite.Sprite):
    def __init__ (self, position):
        self.image = pygame.image.load( base_path + '/img/minion.png' )
        self.image.set_clip(pygame.Rect(0, 0, c_width, c_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = position


# Classe Box - Caixas de resposta
class Box(pygame.sprite.Sprite):
    def __init__ (self, position):
        self.image = pygame.image.load( base_path + '/img/green-box.png' )
        self.image.set_clip(pygame.Rect(0, 0, 53, 53))
        self.rect = self.image.get_rect()
        self.rect.topleft = position


# Musica de fundo
#pygame.mixer.music.load( base_path + '/sound/music.m4a' )
#pygame.mixer.music.play(0)

# texto do box
box_font = pygame.font.SysFont("Comic Sans MS", 23)

def start():
    print("Starting...")

    global eq
    global move
    global filename
    global s_width
    global s_height
    global c_width
    global c_height
    global title_font
    global title_label
    global box_list
    global box_font
    global eq_key
    global res_key
    global colisao
    global v_ini_pos
    global h_ini_pos
    global buffer_equations

    # Screen dimensions
    s_width = 320
    s_height = 500

    # Character dimensions
    c_width = 30
    c_height = 43

    # Atualizando a lista
    eq.equations_update()
    buffer_equations = eq.equations
    #print(str(current_equation["options"]))
    
    '''
    [
        {'options': [43,35,17,69,97,97], 'result': 35, 'label': '7x5'},
        {'options': [34,38,18,77,89,12], 'result': 18, 'label': '3x6'},
        {'options': [10,5,27,73,55,48], 'result': 10, 'label': '2x5'}
    ]
    '''

    box_list = [
        {"name": "box1", "position_x": 0, "position_y": (s_height - (53 + 25)), "value": randint(0, 99), "element": None},
        {"name": "box2", "position_x": 53, "position_y": (s_height - (53 + 25)), "value": randint(0, 99), "element": None},
        {"name": "box3", "position_x": 106, "position_y": (s_height - (53 + 25)), "value": randint(0, 99), "element": None},
        {"name": "box3", "position_x": 159, "position_y": (s_height - (53 + 25)), "value": randint(0, 99), "element": None},
        {"name": "box4", "position_x": 212, "position_y": (s_height - (53 + 25)), "value": randint(0, 99), "element": None},
        {"name": "box4", "position_x": 265, "position_y": (s_height - (53 + 25)), "value": randint(0, 99), "element": None}
    ]

    # Controle de movimento horizontal do personagem
    move = 0 #(0 => stop, 1 => left, 2 => right)

    v_ini_pos = 0 # Initial vertical position
    h_ini_pos = randint(0, (s_width - c_width)) #Initial horizontal position

    colisao = False

    # Sroteio da equacao
    eq_key = randint(0, (len(equations)-1))
    
    #print(equations[eq_key]["label"])
    #print(equations[eq_key]["result"])  

    # Atualiza o label do titulo
    title_font = pygame.font.SysFont("Comic Sans MS", 50)
    title_label = title_font.render(buffer_equations[0]["label"], 1, (0,0,0))

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

    '''
    [
        {'options': [43,35,17,69,97,97], 'result': 35, 'label': '7x5'},
        {'options': [34,38,18,77,89,12], 'result': 18, 'label': '3x6'},
        {'options': [10,5,27,73,55,48], 'result': 10, 'label': '2x5'}
    ]
    '''

    aux = 0
    for current_equation in buffer_equations:
        option_x = 0
        box_height = 53
        
        for option in current_equation["options"]:
            option_y = (s_height - ((len(buffer_equations) - aux) * box_height) - 25) # 2 vezes para ficar na linha acima
            box = Box((option_x, option_y)) # current box
            screen.blit(box.image, box.rect)
            
            # labels dos box
            box_label = box_font.render(str(option), box_height, (255,255,255))
            screen.blit(box_label, ((option_x + 11), (option_y + 12)  ))

            if(player.rect.colliderect(box.rect)):
                if(option == current_equation["result"]):
                    if(colisao == False):
                        print("Voce acertou!")
                else:
                    if(colisao == False):
                        print("Voce errou!")

                if(colisao == False):
                    print("Colidiu com: " + str(option))                
                    colisao = True
                    start()
            option_x = option_x + box.rect.width
        aux = aux + 1       

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