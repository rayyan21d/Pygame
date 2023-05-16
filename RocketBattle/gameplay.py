import pygame
import os

pygame.font.init()
pygame.mixer.init()

#make the main surface first

HEALTH_FONT=pygame.font.SysFont('comicsans',40)

WINNER_FONT=pygame.font.SysFont('comicsans',100)



WIDTH,HEIGHT = 900, 500
WHITE=(255,255,255)
BLACK=(0,0,0)
FPS=60

RED=(255,0,0)
YELLOW=(255,255,0)

VEL=5

BULLETS_VAL=7
MAX_BULLETS=3


SPACE=pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets','space.png')),(WIDTH,HEIGHT))

BORDER=pygame.Rect(WIDTH/2 - 5,0, 10,HEIGHT)


YELLOW_HIT=pygame.USEREVENT + 1 #different event numbers
RED_HIT=pygame.USEREVENT + 2




SPACESHIP_WIDTH, SPACESHIP_HEIGHT=55,40

YELLOW_SPACE_SHIP_IMG= pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))

YELLOW_SPACE_SHIP=pygame.transform.rotate(
    pygame.transform.scale(
        YELLOW_SPACE_SHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),90)

RED_SPACE_SHIP_IMG= pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))

RED_SPACE_SHIP=pygame.transform.scale(RED_SPACE_SHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACE_SHIP=pygame.transform.rotate(RED_SPACE_SHIP,270)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game!") #title


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0)) 
    #WIN.fill(WHITE)#fille in color but without updating the scrn
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text=HEALTH_FONT.render(
        "HEALTH :"+str(red_health),True,WHITE)
    yellow_health_text=HEALTH_FONT.render(
        "HEALTH :"+str(yellow_health),True,WHITE)

    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    WIN.blit(YELLOW_SPACE_SHIP, (yellow.x,yellow.y)) #instead of loading them at some points we load
    WIN.blit(RED_SPACE_SHIP,(red.x,red.y))             #them wherever the rect is defined to contain our herso


    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED, bullet)


    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW, bullet) 

    pygame.display.update()#update the display        




def yellow_handle_movement(keys_pressed, yellow):

    if keys_pressed[pygame.K_a] and (yellow.x - VEL>0): #LEFT
        yellow.x-=VEL #Had to define a velocity

    if keys_pressed[pygame.K_d] and (yellow.x+VEL+yellow.width <BORDER.x): #RIGHT
        yellow.x+=VEL 

    if keys_pressed[pygame.K_w] and (yellow.y-VEL>0): #UP
        yellow.y-=VEL        

    if keys_pressed[pygame.K_s]and (yellow.y+VEL+yellow.height<HEIGHT-15): #DOWN
        yellow.y+=VEL 

def red_handle_movement(keys_pressed, red):

    if keys_pressed[pygame.K_LEFT]and (red.x - VEL>BORDER.x+BORDER.width): #LEFT
        red.x-=VEL 

    if keys_pressed[pygame.K_RIGHT] and (red.x+VEL+red.width <WIDTH): #RIGHT
        red.x+=VEL

    if keys_pressed[pygame.K_UP] and (red.y-VEL>0): #UP
        red.y-=VEL        

    if keys_pressed[pygame.K_DOWN]and (red.y+VEL+red.height<HEIGHT-15): #DOWN
        red.y+=VEL


def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    
    #move the bullets, handle collisions, handle misses

    #We're going to loop through these bullets to check anything happened

    for bullet in yellow_bullets:
       
        bullet.x+=BULLETS_VAL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet) #vanishes from list

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)  

    for bullet in red_bullets:
       
        bullet.x-=BULLETS_VAL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet) #vanishes from list

        elif bullet.x <0 :
           red_bullets.remove(bullet)   




def draw_winner(text):
    draw_text=WINNER_FONT.render(text,True,WHITE)
    WIN.blit(draw_text,(
        WIDTH/2- draw_text.get_width()/2, HEIGHT/2-draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)


#Adding ai to the game
def red_ai_movement(red, yellow):
    # Simple AI logic for the red spaceship
    if yellow.x > red.x and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    elif yellow.x < red.x and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL

    if yellow.y > red.y and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL
    elif yellow.y < red.y and red.y - VEL > 0:
        red.y -= VEL




'''First making the main loop of the game
 which checks for collisions the main program/core u can say'''

def main():
    red=pygame.Rect(700, 300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    
    yellow=pygame.Rect(100, 300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)


    red_bullets=[]
    yellow_bullets=[]

    red_health=10
    yellow_health=10
    
    clock=pygame.time.Clock() 
    run=True
    while run:
       
        clock.tick(FPS) #limits the while loop to the fps
        for event in pygame.event.get(): #First thing to do
           
            #above 'for' creates a list of events to loop through and check
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



            if event.type==pygame.KEYDOWN: #Thw other way of handling keypresses
                
                if event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                   bullet=pygame.Rect(yellow.x+yellow.width-2,yellow.y+yellow.height/2 -2, 10,5 )
                   yellow_bullets.append(bullet)


                if event.key==pygame.K_RCTRL and len(red_bullets)< MAX_BULLETS:
                    bullet=pygame.Rect(red.x+2,red.y+red.height/2 -2, 10,5 )
                    red_bullets.append(bullet)
    

            if event.type==RED_HIT:
                red_health-=1

            if event.type==YELLOW_HIT:
                yellow_health-=1

            winner_text=""
            if red_health<=0:
                winner_text="Yellow wins!"


            if yellow_health <=0:
                winner_text="Red wins!"

            if winner_text!="" :
                draw_winner(winner_text)
                quit()    




        keys_pressed=pygame.key.get_pressed() #gets all keys being pressed down atm 1 way of handling keys
        
        yellow_handle_movement(keys_pressed,yellow) #hah, a function for everything
        #Call AI opponent's movement
        red_ai_movement(red,yellow)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health) #loop call to the drawing
    
    # quits pygame
    pygame.quit() 

    main()


if __name__ == "__main__":
    main()    

#name is name of the file and main is saying that hey
# this was the main file that was run.

""""
The above line29 makes sure that
we wanna run this directly and not 
if this file is imported from somewhere else

"""
