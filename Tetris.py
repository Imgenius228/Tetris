import pygame
import time
pygame.init()

back = (200, 255, 255)

mw = pygame.display.set_mode((500, 500))
mw.fill(back)
clock = pygame.time.Clock()

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0\
        
    def append_option(self, option, callback):
        self._option_surfaces.append((option, True, (255, 255, 255)))
        self._callbacks.append(callback)
    
    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))
    
    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            optiin_rect = option.get_rect()
            optiin_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (0, 100, 0), optiin_rect)
            surf.blit(option, optiin_rect)
            
menu = Menu()
menu.append_option('Hello',  lambda: print('Hello'))
menu.append_option('Quit', quit)      
 
menu.draw(str)

racket_x = 200
racket_y = 330

dx = 5
dy = 5

move_right = False 
move_left = False 

game_over = False
class Area():
    def __init__(self, x=0, y=0, width =10, height =10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw,self.fill_color,self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Label(Area):
    def set_text(self, text, fsize = 12, text_color = (0, 0, 0)):
        self.image = pygame.font.SysFont("verdana", fsize).render(text, True, text_color)
    def draw(self, shift_x = 0, shift_y = 0):
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

class Picture(Area):
    def __init__(self, fileame, x = 0, y = 0, width = 10, height = 10):
        Area.__init__(self, x = x, y = y, width = width, height = height, color = None)
        self.image = pygame.image.load(fileame)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

ball = Picture('ball.png', 160, 200, 50, 50)
ball.image = pygame.transform.scale(ball.image, (50, 50))
platform = Picture('platform.png', racket_x, racket_y, 100, 50)
platform.image = pygame.transform.scale(platform.image, (100, 50))


start_x = 6 
start_y = 6
count = 9
monsters = []
for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        d = Picture('1.png', x, y, 50, 50)
        d.image = pygame.transform.scale(d.image, (50, 50))
        monsters.append(d)
        x = x + 55
    count -= 1



while not game_over:
    ball.fill()
    platform.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_a:
                move_left = True 
        
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_a:
                move_left = False   


    if move_right:
        platform.rect.x += 5

    if move_left:
        platform.rect.x -= 5
 
    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1

    if ball.rect.colliderect(platform.rect):
        dy *= -1

    if ball.rect.y > 350:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text("YOU LOSE", 60, (255, 0, 0))
        time_text.draw(10, 10)   
        game_over = True
        

    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text("YOU WIN", 60, (0, 200, 0))
        time_text.draw(10, 10)    
        game_over = True


    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *= -1


    platform.draw() 
    ball.draw()

    pygame.display.update()

    clock.tick(40)
time.sleep(3)