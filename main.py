from bearlibterminal import terminal
from Dungeon import levelGenerator, level
from Renderers import logoRenderer, renderer, menuRenderer
from Player import playerInputs, playerHp, player
from Resources import font, colors
from Enemies import enemies
import sys
import time
import services
import deathScreen


def main():
    playerHp.hp_init()
    terminal.open()
    terminal.set(
        f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: Resources/FSEX300.ttf, size={font.font_size};")

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

    while True:
        if font.font_size < 8:
            font.font_size = 8
        elif font.font_size > 20:
            font.font_size = 20
        terminal.set(
            f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: Resources/FSEX300.ttf, size={font.font_size};")

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
                print("skip")
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
                            print("dead")
                            if enemy.is_visible:
                                menuRenderer.debug_log(f"You killed {enemy.name}.", color=colors.ORANGE)
                            elif abs(player.player_y - enemy.enemy_pos[0]) + abs(player.player_x - enemy.enemy_pos[1]) >= 10:
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


main()
