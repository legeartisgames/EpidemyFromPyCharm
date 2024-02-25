import common_data as cd
import common_var
import icon_func
import info_carousel
import sizes
import uix_classes
import web_goer

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from custom_kivy.my_scrollview import ScrollView

def add_spaces(num, text):
    text = text.splitlines()
    text2 = ''
    for i in text:
        i = ' '*num+i
        text2+=i+'\n'
    return text2

rules_dict = dict()
rules_dict['contents'] = dict()
rules_dict['contents']['ru'] = 'manual_texts/full_rules/ru/contents_ru.txt'
rules_dict['contents']['en'] = 'manual_texts/full_rules/en/contents_en.txt'
rules_dict['contents']['title'] = ["Оглавление", "Contents"]
rules_dict['contents']['index'] = 1

rules_dict['about'] = dict()
rules_dict['about']['ru'] = 'manual_texts/full_rules/ru/01_about_ru.txt'
rules_dict['about']['en'] = 'manual_texts/full_rules/en/about_en.txt'
rules_dict['about']['title'] = ["Общие сведения", "Common info"]
rules_dict['about']['index'] = 2

rules_dict['signs'] = dict()
rules_dict['signs']['ru'] = 'manual_texts/full_rules/ru/02_signs_ru.txt'
rules_dict['signs']['en'] = 'manual_texts/full_rules/en/signs_en.txt'
rules_dict['signs']['title'] = ["Параметры в игре", "Game parameters and designations"]
rules_dict['signs']['index'] = 3

rules_dict['how_play'] = dict()
rules_dict['how_play']['ru'] = 'manual_texts/full_rules/ru/03_how_play_ru.txt'
rules_dict['how_play']['en'] = 'manual_texts/full_rules/en/how_play_en.txt'
rules_dict['how_play']['title'] = ["Как играть", "How to play"]
rules_dict['how_play']['index'] = 4

rules_dict['partdop'] = dict()
rules_dict['partdop']['ru'] = 'manual_texts/full_rules/ru/04_partdop_ru.txt'
rules_dict['partdop']['en'] = 'manual_texts/full_rules/en/partdop_en.txt'
rules_dict['partdop']['title'] = ['Меню "Дополнительное"', 'Contents of "Additional"']
rules_dict['partdop']['index'] = 5

rules_dict['hex_sys'] = dict()
rules_dict['hex_sys']['ru'] = 'manual_texts/full_rules/ru/05_hex_sys_ru.txt'
rules_dict['hex_sys']['en'] = 'manual_texts/full_rules/en/hex_sys_en.txt'
rules_dict['hex_sys']['title'] = ["Устройство региона", "Hex structure"]
rules_dict['hex_sys']['index'] = 6

rules_dict['points'] = dict()
rules_dict['points']['ru'] = 'manual_texts/full_rules/ru/06_points_ru.txt'
rules_dict['points']['en'] = 'manual_texts/full_rules/en/points_en.txt'
rules_dict['points']['title'] = ["Штрафные и победные очки", "Win and penalty points"]
rules_dict['points']['index'] = 7

rules_dict['progress'] = dict()
rules_dict['progress']['ru'] = 'manual_texts/full_rules/ru/07_progress_ru.txt'
rules_dict['progress']['en'] = 'manual_texts/full_rules/en/progress_en.txt'
rules_dict['progress']['title'] = ["Награды за партии и прогресс в игре", "Awards and progress in the game"]
rules_dict['progress']['index'] = 8

rules_dict['graphs'] = dict()
rules_dict['graphs']['ru'] = 'manual_texts/full_rules/ru/08_graphs_ru.txt'
rules_dict['graphs']['en'] = 'manual_texts/full_rules/en/graphs_en.txt'
rules_dict['graphs']['title'] = ["Графики в игре", "Charts"]
rules_dict['graphs']['index'] = 9

rules_dict['save'] = dict()
rules_dict['save']['ru'] = 'manual_texts/full_rules/ru/save_in_game_ru.txt'
rules_dict['save']['en'] = 'manual_texts/full_rules/en/save_in_game_en.txt'
rules_dict['save']['title'] = ["Техническая информация", "Technical info"]
rules_dict['save']['index'] = 10

