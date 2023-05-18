import pygame
import random
import copy
import numpy as np


#  utility functions
def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """Check to determine which directions are valid from current cell"""
    validdirections = []
    if x != minX: validdirections.append((x-1, y))
    if x != minX and y != minY: validdirections.append((x-1, y-1))
    if x != minX and y != maxY: validdirections.append((x-1, y+1))

    if x!= maxX: validdirections.append((x+1, y))
    if x != maxX and y != minY: validdirections.append((x+1, y-1))
    if x != maxX and y != maxY: validdirections.append((x+1, y+1))

    if y != minY: validdirections.append((x, y-1))
    if y != maxY: validdirections.append((x, y+1))

    return validdirections

def loadImages(path, size):
    """Load an image into the game, and scale the image"""
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    """creates an empty surface, loads a portion of the spritesheet onto the surface, then return that surface as img"""
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image

def evaluateBoard(grid, player):
    score = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            score -= col
    return score

class Grid:

    def __init__(self, rows, columns, cell_size, othello):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.othello = othello
        self.board = np.zeros((rows, columns))

    def draw(self, screen):
        for row in range(self.rows):
            for column in range(self.columns):
                pygame.draw.rect(screen, self.board[row][column], (row * self.cell_size, column * self.cell_size, self.cell_size, self.cell_size))

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
        image = pygame.Surface((960, 960))
        for j, row in enumerate(gridBg):
            for i, img in enumerate(row):
                image.blit(self.bg[img], (i * self.size[0], j * self.size[1]))
        return image

    def regenGrid(self, rows, columns):
        """generate an empty grid for logic use"""
        grid = []
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
        textImg = self.font.render(f'{player} : {score}', 1, 'White')
        return textImg

    def endScreen(self):
        if self.GAME.gameOver:
            endScreenImg = pygame.Surface((320, 320))
            endText = self.font.render(f'{"Congratulations, You Won!!" if self.player1Score > self.player2Score else "Bad Luck, You Lost"}', 1, 'White')
            endScreenImg.blit(endText, (0, 0))
            newGame = pygame.draw.rect(endScreenImg, 'White', (80, 160, 160, 80))
            newGameText = self.font.render('Play Again', 1, 'Black')
            endScreenImg.blit(newGameText, (120, 190))
        return endScreenImg

    def drawGrid(self, window):
        window.blit(self.gridBg, (0, 0))

        window.blit(self.drawScore('White', self.player1Score), (900, 100))
        window.blit(self.drawScore('Black', self.player2Score), (900, 200))

        for token in self.tokens.values():
            token.draw(window)

        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
        if self.GAME.currentPlayer == 1:
            for move in availMoves:
                pygame.draw.rect(window, 'White', (80 + (move[1] * 80) + 30, 80 + (move[0] * 80) + 30, 20, 20))

        if self.GAME.gameOver:
            window.blit(self.endScreen(), (240, 240))

    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()

    def findValidCells(self, grid, curPlayer):
        """Performs a check to find all empty cells that are adjacent to opposing player"""
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                DIRECTIONS = directions(gridX, gridY)

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue

                    if (gridX, gridY) in validCellToClick:
                        continue

                    validCellToClick.append((gridX, gridY))
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
        """Takes the list of validCells and checks each to see if playable"""
        validCells = self.findValidCells(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x, y, grid, currentPlayer)

            #if len(swapTiles) > 0 and cell not in playableCells:
            if len(swapTiles) > 0:
                playableCells.append(cell)

        return playableCells

    def insertToken(self, grid, curplayer, y, x):
        tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player

    def animateTransitions(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].transition(self.transitionWhiteToBlack, self.whitetoken)
        else:
            self.tokens[(cell[0], cell[1])].transition(self.transitionBlackToWhite, self.blacktoken)

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption('Othello')

        self.player1 = 1
        self.player2 = -1

        self.currentPlayer = 1

        self.time = 0

        self.rows = 8
        self.columns = 8

        self.gameOver = True

        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.computerPlayer = ComputerPlayer(self.grid)

        self.RUN = True

        # Create a new Board object.
        self.board = np.array(self.grid.board)

        # Set the current player to "black".
        self.current_player = "black"

        # Set the other player to "white".
        self.other_player = "white"

        # Set the game over flag to False.
        self.game_over = False

    def update(self):
        """
        Update the state of the game.
        """

        # Get the current state of the board.
        board = self.grid.board

        # Get the list of available moves for the current player.
        moves = self.computerPlayer.get_available_moves(board)

        # If there are no available moves, the game is over.
        if not moves:
            self.game_over = True
            return

        # Choose the best move.
        move = self.computerPlayer.computerHard(board, self.color)

        # Make the move.
        self.grid.make_move(move)

        # Switch players.
        self.current_player = self.other_player

    def draw(self):
        self.grid.draw(self.screen)

    def run(self):
        while self.RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUN = False

            self.update()
            self.draw()
            pygame.display.update()

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
            self.image = transitionImages[i // 10]
            self.GAME.draw()
        self.image = tokenImage

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))

