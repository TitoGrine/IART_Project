from zhed.controller import zhed_board
from zhed.model.view_state import Hint
from zhed.view.game_pieces import *


def build_tile(settings, sprites, tile, foreground_color, background_color, symbol):
    """" Builds a tile object with the correct screen coordenates for display.
    :param settings: class information about the pygame screen and font
    :param sprites: list with all current game sprites
    :param tile: tile coordinates in the puzzle "array"
    :param foreground_color: rgb tuple for the foreground color
    :param background_color: rgb tuple for the background color
    :param symbol: character meant to represent the tile
    """

    x_pos = tile[1] * size + 10
    y_pos = tile[0] * size + 10
    sprites.add(Tile(settings.font, symbol, foreground_color, settings.window,
                     background_color, x_pos, y_pos))


def draw_board(settings, board, side, last=False, expandables=[], hints=Hint(Hint.NO_HINT, [])):
    """" Draws all board tiles and returns the sprites that are interactable in the game.
    :param settings: class information about the pygame screen and font
    :param board: list of lists cointaining each tile info (int)
    :param side: length of the board's side in number of tiles
    :param last: boolean stating if it's the last solution state (used only in bot_playing)
    :param expandables: list of tiles that can be filled if the user expands the block previously selected (used only in player_playing)
    :param hints: Hint object for signalying the best current play
    """

    sprites = pygame.sprite.Group()
    interactable_sprites = []

    for i in range(side):
        y_pos = i * size + 10
        for j in range(side):
            x_pos = j * size + 10
            tile = board[i][j]

            if tile == zhed_board.BoardState.GOAL:
                if last:
                    sprites.add(Tile(settings.font, '◈', GameColors.COMPLETED_TEXT,
                                     settings.window, GameColors.COMPLETED, x_pos, y_pos))
                else:
                    sprites.add(Tile(settings.font, '◈', GameColors.GOAL_TEXT,
                                     settings.window, GameColors.GOAL, x_pos, y_pos))
            elif tile == zhed_board.BoardState.EMPTY:
                empty_color = GameColors.empty_color()
                sprites.add(Tile(settings.font, ' ', empty_color, settings.window,
                                 empty_color, x_pos, y_pos))
            elif tile == zhed_board.BoardState.FILLED:
                sprites.add(Tile(settings.font, '∙', GameColors.TILE_TEXT,
                                 settings.window, GameColors.TILE, x_pos, y_pos))
            else:
                tile = Tile(settings.font, str(tile), GameColors.TILE_TEXT,
                            settings.window, GameColors.TILE, x_pos, y_pos, x=j, y=i)
                sprites.add(tile)
                interactable_sprites.append(tile)

    for expandable in expandables:
        for tile in expandable:
            build_tile(settings, sprites, tile, GameColors.COMPLETED, GameColors.empty_color(), '∙')

    if hints.hint is Hint.HINT:
        for hint in hints.path:
            build_tile(settings, sprites, hint, GameColors.HINT, GameColors.empty_color(), '∙')
            build_tile(settings, sprites, hints.block, GameColors.HINT_TEXT,
                       GameColors.HINT, str(board[hints.block[0]][hints.block[1]]))

    sprites.draw(settings.window)

    return interactable_sprites
