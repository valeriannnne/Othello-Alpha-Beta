import pygame
import random
import copy

FPS = 60

# utility functions
def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    # check to determine which directions are valid from the current cell
    validdirections = []
    if x != minX:  # checks if moving to left is valid
        validdirections.append((x-1, y))
    if x != minX and y != minY:   # checks moving diagonally to top left is valid
        validdirections.append((x-1, y-1))
    if x != minX and y != maxY:   # checks if moving diagonally to the bottom left is valid
        validdirections.append((x-1, y+1))

    if x != maxX:   # moving to right
        validdirections.append((x+1, y))
    if x != maxX and y != minY:     # moving to top right
        validdirections.append((x+1, y-1))
    if x != maxX and y != maxY:     # moving to bottom right
        validdirections.append((x+1, y+1))

    if y != minY:   # moving upward
        validdirections.append((x, y-1))
    if y != maxY:   # moving downwards
        validdirections.append((x, y+1))

    return validdirections      # returns the list with valid direction

def loadImages(path, size):
    # Load the image
    img = pygame.image.load(f"{path}").convert_alpha()
    # resize the image to a specified size
    img = pygame.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    # param from loadBackGroundImage
    # imageDict[alpha[j]+str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
    # creates an empty surface, loads a portion of the spritesheet onto the surface,
    # then return that surface as img
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image

def evaluateBoard(grid):
    score =0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            score -= col
    return score

class Othellism:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption('Othellism')

        self.player1 = 1 #White
        self.player2 = -1 #Black

        self.currentPlayer = 1
        self.time = 0
        self.rows = 8
        self.columns = 8

        self.gameOver = False

        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.RUN = True

    # main method
    def run(self):
        clock = pygame.time.Clock()  # control the speed habang nagrurun
        while self.RUN == True:
            clock.tick(FPS)
            self.input()
            self.update()
            self.draw()

    def input(self):
        # all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button == 1:
                    if not self.gameOver:   # para makamove, unless game over na
                        x, y = pygame.mouse.get_pos()
                        x, y = (x-80)//80, (y-80)//80
                        # To make sure na hindi macclick yung hindi valid cell
                        validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
                        if not validCells:
                            pass
                        else:
                            if (y, x) in validCells:
                                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                                #for swapping tiles
                                swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
                                for tile in swappableTiles:
                                    self.grid.animateTransitions(tile, self.currentPlayer)
                                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                                self.currentPlayer *= -1
                                self.time = pygame.time.get_ticks()

                    if self.gameOver:
                        x, y = pygame.mouse.get_pos()
                        #if user clicks the play again
                        if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            self.grid.newGame()
                            self.gameOver = False



    def update(self):

        self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
        self.grid.player2Score = self.grid.calculatePlayerScore(self.player2)
        if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
            self.gameOver = True
            return


    def draw(self):
        self.screen.fill((255, 195, 77))
        self.grid.drawGrid(self.screen)
        pygame.display.update()

