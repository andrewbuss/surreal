

import pygame, sys
pygame.init()
import macromap, menu
import pygame.gfxdraw
from datetime import datetime
from collections import deque

PERIM_WATER = 1
PERIM_METAL = 2
PERIM_TREES = 4
xres = 1280
yres = 720
mapsize = 1024
mapres = 1024
p1x = 0
p1y = 0
p2x = 0
p2y = 0
cx = 0
cy = 0
currentmenu = None
mapsurf = pygame.Surface((mapres,mapres))
map = macromap.map(mapres,mapsurf.subsurface(mapsurf.get_rect()), True)
font = pygame.font.SysFont("microsoftyahei",12)
fps = deque()

def rescale():
    global scaledmapsurf
    scaledmapsurf = pygame.transform.smoothscale(mapsurf, (mapsize,mapsize))


print "Rendering map"
map.render()
print "Scaling map"
rescale()

def movep(p,dx,dy):
    global p1x, p2x, p1y, p2y, cx, cy
    move = True
    if p==1:
        if p1x+dx>=xres/2:
            cx+=dx
            move=False
        elif p1x+dx<-xres/2:
            cx+=dx
            move=False
        elif p1y+dy>yres/2:
            cy+=dy
            move=False
        elif p1y+dy<-yres/2:
            cy+=dy
            move=False
        if move:
            if p1x+dx<=p2x: p1x+=dx
            if p1y+dy>=p2y: p1y+=dy
    else:
        if p2x+dx>=xres/2:
            cx+=dx
            move=False
        elif p2x+dx<-xres/2:
            cx+=dx
            move=False
        elif p2y+dy>yres/2:
            cy+=dy
            move=False
        elif p2y+dy<=-yres/2:
            cy+=dy
            move=False
        if move:
            if p2x+dx>=p1x: p2x+=dx
            if p2y+dy<=p1y: p2y+=dy

screen = pygame.display.set_mode((xres,yres),pygame.DOUBLEBUF|pygame.HWSURFACE)
while 1:
    lst = datetime.now()
    debuginfo = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHTBRACKET:
                mapsize*=2
                cx*=2
                cy*=2
                rescale()
            elif event.key == pygame.K_LEFTBRACKET:
                if mapsize>xres/8: 
                    mapsize/=2
                    cx/=2
                    cy/=2
                    rescale()
            elif event.key == pygame.K_ESCAPE: sys.exit()
            elif event.key == pygame.K_e:
                currentmenu = menu.menu(screen.subsurface(pygame.Rect(0,0,300,yres)), "Build", ["Item A", "Item B", "Item C"])
    pressed = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    if len(fps)>0: v = int(150.0/fps[0])
    else: v=1
    if mods&pygame.KMOD_LSHIFT: v*=2
    if mods&pygame.KMOD_RSHIFT: v*=2
    if mods&pygame.KMOD_LCTRL:
        p2x = p1x
        p2y = p1y
    if mods&pygame.KMOD_RCTRL:
        p1x = p2x
        p1y = p2y
    if pressed[pygame.K_w]: movep(1,0,v)
    if pressed[pygame.K_a]: movep(1,-v,0)
    if pressed[pygame.K_s]: movep(1,0,-v)
    if pressed[pygame.K_d]: movep(1,v,0)
    if pressed[pygame.K_p]: movep(2,0,v)
    if pressed[pygame.K_l]: movep(2,-v,0)
    if pressed[pygame.K_SEMICOLON]: movep(2,0,-v)
    if pressed[pygame.K_QUOTE]: movep(2,v,0)
    screen.fill(pygame.Color(0,0,0,0))
    vcx = -cx+xres/2
    vcy = mapsize+cy+yres/2
    x = vcx%(mapsize*2)-mapsize*2 
    tiles = 0
    while x<xres:
        y = vcy%(mapsize*2)-mapsize*2
        while y<yres:
            screen.blit(scaledmapsurf, (x,y))
            screen.blit(scaledmapsurf, (x+mapsize,y))
            screen.blit(scaledmapsurf, (x,y+mapsize))
            screen.blit(scaledmapsurf, (x+mapsize,y+mapsize))
            y += mapsize*2
            tiles+=4
        x += mapsize*2
    cs = 4
    pygame.gfxdraw.vline(screen,p1x+xres/2,-p1y+yres/2,-p2y+yres/2,(255,128,128))
    pygame.gfxdraw.hline(screen,p1x+xres/2,p2x+xres/2,-p1y+yres/2,(255,128,128))
    pygame.gfxdraw.vline(screen,p2x+xres/2,-p2y+yres/2,-p1y+yres/2,(128,128,255))
    pygame.gfxdraw.hline(screen,p2x+xres/2,p1x+xres/2,-p2y+yres/2,(128,128,255))
    pygame.gfxdraw.aatrigon(screen,xres/2+p1x-cs-1, yres/2+cs-p1y+1, xres/2-cs+p1x-1,yres/2-cs-p1y-1,xres/2+cs+p1x+1,yres/2-cs-p1y-1,(0,0,0))
    pygame.gfxdraw.filled_trigon(screen,xres/2+p1x-cs, yres/2+cs-p1y, xres/2-cs+p1x,yres/2-cs-p1y,xres/2+cs+p1x,yres/2-cs-p1y,(255,0,0))
    pygame.gfxdraw.aatrigon(screen,xres/2+p2x-cs-1, yres/2+cs-p2y+1, xres/2+cs+p2x+1,yres/2+cs-p2y+1,xres/2+cs+p2x+1,yres/2-cs-p2y-1,(0,0,0))
    pygame.gfxdraw.filled_trigon(screen,xres/2+p2x-cs, yres/2+cs-p2y, xres/2+cs+p2x,yres/2+cs-p2y,xres/2+cs+p2x,yres/2-cs-p2y,(0,0,255))
    if len(fps) >= 200:
        for i in range(200):
            screen.set_at((x,yres-fps[i]/10-5),pygame.Color(255,0,0,255))
            x+=1
    debuginfo.append("Camera center: " + str((cx,cy)))
    debuginfo.append("Pointer 1: " + str((p1x,p1y)))
    debuginfo.append("Pointer 2: " + str((p2x,p2y)))
    debuginfo.append("Tiles rendered: " + str(tiles))
    if len(fps)>200:
        debuginfo.append("FPS: " + str(fps.popleft()))
    y = yres-15*len(debuginfo)
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(xres-204,y,204,yres-y))
    for string in debuginfo:
        screen.blit(font.render(string,True,(255,255,255),(0,0,0)),(xres-200,y))
        y+=15
    pygame.display.flip()
    let = datetime.now()
    fps.append(1000000/((let-lst).microseconds))
    
                               
            
                
