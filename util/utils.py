from pieces.piece_code import PieceCode


def is_inside_board(board, cell_x, cell_y):
    return not (cell_x < 0 or cell_y < 0 or cell_x >= len(board[0]) or cell_y >= len(board))

def from_code(code: str):
    will_eat = False
    will_check = False
    if code[0] == '+':
        will_check = True
        code = code[1:]
    
    if code[0] == 'x':
        will_eat = True
        code = code[1:]

    x = ord(code[0]) - 97
    y = 8 - int(code[1])
    return (x, y), will_eat, will_check

def to_code(x: int, y: int, will_eat: bool = False, will_check: bool = False):
    code = str(chr(x + 97)) + str(8 - y)
    if will_eat:
        code = f'x{code}'
    if will_check:
        code = f'+{code}'
    return code

def remove_code_modifiers(code: str):
    if code[0] == '+':
        code = code[1:]
    
    if code[0] == 'x':
        code = code[1:]

    return code

def is_king(piece):
    return piece.get_fen_code().lower() == PieceCode.KING.lower()
 