import pygame
from random import choice, randint
from sys import exit
from copy import deepcopy
from pygame.locals import *
from Color import color
from constants import constants as cst


def drawTitle():
    title_font = pygame.font.Font(cst.font, 55)
    title_obj = title_font.render('Digit Dash', 1, color.foreground)
    title_rect = title_obj.get_rect()
    title_rect.center = (cst.widthOfWindow / 2, 105)
    display.blit(title_obj, title_rect)


def drawBorder():
    OuterSquare = pygame.Rect(0, 0, 357, 357)
    OuterSquare.center = (cst.widthOfWindow / 2, cst.heightOfWindow / 2 + 20)
    pygame.draw.rect(display, color.foreground, OuterSquare)
    InnerSquare = pygame.Rect(0, 0, 351, 351)
    InnerSquare.center = (cst.widthOfWindow / 2, cst.heightOfWindow / 2 + 20)
    pygame.draw.rect(display, color.background, InnerSquare)


def startScreen():
    entry_font = pygame.font.Font(cst.font, 75)
    entries = ['Start', 'Quit']
    selected_entry = 0

    while True:
        display.fill(color.background)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    selected_entry = (selected_entry - 1) % len(entries)
                elif event.key == K_DOWN or event.key == K_s:
                    selected_entry = (selected_entry + 1) % len(entries)
                elif event.key == K_ESCAPE:
                    quit()
                elif event.key == K_RETURN:
                    if selected_entry == 0:
                        RunGame()
                    elif selected_entry == 1:
                        quit()

        drawTitle()

        for i in range(len(entries)):
            if i == selected_entry:
                entry_color = color.hover
            else:
                entry_color = color.foreground

            entry_obj = entry_font.render(entries[i], 1, entry_color)
            entry_rect = entry_obj.get_rect()
            entry_rect.center = (cst.widthOfWindow / 2, 250 + 110 * i)
            display.blit(entry_obj, entry_rect)

        pygame.display.update()
        fps.tick(cst.FPS)


