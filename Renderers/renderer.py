from Renderers import levelRenderer, menuRenderer
from Player import player


def renderer(terminal, menu_opened):
    if not menu_opened:
        levelRenderer.render_level(terminal, player.player_y, player.player_x)
    menuRenderer.menus(terminal, player.player_y, player.player_x)
