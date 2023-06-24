from kivy import Config
Config.set('graphics', 'multisamples', '0')

Width_of_screen = 1200
Height_of_screen = 600

from kivy.utils import platform

import plyer
if platform == 'win':
    from screeninfo import get_monitors
    from kivy.core.window import Window
    m = get_monitors()[0]
    Height_of_screen = m.height
    Width_of_screen = m.width
    Height_of_screen = min(Height_of_screen, 1000)
    Width_of_screen = min(Width_of_screen, 1800)
    Window.size = (Width_of_screen, Height_of_screen)
    #screen_dpi = 70
if platform == 'android':
    from kivy.core.window import Window
    Width_of_screen = Window.size[0]
    Height_of_screen = Window.size[1]
    #from kivy.metrics import Metrics
    #screen_dpi = Metrics.dpi
    from jnius import cast
    from jnius import autoclass    
    
if platform == 'linux':
    import os
    from kivy import Config
    #screen = os.popen("xrandr -q -d :0").readlines()[0]
    #Width_of_screen = int(screen.split()[7])
    #Height_of_screen = int(screen.split()[9][:-1])
    Config.set('graphics', 'width', str(Width_of_screen))
    Config.set('graphics', 'height', str(Height_of_screen))
    #screen_dpi = 70

ACHIEVE_SIZE = Height_of_screen/30 #for achieve_pannel
ASK_SIZE = Height_of_screen/600*22
WIN_SIZE = Height_of_screen/600*24
TEXT_SIZE_OF_COMMON_PAR = round(Width_of_screen/1720*31)
NAST_SIZE = round(Width_of_screen/40)
SIZE_OF_TEXT_FOR_LABEL = 0 #it can be found in draw_for_epidemy
TEXT_SIZE_TABLE_NUMBERS = round(Width_of_screen/1080*21)

SIZE20 = 20*Height_of_screen/600
SIZE22 = 22*Height_of_screen/600
SIZE25 = 25*Height_of_screen/600
SIZE30 = 30*Height_of_screen/600
SIZE35 = 35*Height_of_screen/600
textsize_normal = lambda x: x*Height_of_screen/600
start_s2_pos_x = 0#i don't khow why it isn't 0 forever, for example in start of game