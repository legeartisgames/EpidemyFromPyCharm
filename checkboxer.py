import math

import common_var
import icon_func
import sizes
import uix_classes

from kivy.clock import Clock
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

colors_of_levels = ["f5ad42", "d4f542", "3dbf15", "00f018", "3be3ce", "2b9eb5", "3e59b5" , "953eb5", "cc2763", "d40824"]


class Item_Label(ButtonBehavior, Label):
    def __init__(self, item, **kwargs):
        super(Item_Label, self).__init__(**kwargs)
        self.status = 'normal'
        self.item = item
        self.text_source = self.item.name
        self.text = self.item.name[common_var.lang]
        self.event = None
        self.markup = True
        
    def hide(self, dt):
        if self.opacity < 0.01:
            self.opacity = 0
            self.on_press(dt=0)
            self.show(dt=0)
            return
        self.opacity = (self.opacity-0.01)*0.81
        self.event = Clock.schedule_once(self.hide, 0.01)
        self.event()        
    def show(self, dt):
        self.opacity = (self.opacity +0.03)*1.21
        
        if self.opacity > 1:
            self.opacity = 1
            return
        self.event = Clock.schedule_once(self.show, 0.01)
        self.event()
                
    def on_press(self, dt=0):
        global colors_of_levels
        if self.event!=None:
            self.event.cancel()
            self.event = None
        if self.status == 'normal':
            self.text = ["уровень ", "level "][common_var.lang] + "[b][color=" + colors_of_levels[self.item.level-1]+ "]" +str(self.item.level) + "[/color][/b]" +[" из ", " of "][common_var.lang] + "[b][color=d40824]10[/b][/color]"
            self.font_size_n = self.font_size
            self.font_size/=1.09
            self.status = 'showing_level'
            self.event = Clock.schedule_once(self.hide, timeout=3)
            
        elif self.status == 'showing_level':
            self.opacity = 1
            self.font_size = self.font_size_n
            self.text = self.item.name[common_var.lang]
            self.status = 'normal'


class LockWidget(ButtonBehavior, GridLayout):
    def __init__(self, avail_set = [False, 'stars', 100500], **kwargs):
        super(LockWidget, self).__init__(**kwargs)
        self.cols = 1
        self.status = 'normal'
        self.im = Image(source = 'uix_images/check_locked2.jpg', color = [1, 1, 1,.7])
        #self.avail_set = avail_set
        
        if avail_set[1] == 'stars':
            text = ['нужно ещё '+str(math.ceil(avail_set[2]))+' stars', 'you need '+str(avail_set[2])+' stars'][common_var.lang]
        if avail_set[1] == 'coins':
            text = ['нужно ещё '+str(math.ceil(avail_set[2]))+' coins', 'you need '+str(avail_set[2])+' coins'][common_var.lang]
        text = icon_func.letter_to_icons_increasing_size(size = sizes.width_res/53, coef = 1.6, string = text)    
        self.lab = Label(text = text, font_size = sizes.width_res/53, markup = True)
        self.add_widget(self.im)
        self.event = None
        self.markup = True
        
    def hide(self, dt):
        if self.opacity < 0.01:
            self.opacity = 0
            self.on_press(dt=0)
            self.show(dt=0)
            return
        self.opacity = (self.opacity-0.01)*0.81
        self.event = Clock.schedule_once(self.hide, 0.01)
        self.event()        
    def show(self, dt):
        self.opacity = (self.opacity +0.03)*1.21
        
        if self.opacity > 1:
            self.opacity = 1
            return
        self.event = Clock.schedule_once(self.show, 0.01)
        self.event()
                
    def on_press(self, dt=0):
        global colors_of_levels
        if self.event!=None:
            self.event.cancel()
            self.event = None
        if self.status == 'normal':
            self.remove_widget(self.im)
            self.add_widget(self.lab)
            self.status = 'showing_need'
            self.source = None
            self.event = Clock.schedule_once(self.hide, timeout=3)
            
        elif self.status == 'showing_need':
            self.opacity = 1
            self.add_widget(self.im)
            self.remove_widget(self.lab)
            
            self.status = 'normal'
    
    

