# run: python chess_game.py
# requires: pip install pygame

import pygame
import sys
import copy
import base64
import io

# ---------------------------------------------------------------------------
# Embedded chess-symbol font (12-glyph subset of Apple Symbols, ~4.5 KB)
# Subsetted with fonttools so only U+2654-U+265F are included.
# Loaded entirely from memory -- no temp files, no system-font dependency.
# ---------------------------------------------------------------------------
_CHESS_FONT_B64 = (
    "AAEAAAALAIAAAwAwT1MvMs7OgtUAAA+0AAAAYGNtYXAADEziAAAQFAAAAChnbHlmpSIs2wAAALwA"
    "AA4qaGVhZM8JjwoAAA8kAAAANmhoZWEb/BWEAAAPkAAAACRobXR4UBoHsQAAD1wAAAA0bG9jYRff"
    "G40AAA8IAAAAHG1heHAA3wYHAAAO6AAAACBuYW1lFoAxOQAAEDwAAAFKcG9zdP9tAGQAABGIAAAA"
    "IHByb3AADQALAAARqAAAABAABwCw/tMFogT6AAoAFAAeAEkAVABfAGgAAAUmJiMiBxYzFxcyNycm"
    "IyIHBzYzMjcnJiMiBwc2MzIBBiMvAiYnEyY1NDYzMhcmNTQ3Jwc3FzU3FxcVJwcWFRQHNjYzMhYV"
    "FAcnNjU0JiMiAhEyFwU2MzcQISIGFRQWJTY1NCYjIhUUBGtQkYKaiIBeZGVchgWct5SUB6WacsoM"
    "o6x4jgyXgp4BGq6+KXVcXnIa+7KJQ20TewFcAVtUAlpaAXQdQFU6hp/2XP55VI+URlP+DV1IUv7j"
    "Xn6EAaVQLSRO1SAWNBACAV5CKCRGI2lsGxdrH/7HHAEGBAQRAbXvzomySTgpVAtMAUUBUgJTAUYB"
    "Sw9TM0M2JquR4NMn5LZZgP7I/tUIBA0CAmCCYljL492BKzhpiQAADwCt/ukGbQTRAAwAFgAgACoA"
    "LgAyADgAPABAAEsAVgBiAG0AeAC+AAAFJiMiBgcHFjM3NzI3JyYjIgcHNjMyFycmIyIHFTYzMhc3"
    "JiMiBxc2MzIXNxMDFicTAxYnAwM2MzIHAxM2BwMTNgEmBhUUFjMyNjU0JSIGFRQzMjY1NCYlIgYV"
    "FBYzMjY1NCYFIgYVFBYzMjY1NAUiBhUUFjMyNjU0AQYjIic2NTQnAyI1NDYzMhYVFAcTAyY1NDYz"
    "MhYVFAcTEyY1NDYzMhYVFAcTEyY1NDYzMhYVFAcDEyY1NDYzMhYVFAcDFATnmrWGkFgDvIZxWRak"
    "EKerrqkDoqq+qQe3nqaqpaKotQStrKSvBKO7oKgfkO4yQxi3UF1VVzMiGX22F09j644vA7UYJCMX"
    "GCP+nBYhOhkkJv6iGSQkGRkjI/6gGiUkGRkj/p8YJCQYGSID5OnN68UjBceBSy0qQS3oDmlDLy1D"
    "PKFMS0EuL0ZQTaE7QTEvQm0P6yxFLy9BgdCpMxQeJhICAw2kOjhMMzjLOTpGNjnHNDRRNjmEAYf+"
    "lwwQAfz+HwkKAlv9pwMFAej9/RIVAXD+bhUCoQEjFxkjJBg2lyMYPCEXGiVVIxkYISIXGSNaIxgZ"
    "IiIYPJAjGBgkIxk7+08YGdKLJ1ICLWkwUEcuJDT+oAHcE1suQ0MuLzL+SwIBKEEvQ0IuQir+AAG2"
    "MCszREEvWBn+JAFhOCEsQUQyXQj9vfwAAAcA0/7eBawEcgAbAB8AIwAnACsANwA7AAABBTUzJzM3"
    "EycnETMXNzUhFTMnMwMnBwMfAjMHNQUVJTchByUnJQclEyERAScjFyUnBxUFNSMXBTcFFwWs+ydd"
    "ATCaAWdMxQGeATSQAc8BSmMBlisBWkP7rgP2AfxqAQNhSf1wTQKYAf32AsMBXAH/AALB/vJXAQLj"
    "P/1DPf7gAsGGmwIpZgEBH2cBZ2Zo/t0CZf3RlgKHiVMBUohRUIlLAU2DAjP9ywLirmUBZAFjAmWs"
    "ekABPwAIAK7+0wYTBQ0AQwBNAFwAaAByAHoAjACeAAABJiYjIgcGIyInNQcVBiMiJyYjIgc3NjMy"
    "FxYzNjcmJic3JjU0NjcmNTQ2MzIWFRQHFhcWFRQGBxcGBgcWMzI3NjMyFwEiBhUUMzI2JyYTNjU0"
    "JicGBwYVFBc2MzInJzUjNRc3NxczFycTJyYjIgcHNjMyFyYjIgcWMzIFNyYjIgcGIyInFxYzMjc2"
    "MzIFNwYjIicmIyIHFTYzMhcWMzIGEU/GPQh9FxQ8YSJhOx8dcQl03AHFwRAVlgIQKGVkUFSr1LhQ"
    "Pi0uP1LTZlVaVFNcY11CHQhoHyKa1v1TGCQ5GiMBA6mOx6e9X1mNgGRlMWufngFrApUBlr42dkZM"
    "djeIb2ObjmNxnZloaAIjBMd/JiNqCR1BAUMrGR17Cmz+BgI4FAOIHR+StraMHEotIR7+0ztSEwQx"
    "aAFnLwQRhYl7BCECJhEhKuSKxJv2OyFAL0E/LUUfQpB5h1yqQecuHgonGQh+BXsjGDgjGTf8b4qW"
    "ld8nMXpxf5eKL3gBanECcwF1bwH+I5YkJJUoXS4uPe0sZggWGSYZBRUEJhgaBmIvYw4IAAQAgv7c"
    "BZAEsQA4AHYAggCIAAABJSY1NDY3NzY3BgYHBiMiJzY3BiMiJyY1NBM2Nzc2NyYnJjc2MzIXNzY1"
    "NTQ3MhcWFhcWFhcAERQHNjU0AicmJic0JicWFRQHBgcmJwYVFBcWBwYHBgYHBgcGFRQXNjcXFzY3"
    "NjY3Bgc2NjcWFRQHFhUUBwYGBxMGBwcGIyInByY1NAMUIyInNgWK/GIEZE45NyZJdHg6UAsUJRND"
    "ICZGOaIkCBUMhisUDgECGDl3EwYdAhkwJxlvdkIBM2YESTtVvZcXLAIMKSYhLAkTEwEBKTIoHxtL"
    "cXI8MQcGEwgpPl8/K5iGFQ4SFIZZORsjHwIIBigLFA0DsCQIDgz+3AI3Hk3eYUZEd15JG5gBHDRH"
    "RjkzbQEHPBtQLFNSIRgQGXoFLBQ6OAQKFT5eKEhF/r79ljszXTKlAVxyo6wzTzshHxUeOQYOMicV"
    "CxEXGQcNFBk0TUN4tlJBQiAyIBwjElgyFR4yJLjJRCEkTz4eca1zeIEEHR4OMCUEDhcNXv4KNQUr"
    "AAACALL+3gXPBMcAHQA7AAABBSc0EjcmNTQ3JjU0NjMyFhUUBxYXFhUUBwQXFhUnNCcmJzY1NCYn"
    "NjU0JiMiBhUUFwYVFBYXBgYHBhUFzvrmAtnBUrQ8f0hGfz1wJShRAQFYSUqIgfmyc2NWSTQzS1PO"
    "VF6Pvkhi/uACSMoBQlRxX61+VTJFenZAMlxJUlY8SYJ1wKKfDdemnS9Hq0+TMVVFM0hIMj9fbZ5Y"
    "diwad22TtQAACQCo/tUFmwT5ACoANAA+AEoAVQBhAGoAdQCBAAABBiMnIyInEyY1NDc2MzIXJjU0"
    "NzUnJzM1HwMjBxYVFAc2NjMyFhUUBwMnJiMiBwc2MzI3JyYjIgcHNjMyNzY2NTQmIyICERUXNyc0"
    "EjMyFhUUBwYFECcmIyIGFRQWFzY3ByY1NDYzMhI3NjY1NCYjIgYVFBcmNTQ2NzYVFAcHBgTAsFmU"
    "iU3AFvtyYGRQahV4XAJeVgJYAVoBbhY9U0d/nPU6CcmDf7AIun19yAmyg4qbCp99kqmLdnNciJp6"
    "cbB/ZkRSjxX+ijVHo1l9dImNNbjIU0BtgGkiLi8iGzNOIRUNIAYKA/7xHAMaAbbxz6BURlQ5LlgK"
    "SQFFUwFSAUNPDFA2PzUisI/d0v68VCUjVyJ9ahsWbiCueLZfZ4D+0P71KgcwDd4BFF9Pd5cWVQEQ"
    "kcF+WWa8dw44DtSHR13+8yBXxTovQTcdmEuJMBwwAQJBFitBEgAABAB1/tkGMAS7AAoAFAAeAGYA"
    "AAUnJiYjIgcHNjMyNycmIyIHBzYzMjc3JiMiBxc2MzIBBiMiJzY1JwMGIyImNTQ2MzIWFRQHEwMm"
    "NTQ2MzIWFRQHExMmNTQ2MzIWFRQHExMmNTQ2MzIWFRQHAxMmJyY2MzIWFRQHAxAEsAZjf3C0pASk"
    "t6OuA7ORobwDqa2etAWrtKWtBaqkqQEOyvGr/iEC0RENIztELipHL+kPZ0EtL0M8o0tLQTIuQE9P"
    "oTtDMDBBbg/qLgICTSouQn7LjEsjFjZNNEpKNjhHNztSODdQNv5VGxjJg3ICRwJHKixBPCQoP/6e"
    "AeESXi1CRS8pN/5IAgYlQDJBPy1ALf3/AbctMzBCPy5YG/4gAWQ4JSVHQy9YFP3H/vQAAAYAlv7U"
    "BW4EZQAbAB8AIwAnACsALwAAASU1MyczNwMnBxEfAjUhFTM1NxEHBxEXMxUzBzUhFyU3JRclJwUH"
    "ATchFyUnIRUFbvsoXQI0mwNjSsQBnQE2kcpLZZIvWkX7rwED9AH8awEDXkn9bUkCuEL9O0AC5QH8"
    "ev7UAcCHmgIsYQEBIwFmAmlqZwL+4QFn/dCSiYlVVIhTAVKITAFKAuhAQHhJSAAEALP+1AYYBQwA"
    "BwARAB0AYwAAJSYjIgcWMzI3JyYjIgcHNjMyAzUzNyMnIxUnBzMXASYnJgcFBic1BiMiJwcGByIn"
    "JiMiBgcnNjc2FwUWNyYmJzcmJjU0NjcmNTQ2MzIWFRQHFhYXFhUUBxcGBgcWNzc2FxcWFwRhj1pm"
    "r5Jsb4s4dT9HgzWPa2MzlQGUAW2fAqIBAuhqT20S/v4UUgsECAwBWzAFeRoZU5h4AmddaQkBAQw6"
    "X2NYVF9KxLdFPywsQkxldkBur1V7TFQ6DPUFNHoma00sKTxqmyMjlycBS2tuc3UBbWn83kQfKQEV"
    "AjJpAQJqKgMOAzlNiUAgIwEmAikNIC3jVpdumOU/Py4qPT0pMEEbSUp/mL+L5zcXCigCIgERKQw8"
    "AAQAgf7TBZMEqQA8AEoAUwBbAAABBSY1NDY3NzY3BgYHBgYjIic2NwYjIiY1NDY3NzY3NjY3Jicn"
    "JjU0MzIWFzY1JzQ3NjMyFxYXFhcWEhUHBzc0AicmJicXFhIRBwcBBgYVNzY3NzYBBgcWMzI1NAWM"
    "/GIFXUVGOiVDh2kkQisIFSYZTB0jgUUrOxkXHzJOFgwiCB8aZzYOAgsGC1o1t25nVDJFBEIEOzNM"
    "tpcK2/ABAv01TTQNMwYkBv7gKhIOCiT+1AEtGUveWVpLdFhUElRGAR4xRoolKbFHYCk+VjkoLRY5"
    "DxAXTDo7FEcgDAe+RHNtrmf+nZ1pK4qnAT1vpL1JO3b+Ev6zPl0EHgs3RwwPDEEM/hEEJwQoAQAA"
    "AQB0/tQFjwSwACIAAAEFNDY3NjY3JiY1NDY3JjU0NjMyFhUUBxYXFhUUBxYWFxYVBY765ikxPol4"
    "MCNhWjdwUUxwOGwnMVKAhjVf/tUBh7RQZXc4PWBJVZEyTy5RcXFNNUk4RFVUbmxAc1yjuQAAAAEA"
    "AAANBd8AyAAmAAYAAQAAAAAAAAAAAAAAAAADAAEAAAAAAJkBrwIXAvYDwQQaBNQFaQW8BlAG3gcV"
    "AAEAAAAFAAB5epSrXw889QELCAAAAAAAfCWwgAAAAADcx5TF/W79GRiLB64AAAAJAAIAAAAAAAAC"
    "qgBEBkAAsAbcAK0GWgDTBrEArgZvAIIGrgCyBkkAqAaYAHUGJgCWBuAAswYqAIEGGwB0AAEAAAVV"
    "/gAAqxj8/W7+ehiLAAEAAAAAAAAAAAAAAAAAAAANAAMFPgGQAAUAAAMzAzMAAAAAAzMDMwAAAiIH"
    "CgA3AAACAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAEFQUEwAQCZUJl8FVf4AAKsHDwFbAAAAAQAA"
    "AAADJARfAAAAIAAAAAAAAQAAAAQAAAAMAAwAAAAAABwAAAAAAAAAAQAAJlQAACZfAAAAAQAAAAcA"
    "WgADAAEECQAAAFoAAAADAAEECQABABoAWgADAAEECQACAA4AdAADAAEECQADAEYAggADAAEECQAE"
    "ABoAWgADAAEECQAFABAAyAADAAEECQAGABgA2ACpACAAQwBvAHAAeQByAGkAZwBoAHQAIAAyADAA"
    "MAAzAC0AMgAwADAANgAgAGIAeQAgAEEAcABwAGwAZQAgAEMAbwBtAHAAdQB0AGUAcgAsACAASQBu"
    "AGMALgBBAHAAcABsAGUAIABTAHkAbQBiAG8AbABzAFIAZQBnAHUAbABhAHIAQQBwAHAAbABlACAA"
    "UwB5AG0AYgBvAGwAcwA7ACAAMQA3AC4AMABkADEAZQAyADsAIAAyADAAMgAxAC0AMAA1AC0AMQA2"
    "ADEANwAuADAAZAAxAGUAMgBBAHAAcABsAGUAUwB5AG0AYgBvAGwAcwAAAAMAAAAAAAD/agBkAAAA"
)


