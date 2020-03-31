from zhed.controller import zhed_board
from zhed.model.view_state import Hint
from zhed.view.game_pieces import *


def build_tile(settings, sprites, tile, foreground_color, background_color, symbol):
    x_pos = tile[1] * size + 10
    y_pos = tile[0] * size + 10
    sprites.add(Tile(settings.font, symbol, foreground_color, settings.window,
                     background_color, x_pos, y_pos))


def draw_board(settings, board, side, index, last, expandables=[], hints=Hint(Hint.NO_HINT, [])):
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
