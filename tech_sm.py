import common_data as cd
import sizes
import uix_classes
from uix_classes import Label_touch
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.uix.widget import WidgetException


def on_left_press (self):
    self.parent.sm.transition.direction = 'right'
    self.parent.sm.transition.mode = 'push'
    self.parent.sm.current = self.parent.sm.previous()
def on_right_press (self):
    self.parent.sm.transition.direction = 'left'
    self.parent.sm.transition.mode = 'pop'
    self.parent.sm.current = self.parent.sm.next()


class ViewerScreen(Screen):
    def __init__(self, typ = 'about', **kwargs):
        super(ViewerScreen, self).__init__(**kwargs)  
        self.sc = ScatterLayout(do_rotation = False, do_scale = False, do_translation = False,
                                 scale = 0.9*sizes.height_res/cd.frontend.wid[0].height
                                 )
                
class TechViewer(BoxLayout):
    def __init__(self, **kwargs):
        global tech_viewer
        tech_viewer = self
        super(TechViewer, self).__init__(**kwargs)
        
        self.spacing = 20*sizes.width_res/1000
        self.padding = [20*sizes.width_res/1000, 0]
        
        left_but = uix_classes.Image_touch(source='uix_images/green_left_arrow.png', size_hint_x = .11, on_press = on_left_press,
                                           color=(1, 1, 1, .85))
        self.add_widget(left_but)
        
        self.sm = ScreenManager(transition = CardTransition(duration = .8, mode='push'), size_hint_x = .7)
        self.add_widget(self.sm) 
        
        right_but = uix_classes.Image_touch(source='uix_images/green_right_arrow.png', size_hint_x = .11, on_press = on_right_press,
                                            color=(1, 1, 1, .85))
        self.add_widget(right_but)
        
        for i in cd.common_var.tech_order:
            if cd.frontend.wid[i].is_available == 'no in mode lack of methods' or \
                (cd.stats.are_shown_unlocked_methods == False and cd.mg.techs_avail_bool[i]==False)\
               or i == 2 or i == 9:
                continue
        
            self.add_screen_to_sm(i)
            
    def add_screen_to_sm(self, i):
        screen = ViewerScreen(name='%d' % i)
        self.sm.add_widget(screen)

        screen.sc_stencilbox = uix_classes.StencilBox()
        screen.sc_stencilbox.add_widget(screen.sc)
        screen.add_widget(screen.sc_stencilbox, index = 1)
        
    def remove_screen(self, i):
        screen_being_removed = self.sm.get_screen(str(i))
        if screen_being_removed == self.sm.current:
            self.sm.next()
        self.sm.remove_widget(screen_being_removed)
        
        cd.frontend.wid[i].size_hint_x = 1
        cd.frontend.wid[i].width = 100
        cd.frontend.wid[i].pos_hint = {}
    
        screen_being_removed.sc.remove_widget(cd.frontend.wid[i])
        
        del screen_being_removed
    
    def add_element_to_screen(self, i):
        my_screen = self.sm.get_screen(str(i))
        
        cd.frontend.wid[i].size_hint_x = None
        cd.frontend.wid[i].width = cd.frontend.wid[i].height*0.75
        cd.frontend.wid[i].pos_hint = {'center_x': 0.52/my_screen.sc.scale, 'center_y': 0.52/my_screen.sc.scale}
        cd.page2.remove_widget(cd.frontend.wid[i])
        my_screen.sc.add_widget(cd.frontend.wid[i])
                
    def open_self(self, instance, ind_tech = 0):
        
        self.outer_folders = []
        for i in cd.page2_1.children:
            self.outer_folders.append(i)
        
        cd.page2_1.clear_widgets()
        cd.page2_1.add_widget(self)
        
        cd.frontend.tech_panel_mode = "viewer"
        
        
        for i in cd.common_var.tech_order:
            if cd.frontend.wid[i].is_available == 'no in mode lack of methods' or \
                (cd.stats.are_shown_unlocked_methods == False and cd.mg.techs_avail_bool[i]==False)\
               or i == 2 or i == 9:
                continue
            self.add_element_to_screen(i)
            
        self.sm.current = str(ind_tech)
        
    def close_self(self, instance):
        global tech_viewer
        
        cd.frontend.tech_panel_mode = "panel"
        for i in cd.common_var.tech_order:
            if cd.frontend.wid[i].is_available == 'no in mode lack of methods' or \
                (cd.stats.are_shown_unlocked_methods == False and cd.mg.techs_avail_bool[i]==False)\
               or i == 2 or i == 9:
                continue
        
            cd.frontend.wid[i].size_hint_x = 1
            cd.frontend.wid[i].width = 100
            cd.frontend.wid[i].pos_hint = {}
          
            self.sm.get_screen(str(i)).sc.remove_widget(cd.frontend.wid[i])        
            cd.page2.add_widget(cd.frontend.wid[i])
            
        cd.page2_1.remove_widget(self)
        for i in self.outer_folders:
            try:
                cd.page2_1.add_widget(i)   
            except WidgetException:
                print("[ERROR] with adding", i, "if it is notifier, don't worry")
        self.outer_folders = []
        
        
        del self
        tech_viewer = None    
       


tech_viewer = None



    


