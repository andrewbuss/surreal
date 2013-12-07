import pygame

class menu:
    font = pygame.font.SysFont("microsoftyahei",12)
    def __init__(self,surf, title,items):
        self.surf=surf
        self.title=title
        self.items=items
        self.surf.fill(pygame.Color(0,0,0,255))
        self.surf.blit(self.font.render(title,True,(255,255,255),(0,0,0)),(0,0))
