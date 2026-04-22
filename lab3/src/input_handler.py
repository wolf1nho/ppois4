import pygame

from .constants import GameState, KEY_ALIASES


class InputHandler:
    def handle_keydown(self, game, event):
        if game.state == GameState.NAME_ENTRY:
            if event.key == pygame.K_RETURN:
                game.save_record(game.name_input, game.pending_record)
                game.pending_record = None
                game.state = GameState.HIGHSCORES
            elif event.key == pygame.K_BACKSPACE:
                game.name_input = game.name_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                game.pending_record = None
                game.state = GameState.MENU
                game.reset()
            elif event.unicode and event.unicode.isprintable() and len(game.name_input) < 20:
                game.name_input += event.unicode
            return

        if event.key == pygame.K_ESCAPE:
            if game.state == GameState.PLAYING and game.game_over:
                game.state = GameState.MENU
                game.reset()
            elif game.state == GameState.HIGHSCORES:
                game.state = GameState.MENU
            elif game.state == GameState.PAUSED:
                game.state = GameState.PLAYING
            elif game.state == GameState.PLAYING and not game.game_over:
                game.state = GameState.PAUSED
            else:
                game.running = False

        if game.state == GameState.PLAYING and not game.game_over and event.key in (pygame.K_p, pygame.K_SPACE):
            game.state = GameState.PAUSED

        if game.state == GameState.PLAYING and event.key in (pygame.K_q, KEY_ALIASES["q_ru"]):
            game.player.switch_weapon(-1)
        if game.state == GameState.PLAYING and event.key in (pygame.K_e, KEY_ALIASES["e_ru"]):
            game.player.switch_weapon(1)
        if game.state == GameState.PLAYING and event.key in (pygame.K_1, KEY_ALIASES["1_ascii"]):
            game.player.select_weapon(0)
        if game.state == GameState.PLAYING and event.key in (pygame.K_2, KEY_ALIASES["2_ascii"]):
            game.player.select_weapon(1)
        if game.state == GameState.PLAYING and event.key in (pygame.K_3, KEY_ALIASES["3_ascii"]):
            game.player.select_weapon(2)

        if game.state == GameState.MENU:
            if event.key in (pygame.K_DOWN, KEY_ALIASES["down_ru"]):
                game.menu_selected = (game.menu_selected + 1) % 3
            elif event.key in (pygame.K_UP, KEY_ALIASES["up_ru"]):
                game.menu_selected = (game.menu_selected - 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if game.menu_selected == 0:
                    game.reset()
                    game.state = GameState.PLAYING
                elif game.menu_selected == 1:
                    game.state = GameState.HIGHSCORES
                elif game.menu_selected == 2:
                    game.running = False

        if game.state == GameState.PAUSED:
            if event.key in (pygame.K_DOWN, KEY_ALIASES["down_ru"]):
                game.pause_selected = (game.pause_selected + 1) % 2
            elif event.key in (pygame.K_UP, KEY_ALIASES["up_ru"]):
                game.pause_selected = (game.pause_selected - 1) % 2
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if game.pause_selected == 0:
                    game.state = GameState.PLAYING
                elif game.pause_selected == 1:
                    game.state = GameState.MENU
                    game.reset()

        if game.state == GameState.PLAYING and game.game_over and event.key in (pygame.K_r, KEY_ALIASES["r_ru"]):
            game.reset()
            game.state = GameState.PLAYING
