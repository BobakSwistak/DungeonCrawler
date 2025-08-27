import deathScreen

from Player import player, playerInputs, playerHp
from Resources import font, colors
from Renderers import renderer, menuRenderer
from Dungeon import level
from Enemies import enemyManager


def fast_update(terminal, text=None):
    terminal.clear()
    renderer.renderer(terminal, player.menu_opened)
    if text: menuRenderer.text_renderer(terminal, text)
    terminal.refresh()
    playerHp.hp_update()
    # Move enemies every player turn
    enemyManager.enemy_update()

    terminal.clear()
    renderer.renderer(terminal, player.menu_opened)
    if text: menuRenderer.text_renderer(terminal, text)
    terminal.refresh()

    if playerHp.hp <= 0:
        level.changes = True
        deathScreen.death(terminal)
        return