def _load_chess_font(size):
    raw = base64.b64decode(_CHESS_FONT_B64)
    return pygame.font.Font(io.BytesIO(raw), size)


# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
BOARD_SIZE  = 8
SQUARE_SIZE = 80
BOARD_PX    = BOARD_SIZE * SQUARE_SIZE   # 640
TAB_H       = 44                          # tab bar at top (holds tabs + title)
STATUS_H    = 90                          # status bar at bottom
WINDOW_W    = BOARD_PX                   # 640
WINDOW_H    = TAB_H + BOARD_PX + STATUS_H # 774
BOARD_Y     = TAB_H                      # y-pixel where board starts
FPS         = 60

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
C_LIGHT        = (240, 217, 181)
C_DARK         = (181, 136,  99)
C_HIGHLIGHT    = (247, 247, 105, 160)
C_MOVE_DOT     = ( 20, 160,  20, 140)
C_MOVE_RING    = ( 20, 160,  20, 140)
C_CHECK_KING   = (220,  50,  50, 160)
C_HINT_SQ      = ( 30, 144, 255, 190)
C_CORRECT_SQ   = ( 50, 205,  50, 160)
C_STATUS_BG    = ( 30,  30,  30)
C_TAB_ACTIVE   = ( 55,  55,  55)
C_TAB_INACTIVE = ( 25,  25,  25)
C_TAB_BORDER   = ( 80,  80,  80)
C_TAB_LINE     = ( 90,  90,  90)
C_PROMO_BG     = (255, 255, 255)
C_PROMO_SEL    = (180, 220, 180)
C_PROMO_BDR    = ( 80,  80,  80)
C_BG           = ( 18,  18,  18)

