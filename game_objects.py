# imports 
import pygame
import random
import os 

# Initilizations
bird_state1 = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird_initial_state.png")))
bird_state2 = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird_second_state.png")))
bird_state3 = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird_final_state.png")))

bird_states = [bird_state1, bird_state2, bird_state3]
pipe = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "piping.png")))
background = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "background.png")))
base = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))

pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)

class Bird: 
    imgs = bird_states
    max_rotation = 25
    rotation_velocity = 20
    animation_time = 5 
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.imgs[0]
    
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        d = self.velocity * self.tick_count + 1.5 * self.tick_count**2  # representing arc for when the bird is jumping 
        
        if d >= 16: 
            d = d/abs(d) * 16 
            
        if d < 0: 
            d -= 2 # if moving upwards, lets move a little bit more 
            
        # up/down movemement update
        self.y = self.y + d 
        
        # bird tilt 
        if d < 0 or self.y < self.height + 50: 
            if self.tilt < self.max_rotation: 
                self.tilt = self.max_rotation
        else: 
            if self.tilt > -90:
                self.tilt -= self.rotation_velocity
                
    def draw(self, window): 
        self.img_count += 1 
        # bird flapping (of wings)
        if self.img_count < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_time*2: 
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*3: 
            self.img = self.imgs[2]
        elif self.img_count < self.animation_time*4: 
            self.img = self.imgs[1]
        elif self.img_count == self.animation_time*4 + 1: 
            self.img = self.imgs[0] 
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.animation_time*2 

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe: 
    gap = 192
    velocity = 5
    
    def __init__(self, x): 
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe, False, True)
        self.pipe_bottom = pipe
        
        self.passed = False
        self.set_height() 
        
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap
    
    def move(self):
        self.x -= self.velocity
        
    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))
        
    def collide(self, bird):
        # pixel perfect collission
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        
        if t_point or b_point: 
            return True
        
        return False
    
class Base:
    velocity = 5 
    width = base.get_width()
    img = base 
    
    def __init__(self, y):
        self.y = y 
        self.x1 = 0 
        self.x2 = self.width 
        
    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity
        
        # once the original base image moves out of the screen
        # cycle it to the back 
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
            
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
        
    def draw(self, window):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))
        text = font.render(self.text, 1, (255, 255, 255))
        window.blit(text, (self.x + (self.width // 2) - (text.get_width() // 2),
                           self.y + (self.height // 2) - (text.get_height() // 2)))

    def click(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height