class Player:

    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        raise NotImplementedError

class board:

    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.cells = [[None for _ in range(width)] for _ in range(height)]

    def is_valid_move(self, position):
        return 0 <= position[0] < self.height and 0 <= position[1] < self.width

    def get_cell_color(self, position):
        return self.cells[position[0]][position[1]]

    def make_move(self, position, color):

        if not self.is_valid_move(position):
            return False

        self.cells[position[0]][position[1]] = color

        return True

    def is_game_over(self):

        for row in range(self.height):
            for col in range(self.width):
                if self.cells[row][col] is None:
                    return False

        return True

class ComputerPlayer(Player):

    def __init__(self, color):
        super().__init__(color)

        self.alpha = -float("inf")
        self.beta = float("inf")

    def get_move(self, board):

        # Establish stable disk positions around the edges and corners.
        moves = []
        for row in range(board.height):
            for col in range(board.width):
                if board.is_valid_move((row, col)) and self.is_stable_position((row, col)):
                    moves.append((row, col))

        # If there are no stable positions available, look for any available moves.
        if not moves:
            moves = board.get_available_moves(self.color)

        # Wait to place disks in spaces where your opponent can’t play.
        if moves:
            best_move = moves[0]
            for move in moves:
                if not board.is_valid_move(move, self.opponent_color):
                    best_move = move

        # Limit the number of disks you flip over early in the game.
        if best_move is not None and board.get_num_disks_flipped(best_move) > 2:
            moves = board.get_available_moves(self.color, max_flips=2)
            if moves:
                best_move = moves[0]

        # Place pieces strategically around the board to avoid getting boxed in.
        if best_move is not None and not self.is_strategic_position(best_move):
            moves = board.get_available_moves(self.color, strategic_positions=True)
            if moves:
                best_move = moves[0]

        # Alpha-Beta search
        best_move = self.alphabeta(board, self.color, -float("inf"), float("inf"))

        return best_move

    def alphabeta(self, board, color, alpha, beta):

        if board.is_game_over():
            return None

        if color == board.get_turn():
            best_move = None
            best_value = -float("inf")
            for move in board.get_available_moves(color):
                new_board = board.copy()
                new_board.make_move(move, color)
                new_value = self.alphabeta(new_board, board.get_opponent_color(), alpha, beta)
                if new_value > best_value:
                    best_value = new_value
                    best_move = move
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            return best_move
        else:
            best_move = None
            best_value = float("inf")
            for move in board.get_available_moves(color):
                new_board = board.copy()
                new_board.make_move(move, color)
                new_value = self.alphabeta(new_board, board.get_turn(), alpha, beta)
                if new_value < best_value:
                    best_value = new_value
                    best_move = move
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
            return best_move
        
    def is_stable_position(self, position):

        if position[0] == 0 or position[0] == board.height - 1 or position[1] == 0 or position[1] == board.width - 1:
            return True

        for neighbor in [(position[0] - 1, position[1]), (position[0] + 1, position[1]), (position[0], position[1] - 1), (position[0], position[1] + 1)]:
            if board.is_valid_move(neighbor) and board.get_cell_color(neighbor) == self.color:
                return True

        return False
    
    def computerHard(self, board, color):
        """
        Find the best move for the computer player.
        """

        # Initialize the best move and score.
        best_move = None
        best_score = -float("inf")

        # Iterate over all possible moves.
        for move in self.get_available_moves(board):

            # Make the move.
            self.grid.make_move(move)

            # Get the score of the move.
            score = self.evaluate(board)

            # Undo the move.
            self.grid.undo_move(move)

            # If the score is better than the best score, update the best move.
            if score > best_score:
                best_move = move
                best_score = score

        # Return the best move.
        return best_move

    def get_available_moves(self, board):
        """
        Get the list of available moves for the current player.
        """

        # Get the current state of the board.
        board = self.grid.board

        # Get the list of available moves for the current player.
        moves = []

        # Loop over all rows in the board.
        for row in range(board.shape[0]):

            # Loop over all columns in the board.
            for column in range(board.shape[1]):

                # If the current cell is empty,
                if board[row][column] == 0:

                    # Check if there are any available moves in the current cell.
                    if self.is_available_move(row, column, board):
                        moves.append((row, column))

        return moves

if __name__ == '__main__':
    game = Othello()
    game.run()
    pygame.quit()