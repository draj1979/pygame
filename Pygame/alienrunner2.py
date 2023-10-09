import pygame
from sys import exit
from random import randint



def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5
            if obstacle_rect.bottom==300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle_rect.x>-100]
        return obstacle_list
    else:
        return []
    

def player_animation():
    #play walking animation if the player is on floor
    #display jump surface if player is on air
    global player_surf, player_index
    if player_rect.bottom>300:
        #jump
        player_surf=player_jump
    else:
        #jump
        player_index+=0.1
        if player_index>len(player_walk):player_index=0
        player_surf=player_walk[int(player_index)]



def collision(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):return False
    return True



def display_score():
    current_time=pygame.time.get_ticks()-start_time
    score_surf=test_font.render(f'Score {int(current_time/1000)}',False,(64,64,64))
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return(int(current_time/1000))

pygame.init()
screen=pygame.display.set_mode((800,400))
clock=pygame.time.Clock()
test_font=pygame.font.Font(None,50)
sky_surface=pygame.image.load('graphics/Sky.png')
ground_surface=pygame.image.load('graphics/ground.png')
game_active=False
start_time=0
score=0

score_surf=test_font.render('Pixel Runner',False,'Black')
score_rect=score_surf.get_rect(topleft=(50,50))


player=pygame.sprite.GroupSingle()
player.add(Player())

#obstacles
snail_frame_1=pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2=pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames=[snail_frame_1,snail_frame_2]
snail_frame_index=0
snail_surf=snail_frames[snail_frame_index]

fly_frame_1=pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2=pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames=[fly_frame_1,fly_frame_2]
fly_frame_index=0
fly_surf=fly_frames[fly_frame_index]

obstacle_rect_list=[]

player_gravity=0
player_walk_1=pygame.image.load('graphics/Player/player_walk_1.png')
player_walk_2=pygame.image.load('graphics/Player/player_walk_2.png')
player_walk=[player_walk_1,player_walk_2]
player_index=0
player_jump=pygame.image.load('graphics/Player/jump.png')
player_surf=player_walk[player_index]
player_rect=player_surf.get_rect(midbottom=(80,300))

#Intro screen
player_stand=pygame.image.load('graphics/Player/player_stand.png')
player_stand=pygame.transform.scale_by(player_stand,1.5)
player_stand_rect=player_stand.get_rect(center=(400,200))
game_name=test_font.render("Pixel Runner",False,(64,64,64))
game_name_rect=game_name.get_rect(center=(400,80))
game_message=test_font.render("Press Space to Start",False,(64,64,64))
game_message_rect=game_name.get_rect(center=(400,300))      

#timer
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)

while True:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit
            exit()
       
        if game_active:
            
                       
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    player_gravity=-20

            if event.type==obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1200),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900,1500),200)))

            if event.type==snail_animation_timer:
                if snail_frame_index==0:snail_frame_index=1
                else: snail_frame_index=0
                snail_surf=snail_frames[snail_frame_index]

            if event.type==fly_animation_timer:
                if fly_frame_index==0:fly_frame_index=1
                else: fly_frame_index=0
                fly_surf=fly_frames[fly_frame_index]

        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE: 
                game_active=True
                start_time=pygame.time.get_ticks()
               
    if game_active:
        
        #display background and characters
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(score_surf,score_rect)        
        screen.blit(player_surf,player_rect)

        #move the snails
        obstacle_rect_list=obstacle_movement(obstacle_rect_list)
            
        #display score
        score=display_score()
       
        #let player fall whenever jump
        player_gravity+=1   
        player_rect.y+=player_gravity     
        if player_rect.bottom>=300:player_rect.bottom=300
        player_animation()
        screen.blit(player_surf,player_rect)
        player.draw(screen)

        #collisions:
        game_active=collision(player_rect,obstacle_rect_list)
      
    else:
        #display intro screen
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        obstacle_rect_list.clear()
        player_rect.bottom=300
        player_gravity=0
        
        score_message=test_font.render(f'Your Score is {score}',False,(64,64,64))
        score_message_rect=score_message.get_rect(center=(400,320))
        if score==0:
            #display game message
            screen.blit(game_message,game_message_rect)
        else:
            #display score
            screen.blit(score_message,score_message_rect)
         

    pygame.display.update()
    clock.tick(60)