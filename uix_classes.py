from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from kivy.uix.togglebutton import ToggleButton

import common_var
import sizes 
class CustomGridLayout(BoxLayout):
    def __init__(self, **kwargs): 
        super(CustomGridLayout, self).__init__(**kwargs) 
        self.real_children = []
        self.orientation = 'vertical'
    def add_widgets(self, obj, size_hint_y = .1):
        if len(self.real_children)%2==1:
            self.last_layout.add_widget(obj)
        else:
            self.last_layout = GridLayout(size_hint_y = size_hint_y, cols = 2)
            self.add_widget(self.last_layout)
            self.last_layout.add_widget(obj)
        self.real_children.append(obj)
class StencilBox(StencilView, FloatLayout):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_up(touch)
    
class Button_with_image(Button):
    def __init__(self, text_source = ['', ''], **kwargs): 
        super(Button_with_image, self).__init__(**kwargs) 
        self.text_source = text_source
        self.background_normal = "uix_images/button_with_image_background.jpg" 
        self.background_down = "uix_images/button_with_image_background_pressed.jpg"
        common_var.list_of_btns.append(self)
        self.text = self.text_source[common_var.lang]

class RLabel(Label):

    def __init__(self, color_r, **kwargs):
        super(RLabel, self).__init__(**kwargs)  
        Color(color_r[0], color_r[1], color_r[2], color_r[3])
        Rectangle(pos=self.pos, size=self.size)                     

class ToggleButton_with_image(ToggleButton):
    def __init__(self, text_source = ['', ''], **kwargs): 
        super(ToggleButton_with_image, self).__init__(**kwargs) 
        self.text_source = text_source
        self.background_normal = "uix_images/button_with_image_background.jpg" 
        self.background_down = "uix_images/button_with_image_background_pressed.jpg"
        common_var.list_of_btns.append(self)
        self.text = self.text_source[common_var.lang]

class WrappedLabel_with_tr(Label):
    
    def __init__(self, text_source = '', **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))
        self.text_source = text_source
        common_var.list_of_btns.append(self)
        self.text = self.text_source[common_var.lang]+self.text        
class WrappedLabel(Label):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

class Label_with_tr(Label):
    def __init__(self, text_source = ['', ''], **kwargs): 
        super(Label_with_tr, self).__init__(**kwargs) 
        self.text_source = text_source
        common_var.list_of_btns.append(self)
        self.text = self.text_source[common_var.lang]+self.text

class Button_with_tr(Button):
    def __init__(self, text_source = ['', ''], **kwargs): 
        super(Button_with_tr, self).__init__(**kwargs) 
        self.text_source = text_source
        common_var.list_of_btns.append(self)
        self.text = self.text_source[common_var.lang]+self.text

class Button_asfalt(Button, WrappedLabel):
    def __init__(self, text_source = ['', ''], **kwargs): 
        super(Button_asfalt, self).__init__(**kwargs) 
        self.text_source = text_source
        common_var.list_of_btns.append(self)
        self.halign = 'center'
        self.text = self.text_source[common_var.lang]
        self.background_color = (1, 1, 1, 1)


from kivy.uix.dropdown import DropDown

from kivy.uix.spinner import SpinnerOption, Spinner
class SpinnerOptions(SpinnerOption):

    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0, 0.2, 0.3, 1]    # blue colour
        #self.size_hint_y = None
        #self.height = sizes.Height_of_screen/8
        self.font_size = sizes.ASK_SIZE
        self.markup = True

class SpinnerDropdown(DropDown):

    def __init__(self, **kwargs):
        super(SpinnerDropdown, self).__init__(**kwargs)
        self.auto_width = True
        self.max_height = sizes.Height_of_screen*0.4
        self.container.spacing = 3*sizes.Height_of_screen/720
        #self.width = sizes.Width_of_screen/5


class SpinnerWidget(Spinner):
    def __init__(self, **kwargs):
        super(SpinnerWidget, self).__init__(**kwargs)
        self.dropdown_cls = SpinnerDropdown
        self.option_cls = SpinnerOptions

from kivy.lang import Builder
Builder.load_string("""
<Label_touch@ButtonBehavior+Label>:
    on_press:
        pass""")
class Label_touch(ButtonBehavior, Label):
    pass

Builder.load_string("""
<Image_touch@ButtonBehavior+Label>:
    on_press:
        pass""")
class Image_touch(ButtonBehavior, Image):
    pass
