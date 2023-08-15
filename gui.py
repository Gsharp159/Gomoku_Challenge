import gom_challenge
import pygame as pg

def GUIWindow():
    width = 1200
    height = 800
    white = (255, 255, 255)
    black = (0, 0, 0)
    fps = 30
    CLOCK = pg.time.Clock()

    pg.init()
    screen = pg.display.set_mode((width, height), 0, fps)
    pg.display.set_caption("shut up")

    intiating_window = pg.image.load("Assets/photo_five_comp.jpg")
    black_img = pg.image.load("Assets/black_stone.png")
    white_img = pg.image.load("Assets/white_stone.png")
    board_image = pg.image.load("Assets/board_image.png")
    green_square = pg.image.load("Assets/green.png")

    #resize
    intiating_window = pg.transform.scale(intiating_window, (width, height))
    black_img = pg.transform.scale(black_img, (35, 35))
    white_img = pg.transform.scale(white_img, (35, 35))
    board_image = pg.transform.scale(board_image, (650, 650))
    green_square = pg.transform.scale(green_square, (10, 10))

    def game_initiating_window():
        #screen.blit(intiating_window, (0, 0))

        #pg.display.update()
        #time.sleep(0.5)
        screen.fill(black)

        draw_window()

    def draw_window():

        screen.blit(board_image, ((width / 2) - 500, (height / 2) - 325))

        message = str(longestSequential(1, board, block_detect=False))

        if checkWin(1, board):
            message = 'Black takes the dub'
        if checkWin(-1, board):
            message = 'white *fortnite dance*'

        font = pg.font.Font(None, 40)

        text = font.render(message, 1, black)

        screen.fill(white, ((width / 2) + 200, 75, 350, 75))
        text_rect = text.get_rect(center=((width / 2) + 375, 115))
        screen.blit(text, text_rect)

        draw_board()

        pg.display.update()

    def draw_board():
        #first row is 87, last is 677.5 dif is 45.4
        #first col is 112, last is 702.5
        #row * 45.4 + 87 ? smth like this

        v = prune(board)

        for i in range(13):
            for k in range(13):
                if board[i][k] == 0:
                    if v[i][k]:
                        screen.blit(green_square, ((i * 49.2) + 125, (k * 49.2)+ 100))
                    continue
                if board[i][k] == -1:
                    screen.blit(white_img, ((i * 49.2) + 112, (k * 49.2)+ 87))
                if board[i][k] == 1:
                    screen.blit(black_img, ((i * 49.2) + 112, (k * 49.2)+ 87))


    def user_click():

        first = (112, 87)
        last = (737.5, 702.5)

        x, y = pg.mouse.get_pos()
        coords = [0, 0]

        if not ((x >= 112) and (x <= 737.5)):
            pass#raise Exception('ur only allowed to click the board rn bb')
        else:
            x = (x - 112)
            x = round(x / (625.5 / 12))

            coords[0] = x

        if not ((y >= 87) and (y <= 737.5)):
            pass#raise Exception('ur only allowed to click the board rn bb')
        else:
            y = (y - 87)
            y = round(y / (625.5 / 12))

            coords[1] = y

        aiTurn = True
        if board[coords[0]][coords[1]] != 0:
            aiTurn = False
        else:
            board[coords[0]][coords[1]] = -1
        draw_window()

        if aiTurn:
            ###ai func
            #aiMove = lengthOptimizer(1, board)
            aiMove = minimax(1, board, 1)[0]
            #print(aiMove)
            board[aiMove[0]][aiMove[1]] = 1
            draw_window()

    game_initiating_window()

    while(True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if any(pg.mouse.get_pressed()):
                user_click()

                if(False):
                    reset_game()

        draw_window()
        pg.display.update()
        CLOCK.tick(fps)