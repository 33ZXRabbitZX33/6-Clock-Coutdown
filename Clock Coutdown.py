import pygame ,sys
import datetime
from math import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((700,700))

pygame.display.set_caption("Countdown")

FPS = 60
fpsClock = pygame.time.Clock()

pygame.mixer.music.load("alarm.wav")

WHITE = (255,255,255)
YELOW = (219, 171, 37)
BLACK = (0,0,0)

but = []
but.append((100,100,50,50))#+
but.append((200,100,50,50))#+
but.append((100,300,50,50))#-
but.append((200,300,50,50))#-
but.append((450,100,150,50))#start
but.append((450,300,150,50))#stop

name_but = []
name_but.append("+")
name_but.append("+")
name_but.append("-")
name_but.append("-") 
name_but.append("Start")
name_but.append("Reset")

class Button():
    def draw(self,color):
        for i in but:
            pygame.draw.rect(DISPLAYSURF,color,i)
      
        for i in range(6):
            font = pygame.font.SysFont("consolas",30)
            text = font.render(name_but[i],True,BLACK)
            text_size = text.get_size()
            DISPLAYSURF.blit(text,(but[i][0]+(but[i][2]-text_size[0])/2,but[i][1]+(but[i][3]-text_size[1])/2))


turn = False
now = datetime.datetime.now().timestamp()

class Clock():
    def __init__(self):
        self.total = 0
        self.tinow = 0
        self.mins = self.total // 60 
        self.secs = (self.total + 60) % 60
    def draw(self):
        global now,turn
        now2 = datetime.datetime.now().timestamp()
        if now <= now2:
            now += 1
            self.tinow += -1
        if turn == True:
            self.total += self.tinow
            self.tinow = 0
        else:
            self.tinow = 0

        self.mins = self.total // 60 
        self.secs = (self.total ) % 60

        timenow = str(self.mins)+"  :  "+str(self.secs)    
        text_time = pygame.font.SysFont("consolas",30).render(timenow,True,YELOW)
        DISPLAYSURF.blit(text_time,(120,200))

    
class clockcon():
    def __init__(self):
        self.point = (350,450)
        self.radius = 90
    def draw(self,color,secs,mins):
        pygame.draw.circle(DISPLAYSURF,color,self.point,self.radius)
        pygame.draw.line(DISPLAYSURF,BLACK,self.point,(350+self.radius*sin((pi*secs)/30),450-self.radius*cos((pi*secs)/30)))
        pygame.draw.line(DISPLAYSURF,BLACK,self.point,(350+self.radius*sin((pi*mins)/30),450-self.radius*cos((pi*mins)/30)))

stw = 1
bar_on = True
class LoadBar():
    def __init__(self):
        self.coor = [150,600,400,50]
        self.long = 400
        self.percent = 0
    def draw(self,color,total):
        global stw
        pygame.draw.rect(DISPLAYSURF,color,self.coor)

        
        self.percent = (total/stw)

        log = int(self.long*self.percent)

        if log > 400:
            log = 400
        elif log <=0:
            log = 1
        else:
            pass

        sur = pygame.Surface((log,50))
        sur.fill((255,0,0))
        DISPLAYSURF.blit(sur,(150,600))



def GamePlay(bt,cl,cc,bar):
    global turn,stw,bar_on
    color = WHITE
    but2 =[]
    for i in but:
        but2.append( pygame.Rect(i))
    while True:  
        mouse_xy = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.pause()
                if event.button == 1:
                    if but2[0].collidepoint(mouse_xy):                 
                        cl.total += 60
                    if but2[1].collidepoint(mouse_xy):
                        cl.total += 1
                    if but2[2].collidepoint(mouse_xy):
                        cl.total -= 60
                    if but2[3].collidepoint(mouse_xy):
                        cl.total -= 1    
                        
                    if but2[4].collidepoint(mouse_xy):
                        if not turn:
                            if bar_on == True:
                                stw = cl.total
                                bar_on = False
                            else:
                                pass
                            turn = not turn
                            name_but[4] = "Stop"
                        else:
                            turn = not turn
                            name_but[4] = "Start"
                    if but2[5].collidepoint(mouse_xy):
                        turn = not turn
                        name_but[4] = "Start"
                        cl.total = 0
                        bar_on = True
                        stw = 1

        if cl.total == 0:
            turn = False
            name_but[4] = "Start"
            bar_on = True
            stw = 1
            pygame.mixer.music.play()

        if cl.total <= 0:
            cl.total =0

        DISPLAYSURF.fill((97, 99, 133))

        cl.draw()
    
        cc.draw(color,cl.secs,cl.mins)
        bt.draw(color)

        bar.draw(color,cl.total)
  
        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    bt = Button()
    cl = Clock()
    cc = clockcon()
    bar = LoadBar()
    while True:
        GamePlay(bt,cl,cc,bar)


if __name__ == "__main__":
    main()
