import sys, os, copy, random, pygame
from pygame.locals import *
import numpy as np
from numpy import array


class Rectangle():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Tile():
    def __init__(self, tile_type, tile_position, row, column, floor):
        self.tile_type = tile_type
        self.tile_position = tile_position
        self.row = row
        self.column = column
        self.floor = floor
        self.image = pygame.image.load(os.path.join("./images/{}.png".format(tile_type)))
        self.in_hand = False
        self.on_top = False

        if tile_position == "0" or tile_position == "1":
            self.x = (row * TILE_SIZE) + BOARD_OFFSET
            self.y = (column * TILE_SIZE) + BOARD_OFFSET
        elif tile_position == "2v":
            self.x = (row * TILE_SIZE) + BOARD_OFFSET + TILE_SIZE/2
            self.y = (column * TILE_SIZE) + BOARD_OFFSET
        elif tile_position == "2h":
            self.x = (row * TILE_SIZE) + BOARD_OFFSET
            self.y = (column * TILE_SIZE) + BOARD_OFFSET + TILE_SIZE/2
        elif tile_position == "4":
            self.x = (row * TILE_SIZE) + BOARD_OFFSET + TILE_SIZE/2
            self.y = (column * TILE_SIZE) + BOARD_OFFSET + TILE_SIZE/2

    def draw_tile(tile):
        screen.blit(tile.image, (tile.x, tile.y))

    #removes tile from board_tiles array and adds it to player.hand
    def add_to_hand(tile):
        if tile.in_hand == False:
            player.hand.append(tile)
            tile.in_hand = True
            board_state.board_tiles.remove(tile)
            count = 0

            sounds[random.randint(0, len(sounds) - 1)].play()
        
            for i in player.hand:
                if i.tile_type == tile.tile_type:
                    count += 1
            if count > 2:
                pygame.mixer.Sound(triple_sound).play()
                
                for triple in reversed(player.hand):
                    if tile.tile_type == triple.tile_type:
                        player.hand.remove(triple)

        if(len(player.hand) >= 7):
            print("You lose.")
            pygame.quit()
            sys.exit()

    #adds all the tiles to a 2D array depending on which floor they are on
    def assign_top_tiles():
        tiles_by_floor = []
        for tile in board_state.board_tiles:
            if len(tiles_by_floor) < (tile.floor + 1):
                i = tile.floor - len(tiles_by_floor) + 1
                for count in range(i):
                    tiles_by_floor.append([])
            tiles_by_floor[tile.floor].append(tile)

        rect_tiles = []
        for flr in range(len(tiles_by_floor)):
            rect_tiles.append([])
            for tile in range(len(tiles_by_floor[flr])):
                rect_tiles[flr].append([])
                rect_tiles[flr][tile] = pygame.Rect(Rectangle(tiles_by_floor[flr][tile].x, tiles_by_floor[flr][tile].y))
        
        #assign tiles on top
        for flr in range(len(rect_tiles)):
            if flr + 1 < len(rect_tiles):
                for tile in range(len(rect_tiles[flr])):
                    collisions = rect_tiles[flr][tile].collidelistall(rect_tiles[flr + 1])
                    if not collisions:
                        tiles_by_floor[flr][tile].on_top = True
                    else:
                        tiles_by_floor[flr][tile].on_top = False
            elif flr + 1 == len(rect_tiles):
                for tile in range(len(rect_tiles[flr])):
                    tiles_by_floor[flr][tile].on_top = True
        

class Board():
    def __init__(self):
        self.board_tiles = []

    def addTile(self, tile):
        if len(self.board_tiles) < tile.floor:
            i = tile.floor - self.board_tiles
            for count in range(i):
                self.board_tiles.append([])

    #randomises and shuffles tiles
    def randomise_tiles(level):
        count = 0
        for i in range(len(level)):
            for j in range(len(level[i])):
                for k in range(len(level[i][j])):
                    if level[i][j][k] != "":
                        count += 1
        total_triples = int(count/3)
        
        count = 0
        for i in range(total_triples):
            temp_type = tile_types[count]
            for j in range(3):
                tile_list.append(temp_type)
            count += 1
            if count >= len(tile_types):
                count = 0
                    
        random.shuffle(tile_list)

        count = 0
        for flr in range(len(level)):
            for row in range(len(level[flr])):
                for col in range(len(level[flr][row])):
                    if level[flr][row][col] != "":
                        board_state.board_tiles.append(Tile(tile_list[count], level[flr][row][col], col, row, flr))
                        count += 1
                    

    def build_board():
        for i in board_state.board_tiles:
            Tile.draw_tile(i)
        
                
