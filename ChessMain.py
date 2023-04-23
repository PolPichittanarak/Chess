### handling user input and display current gamestate object

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = []

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    IMAGE_wp = p.transform.scale(p.image.load("images/wp.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_wR = p.transform.scale(p.image.load("images/wR.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_wN = p.transform.scale(p.image.load("images/wN.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_wB = p.transform.scale(p.image.load("images/wB.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_wQ = p.transform.scale(p.image.load("images/wQ.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_wK = p.transform.scale(p.image.load("images/wK.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_bp = p.transform.scale(p.image.load("images/bp.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_bR = p.transform.scale(p.image.load("images/bR.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_bN = p.transform.scale(p.image.load("images/bN.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_bQ = p.transform.scale(p.image.load("images/bQ.bmp"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE_bK = p.transform.scale(p.image.load("images/bK.bmp"), (SQUARE_SIZE, SQUARE_SIZE))

    #pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bQ', 'bK']
    #for piece in pieces:
        #IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".bmp"), (SQUARE_SIZE, SQUARE_SIZE))
        # piece can be called as IMAGES["wp"]


'''
Handle user input and update the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

#all graphics in a current game state
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board)

#squares drawing
def drawBoard(screen):
    colors = [p.Color("White"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            #top left is always light
            #row + column = even then color will be light
            color = colors[((r+c) % 2)] # if odd then ill return 1 so itll turn the square dark
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


#pieces drawing
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                piece_pic = "IMAGE_" + str(piece)
                screen.blit(piece_pic, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



if __name__ == "__main__":
    main()