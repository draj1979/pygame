import pygame, sys, time
from sys import exit
from random import randint
from settings import *
from sprites import BG,Ground,Plane,Obstacles


class Game:
    #setup
    def __init__(self):
        pygame.init()
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock=pygame.time.Clock()
        self.active=True


        #sprite groups
        self.all_sprites=pygame.sprite.Group()
        self.collision_sprites=pygame.sprite.Group()

        #sprite setup
        BG(self.all_sprites,1.6)
        Ground([self.all_sprites,self.collision_sprites])
        self.plane=Plane(self.all_sprites)

        #timer
        self.obstacle_timer=pygame.USEREVENT+1
        pygame.time.set_timer(self.obstacle_timer,1400)

        #font
        self.font=pygame.font.Font(None,30)

        #menu
        self.menu_surf=pygame.image.load('./FlappyBird/graphics/ui/menu.png').convert_alpha()
        self.menu_rect=self.menu_surf.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

        #music
        self.music=pygame.mixer.Sound('./FlappyBird/sounds/music.wav')
        self.music.play(loops=-1)

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
            or self.plane.rect.top<0:
            self.active=False
            self.plane.kill()
            

    def display_score(self):
        if self.active:
            self.score=pygame.time.get_ticks()//1000
            y=WINDOW_HEIGHT/10
        else:
            y=WINDOW_HEIGHT/2+100

        score_surf=self.font.render(str(self.score),True,'black')
        score_rect=score_surf.get_rect(topleft=(WINDOW_WIDTH/2,y))
        self.display_surface.blit(score_surf,score_rect)

    def run(self):
        last_time=time.time()
        while True:

            #delta time
            dt=time.time()-last_time
            last_time=time.time()


            #event loop
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        
                        self.plane=Plane(self.all_sprites)
                        self.active=True

                if event.type==self.obstacle_timer and self.active:
                    Obstacles([self.all_sprites,self.collision_sprites])

            
            #game logic
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            self.all_sprites.update(dt)           
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf,self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

    
if __name__=='__main__':
    game=Game()
    game.run()