# ---------------------------------------------------------------------------
# Chess symbols
# ---------------------------------------------------------------------------
SYMBOLS = {
    'white': {'king':'♔','queen':'♕','rook':'♖','bishop':'♗','knight':'♘','pawn':'♙'},
    'black': {'king':'♚','queen':'♛','rook':'♜','bishop':'♝','knight':'♞','pawn':'♟'},
}
PROMOTION_TYPES = ['queen', 'rook', 'bishop', 'knight']

# ---------------------------------------------------------------------------
# Game definitions (Puzzle Mode: Game 1 has solution validation, Game 2 is free play)
# ---------------------------------------------------------------------------
GAMES = {
    'game1': {
        'label':       'Fork',
        'mode':        'puzzle',
        'fen':         '2b2k2/1p2q1p1/p4p1p/3pN3/3P4/7P/PP1Q1PP1/6K1 w - - 0 1',
        'solution':    [('e5', 'g6')],
        'hint_sq':     'e5',
        'description': 'White to move. Find the winning tactic!',
        'success_msg': 'Ng6+! Royal fork -- Knight attacks King & Queen!',
        'free_play':   False,
    },
    'game2': {
        'label':       'Rook',
        'mode':        'puzzle',
        'fen':         '4r3/1p6/2p2p2/b3k1p1/3p4/1P2p1RP/1BP1P2P/3K4 w - - 0 1',
        'solution':    [('g3', 'e3'), ('e5', 'f5'), ('e3', 'e8')],
        'hint_sq':     'g3',
        'description': 'White to move. Find the 3-move winning combination!',
        'success_msg': 'Rxe3+ Kf5 Rxe8! Rook wins the rook -- excellent combination!',
        'free_play':   False,
    },
    'game3': {
        'label':       "Alekhine's Defense",
        'mode':        'replay',
        'subtitle':    'Four Pawns Attack',
        'moves': [
            ('e2','e4'), ('g8','f6'),
            ('e4','e5'), ('f6','d5'),
            ('d2','d4'), ('d7','d6'),
            ('c2','c4'), ('d5','b6'),
            ('f2','f4'), ('d6','e5'),
            ('f4','e5'), ('b8','c6'),
            ('c1','e3'), ('c8','f5'),
            ('b1','c3'), ('e7','e6'),
            ('g1','f3'), ('f8','e7'),
            ('f1','e2'), ('e8','g8'),
            ('e1','g1'), ('f7','f6'),
            ('e5','f6'), ('e7','f6'),
        ],
        'explanations': [
            "1. e4 — White controls the centre with a pawn",
            "1... Nf6 — Black attacks e4 immediately, inviting White to chase the knight",
            "2. e5 — White advances aggressively, gaining space",
            "2... Nd5 — Knight retreats to the ideal d5 square",
            "3. d4 — White builds a massive pawn centre",
            "3... d6 — Black challenges White's centre immediately",
            "4. c4 — White expands further, pushing the knight away",
            "4... Nb6 — Knight retreats again; hard to dislodge from b6",
            "5. f4 — Four Pawns Attack! White builds a massive pawn wall",
            "5... dxe5 — Black demolishes the centre before it becomes too strong",
            "6. fxe5 — White recaptures, keeping a strong pawn on e5",
            "6... Nc6 — Attacking d4 and pressuring White's centre from the side",
            "7. Be3 — White develops and defends d4",
            "7... Bf5 — Black develops the bishop actively before ...e6 closes it in",
            "8. Nc3 — White develops the knight, adding pressure to d5",
            "8... e6 — Solid defence; Black prepares to castle kingside",
            "9. Nf3 — White completes kingside development",
            "9... Be7 — Black prepares to castle; bishop supports kingside",
            "10. Be2 — White prepares to castle; solid bishop placement",
            "10... O-O — Black castles to safety",
            "11. O-O — White castles; both kings are now safe",
            "11... f6! — Black strikes the pawn centre at its base",
            "12. exf6 — White captures en passant, opening the f-file",
            "12... Bxf6 — Black recaptures with excellent piece activity and open diagonals",
        ],
    },
}


# ---------------------------------------------------------------------------
# Piece
# ---------------------------------------------------------------------------
class Piece:
    __slots__ = ('color', 'type', 'has_moved')

    def __init__(self, color, type_):
        self.color     = color
        self.type      = type_
        self.has_moved = False

    def copy(self):
        p = Piece(self.color, self.type)
        p.has_moved = self.has_moved
        return p

    def symbol(self):
        return SYMBOLS[self.color][self.type]


# ---------------------------------------------------------------------------
# Board helpers
# ---------------------------------------------------------------------------
def make_board():
    b = [[None]*8 for _ in range(8)]
    back = ['rook','knight','bishop','queen','king','bishop','knight','rook']
    for col, t in enumerate(back):
        b[0][col] = Piece('black', t)
        b[7][col] = Piece('white', t)
    for col in range(8):
        b[1][col] = Piece('black', 'pawn')
        b[6][col] = Piece('white', 'pawn')
    return b


def copy_board(board):
    return [[p.copy() if p else None for p in row] for row in board]


_FEN_MAP = {
    'P':('white','pawn'),  'N':('white','knight'), 'B':('white','bishop'),
    'R':('white','rook'),  'Q':('white','queen'),  'K':('white','king'),
    'p':('black','pawn'),  'n':('black','knight'), 'b':('black','bishop'),
    'r':('black','rook'),  'q':('black','queen'),  'k':('black','king'),
}


def board_from_fen(fen):
    """Parse FEN board part into 8x8 Piece list (row 0 = rank 8)."""
    board_part = fen.split()[0]
    b = [[None]*8 for _ in range(8)]
    row = col = 0
    for ch in board_part:
        if ch == '/':
            row += 1; col = 0
        elif ch.isdigit():
            col += int(ch)
        else:
            color, ptype = _FEN_MAP[ch]
            p = Piece(color, ptype)
            p.has_moved = True
            b[row][col] = p
            col += 1
    return b


def alg_to_rc(sq):
    """'e5' -> (row, col) in 0=rank8 system."""
    return 8 - int(sq[1]), ord(sq[0]) - ord('a')


# ---------------------------------------------------------------------------
# GameState  (Play Chess mode)
# ---------------------------------------------------------------------------
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board             = make_board()
        self.turn              = 'white'
        self.en_passant_target = None
        self.selected          = None
        self.valid_moves       = []
        self.status            = 'playing'
        self.promotion_pending = None
        self.promotion_color   = None
        self.last_move         = None


# ---------------------------------------------------------------------------
# PuzzleState  (Puzzle mode)
# ---------------------------------------------------------------------------
class PuzzleState:
    def __init__(self, game_key='game1'):
        self.game_key = game_key
        self._load()

    def _load(self):
        gm = GAMES[self.game_key]
        self.board             = board_from_fen(gm['fen'])
        self.turn              = 'white' if ' w ' in gm['fen'] else 'black'
        self.en_passant_target = None
        self.selected          = None
        self.valid_moves       = []
        self.status            = 'playing'   # playing|check|wrong|solved|stalemate
        self.move_step         = 0
        self.hint_timer        = 0
        self.flash_timer       = 0
        self.correct_timer     = 0
        self.show_nav_popup    = False
        self.nav_pending_key   = None
        self.nav_popup_timer   = 0

    def reset(self):
        self._load()

    def switch_game(self, game_key):
        self.game_key = game_key
        self._load()

    @property
    def puzzle(self):
        return GAMES[self.game_key]


