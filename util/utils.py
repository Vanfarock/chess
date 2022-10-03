def is_inside_board(board, cell_x, cell_y):
    return not (cell_x < 0 or cell_y < 0 or cell_x >= len(board[0]) or cell_y >= len(board))

def from_code(code: str):
    x = ord(code[0]) - 97
    y = 8 - int(code[1])
    return (x, y)

def to_code(x: int, y: int):
    return (chr(x + 97), 8 - y)
