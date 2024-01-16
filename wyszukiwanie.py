from grid import GridCellType
import heapq


class Stan:
    def __init__(self, x, y, kierunek):
        self.x = x
        self.y = y
        self.kierunek = kierunek

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.kierunek == other.kierunek


class Wezel:
    def __init__(self, stan, waga=0, g=0, h=0, rodzic=None, ):
        self.stan = stan
        self.waga = waga
        self.g = g  # koszt dotarcia do wezla
        self.h = h  # heurystyka
        self.rodzic = rodzic
        self.f = g + h  # koszt calkowity

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.stan == other.stan


def znajdz_nastepcow(wezel, search_grid, ktory_algorytm):
    # gora -> prawo -> dol -> lewo          | obrot w prawo
    # gora -> lewo -> dol -> prawo          | obrot w lewo
    # 0 gora 1 prawo 2 dol 3 lewo
    x = wezel.stan.x
    y = wezel.stan.y
    obrot_w_prawo = Wezel(Stan(x, y, (wezel.stan.kierunek + 1) % 4))
    obrot_w_prawo.rodzic = wezel
    obrot_w_prawo.waga = 1
    obrot_w_lewo = Wezel(Stan(x, y, 3 if wezel.stan.kierunek == 0 else wezel.stan.kierunek - 1))
    obrot_w_lewo.rodzic = wezel
    obrot_w_lewo.waga = 1
    if wezel.stan.kierunek == 0:
        y -= 70
    elif wezel.stan.kierunek == 1:
        x += 70
    elif wezel.stan.kierunek == 2:
        y += 70
    elif wezel.stan.kierunek == 3:
        x -= 70

    wezly = [obrot_w_prawo, obrot_w_lewo]
    ruch_w_przod = Wezel(Stan(x, y, wezel.stan.kierunek))
    ruch_w_przod.rodzic = wezel
    # sprawdzenie czy nie wyjdzie poza plansze
    if 0 <= x <= 910 and 0 <= y <= 910:
        if ktory_algorytm == 1:
            x1 = x / 70
            y1 = y / 70
            if search_grid.grid[(x1, y1)] is GridCellType.FREE or search_grid.grid[(x1, y1)] is GridCellType.PLACE:
                wezly.append(ruch_w_przod)
        else:
            wezly.append(ruch_w_przod)
    return wezly


def wyszukiwanie_bfs(stan_poczatkowy, stan_docelowy, search_grid):
    pierwszy_wezel = Wezel(stan_poczatkowy)
    fringe = [pierwszy_wezel]
    odwiedzone = [pierwszy_wezel]
    while fringe:
        wezel = fringe.pop(0)
        if stan_docelowy.x == wezel.stan.x and stan_docelowy.y == wezel.stan.y:
            return wezel
        lista1 = znajdz_nastepcow(wezel, search_grid, 1)
        for obecny_wezel in lista1:
            if obecny_wezel in odwiedzone:
                continue
            fringe.append(obecny_wezel)
            odwiedzone.append(obecny_wezel)
    return None


def znajdz_sciezke(wezel):
    sciezka = []
    while wezel:
        sciezka.append(wezel)
        wezel = wezel.rodzic
    sciezka.reverse()
    return sciezka


def oblicz_heurystyke(obecnyStan, docelowyStan):
    dx = abs(obecnyStan.x - docelowyStan.x)
    dy = abs(obecnyStan.y - docelowyStan.y)
    return dx + dy


def wyszukiwanie_a_star(poczatkowyStan, docelowyStan, search_grid):
    fringe = []
    heapq.heapify(fringe)

    odwiedzone = list()

    heapq.heappush(fringe, Wezel(poczatkowyStan))
    while fringe:
        obecny_wezel = heapq.heappop(fringe)

        if obecny_wezel.stan == docelowyStan:
            return obecny_wezel

        odwiedzone.append(obecny_wezel)

        nastepcy = znajdz_nastepcow(obecny_wezel, search_grid, 2)
        for nastepca in nastepcy:
            dobierz_wage_do_wezla(nastepca, search_grid)
            h = oblicz_heurystyke(nastepca.stan, docelowyStan)
            g = nastepca.waga + obecny_wezel.g
            f = g + h

            if nastepca not in fringe and nastepca not in odwiedzone:
                nastepca.f = f
                nastepca.g = g
                nastepca.h = h
                heapq.heappush(fringe, nastepca)
            elif nastepca in fringe:
                index = fringe.index(nastepca)
                stary_koszt = fringe[index].f
                if stary_koszt > f:
                    nastepca.f = f
                    nastepca.g = g
                    nastepca.h = h
                    fringe[index] = nastepca
                    # print(index)
                    # heapq.heapify(fringe)
    return None


def dobierz_wage_do_wezla(wezel, search_grid):
    # sprawdzenie czy to obrot
    if wezel.waga == 1:
        return None
    x1 = wezel.stan.x / 70
    y1 = wezel.stan.y / 70
    if search_grid.grid[(x1, y1)] is GridCellType.FREE:
        wezel.waga = 1
    elif search_grid.grid[(x1, y1)] is GridCellType.RACK:
        wezel.waga = 99999
    elif search_grid.grid[(x1, y1)] is GridCellType.PLACE:
        wezel.waga = 500

    return None