# ---------------------------------------------------------------------------
# ReplayState  (Alekhine's Defense / replay mode)
# ---------------------------------------------------------------------------
def _build_replay_boards(game_key):
    """Pre-compute list of boards for every step (0=start, 1=after move1, ...)."""
    gm     = GAMES[game_key]
    board  = make_board()
    turn   = 'white'
    ep     = None
    boards = [copy_board(board)]
    last_moves = [None]   # last_move before each step

    for fr, to in gm['moves']:
        r,  c  = alg_to_rc(fr)
        mr, mc = alg_to_rc(to)
        piece  = board[r][c]
        new_ep = None

        # En passant capture
        if piece.type == 'pawn' and ep and (mr, mc) == ep:
            board[r][mc] = None

        # Castling rook move
        if piece.type == 'king' and abs(mc - c) == 2:
            back = r
            if mc == 6:
                board[back][5] = board[back][7]; board[back][7] = None
                if board[back][5]: board[back][5].has_moved = True
            elif mc == 2:
                board[back][3] = board[back][0]; board[back][0] = None
                if board[back][3]: board[back][3].has_moved = True

        # Pawn double push en passant target
        if piece.type == 'pawn' and abs(mr - r) == 2:
            new_ep = ((r + mr) // 2, c)

        board[mr][mc]   = piece
        board[r][c]     = None
        piece.has_moved = True
        ep   = new_ep
        turn = 'black' if turn == 'white' else 'white'

        boards.append(copy_board(board))
        last_moves.append(((r, c), (mr, mc)))

    return boards, last_moves


class ReplayState:
    def __init__(self, game_key='game3'):
        self.game_key        = game_key
        self.step            = 0        # 0 = starting position
        self.boards, self.last_moves = _build_replay_boards(game_key)
        self.total_steps     = len(self.boards) - 1   # 24
        self.show_nav_popup  = False
        self.nav_pending_key = None
        self.nav_popup_timer = 0

    def reset(self):
        self.step            = 0
        self.show_nav_popup  = False
        self.nav_pending_key = None
        self.nav_popup_timer = 0

    def switch_game(self, game_key):
        self.game_key        = game_key
        self.step            = 0
        self.show_nav_popup  = False
        self.nav_pending_key = None
        self.nav_popup_timer = 0
        if GAMES[game_key]['mode'] == 'replay':
            self.boards, self.last_moves = _build_replay_boards(game_key)
            self.total_steps = len(self.boards) - 1

    @property
    def board(self):
        return self.boards[self.step]

    @property
    def last_move(self):
        return self.last_moves[self.step]

    @property
    def explanation(self):
        if self.step == 0:
            return GAMES[self.game_key].get('subtitle', '')
        return GAMES[self.game_key]['explanations'][self.step - 1]

    @property
    def is_finished(self):
        return self.step >= self.total_steps


# ---------------------------------------------------------------------------
# Move generation
# ---------------------------------------------------------------------------
def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def opponent(color):
    return 'black' if color == 'white' else 'white'


def find_king(board, color):
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p.color == color and p.type == 'king':
                return r, c
    return None


def raw_moves(board, r, c, ep):
    piece = board[r][c]
    if not piece:
        return []
    color = piece.color
    opp   = opponent(color)
    moves = []

    def slide(dr, dc):
        nr, nc = r+dr, c+dc
        while in_bounds(nr, nc):
            t = board[nr][nc]
            if t is None:
                moves.append((nr, nc))
            elif t.color == opp:
                moves.append((nr, nc)); break
            else:
                break
            nr += dr; nc += dc

    t = piece.type
    if t == 'pawn':
        d = -1 if color == 'white' else 1
        nr = r + d
        if in_bounds(nr, c) and board[nr][c] is None:
            moves.append((nr, c))
            sr = 6 if color == 'white' else 1
            if r == sr and board[r+2*d][c] is None:
                moves.append((r+2*d, c))
        for dc in (-1, 1):
            nc = c + dc
            if in_bounds(nr, nc):
                tgt = board[nr][nc]
                if tgt and tgt.color == opp:
                    moves.append((nr, nc))
                if ep and (nr, nc) == ep:
                    moves.append((nr, nc))
    elif t == 'knight':
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            nr, nc = r+dr, c+dc
            if in_bounds(nr, nc):
                tgt = board[nr][nc]
                if tgt is None or tgt.color == opp:
                    moves.append((nr, nc))
    elif t == 'bishop':
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]: slide(dr, dc)
    elif t == 'rook':
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]: slide(dr, dc)
    elif t == 'queen':
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]: slide(dr, dc)
    elif t == 'king':
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            nr, nc = r+dr, c+dc
            if in_bounds(nr, nc):
                tgt = board[nr][nc]
                if tgt is None or tgt.color == opp:
                    moves.append((nr, nc))
    return moves


def sq_attacked(board, r, c, by_color):
    for pr in range(8):
        for pc in range(8):
            p = board[pr][pc]
            if p and p.color == by_color:
                if (r, c) in raw_moves(board, pr, pc, None):
                    return True
    return False


def is_in_check(board, color):
    kr, kc = find_king(board, color)
    return sq_attacked(board, kr, kc, opponent(color))


def _apply_simple(board, r, c, mr, mc, ep):
    piece = board[r][c]
    if piece.type == 'pawn' and ep and (mr, mc) == ep:
        board[r][mc] = None
    board[mr][mc] = piece
    board[r][c]   = None


def legal_moves(board, r, c, ep):
    piece = board[r][c]
    if not piece:
        return []
    color  = piece.color
    result = []
    for mr, mc in raw_moves(board, r, c, ep):
        tb = copy_board(board)
        _apply_simple(tb, r, c, mr, mc, ep)
        if not is_in_check(tb, color):
            result.append((mr, mc))
    # Castling
    if piece.type == 'king' and not piece.has_moved and not is_in_check(board, color):
        back = 7 if color == 'white' else 0
        if r == back:
            rk = board[back][7]
            if (rk and rk.type == 'rook' and not rk.has_moved
                    and board[back][5] is None and board[back][6] is None
                    and not sq_attacked(board, back, 5, opponent(color))
                    and not sq_attacked(board, back, 6, opponent(color))):
                result.append((back, 6))
            rk = board[back][0]
            if (rk and rk.type == 'rook' and not rk.has_moved
                    and board[back][1] is None and board[back][2] is None
                    and board[back][3] is None
                    and not sq_attacked(board, back, 3, opponent(color))
                    and not sq_attacked(board, back, 2, opponent(color))):
                result.append((back, 2))
    return result


def all_legal_moves(board, color, ep):
    moves = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p.color == color:
                for m in legal_moves(board, r, c, ep):
                    moves.append(((r, c), m))
    return moves


