from curses import BUTTON_ALT
import pygame
import random
import math
from pygame import mixer
from random import randint
from classes import *

# Initialize pygame
pygame.init()

# Setting useful events (for optimization)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

# Frames per second
fps = 80
clock = pygame.time.Clock()

# Create screen
screen = pygame.display.set_mode((800,575))

# Title and Icon
pygame.display.set_caption('Cooking FIBer')
#icon = pygame.image.load('assets/pictures/ufo1.png').convert_alpha()
#pygame.display.set_icon(icon)

# Background
backgroundImg = pygame.image.load('images/bar.png')
backgroundImg = pygame.transform.scale(backgroundImg, (800,600))

# Images used in classes
bubbleImg = pygame.image.load('images/bubble.png')  
running = True
drag = False
def display_text(text,size,x,y):
    'Display text with size in x,y position'
    font = pygame.font.Font('font/ARCADE_N.ttf', size)
    textimg = font.render(text, True, (250,250,250))
    screen.blit(textimg,(x,y))

def drop_shadow(text, size, x, y, color):
    'Create font shadow of the text of size in x,y position printed in color'
    font = pygame.font.Font('font/ARCADE_N.ttf', size) 
    fontshadow = font.render(text, True, color)
    screen.blit(fontshadow,(x+5,y+5))

# Initializing buttons
btnburger = Button(press_burger,443,520, 90,50,'images/burgbutton.png')
btnfries = Button(press_potato,360,520, 90, 50,'images/frybutton.png')
btnegg = Button(press_egg,675,553, 90, 50, 'images/eggbutton.png')
btncola = [Button(press_cola,265,557, 170,110, 'images/1row.png'),
		   Button(press_cola,265,557, 170,110, 'images/2rows.png'),
		   Button(press_cola,265,557, 170,110, 'images/3rows.png')]


mixer.music.load("music/fons.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.3)

game = Game()
time_start = pygame.time.get_ticks()
client_waiting = False
price=0
game_over= False

while running:
    clock.tick(fps)
    while not game_over:

    # Background
        screen.fill((0,0,0))
        screen.blit(backgroundImg, (0,0))
        all_sprites.draw(screen)

        input_box1 = InputBox(715, 255, 60, 32, text = str(price)+'$')
        input_boxes = [input_box1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Checks if button was pressed 
            btnburger.get_event(event)
            btnfries.get_event(event)
            btnegg.get_event(event)
            i = rows()
            btncola[i].get_event(event)
            num_foods = len(food_sprites)
            for i,food in zip(range(num_foods),food_sprites):
                if food.is_food_dragged(event) and food.state == 'cooked':
                    moving = food
                    drag = True
                if event.type == pygame.MOUSEMOTION:
                    if drag:
                        moving.move(event.rel)
                if event.type == pygame.MOUSEBUTTONUP:
                    drag = False

        time_now = pygame.time.get_ticks()

        for box in input_boxes:
            box.draw(screen)
        
        if client_waiting:
            if new_client.dead:
                new_price = new_client.ordre.price
                price += new_price
                client_waiting = False
                time_start = pygame.time.get_ticks()
        if time_now - time_start > 1500 and not client_waiting:
            new_client = Client()
            all_sprites.add(new_client)
            client_waiting = True

    


    


    # Update sprites like people, banners...
        all_sprites.update()
        all_sprites.draw(screen)

    # Update food sprites
        food_sprites.update()
        food_sprites.draw(screen)

    # Update and draw display (text, background)
        btnburger.render(screen)
        btnfries.render(screen)
        btnegg.render(screen)
        i = rows()
        btncola[i].render(screen)
        pygame.display.update()
        game_over = is_running(price)
    
    all_sprites.update()
    all_sprites.draw(screen)

    # Update food sprites
    food_sprites.update()
    food_sprites.draw(screen)

    # Update and draw display (text, background)
    btnburger.render(screen)
    btnfries.render(screen)
    btnegg.render(screen)
    i = rows()
    btncola[i].render(screen)
    pygame.display.update()
    drop_shadow("THE END", 40, 250, 160, (105,105,105))
    display_text("THE END", 40, 250, 160)
    display_text("You achieved the daily goal :)", 15, 200, 210)

    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    

  
