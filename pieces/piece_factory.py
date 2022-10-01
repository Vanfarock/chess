from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece_code import PieceCode
from pieces.queen import Queen
from pieces.rookie import Rookie

class PieceFactory:
    def create(fen_code: str, x: int, y: int, cell_size: int):
        return {
            PieceCode.PAWN: Pawn(x, y, cell_size, True),
            PieceCode.ROOKIE: Rookie(x, y, cell_size, True),
            PieceCode.KNIGHT: Knight(x, y, cell_size, True),
            PieceCode.BISHOP: Bishop(x, y, cell_size, True),
            PieceCode.QUEEN: Queen(x, y, cell_size, True),
            PieceCode.KING: King(x, y, cell_size, True),
            f'{PieceCode.PAWN.lower()}': Pawn(x, y, cell_size, False),
            f'{PieceCode.ROOKIE.lower()}': Rookie(x, y, cell_size, False),
            f'{PieceCode.KNIGHT.lower()}': Knight(x, y, cell_size, False),
            f'{PieceCode.BISHOP.lower()}': Bishop(x, y, cell_size, False),
            f'{PieceCode.QUEEN.lower()}': Queen(x, y, cell_size, False),
            f'{PieceCode.KING.lower()}': King(x, y, cell_size, False),
        }[fen_code]