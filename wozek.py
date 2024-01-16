import ekran
import pygame
from ekran import lista_itemow
from letter import Letter
import plansza

listOfPackages = lista_itemow

class Wozek(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.obecnyStan = None
        self.height = 64
        self.width = 64
        # Credit: Forklift icons created by Smashicons - Flaticon
        # https://www.flaticon.com/free-icons/forklift
        self.image = pygame.image.load("images/pusty_wozek.png")
        self.rect = self.image.get_rect()
        self.__zainicjuj_stan_poczatkowy()

    def draw(self):
        ekran.screen.blit(self.image, (self.obecnyStan.x, self.obecnyStan.y))

    storage = []
    max_size = 10
    ln = len(storage)

    def dynamic_wozek_picture(self):
        if self.ln == 0:
            self.image = pygame.image.load("images/pusty_wozek.png")
        elif ((self.ln > 0) and (self.ln < 4)):
            self.image = pygame.image.load("images/pelny_wozek_1_crate.png")
        elif ((self.ln > 3) and (self.ln < 10)):
            self.image = pygame.image.load("images/pelny_wozek_2_crates.png")
        elif (self.ln == 10):
            self.image = pygame.image.load("images/pelny_wozek_full_3_crates.png")
        
        self.rect = self.image.get_rect()           

    def __zainicjuj_stan_poczatkowy(self):
        from wyszukiwanie import Stan
        self.obecnyStan = Stan(0, 0, 1)

    def przemiesc_wozek_po_sciezce(self, sciezka):
        kierunek_poprzedni = self.obecnyStan.kierunek
        for wezel in sciezka:
            self.obecnyStan = wezel.stan
            kierunek_obecny = self.obecnyStan.kierunek
            self.ustaw_wozek_w_kierunku(kierunek_obecny, kierunek_poprzedni)
            kierunek_poprzedni = kierunek_obecny
            ekran.odswiez_ekran(self)
            pygame.time.wait(500)

    def ustaw_wozek_w_kierunku(self, kierunek_obecny, kierunek_poprzedni):
        if kierunek_poprzedni < kierunek_obecny:
            # obrot w lewo
            if kierunek_poprzedni == 0 and kierunek_obecny == 3:
                self.image = pygame.transform.rotate(self.image, 90)
            # obrot w prawo
            else:
                self.image = pygame.transform.rotate(self.image, -90)
        elif kierunek_poprzedni > kierunek_obecny:
            # obrot w prawo
            if kierunek_poprzedni == 3 and kierunek_obecny == 0:
                self.image = pygame.transform.rotate(self.image, -90)
            # obrot w lewo
            else:
                self.image = pygame.transform.rotate(self.image, 90)
    
    def picks_up_item(self):
        item_pop = ekran.lista_itemow.pop()
        if isinstance(item_pop,Letter):
            ekran.lista_listow_w_skrzynce.append(item_pop)
            item_pop.is_in_move = True
            self.storage.append(item_pop)
            self.ln = self.ln + 1
        else:
            ekran.lista_paczek_na_regalach.append(item_pop)
            item_pop.is_in_move = True
            self.storage.append(item_pop)
            self.ln = self.ln + 1
    
    def drops_package(self, paczka, reg, predictions):
        paczka.update_position(reg.numerWiersza*70, reg.numerKolumny*70)
        paczka.is_in_move = False
        self.storage.pop()
        self.ln = self.ln - 1
        reg.put_package_on_the_regal(paczka, predictions)

    def drops_letter(self, letter):
        letter.update_position(plansza.c_pix, plansza.d_pix)
        letter.is_in_move = False
        self.storage.pop()
        self.ln = self.ln - 1

