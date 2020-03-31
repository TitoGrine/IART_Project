from zhed.model.view_state import *
from zhed.view.game_pieces import *
from zhed.view.mode_menu import mode_menu


def draw_buttons(settings, button_objs):
    buttons = pygame.sprite.Group()

    for button in button_objs:
        buttons.add(button)
        button.draw(settings.window, GameColors.GOAL_TEXT)

    buttons.draw(settings.window)


def level_menu(game_mode):
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 37, 1, 0)
    window = pygame.display.set_mode((size * 8 + 20, size * 8 + 20))

    window.fill(GameColors.BACKGROUND)

    value = ""

    title = Title("CHOOSE LEVEL", GameColors.TILE, 60)
    settings = BoardSettings(window, font)
    buttons = []
    run = True
    counter = 0

    while run:
        pygame.time.delay(50)

        if counter == 0:
            draw_menu(settings)

        title.draw(window, 0, 0, size * 8 + 20, size * 3.5 + 10)

        TextField(font, "Level:  " + value, GameColors.TILE_TEXT,
                  settings.window, GameColors.TILE, size * 6, round(size * 1.5), size + 10, round(size * 3.5) + 10)

        buttons.clear()
        buttons.append(Button(settings.font, "∙  START  ∙", GameColors.GOAL_TEXT,
                              settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10,
                              round(size * 5.5) + 10, game_mode, arguments=[1 if len(value) == 0 else int(value)]))

        draw_buttons(settings, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP and len(value) != 0:
                check_button_clicks(buttons, pygame.mouse.get_pos(),
                                    condition=bool(int(value) > 0 and int(value) <= 101))
            elif event.type == pygame.KEYDOWN:
                if len(value) < 3:
                    if event.key == pygame.K_0:
                        value += "0"
                    if event.key == pygame.K_1:
                        value += "1"
                    if event.key == pygame.K_2:
                        value += "2"
                    if event.key == pygame.K_3:
                        value += "3"
                    if event.key == pygame.K_4:
                        value += "4"
                    if event.key == pygame.K_5:
                        value += "5"
                    if event.key == pygame.K_6:
                        value += "6"
                    if event.key == pygame.K_7:
                        value += "7"
                    if event.key == pygame.K_8:
                        value += "8"
                    if event.key == pygame.K_9:
                        value += "9"

                if len(value) > 0:
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        value = value[:-1]

        counter = (counter + 1) % 5
        try:
            pygame.display.update()
        except:
            exit(0)

    pygame.quit()


def check_button_clicks(buttons, pos, condition=True):
    clicked_buttons = [s for s in buttons if s.tile.collidepoint(pos)]

    if len(clicked_buttons) != 0 and condition:
        clicked_buttons[0].trigger()


def main_menu():
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 30, 1, 0)
    window = pygame.display.set_mode((size * 8 + 20, size * 8 + 20))

    window.fill(GameColors.BACKGROUND)

    title = Title("ZHED", GameColors.TILE, 110)
    settings = BoardSettings(window, font)
    buttons = []
    run = True
    counter = 0

    while run:
        pygame.time.delay(50)

        if counter == 0:
            draw_menu(settings)

        title.draw(window, 0, 0, size * 8 + 20, size * 3.5 + 10)

        buttons.append(Button(settings.font, "∙  PLAY  ∙", GameColors.GOAL_TEXT,
                              settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10,
                              round(size * 3.5) + 10, mode_menu))

        buttons.append(Button(settings.font, "∙  QUIT  ∙", GameColors.GOAL_TEXT,
                              settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10,
                              round(size * 5.5) + 10, lambda: pygame.quit()))

        draw_buttons(settings, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                check_button_clicks(buttons, pygame.mouse.get_pos())

        counter = (counter + 1) % 5
        try:
            pygame.display.update()
        except:
            exit(0)

    pygame.quit()


def draw_menu(settings):
    sprites = pygame.sprite.Group()

    side_y = round((settings.window.get_width() - 20) / size)
    side_x = round((settings.window.get_height() - 20) / size)

    for i in range(side_y):
        y_pos = i * size + 10
        for j in range(side_x):
            x_pos = j * size + 10
            empty_color = GameColors.empty_color()
            sprites.add(Tile(settings.font, ' ', empty_color, settings.window, empty_color, x_pos, y_pos))

    sprites.draw(settings.window)