import pygame
from pygame.locals import *
from sys import exit
import random



c_cyan=  {"top"  : (0,  240,240),
          "up"   : (179,251,251),
          "side" : (0,  216,216),
          "down" : (0,  120,120) }
c_blue=  {"top"  : (0,  0  ,240),
          "up"   : (179,179,251),
          "side" : (0,  0  ,216),
          "down" : (0,  0  ,120) }
c_yellow={"top"  : (240,240,  0),
          "up"   : (251,251,179),
          "side" : (216,216,0  ),
          "down" : (120,120,0  ) }
c_orange={"top"  : (240,160,0  ),
          "up"   : (240,227,179),
          "side" : (216,144,0  ),
          "down" : (120,80 ,0  ) }
c_green={"top"  : (0  ,240,0  ),
          "up"   : (179,251,179),
          "side" : (0  ,216,0  ),
          "down" : (0  ,120,0  ) }
c_magenta={"top"  : (160,0  ,240),
           "up"   : (0xe3,0xb3,0xfb),
           "side" : (0x90,0   ,0xd8),
           "down" : (0x50,0,   0x78) }
c_red=    {"top"  : (0xf0,0   ,0   ),
           "up"   : (0xfb,0xb3,0xb3),
           "side" : (0xd8,0   ,0   ),
           "down" : (0x78,0   ,0   ) }
c_white=  {"top"  : (0xfb,0xfb,0xfb),
           "up"   : (0xff,0xff,0xff),
           "side" : (0xe8,0xe8,0xe8),
           "down" : (0x98,0x98,0x98)}

class square:
    def __init__(self,col=c_cyan,is_on=False):
        self.col=col
        self.is_on=is_on        
        
    def draw(self,size,x,y):
        border=size/8
        center=size-border
        screen.fill(self.col["side"],(x,y,size,size))
        screen.fill(self.col["top"],(x+border,y+border,size-2*border,size-2*border))
        for i in range(border):
            pygame.draw.line(screen,self.col["up"],(x+i,y+i),(x+size-i-1,y+i))
        for i in range(border):
            pygame.draw.line(screen,self.col["down"],\
                            (x+border-i,y+size-border+i),(x+size-border+i,y+size-border+i))
        pygame.draw.rect(screen,(0,0,0),(x,y,size,size),1)
        
