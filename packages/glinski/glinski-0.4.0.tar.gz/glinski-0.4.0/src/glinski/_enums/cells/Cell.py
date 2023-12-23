import enum as _enum

import isometric as _iso

from glinski._enums import pieces
from glinski._enums.cells.Column import Column
from glinski._enums.PlayerColor import PlayerColor

from .CellColor import CellColor

__all__ = ['Cell']

BLACKSNATIVES = dict()
BLACKSNATIVES['c8'] = 'r'
BLACKSNATIVES['d9'] = 'n'
BLACKSNATIVES['e10'] = 'q'
BLACKSNATIVES['f9'] = 'b'
BLACKSNATIVES['f10'] = 'b'
BLACKSNATIVES['f11'] = 'b'
BLACKSNATIVES['g10'] = 'k'
BLACKSNATIVES['h9'] = 'n'
BLACKSNATIVES['i8'] = 'r'
for column in Column:
    if column in [Column.a, Column.l]:
        continue
    c = column.name
    BLACKSNATIVES[f"{c}7"] = 'p'
NATIVES = dict()

BLACKPROMOTIONS = dict()
for column in Column:
    c = column.name
    BLACKPROMOTIONS[f"{c}1"] = PlayerColor.BLACK
PROMOTIONS = dict()

class BaseCell:
    def column(self):
        return self.name[0]
    def row(self):
        return int(self.name[1:])
    def cellColor(self):
        desc = self.value.description()
        residue = (sum(desc) + 1) % 3
        value = residue / 2
        ans = CellColor(value)
        return ans
    def hflip(self):
        cls = type(self)
        return cls(self.value.hflip())
    def vflip(self):
        cls = type(self)
        return cls(self.value.vflip())
    def native(self):
        return NATIVES.get(self)
    def promotion(self):
        return PROMOTIONS.get(self)
        



dictionary = dict()
for i, c in enumerate("abcdefghikl"):
    x = min(0, 5 - i)
    y = min(0, i - 5)
    for r in range(1, x + y + 12):
        z = r - 6
        dictionary[f"{c}{r}"] = _iso.Vector(x, y, z)
Cell = _enum.Enum('Cell', dictionary, type=BaseCell)


for k, v in BLACKSNATIVES.items():
    blacksCell = Cell[k]
    blacksPieceKind = pieces.PieceKind[v]
    NATIVES[blacksCell] = blacksPieceKind
    whitesCell = blacksCell.vflip()
    whitesPieceKind = blacksPieceKind.invert()
    NATIVES[whitesCell] = whitesPieceKind

for k, v in BLACKPROMOTIONS.items():
    blacksCell = Cell[k]
    PROMOTIONS[blacksCell] = PlayerColor.BLACK
    whitesCell = blacksCell.vflip()
    PROMOTIONS[whitesCell] = PlayerColor.WHITE
