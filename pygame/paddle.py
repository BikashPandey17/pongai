import pygame
BLACK = (0,0,0)

class Paddle(pygame.sprite.Sprite):
    #This class represents a paddle. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the paddle, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def __str__(self):
        # returns the center (x,y) coordinates of the paddle
        return f"{self.rect.x}, {self.rect.y}"

    def moveUp(self, pixels):
        self.rect.y -= pixels
		#Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
	    #Check that you are not going too far (off the screen)
        if self.rect.y > 400:
          self.rect.y = 400
    
    def action(self, choice):
        '''
        Gives us 2 total movement options. (0,1)
        '''
        if choice == 0:
            self.moveUp(5)
        elif choice == 1:
            self.moveDown(5)