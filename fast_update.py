from Player import player, playerInputs, playerHp
from Resources import font, colors
from Renderers import renderer, menuRenderer
from Dungeon import level
from Enemies import enemies
import deathScreen

def fast_update(terminal):
    terminal.clear()
    renderer.renderer(terminal, player.menu_opened)
    terminal.refresh()
    playerHp.hp_update()
    # Move enemies every player turn
    if enemies.enemies_list:
        for enemy in enemies.enemies_list:
            if enemy.hp < 0:
                level.occupied[enemy.enemy_pos[0]][enemy.enemy_pos[1]] = False
                enemies.enemies_list.remove(enemy)
                if enemy.is_visible:
                    menuRenderer.debug_log(f"You killed {enemy.name}.", color=colors.ORANGE)
                else:
                    menuRenderer.debug_log(f"You hear something dying in the distance.", color=colors.WHITE)
                continue
            enemy.controller()

    terminal.clear()
    renderer.renderer(terminal, player.menu_opened)
    terminal.refresh()

    if playerHp.hp <= 0:
        level.changes = True
        deathScreen.death(terminal)
        return