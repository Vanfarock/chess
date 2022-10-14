from pieces.piece_code import PieceCode

def is_inside_board(board, cell_x, cell_y):
    return not (cell_x < 0 or cell_y < 0 or cell_x >= len(board[0]) or cell_y >= len(board))

def from_code(code: str):
    will_eat = False
    will_castle = False
    will_promote = False

    if code[0] == 'p':
        will_promote = True
        code = code[1:]

    if code[0] == 'r':
        will_castle = True
        code = code[1:]
    
    if code[0] == 'x':
        will_eat = True
        code = code[1:]

    x = ord(code[0]) - 97
    y = 8 - int(code[1])
    return (x, y), will_eat, will_castle, will_promote

def to_code(x: int, y: int, will_eat: bool = False, will_castle: bool = False, will_promote: bool = False):
    code = str(chr(x + 97)) + str(8 - y)
    if will_eat:
        code = f'x{code}'
    if will_castle:
        code = f'r{code}'
    if will_promote:
        code = f'p{code}'
    return code

def remove_code_modifiers(code: str):
    if code[0] == 'p':
        code = code[1:]

    if code[0] == 'r':
        code = code[1:]
    
    if code[0] == 'x':
        code = code[1:]

    return code

def is_king(piece):
    return piece.get_fen_code().lower() == PieceCode.KING.lower()
 
def is_rookie(piece) -> bool:
    return piece.get_fen_code().lower() == PieceCode.ROOKIE.lower()

def is_pawn(piece) -> bool:
    return piece.get_fen_code().lower() == PieceCode.PAWN.lower()