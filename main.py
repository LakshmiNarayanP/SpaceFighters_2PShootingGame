import pygame
import os #Used to define the path to the assets 

pygame.init()
#initializes the fonts for the game
pygame.font.init()
#initialize the sound for the game
pygame.mixer.init()

#Dimensions of game window
WIDTH, HEIGHT = 900, 500

#RGB codes for colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#Dimensions of spaceship image
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

#A line that divides 2 halves of the screen
CENTER_LINE = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#Font style that will be used to display the health points on top of the screen
#Parameters - Font family, font size
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
#Font style that will be used to display the winner on the screen
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#OS was used to enable loading images on different OS's as the path syntax may vary
YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
RED_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets','spaceship_red.png'))

#Resizing and rotating images
#Parameters for scale- Image to be resized, Dimensions (width, height), 
#Parameters for rotate - Image, rotation degrees
#Negative value for clockwise rotation and Positive value for anti clockwise rotation
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

#This variable defines how quickly the screen/window is refreshed
#Without this, the game could run differently on different machines based on the speed of execution of the loop
FPS = 60 

VEL = 5 #Velocity for moving the spaceship on key press
BULLET_VEL = 7 #Speed at which the bullet is shot
MAX_BULLETS = 5 #Maximum number of bullets than can be on the screen at once

#Codes / Numbers for custom user event
#+1 for both would make them the same event as they would have the same underlying number representing them
#When these event are posted, they go to a queue where they are checked using the event.type
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#This is the name at the title bar of the window
pygame.display.set_caption("Space Fighters")

#Sound when a bullet hits
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
#Sound when a bullet is fire
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

