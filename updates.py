from Screens import deathScreen, mainScreen
import time

from Player import player, playerInputs, playerHp
from Resources import font
from Renderers import renderer, menuRenderer
from Dungeon import level, levelGenerator
from Enemies import enemyManager


def update(terminal):
    level.levels = []
    level.levels.append(level.Level())
    level.current_level = level.levels[0]
    level.current_level.player_y, level.current_level.player_x = levelGenerator.generate_dungeon(0)
    # for i in range(10):
    #     menuRenderer.debug_log(f"You hear something dying in the distance.", color=colors.WHITE)

    while True:
        if font.font_size < 8:
            font.font_size = 8
        elif font.font_size > 20:
            font.font_size = 20
        terminal.set(
            f"window: size=160x50, cellsize=auto, title='Dungeon Crawler'; font: {font.font_path}, size={font.font_size};")

        terminal.clear()
        time.sleep(0.005)
        renderer.renderer(terminal)
        terminal.refresh()
        level.current_level.occupied[level.current_level.player_y][level.current_level.player_x] = False

        # Handle input every frame (non-blocking)
        if terminal.has_input() and player.can_input:
            key = playerInputs.get_input(terminal)

            result = playerInputs.player_input(terminal, key)
            if not result:
                continue
            elif level.current_level.changes:
                if result is False:
                    mainScreen.main_screen(terminal)
                    return
                elif result is None:
                    continue
                level.current_level.occupied[result[0]][result[1]] = True
                # Move enemies every player turn
                enemyManager.enemy_update()
                level.current_level.player_y, level.current_level.player_x = result
                playerHp.hp_update()
                level.current_level.occupied[level.current_level.player_y][level.current_level.player_x] = True

                terminal.clear()
                renderer.renderer(terminal)
                terminal.refresh()
                level.current_level.changes = False
            player.can_input = True
        if playerHp.hp <= 0:
            level.current_level.changes = True

            deathScreen.death(terminal)
            return


def fast_update(terminal, text=None):
    terminal.clear()
    renderer.renderer(terminal)
    if text: menuRenderer.text_renderer(terminal, text)
    terminal.refresh()
    playerHp.hp_update()
    # Move enemies every player turn
    enemyManager.enemy_update()

    terminal.clear()
    renderer.renderer(terminal)
    if text: menuRenderer.text_renderer(terminal, text)
    terminal.refresh()

    if playerHp.hp <= 0:
        level.changes = True
        deathScreen.death(terminal)
        return
