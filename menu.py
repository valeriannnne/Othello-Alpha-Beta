# import main
import alpha
import pygame
import button

pygame.init()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Othello")

#game variables
game_continue = False
ai_action = False
# multiplayer_action = False

#fonts
font = pygame.font.SysFont("consolas", 30)
font_small = pygame.font.SysFont("consolas", 20)

#define colors
TEXT_COL = (0,0,0)

#load button images
multiplayer_img = pygame.image.load("assets/Buttons/Multiplayer1.png").convert_alpha()
ai_img = pygame.image.load("assets/Buttons/AI-Mode1.png").convert_alpha()
quit_img = pygame.image.load("assets/Buttons/Quit1.png").convert_alpha()

#create button instances
multiplayer_button = button.Button(300, 200, multiplayer_img, 0.45)
ai_button = button.Button(300, 290, ai_img, 0.45)
quit_button = button.Button(300, 380, quit_img, 0.45)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#game loop
run = True
while run:
    #bg color
    screen.fill((217, 179, 95))

    #check if game will continue
    if game_continue == True:
        draw_text("Let's Start!", font, TEXT_COL, 310, 130)
        multiplayer_button.draw(screen)
        ai_button.draw(screen)
        if quit_button.draw(screen):
            run = False
        # if multiplayer_action:
        #     from main import Othello
        #     othello_game = Othello()  # create an instance of the Othello class
        #     othello_game.run()  # call the run method of the Othello class
        #     pygame.quit()
        if ai_action:
            from alpha import Othello
            othello_game = Othello()  # create an instance of the Othello class
            othello_game.run()  # call the run method of the Othello class
            pygame.quit()
    else:
        draw_text("Welcome to Othello", font, TEXT_COL, 250, 250)
        draw_text("Press SPACE to continue", font_small, TEXT_COL, 270, 310)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_continue = True
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ai_button.draw(screen):
                ai_action = True
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if multiplayer_button.draw(screen):
        #         multiplayer_action = True
    
    pygame.display.update()

pygame.quit()
