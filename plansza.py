import algorytm_genetyczny as genetic

def obliczPixeleNaPodstawieKratek(wymiar): #Przeliczanie współrzędnych podanych w kratkach na pixele
    i = 1
    pixele = 70
    if wymiar == 0:
        return 0
    else:
        while (i < wymiar):
            pixele = pixele + 70
            i = i + 1
        return pixele

EKRAN_SZEROKOSC = 770
EKRAN_WYSOKOSC = 770
blockSize = 70

x1, y1, x2, y2, x3, y3, x4, y4 = [None] * 8

najlepszy_osobnik = genetic.ewolucja()
print("Generowana plansza:")
genetic.print_board(najlepszy_osobnik)

(x1, y1), (x2, y2), (x3, y3), (x4, y4), (a, b), (c, d) = najlepszy_osobnik[:6] 

x1, x2, x3, x4, y1, y2, y3, y4 = map(int, [x1, x2, x3, x4, y1, y2, y3, y4])

a_pix = obliczPixeleNaPodstawieKratek(a)
b_pix = obliczPixeleNaPodstawieKratek(b)

c_pix = obliczPixeleNaPodstawieKratek(c)
d_pix = obliczPixeleNaPodstawieKratek(d)