rules_dict['advice'] = dict()
rules_dict['advice']['ru'] = 'manual_texts/full_rules/ru/advices_ru.txt'
rules_dict['advice']['en'] = 'manual_texts/full_rules/en/advices_en.txt'
rules_dict['advice']['title'] = ["Советы по игре", "Tips on playing"]
rules_dict['advice']['index'] = 11

rules_dict['short'] = dict()
rules_dict['short']['ru'] = 'manual_texts/full_rules/ru/00_short_manual_ru.txt'
rules_dict['short']['en'] = 'manual_texts/full_rules/en/short_manual_en.txt'
rules_dict['short']['title'] = ["Краткая игровая справка", "Brief game help"]
rules_dict['short']['index'] = 12

rules_dict['disease'] = dict()
rules_dict['disease']['ru'] = 'manual_texts/ru/diseases_info_ru.txt'
rules_dict['disease']['en'] = 'manual_texts/en/diseases_info_en.txt'
rules_dict['disease']['title'] = ["Информация об инфекциях", "Diseases info"]
rules_dict['disease']['index'] = 13

rules_dict['country'] = dict()
rules_dict['country']['ru'] = 'manual_texts/ru/countryinfo-ru.txt'
rules_dict['country']['en'] = 'manual_texts/en/countryinfo-en.txt'
rules_dict['country']['title'] = ["Информация о странах", "Country info"]
rules_dict['country']['index'] = 14

rules_dict['modes'] = dict()
rules_dict['modes']['ru'] = 'manual_texts/ru/modes_info_ru.txt'
rules_dict['modes']['en'] = 'manual_texts/en/modes_info_en.txt'
rules_dict['modes']['title'] = ["Информация об игровых режимах", "Game modes info"]
rules_dict['modes']['index'] = 15

rules_dict['faq'] = dict()
rules_dict['faq']['ru'] = 'manual_texts/full_rules/ru/faq_ru.txt'
rules_dict['faq']['en'] = 'manual_texts/full_rules/en/faq_en.txt'
rules_dict['faq']['title'] = ["FAQ (они же частые вопросы)", "FAQ"]
rules_dict['faq']['index'] = 16

rules_dict['about_app'] = dict()
rules_dict['about_app']['ru'] = 'manual_texts/ru/about_us_ru.txt'
rules_dict['about_app']['en'] = 'manual_texts/en/about_us_en.txt'
rules_dict['about_app']['title'] = ["Информация о нас", "About us"]
rules_dict['about_app']['index'] = 17


rules_strings = dict()
for i in rules_dict.keys():
    ff = open(rules_dict[i]['ru'], 'r', encoding='utf-8')
    f_m = ff.readlines()
    rules_strings[i] = dict()
    rules_strings[i]['texts'] = ['', '']

    rules_strings[i]['names'] = rules_dict[i]['title']
    rules_strings[i]['index'] = rules_dict[i]['index']
    for j in range(len(f_m)):
        rules_strings[i]['texts'][0]+=(str(f_m[j]))
        
    ff = open(rules_dict[i]['en'], 'r')
    f_m = ff.readlines()
    for j in range(len(f_m)):
        rules_strings[i]['texts'][1]+=(str(f_m[j]))    
        
