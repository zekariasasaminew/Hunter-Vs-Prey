'''
Name: Zekarias Asaminew
CSC 201
Project 3

This is a game where a hunter uses an arrow to hit birds that are falling from the top of the window.
Using the space key a player can fire arrows to hunt birds. To move the hunter use mouse clicks to the left and right of the hunter.
If the hunter hunts 20 birds before any birds escape, they win.

BONUS POINTS
On this project I added diffrent sound effects like:-

arrow_sound(sound when arrow is shot)
game_over_sound(sound when player loses the game)
game_won_sound(sound when player wins the game)
background_sound(a nice bird chirping background sound throughout the game)

I also added:-
game_result_window (a window is created when a player either wins or loses the game and prompt them)
(if they want to play again by a Yes and No button)
(if player wants to play again and clicks Yes button, it loops through main function again is they click No button it exits the game)
level_up (as the score increase by 5 the player passes to the next level where they encounter more birds at a higher speed)
if click is outside the yes and no button, notifies the player to click either Yes or No button.

Assistance:
    Professor Diane Mueller helped me clean my code with removing redundancy and also
    assisted me with is_hunter_close_enough function.
'''
from graphics2 import *
from button import Button
import time
import random
import math
import pygame

# Initialize pygame
pygame.mixer.init()

# Load sound effects
arrow_sound = pygame.mixer.Sound('arrow_shot.mp3')
game_over_sound = pygame.mixer.Sound('game_over.mp3')
game_won_sound = pygame.mixer.Sound('game_won.mp3')
background_sound = pygame.mixer.Sound('background.wav')

# Common constants used
BIRD_SPEED = 7
ARROW_SPEED = 7
HUNTER_SPEED = 25
STALL_TIME = 0.05
THRESHOLD = 50
WINDOW_WIDTH = 666
WINDOW_HEIGHT = 666
DELTA_BIRDS = 6
WINNING_SCORE = 20
DELTA_BIRD_SPEED = 5

GAME_WON_TITLE = 'GAME WON!'
GAME_WON_STATEMENT = "Congratulations.\nYou've won this game."
GAME_OVER_TITLE = 'GAME OVER'
GAME_OVER_STATEMENT = "Game Over!\n\nYou've lost this game."

