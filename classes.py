from socket import if_nametoindex
import pygame
import random
import math
from pygame import mixer
from random import randint

# Spite list
all_sprites = pygame.sprite.OrderedUpdates()
food_sprites = pygame.sprite.OrderedUpdates()
client_sprites = []

# Images used in classes
avatar = [[pygame.image.load('images/happyanna.png'),pygame.image.load('images/sadanna.png')],
        [pygame.image.load('images/happyjaume.png'),pygame.image.load('images/sadjaume.png')],
            [pygame.image.load('images/happyjulia.png'),pygame.image.load('images/sadjulia.png')],
            [pygame.image.load('images/happymarc.png'), pygame.image.load('images/sadmarc.png')],
            [pygame.image.load('images/happysara.png'),pygame.image.load('images/sadsara.png')]]
burgers = [0,0,0]
fries = [0,0,0]
eggs = [0,0,0]
cola = [0,0,0,0]
drag = 0
rows1= 2
moving = None

#TextBox
pygame.init()
COLOR_INACTIVE = pygame.Color('white')
FONT = pygame.font.Font('font/ARCADE_N.TTF', 15)        
class Game():
    def __init__(self):
        self.menu = [Burger, Fries, Cola, Egg]

class Client(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        client_sprites.append(self)
        self.size = 200
        self.X = 400
        self.Y = 155
        self.n_avatar = randint(0,4)
        self.image = pygame.transform.scale(avatar[self.n_avatar][0], (self.size,self.size))        
        self.rect = self.image.get_rect()
        self.rect.center = (self.X,self.Y)
        self.state = 'Happy'
        ordre = Order()
        self.ordre = ordre
        all_sprites.add(ordre)
        self.dead = False
        self.timestart = pygame.time.get_ticks()
    
    def update(self):
        self.time = pygame.time.get_ticks()
        if self.time - self.timestart > 10000:
            self.state = 'Frustrated'
        if self.state == 'Frustrated':
            self.image = pygame.transform.scale(avatar[self.n_avatar][1], (self.size,self.size))
        if self.ordre.is_empty():
            self.ordre.kill()
            self.dead = True
            self.kill()



class Button():
    def __init__(self, command, X, Y, sizex, sizey, file):
        self.color = (255,0,0)
        image = pygame.image.load(file)
        self.image = pygame.transform.scale(image, (sizex,sizey))
        self.rect = self.image.get_rect()
        self.rect.center = (X,Y)
        self.command = command

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command()

class Order(pygame.sprite.Sprite):
    
    def __init__(self):
        # Create speach bubble
        pygame.sprite.Sprite.__init__(self)
        order_sound = mixer.Sound("music/hello.mp3")
        order_sound.play()
        bubbleImg = pygame.image.load('images/bubble.png').convert_alpha()
        self.X = 575
        self.Y = 125
        self.image = pygame.transform.scale(bubbleImg, (225,225))        
        self.rect = self.image.get_rect()
        self.rect.center = (self.X,self.Y)
        self.orders = [0,0,0]
        self.empty = False

        number = randint(1,3)
        for _ in range(number):
            for n in range(3):
                if self.orders[n]==0:
                    x,y = self.get_order_coordinates(n)
                    new_food = game.menu[randint(0,len(game.menu))-1](x,y, state = 'label')
                    food_sprites.add(new_food)
                    self.orders[n] = new_food
                    break
        self.price = self.cost()
    
    def update(self):
        pass
    
    def cost(self):
        price = 0
        for item in self.orders:
            if item != 0:
                if item.type() == 'Cola':
                    price += 1
                elif item.type() == 'Fries':
                    price += 2       
                elif item.type() == 'Burger':
                    price += 3
                elif item.type() == 'Egg':
                    price += 2
        return price
    
    def get_order_coordinates(self,n):
        if n == 0:
            return 575, 120
        if n == 1:
            return 645, 120
        if n == 2:
            return 710, 120

    def new_order(self, altre):
        for i in range(len(self.orders)):
            if type(self.orders[i]) == type(altre):
                self.orders[i].kill()
                self.orders[i] = 0
                if all(order == 0 for order in self.orders):
                    self.empty = True
                break 

    def is_empty(self):
        return self.empty


class InputBox:
    def __init__(self, x, y, w, h, text='0$'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, [740, 262])
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Cola(pygame.sprite.Sprite):
    def __init__(self, X = None, Y = None, state = 'cooked'):
        self.name = "Cola"
        pygame.sprite.Sprite.__init__(self)
        if state == 'label':
            self.X = X - 70
            self.Y = Y - 15
            self.size = (40,55)
        else: #no és bafarada
            self.X , self.Y = self.cola_position()
            self.size = (35,50)
            colasound = mixer.Sound("music/deixacola.mp3")
            colasound.play()
        image = pygame.image.load('images/cocacola.png')
        self.image = pygame.transform.scale(image, self.size)           
        self.rect = self.image.get_rect()
        self.rect.center = (self.X,self.Y) 
        self.state = state

    def update(self):
        # Checks if between time of creation and time now 10 seconds have passed. If so, the burger is cooked
        if self.state != 'label':
            for client in client_sprites:
                if self.is_given(client):
                    drinking = mixer.Sound("music/obrecola.mp3")
                    drinking.play()
                    cola[self.n] = 0
                    client.ordre.new_order(self)
                    self.kill()
        self.rect.center = (self.X,self.Y)

    def given(self):
        self.kill()
    
    def cola_position(self):
        for n in range(len(cola)):
            if cola[n]==0:
                if n==0: 
                    cola[n]=1
                    self.n=n
                    return 290,355
                elif n==1:
                    cola[n]=1
                    self.n=n
                    return 283,390
                elif n==2:
                    cola[n]=1
                    self.n=n
                    return 276,425
                elif n==3:
                    cola[n]=1
                    self.n=n
                    return 269,460
    
    def is_food_dragged(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()): 
                return True
    
    def move(self,rel):
        if self.state == 'cooked':
            pos =  pygame.mouse.get_pos()
            self.X, self.Y = pos[0], pos[1]


    def is_given(self,client):
        distance = math.sqrt((math.pow(client.X  - self.X,2))+(math.pow(client.Y-self.Y,2)))
        if distance < 100:
            return True
        return False
    
    def type(self):
        return "Cola"

class Fries(pygame.sprite.Sprite):
    def __init__(self, X = None, Y = None, state = 'cooking'):
        pygame.sprite.Sprite.__init__(self)
        if state == 'label':
            self.X = X - 70
            self.Y = Y - 15
            self.size = (40,50)
            image = pygame.image.load('images/cookedfries.png')
            self.image = pygame.transform.scale(image, self.size)
        else: #no és bafarada
            fries_sound = mixer.Sound("music/grillfade.mp3")
            fries_sound.play()
            self.X , self.Y = self.fries_position()
            self.size = (35,45)
            image = pygame.image.load('images/rawfries.png')
            self.image = pygame.transform.scale(image, self.size)           
        self.rect = self.image.get_rect()
        self.rect.center = (self.X,self.Y) 
        self.state = state
        self.timestart = pygame.time.get_ticks()
        
    def update(self):
        # Checks if between time of creation and time now 10 seconds have passed. If so, the burger is cooked
        if self.state != 'label':
            self.timenow = pygame.time.get_ticks()
            if self.timenow - self.timestart > 5000:
                self.state = 'cooked'
                image = pygame.image.load('images/cookedfries.png')
                self.image = pygame.transform.scale(image, self.size)
            for client in client_sprites:
                if self.is_given(client):
                    eating = mixer.Sound("music/bite.mp3")
                    eating.play()
                    fries[self.n] = 0
                    client.ordre.new_order(self)
                    self.kill()
        self.rect.center = (self.X,self.Y)
        

    def given(self):
        self.kill()
    
    def fries_position(self):
        for n in range(len(fries)):
            if fries[n]==0:
                if n==0: 
                    fries[n]=1
                    self.n=n
                    return 365,345
                elif n==1:
                    fries[n]=1
                    self.n=n
                    return 365,395
                elif n==2:
                    fries[n]=1
                    self.n=n
                    return 365,450
    
    def is_food_dragged(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()): 
                return True
    
    def move(self,rel):
        if self.state == 'cooked':
            pos =  pygame.mouse.get_pos()
            self.X, self.Y = pos[0], pos[1]


    def is_given(self,client):
        distance = math.sqrt((math.pow(client.X  - self.X,2))+(math.pow(client.Y-self.Y,2)))
        if distance < 100:
            return True
        return False
    
    def type(self):
        return "Fries"

class Burger(pygame.sprite.Sprite):
    def __init__(self, X = None, Y = None, state = 'cooking'):
        self.name = 'Burger'
        pygame.sprite.Sprite.__init__(self)
        if state == 'label':
            self.X = X - 70
            self.Y = Y - 15
            self.size = (65,40)
            image = pygame.image.load('images/cookedburger.png')
            self.image = pygame.transform.scale(image, self.size)
        else:
            burger_sound = mixer.Sound("music/grillfade.mp3")
            burger_sound.play()
            self.X , self.Y = self.burger_position()
            self.size = (60,35)
            image = pygame.image.load('images/rawburger.png')
            self.image = pygame.transform.scale(image, self.size)           
        self.rect = self.image.get_rect()
        self.rect.center = (self.X,self.Y) 
        self.state = state
        self.timestart = pygame.time.get_ticks()

    def update(self):
        # Checks if between time of creation and time now 10 seconds have passed. If so, the burger is cooked
        if self.state != 'label':
            self.timenow = pygame.time.get_ticks()
            if self.timenow - self.timestart > 5000 and self.state == 'cooking': 
                self.state = 'cooked'
                image = pygame.image.load('images/cookedburger.png')
                self.image = pygame.transform.scale(image, self.size)
        for client in client_sprites:
            if self.is_given(client):
                eating = mixer.Sound("music/bite.mp3")
                eating.play()
                burgers[self.n] = 0
                client.ordre.new_order(self)
                #client.tick = self.tick()
                self.kill()
        self.rect.center = (self.X,self.Y)
    
    def burger_position(self):
        for n in range(len(burgers)):
            if burgers[n]==0:
                if n==0: 
                    burgers[n]=1
                    self.n=n
                    return 435,345
                elif n==1:
                    burgers[n]=1
                    self.n=n
                    return 439,395
                elif n==2:
                    burgers[n]=1
                    self.n=n
                    return 445,450
    
    def is_food_dragged(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()): 
                return True
    
    def move(self,rel):
        if self.state == 'cooked':
            pos =  pygame.mouse.get_pos()
            self.X, self.Y = pos[0], pos[1]

    def is_given(self,client):
        distance = math.sqrt((math.pow(client.X  - self.X,2))+(math.pow(client.Y-self.Y,2)))
        if distance < 100:
            return True
        return False
    
    def type(self):      
        return 'Burger'       

class Egg(pygame.sprite.Sprite):
    def __init__(self, X = None, Y = None, state = 'cooking'):
        pygame.sprite.Sprite.__init__(self)
        if state == 'label':
            self.X = X - 70
            self.Y = Y - 15
            self.size = (65,40)
            image = pygame.image.load('images/cookedegg.png')
            self.image = pygame.transform.scale(image, self.size)
        else: #no és bafarada
            egg_sound = mixer.Sound("music/grillfade.mp3")
            egg_sound.play()
            self.X , self.Y = self.egg_position()
            self.size = (50,25)
            image = pygame.image.load('images/rawegg.png')
            self.image = pygame.transform.scale(image, self.size)           
        self.rect = self.image.get_rect()
        self.rect.center = (self.X,self.Y) 
        self.state = state
        self.timestart = pygame.time.get_ticks()

    def update(self):
        # Checks if between time of creation and time now 10 seconds have passed. If so, the burger is cooked
        if self.state != 'label':
            self.timenow = pygame.time.get_ticks()
            if self.timenow - self.timestart > 5000:
                self.state = 'cooked'
                image = pygame.image.load('images/cookedegg.png')
                self.image = pygame.transform.scale(image, self.size)
            for client in client_sprites:
                if self.is_given(client):
                    eating = mixer.Sound("music/bite.mp3")
                    eating.play()
                    eggs[self.n] = 0
                    client.ordre.new_order(self)
                    self.kill()
        self.rect.center = (self.X,self.Y)

    def given(self):
        self.kill()

    def is_food_dragged(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()): 
                return True
    
    def move(self,rel):
        if self.state == 'cooked':
            pos =  pygame.mouse.get_pos()
            self.X, self.Y = pos[0], pos[1]


    def is_given(self,client):
        distance = math.sqrt((math.pow(client.X  - self.X,2))+(math.pow(client.Y-self.Y,2)))
        if distance < 100:
            return True
        return False
    
    def egg_position(self):
        for n in range(len(eggs)):
            if eggs[n]==0:
                if n==0: 
                    eggs[n]=1
                    self.n=n
                    return 587,380
                elif n==1:
                    eggs[n]=1
                    self.n=n
                    return 605,425
                elif n==2:
                    eggs[n]=1
                    self.n=n
                    return 620,475
    
    def type(self):
        return "Egg"

def press_burger():  
    for n in range(len(burgers)):
        if burgers[n]==0:
            food_sprites.add(Burger())
            break

def press_potato():  
    for n in range(len(fries)):
        if fries[n]==0:
            food_sprites.add(Fries())
            break
           
def press_egg():  
    for n in range(len(eggs)):
        if eggs[n]==0:
            food_sprites.add(Egg())
            break

def press_cola():  
    global rows1
    if 1 not in cola:
        if rows1>0: 
            rows1-=1
        else:
            rows1=2
        for n in range(len(cola)):
            food_sprites.add(Cola())

def rows():
	global rows1
	return rows1

def is_running(score):
        return score >= 10
game = Game()
