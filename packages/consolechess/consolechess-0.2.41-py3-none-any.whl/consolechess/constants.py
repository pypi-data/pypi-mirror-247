"""Constants for ChessBoard."""

from platform import system

from .datatypes import Color, Piece, PieceType, Side

COLORS: tuple[Color, Color] = ("white", "black")
SIDES: tuple[Side, Side] = ("queenside", "kingside")
FILES = list("abcdefgh")
SQUARES = [f"{file}{rank}" for rank in range(1, 9) for file in FILES]
PIECE_SYMBOLS: dict[PieceType, str] = {
    "king": "♚",
    "queen": "♛",
    "rook": "♜",
    "bishop": "♝",
    "knight": "♞",
    "pawn": "♟︎" if "Windows" not in system() else ":chess_pawn:",
}
BLACK_SQUARES = [f"{file}{rank}" for file in "aceg" for rank in (1, 3, 5, 7)] + [
    f"{file}{rank}" for file in "bdfh" for rank in (2, 4, 6, 8)
]
WHITE_SQUARES = [sq for sq in SQUARES if sq not in BLACK_SQUARES]
PLAINTEXT_ABBRS: dict[str, str] = {
    "knight": "N",
    "rook": "R",
    "bishop": "B",
    "pawn": "P",
    "queen": "Q",
    "king": "K",
}
ALGEBRAIC_PIECE_ABBRS: dict[str, PieceType] = {
    "K": "king",
    "Q": "queen",
    "R": "rook",
    "B": "bishop",
    "N": "knight",
    "": "pawn",
}
FEN_REPRESENTATIONS: dict[str, Piece] = {
    "N": Piece("knight", "white"),
    "K": Piece("king", "white"),
    "R": Piece("rook", "white"),
    "B": Piece("bishop", "white"),
    "Q": Piece("queen", "white"),
    "P": Piece("pawn", "white"),
    "n": Piece("knight", "black"),
    "k": Piece("king", "black"),
    "r": Piece("rook", "black"),
    "b": Piece("bishop", "black"),
    "q": Piece("queen", "black"),
    "p": Piece("pawn", "black"),
}
PIECES: list[Piece] = [
    *([Piece("rook", "white")] * 2),
    *([Piece("knight", "white")] * 2),
    *([Piece("bishop", "white")] * 2),
    Piece("queen", "white"),
    Piece("king", "white"),
    *([Piece("pawn", "white")] * 8),
    *([Piece("rook", "black")] * 2),
    *([Piece("knight", "black")] * 2),
    *([Piece("bishop", "black")] * 2),
    Piece("queen", "black"),
    Piece("king", "black"),
    *([Piece("pawn", "black")] * 8),
]
KNIGHT_MOVES = [
    ((up_down, steps_1), (left_right, steps_2))
    for up_down in ("up", "down")
    for left_right in ("left", "right")
    for steps_1, steps_2 in ((1, 2), (2, 1))
]
CASTLING_FINAL_SQUARES: dict[tuple[Color, Side], tuple[str, str]] = {
    ("white", "kingside"): ("g1", "f1"),  # color, side: rook, king
    ("white", "queenside"): ("c1", "d1"),
    ("black", "kingside"): ("g8", "f8"),
    ("black", "queenside"): ("c8", "d8"),
}
