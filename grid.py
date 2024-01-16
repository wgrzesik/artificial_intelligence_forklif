from enum import Enum
from plansza import x1,x2,x3,x4,y1,y2,y3,y4
import plansza

from typing import Tuple, Dict

class GridCellType(Enum):
    FREE = 0
    RACK = 1
    PLACE = 2


class SearchGrid:
    grid: Dict[Tuple[int, int], GridCellType] = {}

    def __init__(self) -> None:
        self._init_grid()

    def _init_grid(self) -> None:
        for i in range (0,14):
            for j in range(0,14):
                self.grid[(i, j)] = GridCellType.FREE
        for c, d in [(x1, y1), (x1, y1+1), (x1+1, y1), (x1+1, y1+1), (x2, y2), (x2+1, y2), (x2, y2+1), (x2+1, y2+1),
                     (x3, y3), (x3+1, y3), (x3, y3+1), (x3+1, y3+1), (x4, y4), (x4+1, y4), (x4, y4+1), (x4+1, y4+1),]:
            self.grid[(c,d)] = GridCellType.RACK
        for e, f in [(plansza.a, plansza.b),(plansza.c, plansza.d)]:
            self.grid[(e,f)] = GridCellType.PLACE