class Grid:
    def __init__(self, rows, columns, size, main):
        # self.grid = Grid(self.rows, self.columns, (80, 80), self) passed from Othello class
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size
        self.whitetoken = loadImages('assets/WhiteToken.png', size)
        self.blacktoken = loadImages('assets/BlackToken.png', size)
        # load 3 images for each from the assets
        self.transitionWhiteToBlack = [loadImages(f'assets/BlackToWhite{i}.png', self.size) for i in range(1, 4)]
        self.transitionBlacktoWhite = [loadImages(f'assets/WhiteToBlack{i}.png', self.size) for i in range(1, 4)]
        self.bg = self.loadBackGroundImages()
        self.tokens ={}

        self.gridBg = self.createbgimg()

        self.gridLogic = self.regenGrid(self.y, self.x)

        self.player1Score = 0
        self.player2Score = 0

        self.font = pygame.font.SysFont('Arial', 20, True, False)

    def newGame(self):
        self.tokens.clear()
        self.gridLogic = self.regenGrid(self.y, self.x)

    def loadBackGroundImages(self):
        alpha = 'ABCDEFGHI'
        spriteSheet = pygame.image.load('assets/wood.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j]+str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
        return imageDict

    def createbgimg(self):
        gridBg = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        image = pygame.Surface((800, 800))
        for j, row in enumerate(gridBg):
            for i, img in enumerate(row):
                image.blit(self.bg[img], (i * self.size[0], j * self.size[1]))
        return image

    def regenGrid(self, rows, columns):
        # generate empty grid for logic use
        grid =[]
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(0)
            grid.append(line)
        self.insertToken(grid, 1, 3, 3)
        self.insertToken(grid, -1, 3, 4)
        self.insertToken(grid, 1, 4, 4)
        self.insertToken(grid, -1, 4, 3)

        return grid

    def calculatePlayerScore(self, player):
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    def drawScore(self, player, score):
        textImg = self.font.render(f'{player} : {score}', 1, 'Black')
        return textImg

    def endScreen(self):
        if self.GAME.gameOver:
            endScreenImg = pygame.Surface((320, 320))
            endScreenImg.fill((211, 141, 36, 1))

            endText = self.font.render(
                f'{"Player 1 (White) wins!" if self.player1Score > self.player2Score else "Player 2 (Black) wins!"}', 1,
                'White')

            endScreenImg.blit(endText, (77, 110))
            newGame = pygame.draw.rect(endScreenImg, 'White', (80, 160, 160, 80))
            newGameText = self.font.render('Play Again', 1, 'Black')
            endScreenImg.blit(newGameText, (120, 190))
        return endScreenImg

    def drawGrid(self, window):

        window.blit(self.gridBg, (0, 0))
        # for player turn
        playerTurn = self.font.render(
            f'{"Player 1s Turn" if self.GAME.currentPlayer == 1 else "Player 2s Turn"}', 1,
            'White')

        window.blit(playerTurn, (850, 100))
        window.blit(self.drawScore('Player 1 (White)', self.player1Score), (850, 200))
        window.blit(self.drawScore('Player 2 (Black)', self.player2Score), (850, 300))

        for token in self.tokens.values():
            token.draw(window)

        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
        for move in availMoves:
            if self.GAME.currentPlayer == 1:
                # print("Player 1")
                for move in availMoves:
                    # for the white tiles na nagsasabi kung ano yung pwedeng paglagyan ng player
                    pygame.draw.circle(window, 'Black', (80 + (move[1] * 80) + 40, 80 + (move[0] * 80) + 40), 30)
                    pygame.draw.circle(window, 'White', (80 + (move[1] * 80) + 40, 80 + (move[0] * 80) + 40), 25)
            else:
                # print("Player 2")
                for move in availMoves:
                    pygame.draw.circle(window, 'White', (80 + (move[1] * 80) + 40, 80 + (move[0] * 80) + 40), 30)
                    pygame.draw.circle(window, 'Black', (80 + (move[1] * 80) + 40, 80 + (move[0] * 80) + 40), 25)

        if self.GAME.gameOver:
            window.blit(self.endScreen(), (240, 240))

    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")   # left justify the string
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()

    def findValidCells(self, grid, curPlayer):
        # check to find all empty cells that are adjacent to opposing player
        validCellToClick = []   # store valid cells
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:     # check if current grid is not empty
                    continue           # if not empty, there's already a player token, so continue to next iteration
                DIRECTIONS = directions(gridX, gridY)   # returns valid direction from the current cell

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:   # check if empty or belongs to the current player
                        continue

                    if (gridX, gridY) in validCellToClick:  # check current cell is already present in validCellsToClick
                        continue

                    validCellToClick.append((gridX, gridY))     # add the current cell to the validCellToClick
        return validCellToClick

    def swappableTiles(self, x, y, grid, player):
        surroundCells = directions(x, y)
        if len(surroundCells) == 0:
            return []

        swappableTiles = []
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []

            RUN = True
            while RUN:
                if grid[checkX][checkY] == player * -1:
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    RUN = False
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                checkX += difX
                checkY += difY

                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)

        return swappableTiles


    def findAvailMoves(self, grid, currentPlayer):
        # takes the list of validcells and check each to see if playable
         validCells = self.findValidCells(grid, currentPlayer)
         playableCells = []

         for cell in validCells:
             x, y = cell
             if cell in playableCells:
                 continue
             swapTiles = self.swappableTiles(x, y, grid, currentPlayer)

            # if len(swapTiles) > 0 and cell not in playableCells:
             if len(swapTiles) > 0:
                 playableCells.append(cell)

         return playableCells


    def insertToken(self, grid, curplayer, y, x):
        tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        # x is row, y is column
        grid[y][x] = self.tokens[(y, x)].player

    def animateTransitions(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].transition(self.transitionWhiteToBlack, self.whitetoken)
        else:
            self.tokens[(cell[0], cell[1])].transition(self.transitionBlacktoWhite, self.blacktoken)

class Token:
    def __init__(self, player, gridX, gridY, image, main):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.posX = 80 + (gridY * 80)
        self.posY = 80 + (gridX * 80)
        self.GAME = main

        self.image = image

    def transition(self, transitionImages, tokenImage):
        for i in range(30):
            self.image = transitionImages[i//10]
            self.GAME.draw()
        self.image = tokenImage

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))

if __name__ == '__main__':
    game = Othellism()
    game.run()
    pygame.quit()
