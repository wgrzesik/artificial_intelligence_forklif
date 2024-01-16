import pygame

class listOfItems:
    list = []
    item_group = pygame.sprite.Group()

    def add(self, item):
        self.list.append(item)
        self.item_group.add(item)

    def remove(self):
        last_item = self.list.pop()
        self.item_group.remove(last_item)