# Sets up the game and give instruction in a new window
def set_up():
    """
    Create a window and gives directions.
    
    Explain how the game works and how much score is needed to go to
    the next level. The window closes with a click.
    """
    window = GraphWin("Game Instruction", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    window.setBackground('white')
    background_sound.play()  #play a nice birds chirping background sound
    directions = Text(Point(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 6), f"You'll have a hunter with an arrow.\n\n"
                                                                "Click on the right and left of the hunter to move it.\n\n"
                                                                "Use space to shoot arrows and kill the birds.\n\n"
                                                                "In order to pass to the next level you'll\n\n"
                                                                "need a score of 5.\n\n"
                                                                "You will need 20 points to win the game\n\n"
                                                                "Good Luck!")
    goOnText = Text(Point(WINDOW_WIDTH / 4, 3 *WINDOW_HEIGHT / 8), "Click to continue")
    directions.setSize(9)
    directions.draw(window)
    goOnText.draw(window)
    window.getMouse() #waits for a click before starting the game
    window.close()                                                    

# Calculate distance between two points
def distance_between_points(point1, point2):
    '''
    Calculates the distance between two points
    
    Params:
    point1 (Point): the first point
    point2 (Point): the second point
    
    Returns:
    the distance between the two points
    '''
    p1x = point1.getX()
    p1y = point1.getY()
    p2x = point2.getX()
    p2y = point2.getY()
    return math.sqrt((p1x - p2x)*(p1x - p2x) + (p1y - p2y) * (p1y - p2y))

# Determine if arrow is close to birds
def is_arrow_close_enough(arrow, bird):
    '''
    Determines if the tip of the arrow is close enough to the bird to say the hunter
    killed the bird.
    
    Params:
    arrow (Image): the image of the arrow
    bird (Image): the image of the bird
    
    Returns:
    True if the arrow catches the bird
    '''
    arrow_center_x = arrow.getCenter().getX()
    arrow_tip_y = (arrow.getCenter().getY()) - (arrow.getHeight() / 3)
    center_bird = bird.getCenter()
    distance = distance_between_points(Point(arrow_center_x, arrow_tip_y), center_bird)
    return distance < THRESHOLD 

# Determine if bird is close to hunter
def is_hunter_close_enough(bird, hunter):
    '''
    Determines if a bird is close enough to the hunter to say the hunter
    lost the game.
    
    Params:
    bird (Image): the image of the bird
    hunter (Image): the image of the hunter
    
    Returns:
    True if the bird touches the hunter
    '''
    center_hunter = hunter.getCenter()
    center_bird = bird.getCenter()
    distance = distance_between_points(center_hunter, center_bird)
    return distance < THRESHOLD

# Shoot arrow
def shoot_arrow(arrow_list):
    '''
    Moves every arrow that is shooted one ARROW_SPEED unit up the window
    
    Params:
    arrow_list (list): the list of arrows that are shooted
    '''
    for arrow in arrow_list: #iterates across arrow_list and move each arrow from bottom to top
        arrow.move(0, -ARROW_SPEED)
      
# Move birds one BIRD_SPEED unit down the window when the score is less than 10.
# Increase BIRD_SPEED by score // 10 everytime player passed a score by 10. 
def move_birds(bird_img_list, score):
    '''
    Moves every bird one BIRD_SPEED unit down the window
    
    Params:
    bird_img_list (list): the list of falling birds
    '''
    BIRD_SPEED = 7
    if score > 5:
        BIRD_SPEED += DELTA_BIRD_SPEED
        for bird in bird_img_list:
            bird.move(0, BIRD_SPEED)
    else:
        for bird in bird_img_list:
            bird.move(0, BIRD_SPEED)

# Move hunter if a click is made at the left or right of the hunter
def move_hunter(hunter, window):
    '''
    Each time the left arrow key is pressed the hunter moves HUNTER_SPEED units left and
    each time the right arrow key is pressed the hunter moves HUNTER_SPEED units right.
    
    Params:
    window (GraphWin): the window where game play takes place
    hunter (Image): the hunter image
    '''
    click = window.checkMouse()
    if click:
        x = click.getX()
        y = click.getY()
        hunter_center = hunter.getCenter()
        x_hunter = hunter_center.getX()
        y_hunter = hunter_center.getY()
        
        hunter_height = hunter.getHeight()
        hunter_width = hunter.getWidth()
        
        if x > (x_hunter + (hunter_width / 2)) and y > WINDOW_HEIGHT - hunter_height and y < y_hunter + (hunter_height / 2):
            hunter.move(HUNTER_SPEED, 0)
        elif x < (x_hunter - (hunter_width / 2)) and y > WINDOW_HEIGHT - hunter_height and y < y_hunter + (hunter_height / 2):
            hunter.move(-HUNTER_SPEED, 0)

# Create a bird in the window and return it
def add_bird_to_window(window):
    '''
    Adds one bird to the top of the window at a random location
    
    Params:
    window (GraphWin): the window where game play takes place
    
    Returns:
    the bird added to the window
    '''
    random_location = random.randrange(40, 601)
    bird = Image(Point(random_location, 0), "Bird.png")
    bird.draw(window)
    return bird

# Create the arrow in the window and return it
def add_arrow(window, hunter):
    '''
    Add one arrow down at hunter_center.
    
    Params:
    window (GraphWin): The window where game play takes place
    
    Returns:
    the arrow added to the window
    
    '''
    hunter_center = hunter.getCenter()
    
    arrow = Image(hunter_center, "arrow.png")
    arrow.draw(window)
    arrow_sound.play()
    return arrow

# Create a new window to display the score at the end after player lost the game
# P rompt user if they want to play the game again
def game_result(score, game_title, game_statement):
    '''
    Create another window to display that game was either lost or won and prompt user if they want to
    play again. Also displays the score.
    
    Params:
    score (int): score of the player during the game.
    game_title (str): title of the window
    game_statement (str): text to be displayed on the window
    '''
    window_result = GraphWin(game_title, WINDOW_WIDTH, WINDOW_HEIGHT)
    window_result.setBackground('white')
    background_sound.stop()

    
    directions = Text(Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 6), game_statement)
    directions.setSize(26)
    directions.draw(window_result)
    
    play_again_yes_button = Button(Point(WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3), 80, 40, "Yes")
    play_again_no_button = Button(Point(2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3), 80, 40, "No")
    
    
    choice = Text(Point(333, 333), f"Would you like to play again?")
    choice.setSize(26)
    choice.draw(window_result)
    
    play_again_yes_button.draw(window_result)
    play_again_no_button.draw(window_result)
    
    click_point = window_result.getMouse()
    while not play_again_yes_button.clicked(click_point) and not play_again_no_button.clicked(click_point):
        click_on_window_text = Text(Point(333, 200), 'Please click either Yes or No.')
        click_on_window_text.draw(window_result)
        time.sleep(2)
        click_on_window_text.undraw()
        click_point = window_result.getMouse()
        
    if play_again_yes_button.clicked(click_point): #returns True if user clicked yes button   
        window_result.close()
        return True
    elif play_again_no_button.clicked(click_point): #returns False if user clicked no
        window_result.close()
        return False
        
