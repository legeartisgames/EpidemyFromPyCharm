import webbrowser

def go_to_link(instance, value):
    webbrowser.open(value)
'''
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

ff = open('about_us_ru.txt', 'r', encoding='utf-8')
f_m = ff.readlines()
rules_string = ['', '']
for i in range(len(f_m)):
    rules_string[0]+=(str(f_m[i]))
    
ff = open('about_us_en.txt', 'r')
f_m = ff.readlines()
for i in range(len(f_m)):
    rules_string[1]+=(str(f_m[i]))
    
from kivy.effects.scroll import ScrollEffect


class About_Us_info(BoxLayout):
    def __init__(self, **kwargs): 
        super(About_Us_info, self).__init__(**kwargs)     
        self.effect = ScrollEffect()
        self.effect.scroll = 10
        
        self.orientation = 'vertical'
        self.add_widget(uix_classes.Button_with_image(text_source = ["Закрыть информацию о нас", "Close info"], on_press = self.close_manual, size_hint_y = .2, font_size = int(sizes.Width_of_screen/30)))
        self.text_rules = ScrollView(size_hint_y = .8, do_scroll_x=False, bar_color = [.35, .35, .25, 1], bar_width = 10)
        self.text_rules.rules_label = uix_classes.WrappedLabel(padding = (sizes.Width_of_screen*0.06, sizes.Height_of_screen*0.06),
                                                        text = common_data.letter_to_icons_increasing_size(string=rules_string[common_var.lang], size = int(sizes.Width_of_screen/40), coef = 2), 
                                                        font_size = int(sizes.Width_of_screen/40), markup = True, size_hint_y = None, height = sizes.Height_of_screen*3,
                                                        )        
        self.text_rules.add_widget(self.text_rules.rules_label)
        self.add_widget(self.text_rules)
        self.outer_folders = []
        
    def open_manual(self, instance):
        self.outer_folders = []
        for i in common_data.final_layout.children:
            self.outer_folders.append(i)
        common_data.final_layout.clear_widgets()
        common_data.final_layout.add_widget(self)
        self.text_rules.rules_label.text = common_data.letter_to_icons_increasing_size(string=rules_string[common_var.lang], size = int(sizes.Width_of_screen/40), coef = 2)
        
    def close_manual(self,instance):
        common_data.final_layout.remove_widget(self)
        for i in self.outer_folders:
            common_data.final_layout.add_widget(i)
            
        
        #common_data.final_layout.clear_widgets()
        #for i in common_data.curr_widgets:
         #   common_data.final_layout.add_widget(i)
        
        
about_info = About_Us_info()'''
