import pygame
from sys import exit
from random import randint, choice
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()



        self.image =self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0
        

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.fadeout(200)
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 :
            self.gravity = -20
            self.jump_sound.play()



    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >=300 :
            self.rect.bottom = 300


    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]   






    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210

        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        self.animation_index = 0

        self.image =self.frames[self.animation_index]
        self.rect =self.image.get_rect(midbottom =(randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <-100:
            self.kill()



screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
W,H = 100,200
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

Obstacle_group = pygame.sprite.Group()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #font type, font size


sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()





#snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#obstacles

snail_rect = snail_surf.get_rect(bottomright = (randint(900,1100),300))

#fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []




player_surf = player_walk[player_index]

player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))


game_name = test_font.render('Pixel Runner', False, (169,196,100))
game_name_rect = game_name.get_rect(center = (400, 80))


game_messege = test_font.render('Press space to run!',False,(169,196,100))
game_messege_rect = game_messege.get_rect(center = (400,320))


game_active = True


def display_score():

    current_time = (pygame.time.get_ticks()//1000) - start_time
    score_surf = test_font.render(f'Score : {current_time}', False,'Black')
    score_rect = score_surf.get_rect(topright=(600,100))
    screen.blit(score_surf,score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)   
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list


    else: return []


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index +=0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

def check_collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False


    return True



def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,Obstacle_group,False):
        Obstacle_group.empty()
        return False
    else: return True




#Timer

obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 1000)


snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer, 200)


while True:

    for event in pygame.event.get():




        if event.type == pygame.QUIT:
            pygame.quit() #closes the window
            exit() #stops running all code opp of init 

        if game_active:

            if event.type == pygame.KEYDOWN and player_rect.bottom == 300:
                if event.key == pygame.K_SPACE:
                    player_gravity =-20

            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if player_rect.collidepoint(pygame.mouse.get_pos()):
                    player_gravity =-20

                  


        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.x = 800
                start_time = pygame.time.get_ticks()//1000
                obstacle_rect_list.clear()
                player_gravity = 0
                player_rect.midbottom = (80,300)
                
    
        if game_active:

            if event.type == obstacle_timer :

                Obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

               
    
    
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
     
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
    
    
    if game_active: #game state 1
    

        screen.blit(sky_surface,(0,0))
        score = display_score()
        screen.blit(ground_surface,(0,300))

        

        #Player
       
        player.draw(screen)
        player.update()

        Obstacle_group.draw(screen)
        Obstacle_group.update()

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision_sprite()


    else:
        screen.fill((94,162,129))
        screen.blit(player_stand,player_stand_rect)


        screen.blit(game_name, game_name_rect)
       


        score_messege = test_font.render(f'Your score : {score}',False,'Black')
        score_messege_rect = score_messege.get_rect(center = (400,340))
        
        if score == 0: screen.blit(game_name,game_name_rect)
        else: screen.blit(score_messege,score_messege_rect)



    pygame.display.update()     
    clock.tick(60) 



