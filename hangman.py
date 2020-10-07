"""
Epoka University
Data Structures
Project 1

01/05/2020
Rei Balla
"""
import pygame as pg
from words import easy, hard, turkish
from random import choice
import os, sys

# init for pygame and pygame font
pg.init()
pg.font.init()

# the font i will be using
GAME_FONT = pg.font.SysFont('Lucida Bright',20)
WORD = choice(easy).upper() # temporary choosing a word from the easy list
WORD_DISPLAYED = '_ ' * len(WORD) # word that will be displayed on screen

# size of the window
size = width, height = 700,400
# colors
BLACK = 0,0,0
RED = 255,0,0
WHITE = 255,255,255
WHITELESS = 200,200,200
USED = 20,100,20

# setting screen
screen = pg.display.set_mode(size)
pg.display.set_caption('Hangman Game - Rei Balla')

# getting the absolute path of the file
directory = os.path.dirname(os.path.abspath(__file__))
# putting the paths of the hangman states in png in a list for later use
imgs = [directory + '/assets/hangman_'+str(i)+'.png' for i in range(8)]

# setting the background image
background = pg.image.load(directory+'/assets/bg.png')
background = pg.transform.scale(background,size)
background_rect = background.get_rect()
background_rect.x, background_rect.y = 0,0

# function to change/update the WORD_DISPLAYED
def change_word_display(letter):
    global WORD_DISPLAYED # need global keyword to affect variable globally
    l = WORD_DISPLAYED.split()
    for i in range(len(WORD)):
        if WORD[i] == letter:
            l[i] = letter
    WORD_DISPLAYED = ' '.join(l)

# i am using a generator that yeilds letters from A to Z 
# i know we haven't used generators but i hope this is acceptable
def generate_letter():
    letters = 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z'.split(',')
    for letter in letters:
        yield letter

# class for Hangman
class Hangman(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) # this line is needed everytime a class extends pg.sprite.Sprite
        self.state = 0 # current state of the hangman
        # loading image based on current state
        # convert_alpha is needed to make the png transparent
        self.image = pg.image.load(imgs[self.state]).convert_alpha()
        # scaling the image
        self.image = pg.transform.scale(self.image,(300,300))
        # the rect that holds the image
        self.rect = self.image.get_rect()
        self.rect.center = width/2 - width/4, height/2 + 30

    # updateting state
    def updatestate(self):
        if self.state >= 7:
            return
        else:
            old = self.rect.center # old holds the old position so it stays at the same place
            self.image = pg.image.load(imgs[self.state+1]).convert_alpha()
            self.image = pg.transform.scale(self.image,(300,300))
            self.rect =self.image.get_rect()
            self.rect.center = old
            self.state += 1 
    
    # checks if game is over
    def completed(self):
        check = ''.join(WORD_DISPLAYED.split()) # word displayed has spaces between thats why im using split
        return check == WORD

