from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.piece_code import PieceCode
from pieces.queen import Queen
from pieces.rookie import Rookie

class PieceFactory:
    def create(fen_code: str, cell_size: int) -> Piece:
        return {
            PieceCode.PAWN: Pawn(cell_size, True),
            PieceCode.ROOKIE: Rookie(cell_size, True),
            PieceCode.KNIGHT: Knight(cell_size, True),
            PieceCode.BISHOP: Bishop(cell_size, True),
            PieceCode.QUEEN: Queen(cell_size, True),
            PieceCode.KING: King(cell_size, True),
            f'{PieceCode.PAWN.lower()}': Pawn(cell_size, False),
            f'{PieceCode.ROOKIE.lower()}': Rookie(cell_size, False),
            f'{PieceCode.KNIGHT.lower()}': Knight(cell_size, False),
            f'{PieceCode.BISHOP.lower()}': Bishop(cell_size, False),
            f'{PieceCode.QUEEN.lower()}': Queen(cell_size, False),
            f'{PieceCode.KING.lower()}': King(cell_size, False),
        }[fen_code]