class RulePage(FloatLayout):
    def __init__(self, typ = 'about', **kwargs):
        super(RulePage, self).__init__(**kwargs)
        self.num = rules_strings[typ]['index']
        self.size = (sizes.width_res, sizes.height_res)
        
        if self.num < 17:
            
            self.btn_go_forward = uix_classes.Button_with_image(text_source = ['Следующая страница->', 'Next page ->'], 
                                                            font_size = sizes.textsize_normal(22), 
                                                            pos = (.69*sizes.width_res, .03*sizes.height_res),
                                                            size_hint = [None, None], 
                                                            size = (sizes.width_res*0.26, sizes.height_res*0.11),
                                                            on_press = lambda *args: self.open_page(self.num+1, *args))
            self.add_widget(self.btn_go_forward)
        else:
            
            self.btn_go_forward = uix_classes.Button_with_image(text_source = ['Закрыть правила', 'Close rules'], 
                                                            font_size = sizes.textsize_normal(22), 
                                                            pos = (.69*sizes.width_res, .03*sizes.height_res),
                                                            size_hint = [None, None], 
                                                            size = (sizes.width_res*0.26, sizes.height_res*0.11),
                                                            on_press = self.close_self)
            self.add_widget(self.btn_go_forward)
            
        if self.num!=1:
            
            self.btn_go_backward = uix_classes.Button_with_image(text_source = ['<-Предыдущая страница', '<- Previous Page'], 
                                                             font_size = sizes.textsize_normal(22),
                                                             pos = (.05*sizes.width_res, .03*sizes.height_res),
                                                             size_hint = [None, None], 
                                                             size = (sizes.width_res*0.26, sizes.height_res*0.11),
                                                             on_press = lambda *args: self.open_page(self.num-1, *args))
            self.add_widget(self.btn_go_backward)  
        else:
            self.btn_go_backward = uix_classes.Button_with_image(text_source = ['Закрыть правила', 'Close rules'], 
                                                             font_size = sizes.textsize_normal(22),
                                                             pos = (.05*sizes.width_res, .03*sizes.height_res),
                                                             size_hint = [None, None], 
                                                             size = (sizes.width_res*0.26, sizes.height_res*0.11),
                                                             on_press = self.close_self)
            self.add_widget(self.btn_go_backward)
        
        addition = ''    
        if 2<=self.num <=11:
            addition = [' (раздел ', ' (chapter '][common_var.lang] + str(self.num-1) + '/10)'
        elif self.num > 11:
            addition = [' (приложение ', ' (supplement '][common_var.lang] + str(self.num-11) + '/6)'
            
        self.title = Label(text = rules_strings[typ]['names'][common_var.lang] + addition, 
                           font_size = sizes.textsize_normal(29), 
                           pos = (.15*sizes.width_res, .87*sizes.height_res),
                           size_hint = [None, None], valign = 'top',
                           size = (sizes.width_res*0.7, sizes.height_res*0.1),
                           color = [1, 0, 0, 1],
                           on_press = lambda *args: self.open_page(1, *args),
                           markup = True, bold = True)
        
        self.add_widget(self.title)
        
        self.text_rules = ScrollView(size_hint = [.86, .72], pos = (0.07*sizes.width_res, sizes.height_res*0.13),
                                     do_scroll_x=False, bar_color = [.35, .35, .25, 1], 
                                     bar_margin = sizes.height_res*0.04, bar_width = 10, 
                                     scroll_type = ['bars', 'content'])
        if self.num == 14:#country info
            r_text = rules_strings[typ]['texts'][common_var.lang]
        else:
            r_text = icon_func.letter_to_icons_increasing_size(string = rules_strings[typ]['texts'][common_var.lang], size = int(sizes.width_res/40), coef = 1.6)
        self.text_rules.rules_label = uix_classes.WrappedLabel(padding = (sizes.width_res*0.06, sizes.height_res*0.06),
                                                        text = r_text, 
                                                        font_size = sizes.textsize_normal(25.5), halign = 'left',
                                                        markup = True, size_hint_y = None, height = sizes.height_res*3)  
        if self.num == 1:
            self.text_rules.rules_label.bind(on_ref_press = lambda *args: go_to_page_from_contents(*args))
        if self.num == 17 or self.num == 10:
            self.text_rules.rules_label.bind(on_ref_press = lambda *args: web_goer.go_to_link(*args))
            
        self.text_rules.add_widget(self.text_rules.rules_label)
        self.add_widget(self.text_rules, index = 10) 
        
    def open_page(self, index, instance):
        global rp
        
        for i in rules_dict.keys():
            if rules_dict[i]['index'] == index:
                
                cd.final_layout.remove_widget(rp)
             
                del rp
                rp = RulePage(typ = i)
                cd.final_layout.add_widget(rp)  
                
  
        

    def open_self(self, instance):
        global outer_folders, rp
        outer_folders = []
        for i in cd.final_layout.children:
            outer_folders.append(i)
        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(rp)
        if self!=rp:
            print("Different interact rules exemplars! Warning!")
            del self 
        
    def close_self(self, instance):
        global outer_folders
        cd.final_layout.remove_widget(self)
        for i in outer_folders:
            cd.final_layout.add_widget(i)        
        outer_folders = []
                
def go_to_page_from_contents(instance, value):
    global rp
    if value == 'demo':
        info_carousel.InfoCarousel().open(instance=5)
    else:
        rp.open_page(int(value)+1, instance=0)

outer_folders = []    
rp = RulePage(typ = 'contents') 


