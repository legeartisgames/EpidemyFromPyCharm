from kivy import Config
from kivy.utils import platform

Config.set('graphics', 'multisamples', '0')

width_res = 2500
height_res = 1500

# import plyer

if platform == 'win':
    from screeninfo import get_monitors
    from kivy.core.window import Window

    m = get_monitors()[0]
    height_res = m.height
    width_res = m.width
    height_res = min(height_res, 1000)
    width_res = min(width_res, 1800)
    Window.size = (width_res, height_res)
    # screen_dpi = 70

if platform == 'android':
    from kivy.core.window import Window

    width_res = Window.size[0]
    height_res = Window.size[1]
    # from kivy.metrics import Metrics
    # screen_dpi = Metrics.dpi
    from jnius import cast
    from jnius import autoclass

if platform == 'linux':
    import os
    from kivy import Config

    # screen = os.popen("xrandr -q -d :0").readlines()[0]
    # width_res = int(screen.split()[7])
    # height_res = int(screen.split()[9][:-1])
    Config.set('graphics', 'width', str(width_res))
    Config.set('graphics', 'height', str(height_res))
    # screen_dpi = 70

ACHIEVE_SIZE = height_res / 30  # for achieve_pannel
ASK_SIZE = height_res / 600 * 22
WIN_SIZE = height_res / 600 * 24
TEXT_SIZE_OF_COMMON_PAR = round(width_res / 1720 * 31)
NAST_SIZE = round(width_res / 40)
SIZE_OF_TEXT_FOR_LABEL = 0  # it can be found in draw_for_epidemy
TEXT_SIZE_TABLE_NUMBERS = round(width_res / 1080 * 21)


SIZE20 = 20 * height_res / 600
SIZE22 = 22 * height_res / 600
SIZE25 = 25 * height_res / 600
SIZE30 = 30 * height_res / 600
SIZE35 = 35 * height_res / 600
textsize_normal = lambda x: x * height_res / 600
start_s2_pos_x = 0  # i don't know why it isn't 0 forever, for example in start of game