def RunGame():
    tiles = color.colorPalet1
    gameState = [[0 for _ in range(4)] for _ in range(4)]
    gameStateBefore = [[0 for _ in range(4)] for _ in range(4)]
    moves = []
    presentTiles = []
    game_dynamics = {
        'status': 'dynamic',
        'i': 11
    }
    totalScore = 0
    colorBorder1 = color.hover
    colorBorder2 = color.hover
    colorBorder3 = color.hover


    centers_coordinates = [[(0, 0) for _ in range(4)] for _ in range(4)]
    for row in range(4):
        for col in range(4):
            centers_coordinates[row][col] = [12 + 45 + (84 + 3) * col, 178 + 45 + (84 + 3) * row]

    def drawGameState(game_state_passed):
        for row in range(4):
            for col in range(4):
                if game_state_passed[row][col] != 0:
                    drawTile(row, col, game_state_passed[row][col])

    def drawTile(row, col, number):
        TileBackRect = pygame.Rect(0, 0, 84, 84)
        TileBackRect.center = centers_coordinates[row][col]
        pygame.draw.rect(display, tiles[number], TileBackRect)

        font_size = 28
        if number >= 1024:
            font_size = 19
        TileFont = pygame.font.Font(cst.digitFont, font_size)
        TileObj = TileFont.render(str(number), 1, color.foreground)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row][col]
        display.blit(TileObj, TileRect)

    def spawnTile(row, col, number, movement_i):
        TileBackRect = pygame.Rect(0, 0, 49, 49)
        TileBackRect.center = centers_coordinates[row][col]

        font_size = 28
        if number >= 1024:
            font_size = 19
        TileFont = pygame.font.Font(cst.glitchDigitFont, font_size)
        TileObj = TileFont.render(str(number), 1, color.foreground)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row][col]

        if movement_i > 5:
            movement_i = 5

        TileBackRect = TileBackRect.inflate(7 * movement_i, 7 * movement_i)
        TileBackRect.center = centers_coordinates[row][col]

        pygame.draw.rect(display, tiles[number], TileBackRect)
        display.blit(TileObj, TileRect)

    def drawMovingTile(params, movement_i):
        row_s, col_s, row_f, col_f, number, flag = params
        TileBackRect = pygame.Rect(0, 0, 84, 84)
        TileBackRect.center = centers_coordinates[row_s][col_s]

        font_size = 28
        if number >= 1024:
            font_size = 19
        TileFont = pygame.font.Font(cst.glitchDigitFont, font_size)
        TileObj = TileFont.render(str(number), 1, color.foreground)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row_f][col_f]

        if row_f < row_s:
            distance = centers_coordinates[row_s][col_s][1] - centers_coordinates[row_f][col_f][1]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0],
                                   centers_coordinates[row_s][col_s][1] - step * movement_i]
            TileRect.center = [centers_coordinates[row_s][col_s][0],
                               centers_coordinates[row_s][col_s][1] - step * movement_i]
        if row_f > row_s:
            distance = centers_coordinates[row_f][col_f][1] - centers_coordinates[row_s][col_s][1]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0],
                                   centers_coordinates[row_s][col_s][1] + step * movement_i]
            TileRect.center = [centers_coordinates[row_s][col_s][0],
                               centers_coordinates[row_s][col_s][1] + step * movement_i]
        if col_f < col_s:
            distance = centers_coordinates[row_s][col_s][0] - centers_coordinates[row_f][col_f][0]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0] - step * movement_i,
                                   centers_coordinates[row_s][col_s][1]]
            TileRect.center = [centers_coordinates[row_s][col_s][0] - step * movement_i,
                               centers_coordinates[row_s][col_s][1]]
        if col_f > col_s:
            distance = centers_coordinates[row_f][col_f][0] - centers_coordinates[row_s][col_s][0]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0] + step * movement_i,
                                   centers_coordinates[row_s][col_s][1]]
            TileRect.center = [centers_coordinates[row_s][col_s][0] + step * movement_i,
                               centers_coordinates[row_s][col_s][1]]

        pygame.draw.rect(display, tiles[number], TileBackRect)
        display.blit(TileObj, TileRect)

    def sumTile(row, col, number, movement_i):
        TileBackRect = pygame.Rect(0, 0, 74, 74)
        TileBackRect.center = centers_coordinates[row][col]

        font_size = 28
        if number >= 1024:
            font_size = 19
        TileFont = pygame.font.Font(cst.digitFont, font_size)
        TileObj = TileFont.render(str(number), 1, color.foreground)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row][col]

        if movement_i == 5:
            movement_i = 3
        if movement_i > 5:
            movement_i = 2

        TileBackRect = TileBackRect.inflate(5 * movement_i, 5 * movement_i)
        TileBackRect.center = centers_coordinates[row][col]

        pygame.draw.rect(display, tiles[number], TileBackRect)
        display.blit(TileObj, TileRect)

    def Move(direction):
        if direction == "left":
            for i in range(4):
                for j in range(1, 4):
                    if (gameState[i][j] != 0) and (gameState[i][j - 1] == 0):
                        placeHolder = gameState[i][j]
                        shiftI = 1
                        while (j - shiftI >= 0) and (gameState[i][j - shiftI] == 0):
                            gameState[i][j - shiftI] = gameState[i][j - shiftI + 1]
                            gameState[i][j - shiftI + 1] = 0
                            shiftI += 1
                        moves.append((i, j, i, j - shiftI + 1, placeHolder, 0))
        elif direction == "right":
            for i in range(4):
                for j in range(2, -1, -1):
                    if (gameState[i][j] != 0) and (gameState[i][j + 1] == 0):
                        placeHolder = gameState[i][j]
                        shiftI = 1
                        while (j + shiftI <= 3) and (gameState[i][j + shiftI] == 0):
                            gameState[i][j + shiftI] = gameState[i][j + shiftI - 1]
                            gameState[i][j + shiftI - 1] = 0
                            shiftI += 1
                        moves.append((i, j, i, j + shiftI - 1, placeHolder, 0))
        elif direction == "up":
            for i in range(1, 4):
                for j in range(4):
                    if (gameState[i][j] != 0) and (gameState[i - 1][j] == 0):
                        placeHolder = gameState[i][j]
                        shiftI = 1
                        while (i - shiftI >= 0) and (gameState[i - shiftI][j] == 0):
                            gameState[i - shiftI][j] = gameState[i - shiftI + 1][j]
                            gameState[i - shiftI + 1][j] = 0
                            shiftI += 1
                        moves.append((i, j, i - shiftI + 1, j, placeHolder, 0))
        elif direction == "down":
            for i in range(2, -1, -1):
                for j in range(4):
                    if (gameState[i][j] != 0) and (gameState[i + 1][j] == 0):
                        tmp_n_var = gameState[i][j]
                        shift_index = 1
                        while (i + shift_index <= 3) and (gameState[i + shift_index][j] == 0):
                            gameState[i + shift_index][j] = gameState[i + shift_index - 1][j]
                            gameState[i + shift_index - 1][j] = 0
                            shift_index += 1
                        moves.append((i, j, i + shift_index - 1, j, tmp_n_var, 0))

    def Sum(direction):
        scoreAdd = 0
        if direction == "left":
            for i in range(4):
                for j in range(1, 4):
                    if (gameState[i][j] != 0) and (gameState[i][j - 1] == gameState[i][j]):
                        placeHolder = gameState[i][j]
                        gameState[i][j - 1] = gameState[i][j - 1] * 2
                        gameState[i][j] = 0
                        moves.append((i, j, i, j - 1, placeHolder, 1))
                        scoreAdd += placeHolder * 2
        elif direction == "right":
            for i in range(4):
                for j in range(2, -1, -1):
                    if (gameState[i][j] != 0) and (gameState[i][j + 1] == gameState[i][j]):
                        PlaceHolder = gameState[i][j]
                        gameState[i][j + 1] = gameState[i][j + 1] * 2
                        gameState[i][j] = 0
                        moves.append((i, j, i, j + 1, PlaceHolder, 1))
                        scoreAdd += PlaceHolder * 2
        elif direction == "up":
            for i in range(1, 4):
                for j in range(4):
                    if (gameState[i][j] != 0) and (gameState[i - 1][j] == gameState[i][j]):
                        placeHolder = gameState[i][j]
                        gameState[i - 1][j] = gameState[i - 1][j] * 2
                        gameState[i][j] = 0
                        moves.append((i, j, i - 1, j, placeHolder, 1))
                        scoreAdd += placeHolder * 2
        elif direction == "down":
            for i in range(2, -1, -1):
                for j in range(4):
                    if (gameState[i][j] != 0) and (gameState[i + 1][j] == gameState[i][j]):
                        placeHolder = gameState[i][j]
                        gameState[i + 1][j] = gameState[i + 1][j] * 2
                        gameState[i][j] = 0
                        moves.append((i, j, i + 1, j, placeHolder, 1))
                        scoreAdd += placeHolder * 2
        return scoreAdd

    def MergeMovements():
        queueForDelete = []
        for i in range(len(moves)):
            for j in range(i + 1, len(moves)):
                if (moves[i][4] == moves[j][4]) and (moves[i][2] == moves[j][0]) and (
                        moves[i][3] == moves[j][1]):
                    moves[i] = (moves[i][0], moves[i][1], moves[j][2], moves[j][3], moves[j][4],
                                moves[j][5])
                    queueForDelete.append(j)
                elif (moves[i][5] == 1) and (moves[i][4] * 2 == moves[j][4]) and (
                        moves[i][2] == moves[j][0]) and (moves[i][3] == moves[j][1]):
                    moves[i] = (moves[i][0], moves[i][1], moves[j][2], moves[j][3], moves[i][4],
                                moves[i][5])
                    moves[j] = (moves[j][0], moves[j][1], moves[j][2], moves[j][3], moves[i][4],
                                moves[i][5])
        queueForDelete.sort(reverse=True)
        for z in queueForDelete:
            del moves[z]

    def CreateRandomTiles(n):
        baseValues = [2, 4]
        for i in range(n):
            emptyCell = {'row': randint(0, 3), 'col': randint(0, 3)}
            while (gameState[emptyCell['row']][emptyCell['col']] != 0) or (
                    (emptyCell['row'], emptyCell['col'], 4) in presentTiles) or (
                    (emptyCell['row'], emptyCell['col'], 2) in presentTiles):
                emptyCell = {'row': randint(0, 3), 'col': randint(0, 3)}
            randomValue = choice(baseValues)
            presentTiles.append((emptyCell['row'], emptyCell['col'], randomValue))

    CreateRandomTiles(2)

    while True:

        display.fill(color.background)
        drawTitle()
        drawBorder()


        ScoreFont = pygame.font.Font('freesansbold.ttf', 20)
        Score_String = "Score:  " + str(totalScore)
        ScoreObj = ScoreFont.render(Score_String, 1, color.foreground)
        ScoreRect = ScoreObj.get_rect()
        ScoreRect.topleft = (12, 152)
        display.blit(ScoreObj, ScoreRect)

        CC_String = "Select color:"
        CC_Obj = ScoreFont.render(CC_String, 1, color.foreground)
        CC_Rect = CC_Obj.get_rect()
        CC_Rect.topleft = (165, 152)
        display.blit(CC_Obj, CC_Rect)

        SET1Square = pygame.Rect(0, 0, 20, 20)
        SET1Square.topleft = (296, 152)
        pygame.draw.rect(display, colorBorder1, SET1Square)
        SET1_white_Square = pygame.Rect(0, 0, 14, 14)
        SET1_white_Square.center = SET1Square.center
        pygame.draw.rect(display, color.background, SET1_white_Square)
        SET1_inside_Square = pygame.Rect(0, 0, 10, 10)
        SET1_inside_Square.center = SET1Square.center
        pygame.draw.rect(display, color.colorPalet1[2], SET1_inside_Square)

        if SET1Square.collidepoint(pygame.mouse.get_pos()):
            colorBorder1 = color.hover
        else:
            colorBorder1 = color.foreground

        SET2Square = pygame.Rect(0, 0, 20, 20)
        SET2Square.topleft = (321, 152)
        pygame.draw.rect(display, colorBorder2, SET2Square)
        SET2_white_Square = pygame.Rect(0, 0, 14, 14)
        SET2_white_Square.center = SET2Square.center
        pygame.draw.rect(display, color.background, SET2_white_Square)
        SET2_inside_Square = pygame.Rect(0, 0, 10, 10)
        SET2_inside_Square.center = SET2Square.center
        pygame.draw.rect(display, color.colorPalet2[2], SET2_inside_Square)

        if SET2Square.collidepoint(pygame.mouse.get_pos()):
            colorBorder2 = color.hover
        else:
            colorBorder2 = color.foreground

        SET3Square = pygame.Rect(0, 0, 20, 20)
        SET3Square.topleft = (346, 152)
        pygame.draw.rect(display, colorBorder3, SET3Square)
        SET3_white_Square = pygame.Rect(0, 0, 14, 14)
        SET3_white_Square.center = SET3Square.center
        pygame.draw.rect(display, color.background, SET3_white_Square)
        SET3_inside_Square = pygame.Rect(0, 0, 10, 10)
        SET3_inside_Square.center = SET3Square.center
        pygame.draw.rect(display, color.colorPalet3[2], SET3_inside_Square)

        if SET3Square.collidepoint(pygame.mouse.get_pos()):
            colorBorder3 = color.hover
        else:
            colorBorder3 = color.foreground

        for row in range(4):
            for col in range(4):
                background_rect = pygame.Rect(15 + (3 + 84) * col, 181 + (3 + 84) * row, 84, 84)
                pygame.draw.rect(display, color.GREY1, background_rect)

        if (game_dynamics['status'] == 'static') and (game_dynamics['i'] == cst.moveFrame):

            drawGameState(gameState)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_click, y_click = event.pos
                    if SET1Square.collidepoint(x_click, y_click):
                        tiles = color.colorPalet1
                    elif SET2Square.collidepoint(x_click, y_click):
                        tiles = color.colorPalet2
                    elif SET3Square.collidepoint(x_click, y_click):
                        tiles = color.colorPalet3

                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a):

                        gameStateBefore = deepcopy(gameState)
                        Move("left")
                        totalScore += Sum("left")
                        Move("left")
                        MergeMovements()

                        if (gameState != gameStateBefore):
                            CreateRandomTiles(1)
                            game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'

                    elif (event.key == K_RIGHT or event.key == K_d):

                        gameStateBefore = deepcopy(gameState)
                        Move("right")
                        totalScore += Sum("right")
                        Move("right")
                        MergeMovements()

                        if (gameState != gameStateBefore):
                            CreateRandomTiles(1)
                            game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'

                    elif (event.key == K_UP or event.key == K_w):

                        gameStateBefore = deepcopy(gameState)
                        Move("up")
                        totalScore += Sum("up")
                        Move("up")
                        MergeMovements()

                        if (gameState != gameStateBefore):
                            CreateRandomTiles(1)
                            game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'

                    elif (event.key == K_DOWN or event.key == K_s):

                        gameStateBefore = deepcopy(gameState)
                        Move("down")
                        totalScore += Sum("down")
                        Move("down")
                        MergeMovements()

                        if (gameState != gameStateBefore):
                            CreateRandomTiles(1)
                            game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'

                    elif event.key == K_ESCAPE:
                        quit()


        elif (game_dynamics['status'] == 'dynamic') and (game_dynamics['i'] < cst.moveFrame):
            busy_spot_flag = [[0 for x in range(4)] for y in range(4)]
            for x in range(len(moves)):
                if (moves[x][5] == 0):
                    busy_spot_flag[moves[x][2]][moves[x][3]] = 1
                if (moves[x][5] == 1):
                    busy_spot_flag[moves[x][2]][moves[x][3]] = 2

            if (game_dynamics['i'] < 11):

                for x in range(len(moves)):
                    drawMovingTile(moves[x], game_dynamics['i'])

                for row in range(4):
                    for col in range(4):
                        if (gameState[row][col] != 0) and (busy_spot_flag[row][col] == 0):
                            drawTile(row, col, gameState[row][col])
                        elif (gameState[row][col] != 0) and (busy_spot_flag[row][col] == 2) and (
                                gameState[row][col] == gameStateBefore[row][col] * 2):
                            drawTile(row, col, gameStateBefore[row][col])

            if (game_dynamics['i'] >= 11):
                for row in range(4):
                    for col in range(4):
                        if (gameState[row][col] != 0) and (busy_spot_flag[row][col] != 2):
                            drawTile(row, col, gameState[row][col])
                        elif (gameState[row][col] != 0) and (busy_spot_flag[row][col] == 2):
                            sumTile(row, col, gameState[row][col], game_dynamics['i'] - 11)


                for i in range(len(presentTiles)):
                    spawnTile(presentTiles[i][0], presentTiles[i][1], presentTiles[i][2], game_dynamics['i'] - 11)

            game_dynamics['i'] += 1


        elif (game_dynamics['status'] == 'dynamic') and (game_dynamics['i'] == cst.moveFrame):

            for i in range(len(presentTiles)):
                gameState[presentTiles[i][0]][presentTiles[i][1]] = presentTiles[i][2]

            drawGameState(gameState)

            gameOverFlag = "Yes"
            for row in range(4):
                for col in range(4):
                    if (gameState[row][col] == 0):
                        gameOverFlag = "No"
                    elif (gameState[row][col] == 16384):
                        gameOverFlag = "MAX"
                        break
                        break

            if gameOverFlag == "Yes":

                gameStateBefore = deepcopy(gameState)
                Move("left")
                Sum("left")
                Move("right")
                Sum("right")
                Move("up")
                Sum("up")
                Move("down")
                Sum("down")

                if gameStateBefore == gameState:

                    string_to_display = "Game Over"
                    game_dynamics['status'] = 'over'

                else:
                    gameState = gameStateBefore

                    presentTiles = []
                    moves = []
                    game_dynamics['status'] = 'static'

            elif gameOverFlag == "MAX":

                string_to_display = "Max Value"
                game_dynamics['status'] = 'over'

            else:
                presentTiles = []
                moves = []
                game_dynamics['status'] = 'static'



        elif (game_dynamics['status'] == 'over') and (game_dynamics['i'] == cst.moveFrame):

            drawGameState(gameState)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()

                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:

                        gameState = [[0 for _ in range(4)] for _ in range(4)]
                        gameStateBefore = [[0 for _ in range(4)] for _ in range(4)]
                        moves = []
                        presentTiles = []
                        game_dynamics = {'status': 'dynamic', 'i': 11}
                        totalScore = 0
                        CreateRandomTiles(2)

                    elif event.key == K_ESCAPE:
                        quit()

            GameOverFont = pygame.font.Font('freesansbold.ttf', 50)
            GameOverObj = GameOverFont.render(string_to_display, 1, color.foreground)
            GameOverRect = GameOverObj.get_rect()
            GameOverRect.center = (cst.widthOfWindow / 2, 560)
            display.blit(GameOverObj, GameOverRect)

            GameOverFont = pygame.font.Font('freesansbold.ttf', 14)
            GameOverObj = GameOverFont.render("Press enter to start new game", 1, color.foreground)
            GameOverRect = GameOverObj.get_rect()
            GameOverRect.center = (cst.widthOfWindow / 2, 600)
            display.blit(GameOverObj, GameOverRect)

        pygame.display.update()
        fps.tick(cst.FPS)


def quit():
    pygame.quit()
    exit()


if __name__ == '__main__':
    global display
    global fps

    pygame.init()
    fps = pygame.time.Clock()
    display = pygame.display.set_mode((cst.widthOfWindow, cst.heightOfWindow))
    pygame.display.set_caption("Digit Dash")

    startScreen()