class field:
    def __init__(self,size_x,size_y,coord=(0,0),psize=(320,640),pxcoord=(2,2)):
        self.size_x=size_x
        self.size_y=size_y
        self.coord=coord
        self.psize=psize
        self.pxcoord=pxcoord
        self.tab=[]
        self.settled=False
        for i in range(size_x):
            clmn=[]
            for j in range(size_y):
                clmn.append(square())
            self.tab.append(clmn)
            
    def erase_lines(self):
        lista_l=[]
        for j in range(self.size_y):                    
            k=0
            for i in range(self.size_x):
                if self.tab[i][j].is_on : k+=1
            if k==self.size_x:lista_l.append(j)

        if len(lista_l)==0 : return len(lista_l)
        lines_sound.play()
        for i in range(4):
            for linie in lista_l:
                wl=white_line()
                wl.coord=(0,linie)
                wl.draw(f)
            pygame.display.update()
            pygame.time.wait(1000/vnorm/8)
            self.draw()
            pygame.display.update()
            pygame.time.wait(1000/vnorm/8)
        
        for linie in lista_l:
            for i in range(self.size_x):
                for j in range(linie,0,-1):
                    self.tab[i][j].is_on=self.tab[i][j-1].is_on
                    self.tab[i][j].col=self.tab[i][j-1].col

        return len(lista_l)


    def draw(self,f=None):
        if f==None :
            xs=self.psize[0]/self.size_x
            ys=self.psize[1]/self.size_y
        else :
            xs=f.psize[0]/f.size_x
            ys=f.psize[1]/f.size_y
            
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.tab[i][j].is_on :
                    self.tab[i][j].draw(xs, self.pxcoord[0]+self.coord[0]*xs+i*xs,
                                            self.pxcoord[1]+self.coord[1]*ys+j*ys)

    def draw_anywhere(self,x,y,f=None):
        if f==None :
            xs=self.psize[0]/self.size_x
            ys=self.psize[1]/self.size_y
        else :
            xs=f.psize[0]/f.size_x
            ys=f.psize[1]/f.size_y

        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.tab[i][j].is_on :
                    self.tab[i][j].draw(xs, x+i*xs, y+j*ys)

    def is_over(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.tab[i][j].is_on and j+self.coord[1]==0 :
                    return True
        return False
    
    def test_colis(self,f):
        colis=False
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.tab[i][j].is_on and \
                    (self.coord[0]+i<0 or \
                    self.coord[0]+i>f.size_x-1 or \
                    self.coord[1]+j<0 or \
                    self.coord[1]+j>f.size_y-1):
                        colis=True;break
                elif self.tab[i][j].is_on and \
                   f.tab[int(self.coord[0])+i][int(self.coord[1])+j].is_on:
                       colis=True;break
        return colis

    def rotate(self,f):
        global rotated
        temp=field(self.size_x,self.size_y,self.coord)
        x0=self.size_x/2.0
        y0=self.size_y/2.0
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.tab[i][j].is_on:
                    x1=i+0.5
                    y1=j+0.5
                    x2=-(y1-y0)+x0   
                    y2= (x1-x0)+y0   
                    temp.tab[int(x2)][int(y2)].is_on=True
        colis=temp.test_colis(f)
        if not colis:
            rotated=True
            for i in range(self.size_x):
                for j in range(self.size_y):
                    c=self.tab[i][j].col
                    self.tab[i][j]=temp.tab[i][j]
                    self.tab[i][j].col=c

    def settle(self,f):
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.tab[i][j].is_on:
                    f.tab[self.coord[0]+i][self.coord[1]+j].col=self.tab[i][j].col
                    f.tab[self.coord[0]+i][self.coord[1]+j].is_on=True
        self.settled=True

    def move_down(self,f):
        self.coord[1]+=1
        if self.test_colis(f):
            self.coord[1]-=1
            self.settle(f)

    def drop(self,f):
        global dropped
        while True:
            self.coord[1]+=1
            if self.test_colis(f):
                self.coord[1]-=1
                break
        dropped=True

    def move_left(self,f):
        self.coord[0]-=1
        if self.test_colis(f): self.coord[0]+=1

    def move_right(self,f):
        self.coord[0]+=1
        if self.test_colis(f): self.coord[0]-=1

        
        
class j_tetra(field):
    def __init__(self):
        field.__init__(self,3,3,[3,0])
        for i in range(3):
            for j in range(3):
                self.tab[i][j].col=c_blue
        self.tab[0][0].is_on=True
        self.tab[0][1].is_on=True
        self.tab[1][1].is_on=True
        self.tab[2][1].is_on=True

class l_tetra(field):
    def __init__(self):
        field.__init__(self,3,3,[3,0])
        for i in range(3):
            for j in range(3):
                self.tab[i][j].col=c_orange
        self.tab[0][1].is_on=True
        self.tab[1][1].is_on=True
        self.tab[2][1].is_on=True
        self.tab[2][0].is_on=True

class s_tetra(field):
    def __init__(self):
        field.__init__(self,3,3,[3,0])
        for i in range(3):
            for j in range(3):
                self.tab[i][j].col=c_green
        self.tab[0][1].is_on=True
        self.tab[1][1].is_on=True
        self.tab[1][0].is_on=True
        self.tab[2][0].is_on=True

class t_tetra(field):
    def __init__(self):
        field.__init__(self,3,3,[3,0])
        for i in range(3):
            for j in range(3):
                self.tab[i][j].col=c_magenta
        self.tab[0][1].is_on=True
        self.tab[1][1].is_on=True
        self.tab[1][0].is_on=True
        self.tab[2][1].is_on=True

class z_tetra(field):
    def __init__(self):
        field.__init__(self,3,3,[3,0])
        for i in range(3):
            for j in range(3):
                self.tab[i][j].col=c_red
        self.tab[0][0].is_on=True
        self.tab[1][1].is_on=True
        self.tab[1][0].is_on=True
        self.tab[2][1].is_on=True

class i_tetra(field):
    def __init__(self):
        field.__init__(self,4,4,[3,-1])
        for i in range(4):
            for j in range(4):
                self.tab[i][j].col=c_cyan
        self.tab[0][1].is_on=True
        self.tab[1][1].is_on=True
        self.tab[2][1].is_on=True
        self.tab[3][1].is_on=True

class o_tetra(field):
    def __init__(self):
        field.__init__(self,2,2,[4,0])
        for i in range(2):
            for j in range(2):
                self.tab[i][j].col=c_yellow
        self.tab[0][1].is_on=True
        self.tab[1][0].is_on=True
        self.tab[1][1].is_on=True
        self.tab[0][0].is_on=True

class white_line(field):
    def __init__(self):
        field.__init__(self,10,1)
        for i in range(10):
            self.tab[i][0].col=c_white
            self.tab[i][0].is_on=True

def draw_screen():
    screen.fill((128,128,128))
    screen.fill((192,192,192),(field_x_size+border_size*2,0,panel_x_size,field_y_size+2*border_size))
    screen.blit(title_surf,(field_x_size+(panel_x_size-title_surf.get_width())/2,256))
    lines_surf=score_font.render("Lines : " + str(line_count),True,(56,56,56))
    level_surf=score_font.render("Level : " + str(level),True,(56,56,56))
    score_surf=score_font.render("Score : " + str(score),True,(56,56,56))
    hs_surf=score_font.render("Highscores:", True,hs_col)
    screen.blit(lines_surf,(field_x_size+30,348))
    screen.blit(level_surf,(field_x_size+30,396))
    screen.blit(score_surf,(field_x_size+30,444))
    screen.blit(hs_surf,(field_x_size+(panel_x_size-hs_surf.get_width())/2,600))
    for i in range(len(highscores)) :
        hs_surf=hs_font.render(str(i+1)+'. '+str(highscores[i]),True,hs_col)
        screen.blit(hs_surf,(field_x_size+(panel_x_size-hs_surf.get_width())/2,
                             656+i*(hs_surf.get_height())))
    pygame.draw.rect(screen,(64,64,64),(0,0,field_x_size+border_size*2-1,field_y_size+border_size*2-1),2)
    screen.fill((128,128,128),(field_x_size+border_size*2+24,border_size*2+24,192,192))            #preview area
    pygame.draw.rect(screen,(64,64,64),(field_x_size+border_size*2+24,border_size*2+24,192,192),2) #
    if pause : screen.blit(pause_surf,
                          (border_size+(field_x_size-pause_surf.get_width())/2,\
                           border_size+(field_y_size-pause_surf.get_height())/2))

def init_game():
    global vnorm, v, line_count, piece_queue,level,score,clock
    f=field(10,20,psize=(field_x_size,field_y_size),pxcoord=(border_size,border_size))
    piece_queue=[]
    piece_queue.append(ptype_array[random.randint(0,len(ptype_array)-1)]())
    piece_queue.append(ptype_array[random.randint(0,len(ptype_array)-1)]())
    p=piece_queue[0]
    clock=pygame.time.Clock()
    vnorm=2
    v=vnorm
    line_count=0
    level=1
    score=0
    if music_on : pygame.mixer.music.play(-1)

    return f,p

def myexit():
    hsfile=open("hs.txt","w")
    for hs in highscores:
        hsfile.write(str(hs)+'\n')
    exit()

def endgame():
    global gameover,newgame,delta
    gameover=True
    newgame=False
    delta=0
    for i in range(len(highscores)):
        if score>highscores[i]:
            highscores.insert(i,score)
            del highscores[-1]
            break
    pygame.mixer.music.stop()
    
    
clock=pygame.time.Clock()
delta=0

vdrop=15
line_count=0
v=vnorm=2
level=1
score=0
piece_queue=[]
field_x_size=400; field_y_size=800
border_size=2
panel_x_size=240
gameover=False
pause=False
newgame=False
music_on=True
menucol=(120,120,56)
menucol_act=(170,170,140)
menucol_new=menucol
menucol_quit=menucol
menucol_pause=menucol
hs_col=(120,56,56)
highscores=[]
hsfile=open("hs.txt","r")
for line in hsfile:
    highscores.append(int(line))


piece_queue=[]
ptype_array=[i_tetra,j_tetra,l_tetra,o_tetra,s_tetra,t_tetra,z_tetra]

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.music.load("aceman_-_my_first_console.xm")
drop_sound = pygame.mixer.Sound("drop.wav")
dropped=False
rotate_sound = pygame.mixer.Sound("rotate.wav")
rotated=False
lines_sound = pygame.mixer.Sound("lines.wav")
lines=False
drop_sound.set_volume(0.7)
rotate_sound.set_volume(0.7)
lines_sound.set_volume(0.7)
                                  
pygame.key.set_repeat(1000/vnorm/2,1000/vnorm/8)
screen = pygame.display.set_mode((field_x_size+panel_x_size, field_y_size+2*border_size), 0, 32)
pygame.display.set_caption("Tetris")
font=pygame.font.Font("5thGrader-Bold.ttf",60)
score_font=pygame.font.Font("5thGrader-Bold.ttf",36)
hs_font=pygame.font.Font("5thGrader-Bold.ttf",24)
title_surf=font.render("Tetris",True,(56,56,56))
pause_surf=font.render("Pause",True,(56,56,56))
new_surf=score_font.render("New",True,menucol_new)
quit_surf=score_font.render("Quit",True,menucol_quit)
mpause_surf=score_font.render("Pause",True,menucol_pause)

while True:
    
    while not newgame:
        for event in pygame.event.get():
            if event.type == QUIT:
                myexit()
            if event.type == KEYDOWN:
                if event.key == K_n:
                    newgame=True
                    gameover=False
                if event.key == K_q:
                    myexit()
            if event.type == MOUSEBUTTONDOWN:
                if menucol_quit==menucol_act : myexit()
                if menucol_new==menucol_act :
                    newgame=True
                    gameover=False
        
        mx,my=pygame.mouse.get_pos()
        if mx>field_x_size+30 and mx<field_x_size+30+new_surf.get_width() and \
           my>524 and my<524+new_surf.get_height() :
               menucol_new=menucol_act
        else:
               menucol_new=menucol
        if mx>new_surf.get_width()+field_x_size+64 and \
           mx<quit_surf.get_width()+field_x_size+64+new_surf.get_width() and \
           my>524 and my<524+quit_surf.get_height() :
               menucol_quit=menucol_act
        else:
               menucol_quit=menucol

        new_surf=score_font.render("New",True,menucol_new)
        quit_surf=score_font.render("Quit",True,menucol_quit)

        draw_screen()
        screen.blit(new_surf,(field_x_size+30,524))
        screen.blit(quit_surf,(new_surf.get_width()+field_x_size+64,524))
        clock.tick(30)
        pygame.display.update()

    f,p=init_game()
    while not gameover:

        for event in pygame.event.get():
            if event.type == QUIT:
                myexit()
            if not pause:
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        p.rotate(f)
                    elif event.key == K_LEFT:
                        p.move_left(f)
                    elif event.key == K_RIGHT:
                        p.move_right(f)
                    elif event.key == K_DOWN:
                        v=vdrop
                    elif event.key == K_p:
                        pause = not pause
                    elif event.key == K_q:
                        endgame()
                    elif event.key == K_SPACE:
                        p.drop(f)
                if event.type == KEYUP:
                    if event.key == K_DOWN:
                        v=vnorm
            else :
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        pause = not pause
                        clock=pygame.time.Clock()
            if event.type == KEYDOWN:
                if event.key == K_m:
                        if music_on == True : pygame.mixer.music.stop(); music_on = False
                        else : pygame.mixer.music.play(-1); music_on = True
            if event.type == MOUSEBUTTONDOWN:
                if menucol_quit==menucol_act :
                    endgame()
                    pause=False
                if menucol_pause==menucol_act :
                    pause = not pause

        mx,my=pygame.mouse.get_pos()
        if mx>field_x_size+30 and mx<field_x_size+30+mpause_surf.get_width() and \
           my>524 and my<524+mpause_surf.get_height() :
               menucol_pause=menucol_act
        else:
               menucol_pause=menucol
        if mx>mpause_surf.get_width()+field_x_size+64 and \
           mx<quit_surf.get_width()+field_x_size+64+mpause_surf.get_width() and \
           my>524 and my<524+quit_surf.get_height() :
               menucol_quit=menucol_act
        else:
               menucol_quit=menucol

        mpause_surf=score_font.render("Pause",True,menucol_pause)
        quit_surf=score_font.render("Quit",True,menucol_quit)

        draw_screen()
        screen.blit(mpause_surf,(field_x_size+30,524))
        screen.blit(quit_surf,(mpause_surf.get_width()+field_x_size+64,524))

        if not pause:
            if delta*v>=1000.0:
                p.move_down(f)
                delta=0

            p.draw(f)
            piece_queue[1].draw_anywhere(field_x_size+48,96,f)
            f.draw()
            if dropped : drop_sound.play(); dropped=False
            if rotated : rotate_sound.play(); rotated=False
            if lines :  lines_sound.play(); lines=False
            delta+=clock.tick(30)

            if p.settled :
                erased=f.erase_lines()
                if erased:
                    line_count+=erased
                    score+=level*(erased*2-1)*10
                    l=level
                    level=line_count/10+1
                    if level>14 : level=14
                    v=vnorm=level+1
                    if l<>level : pygame.key.set_repeat(1000/vnorm/2,1000/vnorm/8)

                del piece_queue[0]
                piece_queue.append(ptype_array[random.randint(0,len(ptype_array)-1)]())
                p=piece_queue[0]
                if p.test_colis(f) : endgame()
                delta=0


        pygame.display.update()