class UniToggleCheckbox(ToggleButtonBehavior, Image):
    def __init__(self, item_list, parentt = 5, number = 0,  **kwargs):
        super(UniToggleCheckbox, self).__init__(**kwargs)
        self.item_list = item_list
        self.source = 'uix_images/checkbox_image_up.jpg'
        self.value = 'up'
        self.number = number
        self.border = (200, 200, 200, 200)
        self.parentt = parentt
        
    def on_press(self):
        self.state = 'down'
        self.source = 'uix_images/checkbox_image_down.jpg'
        
        self.chosen = self.item_list[self.number].name[common_var.lang]
        
        if self.parentt.type == "country":
            common_var.Current_country = self.item_list[self.number].name[common_var.lang]
        
        if self.parentt.type == "disease":
            common_var.Current_dis = self.item_list[self.number].name[common_var.lang]
        
        if self.parentt.type == "mode":
            common_var.Current_mode = self.item_list[self.number].name[common_var.lang]
        
            
        for i in range(len(self.item_list)):
            if i!=self.number and self.parentt.avails[i] == True:
                self.parentt.check_boxes[i].state = 'normal'
                self.parentt.check_boxes[i].source = 'uix_images/checkbox_image_up.jpg'
        
class Universal_CheckBox(GridLayout): 

    def __init__(self, item_list, type = None, text_size = sizes.width_res/53, fir_av = 0, availabilites = None, **kwargs): 
        super(Universal_CheckBox, self).__init__(**kwargs) 
        
        self.type = type
        
        self.item_list = item_list
        
        self.num_of_variants = len(self.item_list)
        
        if availabilites == None:
            self.avails = [True]*self.num_of_variants
        else:
            self.avails = availabilites
        
        self.fir_av = fir_av

        self.spacing = (sizes.width_res/50, sizes.height_res/30)
        
        
        self.check_boxes = ['']*self.num_of_variants
        division_par = 12
        for i in range(0, self.num_of_variants):
            if self.avails[i] == True:
                
                self.check_boxes[i] = UniToggleCheckbox(size_hint = [.6, None], item_list = self.item_list, 
                                                             color = [1, 1, 1,.7], number = i, parentt = self,
                                                                  height = sizes.height_res/division_par)  
            else:
                self.check_boxes[i] = LockWidget(size_hint = [.6, None],
                                                 height = sizes.height_res/division_par,
                                                 avail_set = self.avails[i])
            
        if self.num_of_variants > 7:
            self.cols = 2
            my_spacing = (sizes.width_res/50, sizes.height_res/20)
            if self.num_of_variants > 12:
                my_spacing = (sizes.width_res/50, sizes.height_res/30)
            self.lay_left = GridLayout(cols = 2, spacing = my_spacing)
            self.lay_right = GridLayout(cols = 2, spacing = my_spacing)
            self.add_widget(self.lay_left)
            self.add_widget(self.lay_right)
            
            for i in range(self.num_of_variants):
                
                if i <= (self.num_of_variants-1)//2:
                
                    self.lay_left.add_widget(Item_Label(item = self.item_list[i],
                                                        size_hint = [.4, None],
                                                        font_size = text_size, 
                                                        height = sizes.height_res/division_par,
                                                        valign = 'center', text_size = (None, sizes.height_res/division_par),
                                                        halign = 'left'))
                    self.lay_left.add_widget(self.check_boxes[i])
                
                else:
                    
                    self.lay_right.add_widget(Item_Label(item = self.item_list[i],
                                                        size_hint = [.4, None],
                                                        font_size = text_size, 
                                                        height = sizes.height_res/division_par,
                                                        valign = 'center', text_size = (None, sizes.height_res/division_par),
                                                        halign = 'left'))
                    self.lay_right.add_widget(self.check_boxes[i]) 
                
        else:
            self.cols = 2
            
            for i in range(self.num_of_variants):
                self.add_widget(Item_Label(item = self.item_list[i],
                                           size_hint = [.4, None],
                                           font_size = text_size, 
                                           height = sizes.height_res/division_par, 
                                           valign = 'center', text_size = (None, sizes.height_res/division_par), 
                                           halign = 'left'))                
                self.add_widget(self.check_boxes[i])
                
        self.check_boxes[self.fir_av].state = 'down'
        self.check_boxes[self.fir_av].source = 'uix_images/checkbox_image_down.jpg'