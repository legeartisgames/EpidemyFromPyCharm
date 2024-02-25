import sizes
import common_data as cd
import textures

from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

def load_ad(instance):
    cd.App.get_running_app().ads.show_rewarded_ad()

class Notifier(Widget):
    def __init__ (self, parent = None, pos = (sizes.width_res*0.15, sizes.height_res*0.74), **kwargs):
        super(Notifier, self).__init__(**kwargs) 
        self.is_active = None
        self.label = Label(halign = "center")
        self.label.bind(size = self.update_size, pos = self.update_size)
        self.add_widget(self.label)
        self.parent_is = parent
        self.event = Clock.schedule_once(self.hide, 1.5)
        
        self.size = (sizes.width_res*0.7, sizes.height_res*0.2)
        self.pos = pos     
        self.label.font_size = sizes.width_res/50
    def update_size(self, instance, args):
        self.label.size = (self.size[0],self.size[1])
        self.label.pos = (self.pos[0], self.pos[1])
       
    def notify(self, text = "", tau = 2, typ = "good", smooth_show = True):
        if hasattr(self, 'btn_ad') and self.btn_ad in self.children:
            self.remove_widget(self.btn_ad)
        self.is_active = 1
        self.opacity = 0.01
        self.event.cancel()
        self.size_hint = (.7, .2)
        if self in self.parent_is.children:
            self.parent.remove_widget(self)
    
        self.parent_is.add_widget(self, index = 0, canvas = 'after')
        self.canvas.before.clear()
        with self.canvas.before:
            if typ == 'bad' or typ == 'no money':
                if typ == 'bad' or cd.common_var.IS_PREMIUM == True:
                    Color(1, 0, 0, 1)
                else:
                    Color(.9, .9, .9, 1)
                if sizes.platform == 'android':
                    sizes.plyer.vibrator.pattern(pattern = (0, .04, .015, .04)) 
                        
            elif typ == 'info':
                Color(0.9, 0.7, 0.2, 1)
            else:
                Color(.1, 1, .1, 1)
            self.rec = Rectangle(size = self.size, pos = self.pos, texture = textures.error_texture)   
                    
            if typ == 'no money' and cd.spec_func.is_internet() == True and cd.common_var.IS_PREMIUM == False:
                self.btn_ad = Button(text = ['10 монет\nза рекламу',
                                             '10 coins\nfor ad video'][cd.common_var.lang],
                                     on_release = load_ad,
                                     font_size = sizes.width_res/60,
                                     pos = [self.pos[0]+self.size[0]*0.73, self.pos[1]+self.size[1]*0.1],
                                     size = [self.size[0]*0.25, self.size[1]*0.8],
                                     halign = 'center'
                                     )  
                self.add_widget(self.btn_ad)
            
        self.label.color = (1, 1, 1, 1)
        self.label.text = text
        self.label.pos = self.pos
        self.tau = tau
        
        if smooth_show:
            self.show(dt=0)
        else:
            self.opacity = 1
            self.event = Clock.schedule_once(self.hide, self.tau)
            self.event()            
        
    
    def show(self, dt):
        self.opacity = (self.opacity +0.06)*1.8
        
        if self.opacity > 1:
            self.opacity = 1
            self.event = Clock.schedule_once(self.hide, self.tau)
            self.event()
            return
        
        self.event = Clock.schedule_once(self.show, 0.02)
        self.event()
        
    def hide(self, dt):
        if self.opacity < 0.01:
            self.clear_and_delete(dt=0)
            self.opacity = 0
            self.label.text = ""
            return
        self.opacity = (self.opacity-0.03)*0.93
        self.event = Clock.schedule_once(self.hide, 0.05)
        self.event()
        
    def clear_and_delete(self, dt):
        self.is_active = 0
        self.parent_is.remove_widget(self)

notifier_box = Notifier(parent=cd.final_layout)
notifier_box2 = Notifier(parent=cd.final_layout, pos = (sizes.width_res*0.19, sizes.height_res*0.58))