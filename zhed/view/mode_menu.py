from zhed.model.view_state import BoardSettings
from zhed.view.bot_game import bot_playing
from zhed.view.game_pieces import *
import zhed.view.menus
from zhed.view.player_game import player_playing


def mode_menu():
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 30, 1, 0)
    window = pygame.display.set_mode((size * 8 + 20, size * 8 + 20))

    window.fill(GameColors.BACKGROUND)

    title = Title("CHOOSE MODE", GameColors.TILE, 60)
    settings = BoardSettings(window, font)
    buttons = []
    run = True
    counter = 0

    while run:
        pygame.time.delay(50)

        if counter == 0:
            zhed.view.menus.draw_menu(settings)

        title.draw(window, 0, 0, size * 8 + 20, size * 3.5 + 10)

        buttons.append(Button(settings.font, "∙  PLAYER MODE  ∙", GameColors.GOAL_TEXT,
                              settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10,
                              round(size * 3.5) + 10, zhed.view.menus.level_menu, arguments=[player_playing]))

        buttons.append(Button(settings.font, "∙  BOT SOLUTION  ∙", GameColors.GOAL_TEXT,
                              settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10,
                              round(size * 5.5) + 10, zhed.view.menus.level_menu, arguments=[bot_playing]))

        zhed.view.menus.draw_buttons(settings, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                zhed.view.menus.check_button_clicks(buttons, pygame.mouse.get_pos())

        counter = (counter + 1) % 5
        pygame.display.update()

    pygame.quit()
