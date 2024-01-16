import random

EKRAN_SZEROKOSC = 770
EKRAN_WYSOKOSC = 770
blockSize = 70
LICZBA_REGALOW = 4
LICZBA_MIEJSC_NA_PACZKE = 1
LICZBA_SKRZYNEK_NA_LISTY = 1

ROZMIAR_POPULACJI = 100
LICZBA_GENERACJI = 100


def wygeneruj_osobnika(zasieg_wspolrzednych, ilosc_wspolrzednych):
    osobnik = list()
    for j in range(ilosc_wspolrzednych):
        x = random.randint(1, zasieg_wspolrzednych)
        y = random.randint(1, zasieg_wspolrzednych)
        e = (x, y)
        osobnik.append(e)
    return osobnik


def wygeneruj_populacje_poczatkowa(liczebnosc_populacji):
    populacja = list()
    zasieg = int((EKRAN_WYSOKOSC / blockSize) - 3)
    ilosc_wspolrzednych = (LICZBA_REGALOW + LICZBA_MIEJSC_NA_PACZKE + LICZBA_SKRZYNEK_NA_LISTY)
    for i in range(liczebnosc_populacji):
        osobnik = wygeneruj_osobnika(zasieg, ilosc_wspolrzednych)
        while osobnik in populacja:
            osobnik = wygeneruj_osobnika(zasieg, ilosc_wspolrzednych)
        populacja.append(osobnik)
    return populacja


def ocena_osobnika(osobnik):
    ocena = 0

    # Czy koordynaty sie nie powtarzaja
    if len(osobnik) == len(set(osobnik)):
        ocena += 10
    else:
        ocena -= 10

    # Czy zachowany jest minimalny dystans miedzy koordynatami
    for i in range(len(osobnik)):
        for j in range(i + 1, len(osobnik)):
            x1, y1 = osobnik[i]
            x2, y2 = osobnik[j]
            distance = max(abs(x2 - x1), abs(y2 - y1))
            if distance >= 3:
                ocena += 10
            else: 
                ocena -= 10

    return ocena

def mutacja(osobnik):
    # mutacja poprzez zamiane randomowej pary koordynatow
    index_osobnika = random.randint(0, len(osobnik) - 1)
    x = random.randint(1, (EKRAN_SZEROKOSC / blockSize) - 3)
    y = random.randint(1, (EKRAN_WYSOKOSC / blockSize) - 3)
    osobnik[index_osobnika] = (x, y)

def krzyzowanie(rodzic1, rodzic2):
    # krzyzowanie pomiedzy dwojka rodzicow i tworzenie dziecka
    dziecko = []
    for i in range(len(rodzic1)):
        dziecko.append(rodzic1[i] if random.random() < 0.5 else rodzic2[i])
    return dziecko

def ewolucja():

    populacja = (wygeneruj_populacje_poczatkowa(ROZMIAR_POPULACJI))

    for i in range(LICZBA_GENERACJI):

        # sortowanie populacji wynikami oceny osobnikow
        populacja = sorted(populacja, key=lambda x: ocena_osobnika(x), reverse=True)

        # wybranie jedynie najlepszych osobnikow
        rodzice = populacja[:int(ROZMIAR_POPULACJI * 0.2)]

        # stworz nowa generacje poprzez krzyzowanie i mutacje
        potomek = rodzice[:]
        while len(potomek) < ROZMIAR_POPULACJI:
            rodzic1 = random.choice(rodzice)
            rodzic2 = random.choice(rodzice)
            dziecko = krzyzowanie(rodzic1, rodzic2)
            mutacja(dziecko)
            potomek.append(dziecko)

        populacja = potomek

    return populacja[0]

def print_board(osobnik):
    board = [['-' for _ in range(EKRAN_SZEROKOSC // blockSize)] for _ in range(EKRAN_WYSOKOSC // blockSize)]

    for x, y in osobnik:
        if 0 <= x < EKRAN_SZEROKOSC // blockSize and 0 <= y < EKRAN_WYSOKOSC // blockSize:
            board[y][x] = 'X'

    for row in board:
        print(' '.join(row))

# uruchomienie algorytmu genetycznego
# najlepszy_osobnik = ewolucja()
# print_board(najlepszy_osobnik)