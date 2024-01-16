import sys
import random

import joblib
import pygame
from paczka import Paczka
from letter import Letter
from wozek import Wozek
import wyszukiwanie
import ekran
from grid import GridCellType, SearchGrid
import plansza
import NeuralNetwork.prediction as prediction


from plansza import a_pix, b_pix
pygame.init()


def main():
    wozek = Wozek()
    pred_list = prediction.prediction_keys()
    p1 = Paczka('duzy', 12, 'narzedzia', False, True, False,
                any, any, any, any, any, pred_list[3])
    p2 = Paczka('maly', 1, 'ogród', False, True, False,
                any, any, any, any, any, pred_list[1])
    l1 = Letter(pred_list[0])
    l2 = Letter(pred_list[2])
    ekran.dodaj_na_rampe(p2, l1, p1, l2)
    grid_points = SearchGrid()

    # Odczyt drzewa z pliku
    drzewo = joblib.load('DecisionTree/wyuczone_drzewo.pkl')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    while len(ekran.lista_itemow) > 0:
                        wozek_serves_orders(wozek, grid_points, drzewo)

                if event.key == pygame.K_n:
                    add_another_order(ekran, pred_list)
                    wozek_serves_orders(wozek, grid_points, drzewo)


            if event.type == pygame.MOUSEBUTTONDOWN:
                # lewy przycisk myszy
                if event.button == 1:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    wiersz = ekran.sprawdz_ktory_wiersz(x)
                    kolumna = ekran.sprawdz_ktora_kolumna(y)

                    docelowy_stan = wyszukiwanie.Stan(
                        wiersz * 70, kolumna * 70, 1)

                    # wezel = wyszukiwanie.wyszukiwanie_bfs(wozek.obecnyStan, docelowy_stan, grid_points)
                    wezel = wyszukiwanie.wyszukiwanie_a_star(
                        wozek.obecnyStan, docelowy_stan, grid_points)
                    sciezka = wyszukiwanie.znajdz_sciezke(wezel)
                    wozek.przemiesc_wozek_po_sciezce(sciezka)

        ekran.odswiez_ekran(wozek)




def wozek_serves_orders(wozek, grid_points, drzewo):
    # wozek jedzie po itemy
    wiersz = ekran.sprawdz_ktory_wiersz(a_pix)
    kolumna = ekran.sprawdz_ktora_kolumna(b_pix)
    docelowy_stan = wyszukiwanie.Stan(wiersz * 70, kolumna * 70, 1)

    # wezel = wyszukiwanie.wyszukiwanie_bfs(wozek.obecnyStan, docelowy_stan, grid_points)
    wezel = wyszukiwanie.wyszukiwanie_a_star(
        wozek.obecnyStan, docelowy_stan, grid_points)
    sciezka = wyszukiwanie.znajdz_sciezke(wezel)
    wozek.przemiesc_wozek_po_sciezce(sciezka)

    # sprawdzenie czy lista itemow nie jest pusta
    if ekran.lista_itemow:
        if grid_points.grid[(wiersz, kolumna)] is GridCellType.PLACE:  # picks up item
            if wozek.ln == 0:
                wozek.picks_up_item()
                wozek.dynamic_wozek_picture()

                przenoszony_item = wozek.storage[-1]
                if (prediction.predict_one(przenoszony_item.img_path) == 'package'):
                    # wozek jedzie odlozyc paczke na regal
                    przenoszona_paczka = przenoszony_item

                    array, reg = przenoszona_paczka.tablica_do_drzewa(
                        przenoszona_paczka.kategoria)

                    predictions = drzewo.predict([array])

                    if predictions == 0:
                        print('odklada na dolna polke!')
                    else:
                        print('odklada na gorna polke!')

                    docelowy_stan = wyszukiwanie.Stan(
                        reg.numerWiersza * 70, reg.numerKolumny * 70, 1)
                    wezel = wyszukiwanie.wyszukiwanie_a_star(
                        wozek.obecnyStan, docelowy_stan, grid_points)
                    sciezka = wyszukiwanie.znajdz_sciezke(wezel)
                    wozek.przemiesc_wozek_po_sciezce(sciezka)

                    if wozek.ln != 0:   # drops package
                        wozek.drops_package(
                            przenoszona_paczka, reg, predictions)
                        wozek.dynamic_wozek_picture()
                else:
                    # list przenoszony do skrzynki
                    docelowy_stan = wyszukiwanie.Stan(
                        plansza.c_pix, plansza.d_pix, 1)
                    wezel = wyszukiwanie.wyszukiwanie_a_star(
                        wozek.obecnyStan, docelowy_stan, grid_points)
                    sciezka = wyszukiwanie.znajdz_sciezke(wezel)
                    wozek.przemiesc_wozek_po_sciezce(sciezka)

                    if wozek.ln != 0:   # drops letter
                        wozek.drops_letter(przenoszony_item)
                        wozek.dynamic_wozek_picture()

def add_another_order(ekran, pred_list):
    if random.random() < 0.5:
        if random.random() < 0.5:
            order = Paczka('duzy', 12, 'motoryzacja', False, True, False,
                any, any, any, any, any, pred_list[6])
        else:
            order = Paczka('maly', 1, 'kuchnia', False, True, False,
                any, any, any, any, any, pred_list[7])
    else:
        if random.random() < 0.5:
            order = Letter(pred_list[5])
        else:
            order = Letter(pred_list[4])
    
    ekran.dodaj_na_rampe_jedno(order)
        

if __name__ == "__main__":
    main()
