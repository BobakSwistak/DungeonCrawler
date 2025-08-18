from bearlibterminal import terminal
from Dungeon import levelGenerator, level
from Renderers import logoRenderer, renderer, menuRenderer
from Player import playerInputs, playerHp, player
from Resources import font, colors
from Enemies import enemies
import sys
import os
import time
import services
import deathScreen

font_path = 'Resources/FSEX300.ttf'


def main():
    playerHp.hp_init()
    terminal.open()
    font_init()
    terminal.set(
        f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: {font_path}, size={font.font_size};")

    terminal.refresh()

    main_screen(terminal)


def main_screen(terminal):
    terminal.clear()
    logoRenderer.draw_centered_logo(terminal)
    terminal.refresh()

    while True:
        key = terminal.read()
        if key == terminal.TK_CLOSE or key == terminal.TK_Q:
            sys.exit()
        elif key != -1:  # Wait for any key press
            game_cycle(terminal)
            return


def game_cycle(terminal):
    player.player_y, player.player_x = levelGenerator.generate_dungeon()
    for i in range(10):
        menuRenderer.debug_log(f"You hear something dying in the distance.", color=colors.WHITE)

    while True:
        if font.font_size < 8:
            font.font_size = 8
        elif font.font_size > 20:
            font.font_size = 20
        terminal.set(
            f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: {font_path}, size={font.font_size};")

        terminal.clear()
        time.sleep(0.005)
        renderer.renderer(terminal, player.menu_opened)
        terminal.refresh()
        level.occupied[player.player_y][player.player_x] = False

        # Handle input every frame (non-blocking)
        if terminal.has_input() and player.can_input:
            key = playerInputs.get_input(terminal)

            result = playerInputs.player_input(terminal, key, player.player_y, player.player_x)
            if not result:
                continue
            elif level.changes:
                if result is False:
                    main_screen(terminal)
                    return
                elif result is None:
                    continue
                player.player_y, player.player_x = result
                playerHp.hp_update()
                level.occupied[player.player_y][player.player_x] = True
                # Move enemies every player turn
                if enemies.enemies_list:
                    for enemy in enemies.enemies_list:
                        if enemy.hp < 0:
                            level.occupied[enemy.enemy_pos[0]][enemy.enemy_pos[1]] = False
                            enemies.enemies_list.remove(enemy)
                            if enemy.is_visible:
                                menuRenderer.debug_log(f"{enemy.name} died.", color=colors.ORANGE)
                            elif abs(player.player_y - enemy.enemy_pos[0]) + abs(
                                    player.player_x - enemy.enemy_pos[1]) >= 10:
                                menuRenderer.debug_log(f"You hear something dying in the distance.", color=colors.WHITE)
                            continue
                        enemy.controller()

                terminal.clear()
                renderer.renderer(terminal, player.menu_opened)
                terminal.refresh()
                level.changes = False
            player.can_input = True
        if playerHp.hp <= 0:
            level.changes = True

            deathScreen.death(terminal)
            return


def font_init():
    global font_path
    if hasattr(sys, '_MEIPASS'):
        font_path = os.path.join(sys._MEIPASS, 'Resources', 'FSEX300.ttf')
    else:
        font_path = 'Resources/FSEX300.ttf'


main()
