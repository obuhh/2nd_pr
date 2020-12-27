import sys
import math
import random
import pygame

pygame.init()
win = pygame.display.set_mode((850, 600))
pygame.display.set_caption("koni")
ba = pygame.image.load('skin/b.png')
wk = [pygame.image.load('skin/w.png'), pygame.image.load('skin/g.png'), pygame.image.load('skin/r.png')]
men = pygame.image.load('skin/menu.png')
map_len = 6
next_step = [[-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2]]
COMP_STEP = False
AI_TURN = True
USER_TURN = False

b = []
for i in range(6):
    b.append([0] * 6)

def can_go(field, x, y, gx, gy):
    print(x,' ',y,' ',gx,' ',gy,' ',math.fabs(gx - x),' ',math.fabs(gy - y),' ',field[gx][gy], ' ',(field[gy][gx] == 0))
    if (x < 0):
        return True
    if (((math.fabs(gx - x) == 2) and (math.fabs(gy - y) == 1)) or (
            (math.fabs(gx - x) == 1) and (math.fabs(gy - y) == 2))) and (field[gy][gx] == 0):
        return True
    return False


def print_text(message, x, y, font_color=(0, 0, 0), font_size=30):
    # font_type = pygame.font.Font(font_type, font_size)
    font = pygame.font.SysFont('comicsansms', font_size)
    text = font.render(message, 1, font_color)
    win.blit(text, (x, y))


def drawWindow(st, gw, cw):
    global COMP_STEP
    for i in range(map_len):
        for j in range(map_len):
            # win.blit(wk[0], (j * 100, i * 100))
            if b[i][j] == 0:
                win.blit(wk[0], (j * 100, i * 100))
            elif b[i][j] % 2:
                win.blit(wk[1], (j * 100, i * 100))
                print_text(str(b[i][j]), j * 100 + 7, i * 100)
            else:
                win.blit(wk[2], (j * 100, i * 100))
                print_text(str(b[i][j]), j * 100 + 7, i * 100)
    win.blit(ba, (600, 0))
    if COMP_STEP:
        print_text("Computer turn", 620, 10)
    else:
        print_text("Your turn", 620, 10)
    print_text("Last move " + str(st - 1), 620, 50)
    print_text("Press esc to", 620, 470)
    print_text("bring up", 620, 510)
    print_text("the menu", 620, 550)
    if gw:
        print_text("!You win!", 620, 270)
    if cw:
        print_text("!Computer win!", 620, 270)


def new_game():
    global b
    global nx
    global ny
    global st
    global COMP_STEP
    global gwin
    global cwin
    for i in range(6):
        for j in range(6):
            b[i][j] = 0
    nx = -2
    ny = -2
    st = 1
    COMP_STEP = False
    gwin = False
    cwin = False


def menu():
    kek = True
    while kek:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            new_game()
            kek = False
        if keys[pygame.K_b]:
            kek = False
        win.blit(men, (0, 0))
        pygame.display.update()

def is_draw(field, x, y):
    count = 0
    for i in range(8):
        nay = y + next_step[i][0]
        nax = x + next_step[i][1]
        if (nay >= 0) and (nay < map_len) and (nax >= 0) and (nax < map_len) and (field[nay][nax] == 0):
            count += 1
    return count == 0

def minimax(board, depth, is_ai_turn, x, y, alpha, beta, st):
    if depth > 6 and st == 2:
        return  -25
    if depth >= 12 and st < 10:
        return -15
    #global kk
    #kk += 1
    if is_draw(board, x, y):
        if is_ai_turn:
            return -100
        else:
            return 100 - depth

    if is_ai_turn:
        best_score = - sys.maxsize
        for i in range(8):
            nay = y + next_step[i][0]
            nax = x + next_step[i][1]
            if (nay >= 0) and (nay < map_len) and (nax >= 0) and (nax < map_len) and (board[nay][nax] == 0):
                board[nay][nax] = st
                score = minimax(board, depth + 1, USER_TURN, nax, nay, alpha, beta, st)
                board[nay][nax] = 0
                best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta < alpha:
                break
    else:
        best_score = sys.maxsize
        for i in range(8):
            nay = y + next_step[i][0]
            nax = x + next_step[i][1]
            if (nay >= 0) and (nay < map_len) and (nax >= 0) and (nax < map_len) and (board[nay][nax] == 0):
                board[nay][nax] = st
                score = minimax(board, depth + 1, AI_TURN, nax, nay, alpha, beta, st)
                board[nay][nax] = 0
                best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta < alpha:
                break
    return best_score


def get_computer_position(field, x, y, st):
    #global kk
    #kk = 0
    move = None
    best_score = -sys.maxsize
    board = []
    for i in range(6):
        board.append([0] * 6)
    for i in range(6):
        for j in range(6):
            board[i][j] = field[i][j]
    for i in range(8):
        nay = y + next_step[i][0]
        nax = x + next_step[i][1]
        if (nay >= 0) and (nay < map_len) and (nax >= 0) and (nax < map_len) and (board[nay][nax] == 0):
            board[nay][nax] = st
            score = minimax(board, 0, USER_TURN, nax, nay, -10000000000, 100000000000, st)
            board[nay][nax] = 0
            if score > best_score:
                best_score = score
                move = (nax, nay)
                print("ck ", score)
            elif (score == best_score) and (random.randint(0, 1)):
                move = (nax, nay)
                print("ch ", score)
    #print(kk)
    return move

run = True
gwin = False
cwin = False
nx = -2
ny = -2
st = 1
menu()
drawWindow(st, gwin, cwin)
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        menu()
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if COMP_STEP:
        move = get_computer_position(b, nx, ny, st)
        x, y = move
        print(x, ' ', y)
        b[y][x] = st
        st += 1
        nx = x
        ny = y
        COMP_STEP = False
        if is_draw(b, nx, ny):
            cwin = True
    else:
        if pressed[0] and (pos[1] < 600) and (pos[0] < 600) and not gwin and not cwin:
            y = ((pos[1] - 1) // 100)
            x = ((pos[0] - 1) // 100)
            print(pos[0],' ', pos[1],' ',x,' ',y)
            if can_go(b, nx, ny, x, y):
                b[y][x] = st
                st += 1
                nx = x
                ny = y
                COMP_STEP = True
                if is_draw(b, nx, ny):
                    COMP_STEP = False
                    gwin = True
    drawWindow(st, gwin, cwin)
    pygame.display.update()
pygame.quit()
