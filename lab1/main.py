board = [['_'] * 3 for i in range(3)]
xo_list = ['X'] + ['O', 'X'] * 4


def p(mymap):
    print('-------------')
    for i in range(3):
        print('| {0} | {1} | {2} |'.format(*mymap[i]))
        print('-------------')


def win_validation(mymap, symb):
    raw_cols = [row[i] for i in range(3) for row in mymap]
    cols = [raw_cols[i : i + 3] for i in range(0, 9, 3)]
    diagonals = [[mymap[i][i] for i in range(3)], [mymap[i][2 - i] for i in range(3)]]

    for row in mymap + cols + diagonals:
        if all(True if i == symb else False for i in row):
            return True

    return False


def main(mymap):
    p(mymap)
    for i in xo_list:

        while True:
            y, x = int(input('x = ')), int(input('y = '))

            if mymap[x][y] == '_':
                break

        mymap[x][y] = i

        p(mymap)

        if win_validation(mymap, i):
            print('Good game')
            break
        
    print('Draw')
        
        


if __name__ == '__main__':
    main(board)