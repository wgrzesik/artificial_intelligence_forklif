import pygame

MAX_STORAGE = 3

def obliczPixeleNaPodstawieKratek(wymiar): #Przeliczanie współrzędnych podanych w kratkach na pixele
    i = 1
    pixele = 73
    while (i < wymiar):
        pixele = pixele + 70
        i = i + 1
    return pixele

def obliczPixeleDlugosciRegalu(self):   #Przeliczanie dlugości regału podanego w kratkach na pixele
    i = 1
    dlugoscRegalu = 40
    while (i < 1) and (i <= 11 - self.numerKolumny):  #Sprawdzenie, żeby regał nie wychodził poza plansze, jeżeli tak to jest ucinany tak, żeby nie wychodził
        dlugoscRegalu = dlugoscRegalu + 80
        i = i + 1
    return dlugoscRegalu

class Regal(pygame.sprite.Sprite):

    def __init__(self, nazwaRegalu, numerWiersza, numerKolumny):
        super().__init__()
        from ekran import screen
        self.nazwaRegalu = nazwaRegalu
        self.wysokoscRegalu = 64
        self.numerKolumny = numerKolumny
        self.numerWiersza = numerWiersza

        self.wiersz = obliczPixeleNaPodstawieKratek(numerWiersza)
        self.kolumna = obliczPixeleNaPodstawieKratek(numerKolumny)
        self.dlugosc = obliczPixeleDlugosciRegalu(self)

        storage_dolna = []
        storage_gorna = []

        self.dolna = storage_dolna
        self.gorna = storage_gorna

        if(self.nazwaRegalu == 'ogród'):
            reg = pygame.Surface([self.dlugosc, self.wysokoscRegalu])
            reg = pygame.image.load("images/regal.png")
            self.rect = reg.get_rect()
            screen.blit(reg, (self.wiersz, self.kolumna))

        if(self.nazwaRegalu == 'narzedzia'):
            reg = pygame.Surface([self.dlugosc, self.wysokoscRegalu])
            reg = pygame.image.load("images/regal1.png")
            self.rect = reg.get_rect()
            screen.blit(reg, (self.wiersz, self.kolumna))

        if(self.nazwaRegalu == 'kuchnia'):
            reg = pygame.Surface([self.dlugosc, self.wysokoscRegalu])
            reg = pygame.image.load("images/regal2.png")
            self.rect = reg.get_rect()
            screen.blit(reg, (self.wiersz, self.kolumna))
        
        if(self.nazwaRegalu == 'motoryzacja'):
            reg = pygame.Surface([self.dlugosc, self.wysokoscRegalu])
            reg = pygame.image.load("images/regal3.png")
            self.rect = reg.get_rect()
            screen.blit(reg, (self.wiersz, self.kolumna))
    
    def is_dolna_free(self):
        if len(self.dolna) <= MAX_STORAGE:
            return True
        return False
    
    def is_gorna_free(self):
        if len(self.gorna) <= MAX_STORAGE:
            return True
        return False
    
    def czy_na_gornej_wiecej_miejsca(self):
        if len(self.gorna) > len(self.dolna):
            return True
        return False
    
    def put_package_on_the_regal(self, package, where):
        if(where == 0):
            self.dolna.append(package)
        else:
            self.gorna.append(package)