class PlayerHand():
    def __init__(self):
        self.hand = []

    def build_hand():
        for i in range(len(player.hand)):
            screen.blit(player.hand[i].image, (i * TILE_SIZE + BOARD_OFFSET, int(BOARD_OFFSET/4)))

    

level1 =np.array([[
                ["0", "", "0", "", "0"],
                ["", "0", "0", "0", ""],
                ["0", "0", "0", "0", "0"],
                ["", "0", "0", "0", ""],
                ["0", "", "0", "", "0"],],
         
                [["4", "4", "4", "4", ""],
                 ["4", "", "", "4", ""],
                 ["4", "", "", "4", ""],
                 ["4", "4", "4", "4", ""],
                 ["", "", "", "", ""],],
         
                 [["", "", "", "", ""],
                  ["", "1", "1", "1", ""],
                  ["", "1", "", "1", ""],
                  ["", "1", "1", "1", ""],
                  ["", "", "", "", ""]],
         
                 [["", "", "", "", ""],
                  ["", "4", "4", "", ""],
                  ["", "4", "4", "", ""],
                  ["", "", "", "", ""],
                  ["", "", "", "", ""]],
         
                 [["", "", "", "", ""],
                  ["", "", "", "", ""],
                  ["", "", "1", "", ""],
                  ["", "", "", "", ""],
                  ["", "", "", "", ""]]], dtype=object)

level2 =np.array([[
                ["0", "0", "0", "0", "0"],
                ["0", "0", "", "0", "0"],
                ["0", "", "", "", "0"],
                ["0", "0", "", "0", "0"],
                ["0", "0", "0", "0", "0"],],
         
                [["4", "4", "4", "4", ""],
                 ["4", "", "", "4", ""],
                 ["4", "", "", "4", ""],
                 ["4", "4", "4", "4", ""],
                 ["", "", "", "", ""],],
         
                 [["", "1", "1", "1", ""],
                  ["1", "1", "", "1", "1"],
                  ["1", "", "", "", "1"],
                  ["1", "1", "", "1", "1"],
                  ["", "1", "1", "1", ""]]], dtype=object)

level3 =np.array([[
                ["1", "1", "", "1", "1"],
                ["1", "1", "", "1", "1"],
                ["1", "", "", "", "1"],
                ["1", "", "", "", "1"],
                ["1", "1", "", "1", "1"],],
         
                [["4", "4", "4", "4", ""],
                 ["4", "", "", "4", ""],
                 ["4", "", "", "4", ""],
                 ["4", "4", "4", "4", ""],
                 ["1", "", "", "", ""],],
         
                 [["", "1", "1", "1", ""],
                  ["1", "1", "", "1", "1"],
                  ["1", "", "", "", "1"],
                  ["1", "1", "", "1", "1"],
                  ["", "1", "1", "1", ""]]], dtype=object)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 480
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CURRENT_LEVEL = level3

    bg = pygame.image.load(os.path.join("./", "images/background.png"))
    sounds = []
    sounds.append(pygame.mixer.Sound("sounds/click_sound1.wav"))
    sounds.append(pygame.mixer.Sound("sounds/click_sound2.wav"))
    triple_sound = pygame.mixer.Sound("sounds/triple_sound1.wav")
    pygame.mouse.set_visible(1)
    pygame.display.set_caption("Mahjong")

    BOARD_OFFSET = 128
    tile_types = [
        'kiwi',
        'apple',
        'strawberry',
        'cherry',
        'pear',
        'orange',
        'banana',
        ]
    TILE_SIZE = 64
    tile_list = []

    board_state = Board()
    player = PlayerHand()
    Board.randomise_tiles(CURRENT_LEVEL)
    Tile.assign_top_tiles()
    
    while True:
        clock.tick(60)
        screen.blit(bg, (0, 0))
        Board.build_board()
        PlayerHand.build_hand()
        

        if len(board_state.board_tiles) == 0:
            print("You WIN!")
            pygame.quit()
            sys.exit()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                for tile in board_state.board_tiles:
                    rectangle = pygame.Rect(Rectangle(tile.x, tile.y))
                    if rectangle.collidepoint(mouse_x, mouse_y) and tile.on_top and not tile.in_hand:
                        Tile.add_to_hand(tile)
                        Tile.assign_top_tiles()
                        break
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
