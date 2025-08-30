import sys, os

font_size = 14
font_path = "Resources/FSEX300.ttf"

def font_init():
    global font_path
    if hasattr(sys, '_MEIPASS'):
        font_path = os.path.join(sys._MEIPASS, 'Resources', 'FSEX300.ttf')
    else:
        font_path = 'Resources/FSEX300.ttf'