#The parameters here are in the form a tuple having the width and the height of the playing window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#Loading an image as background
#Transform parameters - image, dimensions
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    #-----Function Description-----
    #This function is responsible for all the drawing on the window
    #Drawing is done in order of code. What is written first gets rendered first
    #Red and yellow are passed as parameters so that instead of drawing spaceships at static positions, 
    #It can be drawn wherever they are moved to. Movement is tracked using the rectangle in the main()
    
    #To fill a screen with a specific color as a parameter
    #The colors are in the RGB format in a tuple
    #WIN.fill(WHITE)

    #Drawing an image as the backgorund
    WIN.blit(SPACE, (0,0))

    #A line that divides 2 halves of the screen
    #Parameters - Where to draw, color, specifications of the rectangle
    pygame.draw.rect(WIN, BLACK, CENTER_LINE)
    
    #Drawing fonts on the game window
    #red_health_text is the rendered object so it can be drawn on the screen
    # 1 is for anti-aliasing
    #Parameters for render - Text, anti-alisasing, color
    yellow_health_text = HEALTH_FONT.render("HP : " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("HP : " + str(red_health), 1, WHITE)
    #Drawing the above on the screen 
    #10 has been used for padding
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    
    #Use this to draw a surface on the screen
    #Images when loaded by pygame come as surfaces
    #Can be used for text too
    #The second parameter is the position co-ordinates
    #Co-ordinates system of pygame starts from top left corner which is (0,0)
    #As you go down, the y-coordinate increases and going left increases the x-coordinate
    #Drawing of an image is also done from the top left of the image
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    #Drawing the bullets for yellow
    for bullet in yellow_bullets:
        #Drawing a rectangle and the parameters -  Where, color, object
        pygame.draw.rect(WIN, YELLOW, bullet)
    #Drawing bullets for red
    for bullet in red_bullets:
        #Drawing a rectangle and the parameters - Where, color, object
        pygame.draw.rect(WIN, RED, bullet)
    #Every time something is drawn, the screen must be updated
    pygame.display.update()




def yellow_handle_movement(keys_pressed, yellow):
    #Capturing key stokes for movement of yellow spaceship
    #Parameters passed is the list of keys pressed and the yellow rectangel which represents the spaceship
    #_a mentions if A key was pressed
    #On subtracting the VEL from the current position, it shouldnt be less than 0 which is outside the screen
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Left movement and not letting the user out of screen from left
        yellow.x -= VEL #Moving to the left by VEL pixel on one press
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < CENTER_LINE.x: #Right movement and not letting the user cross the border
        yellow.x += VEL #Moving to the right by VEL pixel on one press
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Up movement and not letting the user out of the screen from top
        yellow.y -= VEL #Moving up by VEL pixel on one press
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #Down movement and not letting the user out of the screen from bottom
        yellow.y += VEL #Moving down by VEL pixel on one press

def red_handle_movement(keys_pressed, red):
    #Capturing key stokes for movement of red spaceship
    #Parameters passed is the list of keys pressed and the yellow rectangel which represents the spaceship
    #_a mentions if A key was pressed
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > CENTER_LINE.x + CENTER_LINE.width: #Left movement and not letting the user cross the border
        red.x -= VEL #Moving to the left by VEL pixel on one press
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #Right movement and not letting the user out of the screen from right
        red.x += VEL #Moving to the right by VEL pixel on one press
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #Up movement and not letting the user out of screen from the top
        red.y -= VEL #Moving up by VEL pixel on one press
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #Down movement and not letting the user out from the bottom of the screen
        red.y += VEL #Moving down by VEL pixel on one press
    

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    #-----Function Description
    #For bullet movement and collisions check and removing bullets when they collide or leave the screen on a miss
    
    #Loop through all the yellow bullets, check for collisions or leaving the screen
    for bullet in yellow_bullets:
        #Moving the bullets
        bullet.x += BULLET_VEL
        #Collision check
        #Checking if the yellow character rectangle has collided with the rect bullet
        if red.colliderect(bullet): #Works only if both objects are rectangles
            pygame.event.post(pygame.event.Event(RED_HIT))
            #Remove the bullet
            yellow_bullets.remove(bullet)
        elif bullet.x + bullet.width  > WIDTH: #elif is used to prevent removing the same bullet twice
            yellow_bullets.remove(bullet)

    #Loop through all the red bullets, check for collisions or leaving the screen
    for bullet in red_bullets:
        #Moving the bullets
        bullet.x -= BULLET_VEL
        #Collision check
        #Checking if the yellow character rectangle has collided with the rect bullet
        if yellow.colliderect(bullet): #Works only if both objects are rectangles
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            #Remove the bullet
            red_bullets.remove(bullet)
        elif bullet.x < 0: #elif is used to prevent removing the same bullet twice
            red_bullets.remove(bullet)


def draw_winner(text):
    #-----Function Description-----
    #Displays the winner text on the screen
    
    #Making the text an object to be rendered on the screen
    winner_font_text = WINNER_FONT.render(text, 1, WHITE)
    #Drawing the object
    WIN.blit(winner_font_text, (WIDTH//2 - winner_font_text.get_width()//2, HEIGHT//2 - winner_font_text.get_height()//2))
    #Updating the display
    pygame.display.update()
    #Delay for 5000ms or 5secs
    pygame.time.delay(5000)
    #So when someone wins, show the winner, pause the game for 5secs and restart the game. Hence it is not in the draw_window() function


def main():
    #-----Function Description-----
    #This is the main game loop or the event loop
    #This loop does things like redrawing the window, checking for collisions, updating the score

    #Below are rectangles that represent the spaceships so we can control movement
    #Since the control movement, everytime they move, they must be redrawn
    #So pass them into the draw() function
    #Parameters for rectangle - x position, y position, width, height
    red = pygame.Rect(600,100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(300,100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    #Stores the list of bullets for yellow. Bullets are limited
    yellow_bullets = []
    #Stores the list of bullets for red. Bullets are limited
    red_bullets = []

    #Hit points/ health for yellow player
    yellow_health = 15
    #Hit points / health for red player
    red_health = 15
    
    clock = pygame.time.Clock()
    
    #Below is a WHILE loop that is for keeping the game open. It is similar to an infinite loop.
    #It is terminated when the game ends
    run = True
    while run:
        #This loop will run until the 'run' variable becomes false

        #This line controls the speed of the while loop
        #So here the WHILE loop is run 60 times a second
        #This makes the game run consistently on different computers
        clock.tick(FPS)

        #Without a set rate, the window would be rendered as many times as possible that the PC can handle

        for event in pygame.event.get():
            #Below you check for the different events happening in the game
            #This gets us a list of all the events which are looped through and checked.
            #Based on that an action can be performed

            #The first even being checked for is if the user quit the window
            #Without this, the application must be force closed as the X button on the window will not do anyting
            if event.type == pygame.QUIT:
                run = False #This will end the WHILE loop hence quitting the game
                pygame.quit()

            #If a key is pressed down
            if event.type == pygame.KEYDOWN:
                #If the Left control button is pressed, a bullet is fired
                #MAX_BULLETS is used to make sure that at once only 3 bullets are there on the screen which are fired by yellow
                #Once its less than 3, then again new bullets can be fired
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    #x position, y position, width, height
                    #-2 is is done considering the width of the bullet
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    #Creating bullet for yellow player
                    yellow_bullets.append(bullet)
                    #Playing on the sound on firing
                    BULLET_FIRE_SOUND.play()
                #If Right Control button is pressed, a bullet is fired
                #MAX_BULLETS is used to make sure that at once only 3 bullets are there on the screen which are fired by yellow
                #Once its less than 3, then again new bullets can be fired 
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    #x position, y position, width, height
                    #-2 is is done considering the width of the bullet
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    #Creating bullet for yellow player
                    red_bullets.append(bullet)
                    #Playing a sound on firing
                    BULLET_FIRE_SOUND.play()

            #Checking out custom events
            #When the red player is hit
            if event.type == RED_HIT:
                #Subtracting 1 from the health when hit by a bullet
                red_health -= 1
                #Play a sound on getting hit
                BULLET_HIT_SOUND.play()
            #When the yellow player is hit
            if event.type == YELLOW_HIT:
                #Subtracting 1 from the health when hit by a bullet
                yellow_health -= 1
                #Play a sound on getting hit
                BULLET_HIT_SOUND.play()
        #Moving the yellow spaceship by 1 pixel everytime the loop is run
        #1 is added to the x coordinate of yello and then drawn on window
        #So it moves 60 pixels per sec as our FPS is set at 60
        #yellow.x += 1
        #red.x -= 1

        #Initially winner_text has nothing. If either of the players lost, then the winner_text is set other than empty string
        #If winner text is not equal to an empty string, then someone won    
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS !"
        if yellow_health <= 0:
            winner_text = "RED WINS !"

        if winner_text != "":
            draw_winner(winner_text)
            break #On breaking, it takes us to pygame.quit()

        #Every single time the while loop is run, this line tells us what keys are currently being pressed
        #So we can check all the keys and check if the ones we are looking for are present and if yes then respond to that press
        #If the key is continuously being pressed, it will still be registered
        keys_pressed = pygame.key.get_pressed()
        #Passing the list of key presses and the yellow rectangle object
        yellow_handle_movement(keys_pressed, yellow)
        #Passing the list of key presses and the red rectangle object
        red_handle_movement(keys_pressed, red) 

        #For bullet movement and collisions check
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets,red_bullets, yellow_health, red_health)

    #pygame.quit() #This quits the game and closes the window
    main() #Restarting the game once the game is over
    #When the function is recalled, the variables are re-defined and game restarts

#Below IF is used when this file is imported elsewhere and used
if __name__ == "__main__":
    main() #Calling the "main" function
