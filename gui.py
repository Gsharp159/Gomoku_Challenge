import gomoku.algorithms
import pygame as pg
import tensorflow as tf
import numpy as np
import sys
from copy import deepcopy

print('done imports')
#
#End goal is to migrate away from pygame. I'm using it for simplicity at the moment
#

def GUIWindow():
    board = gomoku.board
    width = 1200
    height = 800
    white = (255, 255, 255)
    black = (0, 0, 0)
    fps = 30
    CLOCK = pg.time.Clock()
    global updatemsg, message
    updatemsg = True
    message = 'init'

    pg.init()
    screen = pg.display.set_mode((width, height), 0, fps)
    pg.display.set_caption("shut up")

    black_img = pg.image.load("Assets/black_stone.png")
    white_img = pg.image.load("Assets/white_stone.png")
    board_image = pg.image.load("Assets/board_image.png")
    green_square = pg.image.load("Assets/green.png")
    button_b = pg.image.load("Assets/button_black.png")
    button_w = pg.image.load("Assets/button_white-2.png")

    #resize
    black_img = pg.transform.scale(black_img, (40, 40))
    white_img = pg.transform.scale(white_img, (40, 40))
    board_image = pg.transform.scale(board_image, (730, 730)) #650->730 scale = 1.123
    green_square = pg.transform.scale(green_square, (14, 14))

    #model = tf.keras.models.load_model("models/dq_0.1.3", compile=False)
    #model.compile(loss='', optimizer = tf.keras.optimizers.legacy.Adam())
    #print(model(np.array(board).flatten().reshape(1, 169)))

    def game_initiating_window():
        screen.fill((40, 40, 40))

        #font = pg.font.Font(None, 40)

        #text = font.render(str(driver.bot_func), 1, black)

        #screen.fill(white, (300, 75, 300, 75))
        #text_rect = text.get_rect(center=(320, 320))
        #screen.blit(text, text_rect)

        #pg.display.update()
        #time.sleep(4)
        draw_window()



    def draw_window():
        screen.blit(board_image, (35, 35)) 
        global updatemsg, message

        if updatemsg:
            #out = model((np.array(board).flatten()).reshape(1, 169))
            #message = str([round(n, 2) for n in tf.nn.softmax(out).numpy()[0]])
            message = 'hi'

            if gomoku.checkWin(1, board):
                message = 'Black takes the dub'
            if gomoku.checkWin(-1, board):
                message = 'white *fortnite dance*'

            updatemsg = False

        font = pg.font.Font(None, 40)

        text = font.render(message, 1, black)

        screen.fill(white, ((width / 2) + 200, 75, 350, 75))
        text_rect = text.get_rect(center=((width / 2) + 375, 115))
        screen.blit(text, text_rect)

        screen.blit(button_b, (800, 195))
        screen.blit(button_w, (985, 195))

        draw_board()

        pg.display.update()

    def draw_board():

        v = gomoku.prune(board)

        for i in range(13):
            for k in range(13):
                if board[i][k] == 0:
                    if v[i][k]:
                        screen.blit(green_square, ((i * 55) + 63, (k * 55)+ 63))
                    continue
                if board[i][k] == -1:
                    screen.blit(white_img, ((i * 55) + 48, (k * 55) + 48))
                if board[i][k] == 1:
                    screen.blit(black_img, ((i * 55) + 48, (k * 55) + 48))


    def user_click():
        global updatemsg

        x, y = pg.mouse.get_pos()
        coords = [0, 0]

        if not ((x >= 35) and (x <= 765)):
            #clicked outside board
            pass
        else:
            x = (x - 35)
            x = round(x / (730 / 12))

            coords[0] = x

        if not ((y >= 35) and (y <= 765)):
            #clicked outside board
            pass
        else:
            y = (y - 35)
            y = round(y / (730 / 12))

            coords[1] = y

        aiTurn = True
        if board[coords[0]][coords[1]] != 0:
            aiTurn = False
        else:
            gomoku.place(-1, (coords))
        draw_window()

        if aiTurn:
            #aiMove = lengthOptimizer(1, board)
            #aiMove = minimax(1, board, _depth=2)[0]
            gomoku.placeAiMove(1, deepcopy(board), func=gomoku.algorithms.MCTS)
            #res = tf.nn.softmax(model(np.array(board).flatten().reshape(1, 169)))
            #action = np.argmax(res[0])
            #aiMove = (action // 13, action % 13)
            #print(aiMove, (np.array(res)))
            #board[aiMove[0]][aiMove[1]] = 1
            draw_window()

        updatemsg = True
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

if __name__ == "__main__":
    GUIWindow()