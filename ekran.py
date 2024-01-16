import pygame
import plansza
from regal import Regal
from itemList import *

EKRAN_SZEROKOSC = 770
EKRAN_WYSOKOSC = 770
screen = pygame.display.set_mode((EKRAN_SZEROKOSC, EKRAN_WYSOKOSC))
miejsce = pygame.image.load('images/miejsce_paczek.png')
miejsce = pygame.transform.scale(miejsce, (70, 70))
skrzynka = pygame.image.load('images/letterbox.png')
skrzynka = pygame.transform.scale(skrzynka, (64, 64))
pygame.display.set_caption("Inteligentny wozek")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

lista_itemow = []
lista_paczek_na_regalach = []
lista_listow_w_skrzynce = []
        
def narysuj_regaly():
    global lista_regalow
    r1 = Regal('ogród', plansza.x1, plansza.y1)
    r2 = Regal('ogród', plansza.x1, plansza.y1+1)
    r3 = Regal('ogród', plansza.x1+1, plansza.y1)
    r4 = Regal('ogród', plansza.x1+1, plansza.y1+1)

    r5 = Regal('narzedzia', plansza.x2, plansza.y2)
    r6 = Regal('narzedzia', plansza.x2, plansza.y2+1)
    r7 = Regal('narzedzia', plansza.x2+1, plansza.y2)
    r8 = Regal('narzedzia', plansza.x2+1, plansza.y2+1)

    r9 = Regal('kuchnia', plansza.x3, plansza.y3)
    r10 = Regal('kuchnia', plansza.x3, plansza.y3+1)
    r11 = Regal('kuchnia', plansza.x3+1, plansza.y3)
    r12 = Regal('kuchnia', plansza.x3+1, plansza.y3+1)

    r13 = Regal('motoryzacja', plansza.x4, plansza.y4)
    r14 = Regal('motoryzacja', plansza.x4, plansza.y4+1)
    r15 = Regal('motoryzacja', plansza.x4+1, plansza.y4)
    r16 = Regal('motoryzacja', plansza.x4+1, plansza.y4+1)

    lista_regalow = [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16]

def zwroc_regaly_kategoria(kategoria):
    lista_reg = []
    for reg in lista_regalow:
        if reg.nazwaRegalu == kategoria:
            lista_reg.append(reg)
    return lista_reg

def narysuj_siatke():
    blockSize = 70  # Set the size of the grid block
    WHITE = (200, 200, 200)
    for x in range(0, EKRAN_SZEROKOSC, blockSize):
        for y in range(0, EKRAN_WYSOKOSC, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, WHITE, rect, 1)


def odswiez_ekran(wozek):
    screen.fill((51, 51, 51)) # removes object trail
    screen.blit(miejsce,(plansza.a_pix, plansza.b_pix))
    screen.blit(skrzynka,(plansza.c_pix, plansza.d_pix))
    narysuj_siatke()
    narysuj_items()
    narysuj_paczke_na_regale()
    narysuj_regaly()
    wozek.draw()
    pygame.display.flip()


def sprawdz_ktory_wiersz(x):
    nr_wiersza = 0
    for i in range(70, EKRAN_WYSOKOSC + 70, 70):
        if x < i:
            return nr_wiersza
        nr_wiersza = nr_wiersza + 1


def sprawdz_ktora_kolumna(y):
    nr_kolumny = 0
    for i in range(70, EKRAN_SZEROKOSC + 70, 70):
        if y < i:
            return nr_kolumny
        nr_kolumny = nr_kolumny + 1


def narysuj_items():
    for item in lista_itemow:
        item.narysuj(item.x, item.y, screen)

def narysuj_paczke_na_regale():
    for paczka in lista_paczek_na_regalach:
        if paczka.is_in_move is False:
            paczka.narysuj(paczka.x, paczka.y, screen)

def narysuj_list_na_skrzynce():
    for letter in lista_listow_w_skrzynce:
        if letter.is_in_move is False:
            letter.narysuj(letter.x, letter.y, screen)

def dodaj_na_rampe(p1, p2, l1, l2):
    lista_itemow.append(p1)
    lista_itemow.append(p2)
    lista_itemow.append(l1)
    lista_itemow.append(l2)
    p1.update_position(plansza.a_pix, plansza.b_pix)
    p2.update_position(plansza.a_pix, plansza.b_pix)
    l1.update_position(plansza.a_pix, plansza.b_pix)
    l2.update_position(plansza.a_pix, plansza.b_pix)

def dodaj_na_rampe_jedno(order):
    lista_itemow.append(order)
    order.update_position(plansza.a_pix, plansza.b_pix)