def display_level_up(window, current_level):
    '''
    Displays the level upgrade as the player hit 5 birds
    
    Params:
    window (GraphWin): The window where game play takes place
    current_level (int): The current level the player is at.    
    
    '''
    level_up_text = Text(Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), f"Level {str(current_level)}!")
    level_up_text.setSize(30)
    level_up_text.setTextColor("green")
    level_up_text.draw(window)
    time.sleep(2)  # Display the "Level Up" message for 2 seconds
    level_up_text.undraw()
    
def generate_bird(window, score, bird_list):
    '''
    Add multiple birds on the window at random location.
    
    Params:
    window (GraphWin): The window where the game takes place.
    score (int): The score of the player
    bird_list (list): list where all the birds in the window are found
    '''
    add_more_birds = 6
    if score // 10 > 0:
        add_more_birds += DELTA_BIRDS
        if random.randrange(100) < add_more_birds:
            bird = add_bird_to_window(window)
            bird_list.append(bird)
    else:
        if random.randrange(100) < add_more_birds:
            bird = add_bird_to_window(window)
            bird_list.append(bird)
        
# Loops through the game
def game_loop(window, hunter, arrow):
    '''
    Loop continues to allow the birds to fall and the hunter to move
    until enough birds escape or the hunter catches enough birds to
    end the game.
    
    Params:
    window (GraphWin): the window where game play takes place
    hunter (Image): the hunter image
    '''
    score = 0
    bird_list = []
    arrow_list = []
    
    score_label = Text(Point(70, 50), str(score))
    score_label.setSize(16)
    score_label.draw(window)
    
    current_level = 1
    while score < WINNING_SCORE:
        key = window.checkKey()
        if key == 'space':
            arrow = add_arrow(window, hunter)
            arrow_list.append(arrow)
                
        shoot_arrow(arrow_list)
        
        move_hunter(hunter, window)
        
        generate_bird(window, score, bird_list)
            
        move_birds(bird_list, score)
        
        if score >= current_level * 5:
            display_level_up(window, current_level)
            current_level += 1
            
        for arrow in arrow_list:
            for bird in bird_list: 
                if is_arrow_close_enough(arrow, bird):
                    score += 1
                    arrow_list.remove(arrow)
                    bird.undraw()
                    bird_list.remove(bird)
                    arrow.undraw()
                    score_label.setText(str(score))
                    
        for bird in bird_list:     
            bird_y = bird.getCenter().getY()
            if bird_y > WINDOW_HEIGHT:
                score -= 1
                bird_list.remove(bird)
                score_label.setText(str(score))
                        
        for bird in bird_list:       
            if is_hunter_close_enough(bird, hunter):
                game_over_sound.play()
                if not game_result(score, GAME_OVER_TITLE, GAME_OVER_STATEMENT): #calls game_result function to exit the game
                    exit(1)
                else:
                    window.close() #calls game_result
                    main()  
        time.sleep(STALL_TIME)
        
    game_won_sound.play()  #plays sound when player won the game
    
    if not game_result(score, GAME_WON_TITLE, GAME_WON_STATEMENT):
        window.close()
        return False
    else:
        window.close()
        main()
def main():
    # setup the game
    set_up()
    window = GraphWin("Hunter!!!", WINDOW_WIDTH, WINDOW_HEIGHT)
    
    background = Image(Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), "jungle.png")
    background.draw(window)
    
    hunter = Image(Point(WINDOW_WIDTH / 2, 580), "man.gif")
    hunter.draw(window)
    
    arrow = Image(Point(hunter.getCenter().getX(), hunter.getCenter().getY()), "arrow.png")
    game_loop(window, hunter, arrow)
    
main()