# class for game buttons
class Button:
    # since pygame doesnt have buttons i had to make my own
    def __init__(self, _pos, txt, w, h):
        # colors for the button states
        self.STILL = 70, 120, 142
        self.HOVER = 121, 216, 209
        self.USED = 214, 126, 81
        self.FONT = 162, 234, 222
        
        self.used = False
        self.txt = txt
        self.textsurface, self.textrect =  self.textsurf(txt,GAME_FONT)
        self.image = pg.Surface((w,h))  # setting an empty surface as image
        self.image.fill(self.STILL)     # filling surface with color
        self.rect = self.image.get_rect()
        self.rect.center = _pos
        self.pos = _pos

    # function for better readability inside class
    def textsurf(self,txt, font):
        s = font.render(txt, True, self.FONT)
        return s, s.get_rect()

    # checks if mouse is hovering over the button
    def ishover(self):
        ms = pg.mouse.get_pos()
        return self.rect.collidepoint(ms)

    # checks if mouse is clicked
    def isclicked(self):
        ms = pg.mouse.get_pos()
        return self.rect.collidepoint(ms)

    # checks if mouse is clicked using every event
    def isclicked_event(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                return self.rect.collidepoint(pg.mouse.get_pos())

    # renders button on screen
    def render(self, screen, hangman):
        # set text on center of rectangle
        self.textrect.center = (self.rect.x + self.rect.width / 2) ,(self.rect.y + self.rect.height / 2)
        if not self.used:
            # if its not used
            if self.ishover():
                # if mouse over button
                if self.isclicked_event():
                    # when clicked it is used
                    self.used = True
                    if self.txt in WORD:
                        # if the letter is in the real word change the displayed text
                        change_word_display(self.txt)
                    else:
                        # else draw the next state of hangman
                        if len(self.txt) == 1:
                            hangman.updatestate()
                self.image.fill(self.HOVER)
                screen.blit(self.image, self.rect)
            else:
                self.image.fill(self.STILL)
                screen.blit(self.image, self.rect)
        else:
            self.image.fill(self.USED)
            screen.blit(self.image, self.rect)
        screen.blit(self.textsurface, self.textrect)

# start screen buttons
easy_mode_button = Button((width/2-100,height/2-100),'Easy',60,30)
hard_mode_button = Button((width/2+100, height/2-100),'Hard',60,30)
quit_button = Button((width/2, height - 100),'Quit',60,30)


hangman_buttons = []
# list to hold buttons
def fillbuttons():
    global hangman_buttons          # using the global variable
    hangman_buttons = []            # empty the list
    dist = 40                       # button width
    gap = 10                        # gap between
    bx, by = width/2 + dist, 125    # buttons starting position
    letter = generate_letter()      # init generator
    for i in range(26):
        # used genterator becomes it seems easier to read to me
        hangman_buttons.append(Button((bx,by),next(letter), dist, dist))
        bx += dist + gap            
        if bx + dist + gap > width: 
            bx = width/2 + dist     # moving through the screen to create 
            by += dist + gap        # buttons in diffferent positions

fillbuttons()
# hangman sprite
hangman = Hangman()

mode = False # 0 easy 1 hard

# function to show start screen
def startscreen(screen):
    global WORD, WORD_DISPLAYED, mode
    wait = True
    while wait:
        for event in pg.event.get():
            # going through events every frame
            if event.type == pg.QUIT:
                # if quits window
                wait = False
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                # mouse is clicked
                if easy_mode_button.isclicked():
                    # if clicks easy button
                    wait = False
                    WORD = choice(easy).upper()
                    mode = False
                    WORD_DISPLAYED = '_ ' * len(WORD)
                if hard_mode_button.isclicked():
                    # if clicks hard button
                    wait = False
                    mode = True
                    WORD = choice(hard).upper()
                    WORD_DISPLAYED = '_ ' * len(WORD)
                if quit_button.isclicked():
                    # if clicks quit button
                    wait = False
                    pg.quit()
                    sys.exit()
                    break
                
        screen.fill(WHITE)
        screen.blit(background, background_rect) # bg
        easy_mode_button.render(screen, hangman) # easy button
        hard_mode_button.render(screen, hangman) # hard button
        quit_button.render(screen, hangman)      # quit button
        pg.display.flip()                        # updating every frame

# function to show the main game screen
def gamescreen(screen):
    gameover = False # boolean for the game loop
    toend = False    # boolean to determine if its the last step of the loop
    # pcsolve sends you to the screen where the pc solves the word
    pcsolve = Button((width-100,height-30),'Solve it',80,30)
    # changing colors for visibility
    pcsolve.STILL = 230, 80, 39
    pcsolve.HOVER = 250, 133, 110
    pcsolve.USED = 28, 28, 28
    pcsolve.FONT = 242, 252, 251

    while not gameover:
        
        # places on left side the tries left until game over
        tries = f'Tries left {7 - hangman.state}/7'
        text_surf = GAME_FONT.render(WORD_DISPLAYED, True, (214, 126, 81))
        text_rect = text_surf.get_rect()
        text_rect.center = width/2 + 100,50

        tries_surf = GAME_FONT.render(tries, True, (214, 126, 81))
        tries_rect = tries_surf.get_rect()
        tries_rect.center = width/2 - 170,50

        # events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                # if solve it button is clicked gameloop is over and go to solvescreen
                if pcsolve.isclicked():
                    gameover = True
                    solvescreen(screen)

        # rendering on screen
        screen.fill(WHITE)
        screen.blit(background, background_rect)
        screen.blit(text_surf,text_rect) 
        screen.blit(tries_surf,tries_rect) 
        screen.blit(hangman.image, hangman.rect)
        pcsolve.render(screen,hangman)
        for button in hangman_buttons:
            button.render(screen, hangman)


        # if last step of game
        if toend:
            pg.display.flip()   # update display
            pg.time.wait(2000)  # wait 2 sec
            gameover = True     # end
            endscreen(screen)   # go to enscreen
            
        # if game is completed -> toend is true
        if hangman.completed() or 7-hangman.state == 0:
            toend = True
            
        pg.display.flip()

# function to display the end screen
def endscreen(screen):
    global hangman, WORD, WORD_DISPLAYED, mode
    gameover = False # boolean for loop

    # deciding what the end message will be
    if hangman.completed():
        message = 'You won!'
    else:
        message = f'Sorry that you lost! The word was {WORD}'

    # play again text
    playagain = 'Press any key to play again'  

    while not gameover:
        # for message
        message_surf = GAME_FONT.render(message, True, (214, 126, 81))
        message_rect = message_surf.get_rect()
        message_rect.center = width/2, height/2

        # play again text
        playagain_surf = GAME_FONT.render(playagain, True, (214, 126, 81))
        playagain_rect = playagain_surf.get_rect()
        playagain_rect.center = width/2, height/2+50

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
            if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                # if a key in keyboard is pressed or the screen is clicked

                gameover = True     # this loop is over
                hangman = Hangman() # making a new hangman
                fillbuttons()       # new button list

                # choosing new word
                if mode: # mode is boolean for game level
                    WORD = choice(hard)
                else:
                    WORD = choice(easy)

                # changing displayed word
                WORD_DISPLAYED = '_ ' * len(WORD)
                easy_mode_button.used = False
                hard_mode_button.used = False
                startscreen(screen) # go to start screen first
                gamescreen(screen)  # go to game screen next

        screen.fill(WHITE)
        screen.blit(background, background_rect)
        screen.blit(message_surf, message_rect)
        screen.blit(playagain_surf, playagain_rect)

        pg.display.flip()

# function to show the solve screen 
def solvescreen(screen):
    global hangman, WORD, WORD_DISPLAYED, mode
    solve = solvealgorithm() # solve is the generator
    done = False # to display a message after word is found
    gameover = False # end game loop
    while not gameover:
        try:
            guess = next(solve) # iterating over next guess every frame
        except StopIteration: # until stop iteration is reached
            text = GAME_FONT.render('Error',True, WHITE)
        if guess != WORD:
            text = GAME_FONT.render(guess,True, WHITE)
        else:
            text = GAME_FONT.render(WORD,True, WHITE)
            done = True

        text_rect = text.get_rect()
        text_rect.center = width/2, height/2
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if done:
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    # exactly the same as end screen

                    # if a key in keyboard is pressed or the screen is clicked

                    gameover = True     # this loop is over
                    hangman = Hangman() # making a new hangman
                    fillbuttons()       # new button list

                    # choosing new word
                    if mode: # mode is boolean for game level
                        WORD = choice(hard)
                    else:
                        WORD = choice(easy)

                    # changing displayed word
                    WORD_DISPLAYED = '_ ' * len(WORD)
                    easy_mode_button.used = False
                    hard_mode_button.used = False
                    startscreen(screen) # go to start screen first
                    gamescreen(screen)  # go to game screen next

        screen.fill(WHITE)
        screen.blit(background, background_rect)
        pg.time.wait(100) # wait a bit to update screen for the finding letter effect
        screen.blit(text, text_rect)
        if done:
            msg = GAME_FONT.render('Thanks for playing',True, WHITE)
            msg_rect = msg.get_rect()
            msg_rect.center = width/2, height/2 - 50
            screen.blit(msg, msg_rect)

        pg.display.flip()


def solvealgorithm():
    # brute force algorithm to find the word
    # i am using generator to yield each current step for a better display effect
    array = ['']*len(WORD)
    for i in range(len(WORD)):
        for letter in generate_letter():
            if letter == WORD[i]:
                array[i] = letter
            yield ''.join(array)[:-1] + letter
    yield ''.join(array)

# start the start screen
startscreen(screen)
print(WORD)
# start the game loop
gamescreen(screen)
# quit
pg.quit()
sys.exit()