def apply_move(gs, r, c, mr, mc):
    """Apply a fully-legal move to a GameState, handling all side-effects."""
    board  = gs.board
    piece  = board[r][c]
    opp    = opponent(piece.color)
    new_ep = None

    if piece.type == 'pawn' and gs.en_passant_target and (mr, mc) == gs.en_passant_target:
        board[r][mc] = None

    if piece.type == 'king' and abs(mc - c) == 2:
        back = r
        if mc == 6:
            board[back][5] = board[back][7]; board[back][7] = None
            if board[back][5]: board[back][5].has_moved = True
        elif mc == 2:
            board[back][3] = board[back][0]; board[back][0] = None
            if board[back][3]: board[back][3].has_moved = True

    if piece.type == 'pawn' and abs(mr - r) == 2:
        new_ep = ((r + mr) // 2, c)

    board[mr][mc]   = piece
    board[r][c]     = None
    piece.has_moved = True

    promote_row = 0 if piece.color == 'white' else 7
    if piece.type == 'pawn' and mr == promote_row:
        gs.promotion_pending = (mr, mc)
        gs.promotion_color   = piece.color
        gs.en_passant_target = new_ep
        gs.last_move = ((r, c), (mr, mc))
        return

    gs.en_passant_target = new_ep
    gs.last_move = ((r, c), (mr, mc))
    gs.turn = opp
    _update_status(gs)


def _update_status(gs):
    color = gs.turn
    chk   = is_in_check(gs.board, color)
    has_m = bool(all_legal_moves(gs.board, color, gs.en_passant_target))
    if chk and not has_m:
        gs.status = 'checkmate'
    elif not chk and not has_m:
        gs.status = 'stalemate'
    elif chk:
        gs.status = 'check'
    else:
        gs.status = 'playing'


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
def load_fonts():
    piece_font  = _load_chess_font(62)
    ui_font     = pygame.font.SysFont('arial', 23, bold=True)
    small_font  = pygame.font.SysFont('arial', 17)
    tab_font    = pygame.font.SysFont('arial', 16, bold=True)
    title_font  = pygame.font.SysFont('georgia', 22, bold=True)
    return piece_font, ui_font, small_font, tab_font, title_font


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------
def sq_rect(r, c):
    return pygame.Rect(c * SQUARE_SIZE, BOARD_Y + r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)


def pixel_to_sq(px, py):
    bx, by = px, py - BOARD_Y
    if bx < 0 or bx >= BOARD_PX or by < 0 or by >= BOARD_PX:
        return None
    return by // SQUARE_SIZE, bx // SQUARE_SIZE


# ---------------------------------------------------------------------------
# Tab bar
# ---------------------------------------------------------------------------
TABS    = [('Play Chess', 'play'), ('Puzzle Mode', 'puzzle')]
TAB_W   = WINDOW_W // len(TABS)


def draw_tabs(surface, app_mode, tab_font, title_font):
    """Draw the tab bar. Left side: mode tabs. Right side: academy title."""
    # Full tab bar background
    pygame.draw.rect(surface, C_TAB_INACTIVE, (0, 0, WINDOW_W, TAB_H))

    # --- Mode tabs (left half of the bar) ---
    tab_area_w = WINDOW_W // 2          # tabs occupy left 320px
    tab_w      = tab_area_w // len(TABS)
    for i, (label, mode) in enumerate(TABS):
        rect   = pygame.Rect(i * tab_w, 0, tab_w, TAB_H)
        active = (mode == app_mode)
        bg     = C_TAB_ACTIVE if active else C_TAB_INACTIVE
        pygame.draw.rect(surface, bg, rect)
        if active:
            pygame.draw.rect(surface, (100, 180, 255),
                             pygame.Rect(i * tab_w, TAB_H - 3, tab_w, 3))
        pygame.draw.rect(surface, C_TAB_BORDER, rect, 1)
        col = (255, 255, 255) if active else (150, 150, 150)
        lbl = tab_font.render(label, True, col)
        surface.blit(lbl, lbl.get_rect(center=rect.center))

    # --- Academy title (right half of the bar) ---
    title_area = pygame.Rect(WINDOW_W // 2, 0, WINDOW_W // 2, TAB_H)
    # Subtle vertical separator
    pygame.draw.line(surface, (80, 80, 80), (WINDOW_W // 2, 6), (WINDOW_W // 2, TAB_H - 6), 1)
    lbl = title_font.render("The Brain Games Academy", True, (220, 175, 60))
    surface.blit(lbl, lbl.get_rect(midright=(WINDOW_W - 10, TAB_H // 2)))

    # Bottom separator line
    pygame.draw.line(surface, (70, 70, 70), (0, TAB_H - 1), (WINDOW_W, TAB_H - 1), 1)


def tab_click(px, py):
    if 0 <= py < TAB_H:
        tab_area_w = WINDOW_W // 2
        tab_w      = tab_area_w // len(TABS)
        if px < tab_area_w:
            idx = px // tab_w
            if 0 <= idx < len(TABS):
                return TABS[idx][1]
    return None


# ---------------------------------------------------------------------------
# Shared board drawing
# ---------------------------------------------------------------------------
def draw_board_and_pieces(surface, board, selected, valid_moves, piece_font,
                          check_king_pos=None, hint_sq=None,
                          wrong_flash_alpha=0, correct_sq=None, last_move=None):
    C_LAST_MOVE = (205, 185, 80, 160)   # golden yellow for replay last-move highlight

    # 1. Squares
    for r in range(8):
        for c in range(8):
            rect  = sq_rect(r, c)
            color = C_LIGHT if (r + c) % 2 == 0 else C_DARK
            pygame.draw.rect(surface, color, rect)

            # Last-move highlight (golden yellow) for replay mode
            if last_move and ((r, c) == last_move[0] or (r, c) == last_move[1]):
                ov = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                ov.fill(C_LAST_MOVE)
                surface.blit(ov, rect.topleft)

            # King-in-check red tint
            if check_king_pos and (r, c) == check_king_pos:
                ov = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                ov.fill(C_CHECK_KING)
                surface.blit(ov, rect.topleft)

            # Hint highlight (blue)
            if hint_sq and (r, c) == hint_sq:
                ov = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                ov.fill(C_HINT_SQ)
                surface.blit(ov, rect.topleft)

            # Correct-move highlight (green)
            if correct_sq and (r, c) == correct_sq:
                ov = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                ov.fill(C_CORRECT_SQ)
                surface.blit(ov, rect.topleft)

    # 2. Selected square
    if selected:
        sr, sc = selected
        ov = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        ov.fill(C_HIGHLIGHT)
        surface.blit(ov, sq_rect(sr, sc).topleft)

    # 3. Valid move dots / rings
    for mr, mc in valid_moves:
        rect = sq_rect(mr, mc)
        ov   = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        if board[mr][mc] is None:
            pygame.draw.circle(ov, C_MOVE_DOT, (SQUARE_SIZE//2, SQUARE_SIZE//2), 14)
        else:
            pygame.draw.circle(ov, C_MOVE_RING, (SQUARE_SIZE//2, SQUARE_SIZE//2),
                               SQUARE_SIZE//2 - 4, 6)
        surface.blit(ov, rect.topleft)

    # 4. Wrong-move full-board red flash
    if wrong_flash_alpha > 0:
        flash = pygame.Surface((BOARD_PX, BOARD_PX), pygame.SRCALPHA)
        flash.fill((220, 50, 50, int(wrong_flash_alpha)))
        surface.blit(flash, (0, BOARD_Y))

    # 5. Pieces
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p is None:
                continue
            rect   = sq_rect(r, c)
            sym    = p.symbol()
            oc = (30,30,30)    if p.color == 'white' else (220,220,220)
            fc = (255,255,255) if p.color == 'white' else (10,10,10)
            for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                s = piece_font.render(sym, True, oc)
                surface.blit(s, s.get_rect(center=(rect.centerx+dx, rect.centery+dy)))
            s = piece_font.render(sym, True, fc)
            surface.blit(s, s.get_rect(center=rect.center))

    # 6. Rank / file labels
    small = pygame.font.SysFont('arial', 13, bold=True)
    for i in range(8):
        tc = C_DARK if i % 2 == 0 else C_LIGHT
        lbl = small.render(chr(ord('a') + i), True, tc)
        surface.blit(lbl, (i * SQUARE_SIZE + 4, BOARD_Y + BOARD_PX - 16))
        lbl = small.render(str(8 - i), True, tc)
        surface.blit(lbl, (4, BOARD_Y + i * SQUARE_SIZE + 4))


# ---------------------------------------------------------------------------
# Play mode -- status bar & promotion popup
# ---------------------------------------------------------------------------
def draw_play_status(surface, gs, ui_font, small_font):
    bar_y = BOARD_Y + BOARD_PX
    pygame.draw.rect(surface, C_STATUS_BG, (0, bar_y, WINDOW_W, STATUS_H))

    if gs.status == 'checkmate':
        msg = f"Checkmate!  {opponent(gs.turn).capitalize()} wins!"
        col = (255, 100, 100)
    elif gs.status == 'stalemate':
        msg = "Stalemate!  Draw."
        col = (255, 200,  80)
    elif gs.status == 'check':
        msg = f"{gs.turn.capitalize()}'s Turn  --  CHECK!"
        col = (255, 160,  50)
    elif gs.promotion_pending:
        msg = "Choose promotion piece"
        col = (150, 220, 255)
    else:
        msg = f"{gs.turn.capitalize()}'s Turn"
        col = (200, 230, 200) if gs.turn == 'white' else (160, 180, 220)

    s = ui_font.render(msg, True, col)
    surface.blit(s, s.get_rect(centerx=WINDOW_W//2, centery=bar_y + 26))
    s2 = small_font.render("Press R to restart", True, (110, 110, 110))
    surface.blit(s2, s2.get_rect(centerx=WINDOW_W//2, centery=bar_y + 62))


def draw_promotion_popup(surface, gs, piece_font, ui_font):
    if not gs.promotion_pending:
        return
    color = gs.promotion_color
    n     = len(PROMOTION_TYPES)
    bw    = n * SQUARE_SIZE + (n + 1) * 10
    bh    = SQUARE_SIZE + 60
    bx    = (WINDOW_W - bw) // 2
    by    = BOARD_Y + (BOARD_PX - bh) // 2

    panel = pygame.Surface((bw, bh), pygame.SRCALPHA)
    panel.fill((245, 245, 245, 235))
    surface.blit(panel, (bx, by))
    pygame.draw.rect(surface, C_PROMO_BDR, (bx, by, bw, bh), 3, border_radius=8)

    title = ui_font.render("Promote pawn to:", True, (40, 40, 40))
    surface.blit(title, title.get_rect(centerx=bx+bw//2, centery=by+22))

    for i, ptype in enumerate(PROMOTION_TYPES):
        btnx = bx + 10 + i * (SQUARE_SIZE + 10)
        btny = by + 40
        btn  = pygame.Rect(btnx, btny, SQUARE_SIZE, SQUARE_SIZE)
        mx, my = pygame.mouse.get_pos()
        bg = C_PROMO_SEL if btn.collidepoint(mx, my) else C_PROMO_BG
        pygame.draw.rect(surface, bg, btn, border_radius=6)
        pygame.draw.rect(surface, C_PROMO_BDR, btn, 2, border_radius=6)
        sym = SYMBOLS[color][ptype]
        oc  = (30,30,30)    if color == 'white' else (210,210,210)
        fc  = (255,255,255) if color == 'white' else (10,10,10)
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            s = piece_font.render(sym, True, oc)
            surface.blit(s, s.get_rect(center=(btn.centerx+dx, btn.centery+dy)))
        s = piece_font.render(sym, True, fc)
        surface.blit(s, s.get_rect(center=btn.center))


def get_promotion_rects(gs):
    if not gs.promotion_pending:
        return []
    n  = len(PROMOTION_TYPES)
    bw = n * SQUARE_SIZE + (n + 1) * 10
    bh = SQUARE_SIZE + 60
    bx = (WINDOW_W - bw) // 2
    by = BOARD_Y + (BOARD_PX - bh) // 2
    rects = []
    for i, ptype in enumerate(PROMOTION_TYPES):
        btnx = bx + 10 + i * (SQUARE_SIZE + 10)
        btny = by + 40
        rects.append((pygame.Rect(btnx, btny, SQUARE_SIZE, SQUARE_SIZE), ptype))
    return rects


# ---------------------------------------------------------------------------
# Play mode click handler
# ---------------------------------------------------------------------------
def handle_play_click(gs, px, py):
    if gs.promotion_pending:
        for rect, ptype in get_promotion_rects(gs):
            if rect.collidepoint(px, py):
                pr, pc = gs.promotion_pending
                gs.board[pr][pc].type = ptype
                gs.promotion_pending  = None
                gs.promotion_color    = None
                gs.turn = opponent(gs.turn)
                _update_status(gs)
                break
        return
    sq = pixel_to_sq(px, py)
    if sq is None:
        return
    r, c  = sq
    piece = gs.board[r][c]
    if gs.selected is None:
        if piece and piece.color == gs.turn:
            gs.selected    = (r, c)
            gs.valid_moves = legal_moves(gs.board, r, c, gs.en_passant_target)
    else:
        sr, sc = gs.selected
        if (r, c) in gs.valid_moves:
            apply_move(gs, sr, sc, r, c)
            gs.selected = None; gs.valid_moves = []
        elif piece and piece.color == gs.turn:
            gs.selected    = (r, c)
            gs.valid_moves = legal_moves(gs.board, r, c, gs.en_passant_target)
        else:
            gs.selected = None; gs.valid_moves = []


# ---------------------------------------------------------------------------
# Puzzle selector screen
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Puzzle mode -- arrow button geometry
# ---------------------------------------------------------------------------
ARROW_W = 44
ARROW_H = 28
GAME_KEYS = list(GAMES.keys())   # ['game1', 'game2']


def get_arrow_rects(state):
    """Return list of (rect, target_game_key, direction) for visible arrows.
    Works for both PuzzleState and ReplayState."""
    bar_y   = BOARD_Y + BOARD_PX
    btn_y   = bar_y + STATUS_H - ARROW_H - 8
    idx     = GAME_KEYS.index(state.game_key)
    arrows  = []
    if idx > 0:
        arrows.append((pygame.Rect(10, btn_y, ARROW_W, ARROW_H),
                       GAME_KEYS[idx - 1], 'left'))
    if idx < len(GAME_KEYS) - 1:
        arrows.append((pygame.Rect(WINDOW_W - ARROW_W - 10, btn_y, ARROW_W, ARROW_H),
                       GAME_KEYS[idx + 1], 'right'))
    return arrows


def get_replay_step_arrow_rects(rs):
    """Return (prev_rect, next_rect) for stepping through replay moves.
    These are INNER arrows inside the status bar, distinct from game-navigation arrows."""
    bar_y  = BOARD_Y + BOARD_PX
    btn_y  = bar_y + STATUS_H - ARROW_H - 8
    centre = WINDOW_W // 2
    gap    = 60
    prev_r = pygame.Rect(centre - gap - ARROW_W, btn_y, ARROW_W, ARROW_H)
    next_r = pygame.Rect(centre + gap,            btn_y, ARROW_W, ARROW_H)
    return prev_r, next_r


# ---------------------------------------------------------------------------
# Puzzle mode -- status bar
# ---------------------------------------------------------------------------
def draw_puzzle_status(surface, ps, ui_font, small_font):
    bar_y = BOARD_Y + BOARD_PX
    pygame.draw.rect(surface, C_STATUS_BG, (0, bar_y, WINDOW_W, STATUS_H))

    pz = ps.puzzle

    # --- Status message (top of bar) ---
    if ps.status == 'solved':
        msg = pz['success_msg']
        col = (80, 220, 80)
    elif ps.status == 'wrong':
        msg = "Wrong move!  Resetting..."
        col = (255, 70, 70)
    elif ps.status == 'check':
        msg = pz['label'] + "  --  CHECK!  Keep going."
        col = (255, 160, 50)
    elif ps.status == 'stalemate':
        msg = pz['label'] + "  --  Stalemate."
        col = (255, 200, 80)
    else:
        turn_str = ps.turn.capitalize()
        msg = pz['label'] + "  --  " + turn_str + " to move"
        col = (200, 230, 200) if ps.turn == 'white' else (160, 180, 220)

    s = ui_font.render(msg, True, col)
    surface.blit(s, s.get_rect(centerx=WINDOW_W // 2, centery=bar_y + 30))

    # --- Arrow buttons (bottom corners) ---
    mx, my = pygame.mouse.get_pos()
    for rect, _key, direction in get_arrow_rects(ps):
        hovered  = rect.collidepoint(mx, my)
        bg_col   = (70, 90, 140) if hovered else (40, 42, 54)
        bdr_col  = (120, 150, 220) if hovered else (70, 72, 90)
        pygame.draw.rect(surface, bg_col, rect, border_radius=6)
        pygame.draw.rect(surface, bdr_col, rect, 1, border_radius=6)
        symbol = '\u25c4' if direction == 'left' else '\u25ba'   # ◄ ►
        lbl = ui_font.render(symbol, True, (220, 220, 220))
        surface.blit(lbl, lbl.get_rect(center=rect.center))


# ---------------------------------------------------------------------------
# Replay mode -- status bar
# ---------------------------------------------------------------------------
def draw_replay_status(surface, rs, ui_font, small_font):
    bar_y = BOARD_Y + BOARD_PX
    pygame.draw.rect(surface, C_STATUS_BG, (0, bar_y, WINDOW_W, STATUS_H))

    gm = GAMES[rs.game_key]

    # --- Title line ---
    if rs.step == 0:
        title_msg = gm['label'] + "  --  " + gm.get('subtitle', '')
        title_col = (220, 175, 60)
    else:
        # Which move number and whose turn label
        move_num  = (rs.step + 1) // 2
        side      = "White" if rs.step % 2 == 1 else "Black"
        title_msg = gm['label'] + "  --  Move " + str(move_num) + " (" + side + ")"
        title_col = (200, 230, 200) if rs.step % 2 == 1 else (160, 180, 220)

    s = ui_font.render(title_msg, True, title_col)
    surface.blit(s, s.get_rect(centerx=WINDOW_W // 2, centery=bar_y + 16))

    # --- Explanation line ---
    expl = rs.explanation
    s2 = small_font.render(expl, True, (180, 180, 190))
    surface.blit(s2, s2.get_rect(centerx=WINDOW_W // 2, centery=bar_y + 38))

    # --- Step counter ---
    counter = str(rs.step) + " / " + str(rs.total_steps)
    s3 = small_font.render(counter, True, (100, 100, 120))
    surface.blit(s3, s3.get_rect(centerx=WINDOW_W // 2, centery=bar_y + 60))

    # --- Inner step arrows (◄ prev move / ► next move) ---
    mx, my = pygame.mouse.get_pos()
    prev_r, next_r = get_replay_step_arrow_rects(rs)

    for rect, active, symbol in [
        (prev_r, rs.step > 0,              '\u25c4'),
        (next_r, rs.step < rs.total_steps, '\u25ba'),
    ]:
        if not active:
            # Greyed out
            pygame.draw.rect(surface, (30, 32, 40), rect, border_radius=6)
            pygame.draw.rect(surface, (50, 52, 60), rect, 1, border_radius=6)
            lbl = small_font.render(symbol, True, (60, 62, 70))
        else:
            hovered = rect.collidepoint(mx, my)
            bg_col  = (70, 90, 140) if hovered else (40, 42, 54)
            bdr_col = (120, 150, 220) if hovered else (70, 72, 90)
            pygame.draw.rect(surface, bg_col, rect, border_radius=6)
            pygame.draw.rect(surface, bdr_col, rect, 1, border_radius=6)
            lbl = ui_font.render(symbol, True, (220, 220, 220))
        surface.blit(lbl, lbl.get_rect(center=rect.center))

    # --- Outer game-navigation arrows (far left / far right) ---
    for rect, _key, direction in get_arrow_rects(rs):
        hovered  = rect.collidepoint(mx, my)
        bg_col   = (70, 90, 140) if hovered else (40, 42, 54)
        bdr_col  = (120, 150, 220) if hovered else (70, 72, 90)
        pygame.draw.rect(surface, bg_col, rect, border_radius=6)
        pygame.draw.rect(surface, bdr_col, rect, 1, border_radius=6)
        sym = '\u25c4' if direction == 'left' else '\u25ba'
        lbl = ui_font.render(sym, True, (220, 220, 220))
        surface.blit(lbl, lbl.get_rect(center=rect.center))


# ---------------------------------------------------------------------------
# Puzzle mode -- navigation popup (drawn over board)
# ---------------------------------------------------------------------------
def draw_nav_popup(surface, state, ui_font, small_font):
    if not state.show_nav_popup:
        return

    # Works for PuzzleState (has .status) and ReplayState (check is_finished)
    is_ps    = isinstance(state, PuzzleState)
    solved   = (state.status == 'solved') if is_ps else state.is_finished
    cur_lbl  = GAMES[state.game_key]['label']
    dest_key = state.nav_pending_key
    dest_lbl = GAMES[dest_key]['label'] if dest_key else ''

    # Panel dimensions
    pw, ph = 420, 160
    px_    = (WINDOW_W - pw) // 2
    py_    = BOARD_Y + (BOARD_PX - ph) // 2

    # Background panel
    panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
    panel.fill((30, 32, 44, 240))
    surface.blit(panel, (px_, py_))
    pygame.draw.rect(surface, (100, 120, 200), (px_, py_, pw, ph), 2, border_radius=12)

    if solved:
        # --- Completed popup (auto-dismiss) ---
        line1 = cur_lbl + " completed!"
        line2 = "Moving to " + dest_lbl + "..."
        col1  = (80, 220, 80)
        col2  = (180, 200, 180)
        s1 = ui_font.render(line1, True, col1)
        s2 = small_font.render(line2, True, col2)
        surface.blit(s1, s1.get_rect(centerx=px_ + pw // 2, centery=py_ + 55))
        surface.blit(s2, s2.get_rect(centerx=px_ + pw // 2, centery=py_ + 95))
    else:
        # --- Unfinished popup (with Stay / Yes buttons) ---
        line1 = "You haven't finished " + cur_lbl + " yet."
        line2 = "Move to " + dest_lbl + " anyway?"
        col1  = (255, 200, 80)
        col2  = (200, 200, 200)
        s1 = ui_font.render(line1, True, col1)
        s2 = small_font.render(line2, True, col2)
        surface.blit(s1, s1.get_rect(centerx=px_ + pw // 2, centery=py_ + 38))
        surface.blit(s2, s2.get_rect(centerx=px_ + pw // 2, centery=py_ + 68))

        # Buttons
        stay_r, confirm_r = _nav_popup_btn_rects(px_, py_, pw, ph)
        for rect, label, base_col in [
            (stay_r,    "Stay",         (70, 70, 90)),
            (confirm_r, "Yes, continue",(60, 110, 60)),
        ]:
            mx, my = pygame.mouse.get_pos()
            hov = rect.collidepoint(mx, my)
            bg  = tuple(min(255, c + 20) for c in base_col) if hov else base_col
            pygame.draw.rect(surface, bg, rect, border_radius=7)
            pygame.draw.rect(surface, (130, 130, 160), rect, 1, border_radius=7)
            lbl = small_font.render(label, True, (230, 230, 230))
            surface.blit(lbl, lbl.get_rect(center=rect.center))


def _nav_popup_btn_rects(px_, py_, pw, ph):
    bw, bh = 130, 32
    gap    = 20
    total  = 2 * bw + gap
    sx     = px_ + (pw - total) // 2
    by_    = py_ + ph - bh - 18
    stay_r    = pygame.Rect(sx,          by_, bw, bh)
    confirm_r = pygame.Rect(sx + bw + gap, by_, bw, bh)
    return stay_r, confirm_r


def get_nav_popup_click(ps, px, py):
    """
    Returns 'stay', 'confirm', or None depending on what was clicked in the popup.
    Only meaningful when ps.show_nav_popup is True and puzzle is NOT solved.
    """
    if not ps.show_nav_popup or ps.status == 'solved':
        return None
    pw, ph = 420, 160
    px_    = (WINDOW_W - pw) // 2
    py_    = BOARD_Y + (BOARD_PX - ph) // 2
    stay_r, confirm_r = _nav_popup_btn_rects(px_, py_, pw, ph)
    if stay_r.collidepoint(px, py):
        return 'stay'
    if confirm_r.collidepoint(px, py):
        return 'confirm'
    return None


# ---------------------------------------------------------------------------
# Puzzle move application
# ---------------------------------------------------------------------------
def _apply_puzzle_move(ps, r, c, mr, mc):
    """Apply a move on the puzzle board (no promotion UI, auto-queen)."""
    board  = ps.board
    piece  = board[r][c]
    new_ep = None

    if piece.type == 'pawn' and ps.en_passant_target and (mr, mc) == ps.en_passant_target:
        board[r][mc] = None
    if piece.type == 'pawn' and abs(mr - r) == 2:
        new_ep = ((r + mr) // 2, c)

    board[mr][mc]   = piece
    board[r][c]     = None
    piece.has_moved = True

    # Auto-promote to queen
    promote_row = 0 if piece.color == 'white' else 7
    if piece.type == 'pawn' and mr == promote_row:
        piece.type = 'queen'

    ps.en_passant_target = new_ep
    ps.turn = opponent(ps.turn)


def _puzzle_validate_and_move(ps, r, c, mr, mc):
    """Make a move in puzzle mode. Validates solution for game1; free play for game2."""
    pz   = ps.puzzle
    step = ps.move_step   # capture before applying

    # Free-play game: just apply and update status
    if pz['free_play']:
        _apply_puzzle_move(ps, r, c, mr, mc)
        ps.selected    = None
        ps.valid_moves = []
        chk   = is_in_check(ps.board, ps.turn)
        has_m = bool(all_legal_moves(ps.board, ps.turn, ps.en_passant_target))
        if chk and not has_m:
            ps.status = 'solved'
        elif not chk and not has_m:
            ps.status = 'stalemate'
        elif chk:
            ps.status = 'check'
        else:
            ps.status = 'playing'
        return

    # Solution-validated game: check correctness BEFORE applying
    sol_from = alg_to_rc(pz['solution'][step][0])
    sol_to   = alg_to_rc(pz['solution'][step][1])
    correct  = ((r, c) == sol_from and (mr, mc) == sol_to)

    _apply_puzzle_move(ps, r, c, mr, mc)
    ps.selected    = None
    ps.valid_moves = []

    if correct:
        ps.correct_timer = FPS
        ps.move_step    += 1
        if ps.move_step >= len(pz['solution']):
            ps.status = 'solved'
        else:
            chk   = is_in_check(ps.board, ps.turn)
            has_m = bool(all_legal_moves(ps.board, ps.turn, ps.en_passant_target))
            if chk and not has_m:
                ps.status = 'solved'
            elif not chk and not has_m:
                ps.status = 'stalemate'
            elif chk:
                ps.status = 'check'
            else:
                ps.status = 'playing'
    else:
        ps.status      = 'wrong'
        ps.flash_timer = FPS * 2       # 2-second red flash then auto-reset


# ---------------------------------------------------------------------------
# Puzzle click handler
# ---------------------------------------------------------------------------
def handle_puzzle_click(ps, px, py):
    if ps.status in ('solved', 'wrong', 'stalemate'):
        return
    sq = pixel_to_sq(px, py)
    if sq is None:
        return
    r, c  = sq
    piece = ps.board[r][c]

    if ps.selected is None:
        if piece and piece.color == ps.turn:
            ps.selected    = (r, c)
            ps.valid_moves = legal_moves(ps.board, r, c, ps.en_passant_target)
    else:
        sr, sc = ps.selected
        if (r, c) in ps.valid_moves:
            _puzzle_validate_and_move(ps, sr, sc, r, c)
        elif piece and piece.color == ps.turn:
            ps.selected    = (r, c)
            ps.valid_moves = legal_moves(ps.board, r, c, ps.en_passant_target)
        else:
            ps.selected = None; ps.valid_moves = []


# ---------------------------------------------------------------------------
# Helpers: create the right state object for a game key
# ---------------------------------------------------------------------------
def _make_puzzle_state(game_key):
    return PuzzleState(game_key)

def _make_replay_state(game_key):
    return ReplayState(game_key)

def _make_state(game_key):
    if GAMES[game_key]['mode'] == 'replay':
        return _make_replay_state(game_key)
    return _make_puzzle_state(game_key)


# ---------------------------------------------------------------------------
# Shared nav-popup handler (works for both state types)
# ---------------------------------------------------------------------------
def _handle_nav_arrow_click(state, dest_key):
    """Called when user clicks an outer game-navigation arrow."""
    is_ps   = isinstance(state, PuzzleState)
    finished = (state.status == 'solved') if is_ps else state.is_finished
    state.nav_pending_key = dest_key
    state.show_nav_popup  = True
    if finished:
        state.nav_popup_timer = int(FPS * 1.5)

def _handle_nav_popup_action(state, action):
    """Returns new state object or same state depending on action."""
    if action == 'stay':
        state.show_nav_popup  = False
        state.nav_pending_key = None
        return state
    elif action == 'confirm':
        dest = state.nav_pending_key
        state.reset()
        new_state = _make_state(dest)
        return new_state
    return state

def _tick_nav_popup(state):
    """Auto-dismiss popup for finished games. Returns (possibly new) state."""
    is_ps    = isinstance(state, PuzzleState)
    finished = (state.status == 'solved') if is_ps else state.is_finished
    if state.show_nav_popup and finished and state.nav_popup_timer > 0:
        state.nav_popup_timer = max(0, state.nav_popup_timer - 1)
        if state.nav_popup_timer == 0:
            dest = state.nav_pending_key
            state.reset()
            return _make_state(dest)
    return state


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Chess  --  The Brain Games Academy")
    clock = pygame.time.Clock()

    piece_font, ui_font, small_font, tab_font, title_font = load_fonts()

    app_mode = 'play'
    gs       = GameState()
    # Active puzzle/replay state — can be PuzzleState or ReplayState
    cur_state = _make_state('game1')

    running = True
    while running:
        clock.tick(FPS)

        # ---- Events -------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if app_mode == 'play':
                    if event.key == pygame.K_r:
                        gs = GameState()
                elif app_mode == 'puzzle':
                    if not cur_state.show_nav_popup:
                        if isinstance(cur_state, PuzzleState):
                            if event.key == pygame.K_r:
                                cur_state.reset()
                            elif event.key == pygame.K_h and cur_state.status not in ('solved',):
                                cur_state.hint_timer = FPS * 3
                        elif isinstance(cur_state, ReplayState):
                            if event.key == pygame.K_LEFT and cur_state.step > 0:
                                cur_state.step -= 1
                            elif event.key == pygame.K_RIGHT and not cur_state.is_finished:
                                cur_state.step += 1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px, py = event.pos

                # Main tab bar click
                mode = tab_click(px, py)
                if mode:
                    app_mode = mode

                elif app_mode == 'play':
                    if gs.status in ('playing', 'check') or gs.promotion_pending:
                        handle_play_click(gs, px, py)

                elif app_mode == 'puzzle':
                    if cur_state.show_nav_popup:
                        action = get_nav_popup_click(cur_state, px, py)
                        cur_state = _handle_nav_popup_action(cur_state, action)

                    elif isinstance(cur_state, ReplayState):
                        # Outer game-nav arrows (far left / far right)
                        nav_clicked = False
                        for rect, dest_key, _dir in get_arrow_rects(cur_state):
                            if rect.collidepoint(px, py):
                                _handle_nav_arrow_click(cur_state, dest_key)
                                nav_clicked = True
                                break
                        if not nav_clicked:
                            # Inner step arrows (◄ prev / ► next move)
                            prev_r, next_r = get_replay_step_arrow_rects(cur_state)
                            if prev_r.collidepoint(px, py) and cur_state.step > 0:
                                cur_state.step -= 1
                            elif next_r.collidepoint(px, py) and not cur_state.is_finished:
                                cur_state.step += 1

                    elif isinstance(cur_state, PuzzleState):
                        # Outer game-nav arrows
                        nav_clicked = False
                        for rect, dest_key, _dir in get_arrow_rects(cur_state):
                            if rect.collidepoint(px, py):
                                _handle_nav_arrow_click(cur_state, dest_key)
                                nav_clicked = True
                                break
                        if not nav_clicked:
                            handle_puzzle_click(cur_state, px, py)

        # ---- Timers -------------------------------------------------------
        if app_mode == 'puzzle':
            if isinstance(cur_state, PuzzleState):
                if cur_state.hint_timer > 0:
                    cur_state.hint_timer = max(0, cur_state.hint_timer - 1)
                if cur_state.correct_timer > 0:
                    cur_state.correct_timer = max(0, cur_state.correct_timer - 1)
                if cur_state.status == 'wrong' and cur_state.flash_timer > 0:
                    cur_state.flash_timer = max(0, cur_state.flash_timer - 1)
                    if cur_state.flash_timer == 0:
                        cur_state.reset()
            cur_state = _tick_nav_popup(cur_state)

        # ---- Draw ---------------------------------------------------------
        screen.fill(C_BG)

        if app_mode == 'play':
            chk_pos = find_king(gs.board, gs.turn) if gs.status == 'check' else None
            draw_board_and_pieces(
                screen, gs.board, gs.selected, gs.valid_moves, piece_font,
                check_king_pos=chk_pos)
            draw_play_status(screen, gs, ui_font, small_font)
            if gs.promotion_pending:
                draw_promotion_popup(screen, gs, piece_font, ui_font)

        elif app_mode == 'puzzle':
            if isinstance(cur_state, ReplayState):
                draw_board_and_pieces(
                    screen, cur_state.board, None, [], piece_font,
                    last_move=cur_state.last_move)
                draw_replay_status(screen, cur_state, ui_font, small_font)
                if cur_state.show_nav_popup:
                    draw_nav_popup(screen, cur_state, ui_font, small_font)

            elif isinstance(cur_state, PuzzleState):
                pz      = cur_state.puzzle
                chk_pos = find_king(cur_state.board, cur_state.turn) \
                          if cur_state.status == 'check' else None
                hint_rc = alg_to_rc(pz['hint_sq']) if cur_state.hint_timer > 0 else None
                wrong_alpha = 0
                if cur_state.status == 'wrong' and cur_state.flash_timer > 0:
                    wrong_alpha = int(110 * cur_state.flash_timer / (FPS * 2))
                correct_rc = None
                if not pz['free_play'] and cur_state.correct_timer > 0 and cur_state.move_step > 0:
                    correct_rc = alg_to_rc(pz['solution'][cur_state.move_step - 1][1])
                draw_board_and_pieces(
                    screen, cur_state.board, cur_state.selected,
                    cur_state.valid_moves, piece_font,
                    check_king_pos=chk_pos,
                    hint_sq=hint_rc,
                    wrong_flash_alpha=wrong_alpha,
                    correct_sq=correct_rc)
                draw_puzzle_status(screen, cur_state, ui_font, small_font)
                if cur_state.show_nav_popup:
                    draw_nav_popup(screen, cur_state, ui_font, small_font)

        draw_tabs(screen, app_mode, tab_font, title_font)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
