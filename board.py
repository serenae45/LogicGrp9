BOARD = [
    '[0][0]',
    '[0][1]',
    '[0][2]',
    '[1][0]',
    '[1][1]',
    '[1][2]',
    '[2][0]',
    '[2][1]',
    '[2][2]'
]

for pos in BOARD:
    if pos != '[0][0]':
        print(pos-1)
