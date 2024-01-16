import pygame

letter_pic = pygame.image.load("images/letter.png")

class Letter(pygame.sprite.Sprite):
    def __init__(self, img_path):
        super().__init__()
        self.img_path = img_path
        self.image = pygame.transform.scale(letter_pic, (40, 40))
        self.rect = self.image.get_rect()
        self.x = 430
        self.y = 400
        self.is_in_move = False

    def narysuj(self, x, y, screen):
        self.x = x
        self.y = y
        screen.blit(self.image, (self.x, self.y))

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)