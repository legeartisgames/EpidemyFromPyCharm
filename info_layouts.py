
import common_data
import common_var
import frases
#from kivy.core.window import Window
import sizes
import uix_classes
#import web_goer
import icon_func

from kivy.uix.boxlayout import BoxLayout
from custom_kivy.my_scrollview import ScrollView
files_dict = dict()
'''
files_dict['manual'] = dict()
files_dict['manual']['ru'] = 'manual_texts/ru/manual-ru.txt'
files_dict['manual']['en'] = 'manual_texts/en/manual-en.txt'

files_dict['short_manual'] = dict()
files_dict['short_manual']['ru'] = 'manual_texts/ru/short-manual-ru.txt'
files_dict['short_manual']['en'] = 'manual_texts/en/short-manual-en.txt'
'''
files_dict['countryinfo'] = dict()
files_dict['countryinfo']['ru'] = 'manual_texts/ru/countryinfo-ru.txt'
files_dict['countryinfo']['en'] = 'manual_texts/en/countryinfo-en.txt'

files_dict['diseasesinfo'] = dict()
files_dict['diseasesinfo']['ru'] = 'manual_texts/ru/diseases_info_ru.txt'
files_dict['diseasesinfo']['en'] = 'manual_texts/en/diseases_info_en.txt'

files_dict['modesinfo'] = dict()
files_dict['modesinfo']['ru'] = 'manual_texts/ru/modes_info_ru.txt'
files_dict['modesinfo']['en'] = 'manual_texts/en/modes_info_en.txt'
'''
files_dict['about_us'] = dict()
files_dict['about_us']['ru'] = 'manual_texts/ru/about_us_ru.txt'
files_dict['about_us']['en'] = 'manual_texts/en/about_us_en.txt'
'''
rules_strings = dict()
for i in files_dict.keys():
    ff = open(files_dict[i]['ru'], 'r', encoding='utf-8')
    f_m = ff.readlines()
    rules_strings[i] = ['', '']
    for j in range(len(f_m)):
        rules_strings[i][0]+=(str(f_m[j]))
        
    ff = open(files_dict[i]['en'], 'r')
    f_m = ff.readlines()
    for j in range(len(f_m)):
        rules_strings[i][1]+=(str(f_m[j]))    

    
from kivy.effects.scroll import ScrollEffect


class Info_Layout(BoxLayout):
    def __init__(self, frase_close = ["Закрыть файл", "Close"], typ = 'manual', **kwargs): 
        super(Info_Layout, self).__init__(**kwargs)     
        self.typ = typ
        self.effect = ScrollEffect()
        self.effect.scroll = 10
        
        self.orientation = 'vertical'
        self.add_widget(uix_classes.Button_with_image(text_source = frase_close, on_press = self.close_manual, size_hint_y = .2, font_size = int(sizes.Width_of_screen/30)))
        self.text_rules = ScrollView(size_hint_y = .8, do_scroll_x=False, bar_color = [.35, .35, .25, 1], bar_margin = sizes.Height_of_screen*0.04, bar_width = 10, scroll_type = ['bars', 'content'])
        
        self.text_rules.rules_label = uix_classes.WrappedLabel(padding = (sizes.Width_of_screen*0.06, sizes.Height_of_screen*0.06),
                                                        text = icon_func.letter_to_icons_increasing_size(string = rules_strings[typ][common_var.lang], size = int(sizes.Width_of_screen/40), coef = 1.6), 
                                                        font_size = int(sizes.Width_of_screen/40), 
                                                        markup = True, size_hint_y = None, height = sizes.Height_of_screen*3)        
        self.text_rules.add_widget(self.text_rules.rules_label)
        self.add_widget(self.text_rules)
        self.outer_folders = []
        
    def open_manual(self, instance):
        self.outer_folders = []
        for i in common_data.final_layout.children:
            self.outer_folders.append(i)
        common_data.final_layout.clear_widgets()
        common_data.final_layout.add_widget(self)
        self.text_rules.rules_label.text = icon_func.letter_to_icons_increasing_size(string=rules_strings[self.typ][common_var.lang], size = int(sizes.Width_of_screen/40), coef = 2)
        
    def close_manual(self,instance):
        common_data.final_layout.remove_widget(self)
        for i in self.outer_folders:
            common_data.final_layout.add_widget(i)
            
        
#about_info = Info_Layout(frase_close = ["Закрыть информацию о нас", "Close info"], typ = 'about_us')   
#about_info.text_rules.rules_label.bind(on_ref_press = lambda *args: web_goer.go_to_link(*args))
#about_info.text_rules.rules_label.halign = "center"
#manual_pannel = Info_Layout(frase_close = frases.str_close_manual, typ = 'manual')
#short_manual_pannel = Info_Layout(frase_close = ['Закрыть справку', 'Close short help'], typ = 'short_manual')
country_info_pannel = Info_Layout(frase_close = ['Закрыть справку', 'Close short help'], typ = 'countryinfo')
diseases_info_pannel = Info_Layout(frase_close = ['Закрыть справку', 'Close short help'], typ = 'diseasesinfo')
modes_info_pannel = Info_Layout(frase_close = ['Закрыть справку', 'Close short help'], typ = 'modesinfo')