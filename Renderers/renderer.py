from Renderers import levelRenderer, menuRenderer
from Dungeon import level
from Player import player


def renderer(terminal):
    if not player.menu_opened:
        levelRenderer.render_level(terminal, level.current_level.player_x, level.current_level.player_y)
    menuRenderer.menus(terminal, level.current_level.player_x, level.current_level.player_y)
