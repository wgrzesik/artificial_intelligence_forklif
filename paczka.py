from etykieta import Etykieta
import pygame
import ekran


class Paczka(pygame.sprite.Sprite):
    def __init__(self, rozmiar, waga, kategoria, priorytet, ksztalt, kruchosc, nadawca, adres, imie, nazwisko, telefon, img_path):
        super().__init__()
        self.rozmiar = rozmiar
        self.image = pygame.image.load("images/paczka.png")
        self.rect = self.image.get_rect()
        if rozmiar == 'duzy':
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.szerokosc = 50
            self.wysokosc = 50
        elif rozmiar == 'sredni':
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.szerokosc = 35
            self.wysokosc = 35
        elif rozmiar == 'maly':
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.szerokosc = 20
            self.wysokosc = 20
        else:
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.szerokosc = 20
            self.wysokosc = 20
            self.rozmiar = 'undefined'
        self.waga = waga
        self.kategoria = kategoria
        self.priorytet = priorytet
        self.ksztalt = ksztalt
        self.kruchosc = kruchosc
        self.img_path = img_path
        self.x = 430
        self.y = 400
        self.label = Etykieta(nadawca, adres, imie, nazwisko, telefon, priorytet)
        self.is_in_move = False

    # zmienia rozmiar obrazka w zaleznosci od rozmiaru
    def __dobierz_rozmiar_obrazka(self):
        if self.rozmiar == "duzy":
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.szerokosc = 50
            self.wysokosc = 50
            return 1
        elif self.rozmiar == "sredni":
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.szerokosc = 35
            self.wysokosc = 35
            return 1
        elif self.rozmiar == "maly":
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.szerokosc = 20
            self.wysokosc = 20
            return 1
        else:
            return 0

    def narysuj(self, x, y, screen):
        self.x = x
        self.y = y
        if self.__dobierz_rozmiar_obrazka() == 1:
            screen.blit(self.image, (self.x, self.y))
        else:
            print("Zmien rozmiar paczki")
            print("Paczka moze miec rozmiar duzy, sredni lub maly")
            exit(0)

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
    
    def tablica_do_drzewa(self, kategoria):
        tablica = []
        # rozmiar
        if self.rozmiar == 'maly':
            tablica.append(0)
        elif self.rozmiar == 'sredni':
            tablica.append(1)
        else: tablica.append(2)

        # waga
        if self.waga <= 2:
            tablica.append(0)
        elif self.waga <= 10:
            tablica.append(1)
        else: tablica.append(2)

        # piorytet
        if self.priorytet is True:
            tablica.append(1)
        else: tablica.append(0)

        # kształt
        if self.ksztalt is True:
            tablica.append(1)
        else: tablica.append(0)           

        # kruchość
        if self.kruchosc is True:
            tablica.append(1)
        else: tablica.append(0)

        reg = ekran.zwroc_regaly_kategoria(kategoria)
        # czy dolna wolna
        if reg[0].is_dolna_free() is True:
            tablica.append(1)
        else: 
            tablica.append(0)

        #czy górna wolna
        if reg[0].is_dolna_free() is True:
            tablica.append(1)
        else: 
            tablica.append(0)
        
        # czy na górnej więcej miejsca
        if reg[0].czy_na_gornej_wiecej_miejsca() is True:
            tablica.append(1)
        else: 
            tablica.append(0)

        return tablica, reg[0]