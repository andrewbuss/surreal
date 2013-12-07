import tg
import pygame
import interps

PERIM_WATER = 0b001
PERIM_METAL = 0b010
PERIM_TREES = 0b100

class macrosquare:
    def __init__(self, x, y, h, f):
        self.h = h
        self.x = x
        self.y = y
        self.f = f
        self.v = 0
        self.t = 0
        self.m = 0
    def setflags(self):
        if self.h < 70: self.f |= PERIM_WATER
        if self.m > 200: self.f |= PERIM_METAL
        if self.t>150 and self.h < 228: self.f |= PERIM_TREES

    def color(self):
        if self.f & PERIM_WATER: return interps.lin((25,75,125),(50,120,150),0,75,self.h)
        if self.h < 75 : return 194, 178, 128
        if self.f & PERIM_TREES and self.f & PERIM_METAL:
            if (self.x+self.y)%4: return 0, 115, 0
            else: return 170,170,200
        if self.f & PERIM_METAL: return 170,170,200
        if self.f & PERIM_TREES: return 0, 115, 0
        if self.h < 175: return interps.lin((194, 178, 128),(150,75,0),75,175,self.h)
        return interps.lin((150,75,0),(255,255,255),175,255,self.h)
class map:
    def __init__(self, res, surf, newmap=False):
        self.surf = surf
        self.res = res
        self.macrosquares = [[macrosquare(x, y, 0, 0) for x in range(self.res)] for y in range(self.res)]
        if not newmap:
            print "Initializing map from file"
            terrainfile = open("map", 'rb')
            for x in range(self.res):
                for y in range(self.res):
                    self.macrosquares[x][y].h=ord(terrainfile.read(1))
                    self.macrosquares[x][y].t=ord(terrainfile.read(1))
                    self.macrosquares[x][y].m=ord(terrainfile.read(1))
                    self.macrosquares[x][y].v=ord(terrainfile.read(1))
        else:
            print "Generating new map"
            print "Making HM"
            heightmap = tg.terrain(self.res,100000,1)
            print "Making TM"
            treemap = tg.terrain(self.res,1000,1)
            print "Making MM"
            metalmap = tg.terrain(self.res,100,1.5)
            terrainfile = open("map", 'wb')
            print "Saving map to file"
            for x in range(self.res):
                for y in range(self.res):
                    lmax = 0
                    lmin = 255
                    for dx in range(-2,3):
                        for dy in range(-2,3):
                            h = self.macrosquares[(x+dx)%self.res][(y+dy)%self.res].h
                            lmax = max(lmax, h)
                            lmin = min(lmin, h)
                    v = lmax-lmin
                    h = int(heightmap[x][y]*255)
                    t = int(treemap[x][y]*255)
                    m = int(metalmap[x][y]*255)
                    self.macrosquares[x][y].h=h
                    self.macrosquares[x][y].t=t
                    self.macrosquares[x][y].m=m
                    self.macrosquares[x][y].v=v
                    terrainfile.write(chr(h))
                    terrainfile.write(chr(t))
                    terrainfile.write(chr(m))
                    terrainfile.write(chr(v))
        for x in range(self.res):
            for y in range(self.res):
                self.macrosquares[x][y].setflags()

    def render(self):
        for x in range(self.res):
            for y in range(self.res):
                c = self.macrosquares[x][y].color()
                if x == self.res or x == 0 or y == self.res or y == 0:
                    self.surf.set_at((x,y),pygame.Color(0x000000FF))
                else:
                    self.surf.set_at((x,y),pygame.Color(c[0]*0xFFFFFF+c[1]*0xFFFF+c[2]*0xFF+0xFF))