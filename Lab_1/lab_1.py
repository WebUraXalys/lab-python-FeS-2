1# Оголошення і початкове заповнення дошки
tabel = [
    ['-','-','-'],
    ['-','-','-'],
    ['-','-','-']
]

# Функція для виводу поточного стану дошки
def print_board(board):
    for row in board:
        for cell in row:
            print (cell, end=' ')
        print()

# Функція для перевірки наявності перемоги одного з гравців
def check_win(board, plaer):
    # Перевірка рядків
    for row in board:
        if row.count(plaer) == 3:
            return True
            
    # Перевірка стовпчиків
    for i in range(3):
        if board[0][i] == plaer and board[1][i] == plaer and board[2][i] == plaer:
            return True    
        
    # Перевірка діагоналей
    if board[0][0] == plaer and board[1][1] == plaer and board[2][2] == plaer:
        return True 
    if board[0][2] == plaer and board[1][1] == plaer and board[2][0] == plaer:
        return True 
            
# Початковий гравець 'X'
current_plaer = 'X'

# Геймплей
while True:
    # Вивід поточного стану дошки
    print_board(tabel)
    print('Хід Гравця', current_plaer)
    # Ввід координати від гравця
    row = int(input('Введіть номер рядка: ')) - 1
    col = int(input('Введіть номер стовбця: ')) - 1
    # Перевірка наявності вільної комірки
    if tabel[row][col] != '-':
        print('Комірка зайнята!')
        continue
    
    # Постановка символу гравця на дошку
    tabel[row][col] = current_plaer
    
    # Перевірка на перемогу
    if check_win(tabel, current_plaer):
        print_board(tabel)
        print(f'Гравець {current_plaer} переміг!')
        break
        
    # Перевірка на нічию
    if all([cell != '-' for row in tabel for cell in row]):
        print('Нічия!')
        print_board(tabel)
        break
    
    # Зміна гравця
    current_plaer = '0' if current_plaer == 'X' else 'X'
