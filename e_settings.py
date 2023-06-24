import achieve_pannel
import common_data
import common_var
import draw_for_epidemy
import gold_transaction
import icon_func
import info_layouts
import init_of_tech
import interact_rules
import lang_checkbox
import music_module
import textures
import sizes
import uix_classes
import widget_of_common_par

from kivy.clock import Clock
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from custom_kivy.my_scrollview import ScrollView
from kivy.uix.slider import Slider

class Additional_Menu(GridLayout): 

    def __init__(self, type_of_nast = "game_nast", **kwargs): 
        super(Additional_Menu, self).__init__(**kwargs) 
        self.need_s = BoxLayout()
        self.need_c = BoxLayout()
        self.create(type_of_nast)
        self.type_of_nast = type_of_nast
    
    def create(self, type_of_nast = "game_nast"):
        
        self.cols = 2
        self.spacing = (sizes.Width_of_screen/250, sizes.Height_of_screen/250)
        if type_of_nast  == "game_nast":
            self.add_widget(uix_classes.Button_with_image(on_press = self.increase_money,  
                                                          size_hint_y = None, height = sizes.Height_of_screen/5, 
                                                          font_size = sizes.NAST_SIZE, 
                                                          halign = 'center', text_source = ["Пополнить казну", "Get money"]))
            
        self.add_widget(uix_classes.Button_with_image(text_source = ["Панель достижений", "Achievement bar"], 
                                                          on_press = achieve_pannel.achieve_p.open_layout,
                                                          size_hint_y = None, height = sizes.Height_of_screen/5, 
                                                          font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.add_widget(uix_classes.Button_with_image(text_source = ["Правила игры", "Game guide"], 
                                                              on_press = interact_rules.rp.open_self, 
                                                              size_hint_y = None, height = sizes.Height_of_screen/5, 
                                                              font_size = sizes.NAST_SIZE))       
        if type_of_nast  == "game_nast":
            
            self.add_widget(uix_classes.Button_with_image(text_source = ['Назад к игре', "Back to the game"], 
                                                              on_press = self.close_nast, 
                                                              size_hint_y = None, height = sizes.Height_of_screen/5, 
                                                              font_size = sizes.NAST_SIZE, halign = 'center')) 
            
            self.add_widget(uix_classes.Label_with_tr(text_source = ["Текущая страна", "Current country"], 
                                                      size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                      font_size = sizes.NAST_SIZE, halign = 'center'))
            
            self.label_current_country_is = uix_classes.Label_with_tr(text_source = common_data.my_game.My_Country.name, size_hint = [1, .3], 
                                                                      font_size = sizes.NAST_SIZE, color = "56b344")
            self.add_widget(self.label_current_country_is)  
        
            self.add_widget(uix_classes.Label_with_tr(text_source = ["Текущая инфекция", "Current infection"], 
                                                      size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                      font_size = sizes.NAST_SIZE, halign = 'center'))
            
            self.label_current_disease_is = uix_classes.Label_with_tr(text_source = common_data.my_game.My_disease.name, size_hint = [1, .3], 
                                                                      font_size = sizes.NAST_SIZE, color = [1, 0, 0, 1])
            self.add_widget(self.label_current_disease_is)  
            
            self.add_widget(uix_classes.Label_with_tr(text_source = ["Текущий режим", "Current mode"], 
                                                      size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                      font_size = sizes.NAST_SIZE, halign = 'center'))
            
            self.label_current_mode_is = uix_classes.Label_with_tr(text_source = common_data.my_game.My_mode.name, size_hint = [1, .3], 
                                                                      font_size = sizes.NAST_SIZE, color = "2065ab")
            self.add_widget(self.label_current_mode_is)              
            
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Музыка", "Music"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.music_switch = music_module.My_switch(size_hint = [1, .2])
        self.add_widget(self.music_switch)
        
        
        self.volume_ind = Slider(min = 0, max = 1, size_hint = [1, .2], value = 0.7, sensitivity = "all", value_track = True,
                                              value_track_color = [70/256, 89/256, 94/256, 1], value_track_width = "4.5dp")
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Громкость музыки", "Music volume"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.volume_ind.bind(value = self.Set_volume)
        
        self.add_widget(self.volume_ind)
         
        if type_of_nast  == "game_nast":
            self.add_widget(uix_classes.Label_with_tr(text_source = ["Линейка на карте страны", "Ruler on country map"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
            self.switch_real_sizes = music_module.Switch(size_hint = [1, .2], active = common_data.my_stats.is_shown_real_sizes_of_country)
            self.add_widget(self.switch_real_sizes)
            
            self.switch_real_sizes.bind(active=self.draw_redraw_real_country_sizes)
            
            self.add_widget(uix_classes.Label_with_tr(text_source = ["Отображение\nнедоступных методов", "Show yet unlocked\nmethods"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
            self.switch_show_unlocked = music_module.Switch(size_hint = [1, .2], active = common_data.my_stats.are_shown_unlocked_methods)
            self.add_widget(self.switch_show_unlocked)
            
            self.switch_show_unlocked.bind(active=self.operate_unlocked_methods)
            
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Процент побед", "Victory percent"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.lab_percent_of_v = Label(text = common_data.str_percent_of_v[common_var.lang], 
                                                   size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                   font_size = sizes.NAST_SIZE)
        self.add_widget(self.lab_percent_of_v)
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Число сыгранных партий", "Completed games"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.lab_number_of_games = Label(text = str(common_data.my_stats.number_of_games), 
                                                      size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                      font_size = sizes.NAST_SIZE)
        self.add_widget(self.lab_number_of_games)
           
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Дней в игре", "Days with gaming"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.add_widget(uix_classes.Label(text = str(len(common_data.my_stats.days_of_activity)), 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))        
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Звёзды репутации", "Reputation stars"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.lab_quant_of_stars = Label(text = icon_func.add_star_icon(string = str(common_data.my_stats.stars), 
                                                                                    size = sizes.NAST_SIZE), 
                                                     size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                     font_size = sizes.NAST_SIZE, markup = True)
        self.add_widget(self.lab_quant_of_stars)
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Статус репутации", "Reputation Status"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.lab_status_of_rep = uix_classes.Label_with_tr(text_source = common_var.statuses_stars[common_data.my_stats.level_stars], 
                                                           size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                           font_size = sizes.NAST_SIZE, halign = 'center')
        self.add_widget(self.lab_status_of_rep)  
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["До следующего\nстатуса репутации", "For next reputation status"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.lab_need_for_s = Label(text = icon_func.add_star_icon(string = str(common_var.need_s), size = sizes.NAST_SIZE), 
                                                 size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                 font_size = sizes.NAST_SIZE, markup = True)
        
        self.lab_need_for_s.font_size = sizes.NAST_SIZE
        self.need_s.clear_widgets()
        self.add_widget(self.need_s)
        self.lab_need_for_s.size_hint_x = .35
        self.need_s.add_widget(self.lab_need_for_s)
        
        self.progress_s = ProgressBar(value = common_data.my_stats.stars, 
                                                   max = common_data.my_stats.stars + common_var.need_s, 
                                                   size_hint_x = .57)
        self.need_s.add_widget(self.progress_s)
        self.progress_s.value = common_data.my_stats.stars
        
        if type_of_nast == "game_nast":
            self.add_widget(uix_classes.Label_with_tr(text_source=["Звёзды за победу в партии", "Stars for winning"], 
                                                      size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                      font_size = sizes.NAST_SIZE))    
            
            self.lab_can_get_stars = Label(text = icon_func.add_star_icon(string = str(common_data.my_game.My_Country.stars+common_data.my_game.My_disease.level-2), 
                                                                                       size = sizes.NAST_SIZE), 
                                                        size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                        font_size = sizes.NAST_SIZE, markup = True)
            self.add_widget(self.lab_can_get_stars)
        
        
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Золотовалютные\nрезервы", "Gold Exchange\nReserves"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.str_of_reserves = Label(text = icon_func.add_money_icon(string = str(common_data.my_stats.goldreserves), 
                                                                                  size = sizes.NAST_SIZE), 
                                                  size_hint = [1, .3], markup = True, font_size = sizes.NAST_SIZE)
        
        self.add_widget(self.str_of_reserves)        
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["Статус Благосостояния", "Wealth status"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.lab_status_of_rich = uix_classes.Label_with_tr(text_source = common_var.statuses_coins[common_data.my_stats.level_coins], 
                                                            size_hint = [1, None], height = sizes.Height_of_screen/5,
                                                            font_size = sizes.NAST_SIZE, halign = 'center')
        self.add_widget(self.lab_status_of_rich)      
        
        self.add_widget(uix_classes.Label_with_tr(text_source = ["До следующего\nстатуса благосостояния", "For next wealth status"], 
                                                  size_hint = [1, None], height = sizes.Height_of_screen/5, 
                                                  font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.lab_need_coins_for_next_status = Label(text = icon_func.add_money_icon(string = str(common_var.need_c), 
                                                                                                 size = sizes.NAST_SIZE), 
                                                                 size_hint = [.35, None], height = sizes.Height_of_screen/5, 
                                                                 font_size = sizes.NAST_SIZE, markup = True)
        self.need_c.clear_widgets()
        self.need_c.add_widget(self.lab_need_coins_for_next_status) 
        self.add_widget(self.need_c)
        
        self.progress_c = ProgressBar(value = int(common_data.my_stats.goldreserves), 
                                                   max = common_data.my_stats.goldreserves + common_var.need_c, 
                                                   size_hint_x = .57)
        self.progress_c.value = int(common_data.my_stats.goldreserves)
        self.need_c.add_widget(self.progress_c)
        
        
        
        self.label_change_lang = uix_classes.Label_with_tr(text_source = ["Текущий язык", "Language"], 
                                                           size_hint = [1, None], height = sizes.Height_of_screen/3, 
                                                           font_size = sizes.NAST_SIZE, halign = 'center')
        self.add_widget(self.label_change_lang)
        
        self.choose_langs = lang_checkbox.checkbox_for_langs()
        self.add_widget(self.choose_langs)
        
        if type_of_nast  == "game_nast":
            self.btn_redraw = uix_classes.Button_with_image(text_source = ["Карту по центру", "Center country map"], on_press = self.Redraw, 
                                                            size_hint = [1, None],  height = sizes.Height_of_screen/6, 
                                                            font_size = sizes.NAST_SIZE, halign = 'center')
            self.add_widget(self.btn_redraw) 
        
        
        if type_of_nast == "common_stats":
            self.add_widget(uix_classes.Button_with_image(text_source = ["Закрыть статистику", "Close stats"], 
                                                          on_press = self.close_nast,
                                                          size_hint_y = None, height = sizes.Height_of_screen/6, 
                                                          font_size = sizes.NAST_SIZE, halign = 'center'))
        
        self.btn_close_game = uix_classes.Button_with_image(text_source = ["Выйти из игры", "Exit the app"], on_press = self.do_you_want_to_exit, 
                                                    size_hint_y = None, height = sizes.Height_of_screen/6, 
                                                    font_size = sizes.NAST_SIZE, halign = 'center')
        self.add_widget(self.btn_close_game)               
        
        
              
        
    
    def update_stats_after_end_of_the_game (self):
        self.lab_number_of_games.text = str(common_data.my_stats.number_of_games)
        
        self.lab_percent_of_v.text = common_data.str_percent_of_v[common_var.lang]
        self.lab_percent_of_v.text_source = common_data.str_percent_of_v
        
        self.str_of_reserves.text = icon_func.add_money_icon(string = str(common_data.my_stats.goldreserves), 
                                                             size = self.str_of_reserves.font_size)
        
        self.lab_need_coins_for_next_status.text = icon_func.add_money_icon(string = str(common_var.need_c),
                                                                            size = self.lab_need_coins_for_next_status.font_size)
        self.progress_c.value = int(common_data.my_stats.goldreserves) 
        self.progress_c.max = common_data.my_stats.goldreserves + common_var.need_c
        
        self.lab_status_of_rich.text_cource = common_var.statuses_coins[common_data.my_stats.level_coins]
        self.lab_status_of_rich.text = common_var.statuses_coins[common_data.my_stats.level_coins][common_var.lang]
    
             
            
        self.progress_s.value = int(common_data.my_stats.stars) 
        self.progress_s.max = common_data.my_stats.stars + common_var.need_s  
        
        self.lab_need_for_s.text = icon_func.add_star_icon(string = str(common_var.need_s), size = self.lab_need_for_s.font_size)
        
        self.lab_status_of_rep.text_cource = common_var.statuses_stars[common_data.my_stats.level_stars]
        self.lab_status_of_rep.text = common_var.statuses_stars[common_data.my_stats.level_stars][common_var.lang]
        self.lab_quant_of_stars.text = icon_func.add_star_icon(string = str(common_data.my_stats.stars), 
                                                               size =  self.lab_quant_of_stars.font_size)       
        
    def do_you_want_to_exit (self, instance):
        
        widget_of_common_par.Ask_start = widget_of_common_par.Ask_pannel()
        if common_var.is_game_running == "gaming":
            
            if common_var.lang == 0:
                widget_of_common_par.Ask_start.open_ask_pannel(messages=["Вы хотите выйти из приложения?\n", "Если вы это сделаете,\n то эта партия сохранится."], texture = textures.texture_questions, color_texture = (1,1,1,.6))
            if common_var.lang == 1:
                widget_of_common_par.Ask_start.open_ask_pannel(messages=["Do you want to exit the app?\n", "All will be ok, this game will be saved"], texture = textures.texture_questions, color_texture = (1,1,1,.6))
            
            btn_yes = Button(text = (["Выйти из\nприложения", "Exit\nthe app"][common_var.lang]), 
                            size_hint = (.3*widget_of_common_par.Ask_start.size_zone[0]/sizes.Width_of_screen, .17*widget_of_common_par.Ask_start.size_zone[1]/sizes.Height_of_screen), 
                            pos=(widget_of_common_par.Ask_start.left_edge_pos[0]+widget_of_common_par.Ask_start.size_zone[0]*0.6, widget_of_common_par.Ask_start.left_edge_pos[1]+ widget_of_common_par.Ask_start.size_zone[1]*0.25),                            
                            font_size = sizes.ASK_SIZE, on_press = self.finish_all,
                            background_color = [1, 0, 0, 1], halign = 'center')
                        
            widget_of_common_par.Ask_start.add_widget(btn_yes)
        
            btn_no = Button(text= (["Вернуться\nв игру", "Back to\nthe game"][common_var.lang]), 
                            size_hint = (.3*widget_of_common_par.Ask_start.size_zone[0]/sizes.Width_of_screen, .17*widget_of_common_par.Ask_start.size_zone[1]/sizes.Height_of_screen), 
                            pos=(widget_of_common_par.Ask_start.left_edge_pos[0]+widget_of_common_par.Ask_start.size_zone[0]*0.1, widget_of_common_par.Ask_start.left_edge_pos[1]+ widget_of_common_par.Ask_start.size_zone[1]*0.25),                                                        
                            font_size = sizes.ASK_SIZE, on_press = widget_of_common_par.Ask_start.close_ask_pannel,
                            background_color = [0, 1, 0, 1], halign = 'center')
            widget_of_common_par.Ask_start.add_widget(btn_no) 
            widget_of_common_par.Ask_start.remove_widget(widget_of_common_par.Ask_start.btn_ask_close)
        else:
            self.finish_all(instance=5)
 
    def close_nast (self, instance):
        common_data.final_layout.remove_widget(self.parent)
        for i in self.outer_folders:
            common_data.final_layout.add_widget(i)
        
    def finish_all(self, instance):
        common_data.my_game.was_playing_before = True
        
        mes = ["До встречи в новой игре!", "Goodbye for next game!"] 
        widget_of_common_par.inform_about_error(mes[common_var.lang], 'good', t = 1.5)
        
        Clock.schedule_once(common_data.close_game, 0.7)
        
    def Redraw (self, instance):
        common_data.s2.scale = .5
        common_data.s2.pos = (sizes.start_s2_pos_x + sizes.Width_of_screen*common_data.my_game_frontend.left_pannel.table.size_hint_x, 0) 
        mes = ["Карта страны в центральном положении", "Country map is centered"]
        widget_of_common_par.inform_about_error(mes[common_var.lang], 'good', 3)
    
    def draw_redraw_real_country_sizes(self, instance, value):
        if True:
            common_data.s2.scale = .43
            common_data.s2.pos = (sizes.start_s2_pos_x*2 + sizes.Width_of_screen*common_data.my_game_frontend.left_pannel.table.size_hint_x, sizes.Height_of_screen/20) 
            print("draw real sizes")
            draw_for_epidemy.redraw_undraw_real_sizes()
            common_data.my_stats.save_to_file()
            
    def operate_unlocked_methods (self, instance, value):
        common_data.my_stats.are_shown_unlocked_methods = not common_data.my_stats.are_shown_unlocked_methods
        common_data.my_stats.save_to_file()
        for j in range(common_var.QUANT_OF_TECH):
            i = common_var.tech_order[j]
            init_of_tech.init_tech_card(i)
            
        print("operated")
                    
    def Set_volume(self, value, instance):
        if True:
            common_data.my_stats.volume_of_music = self.volume_ind.value 
            music_module.sound.volume = self.volume_ind.value     
        
    def increase_money(self, instance):
        gold_transaction.create_gold_menu()

   
    def open_nast(self, instance):
        self.outer_folders = []
        for i in common_data.final_layout.children:
            self.outer_folders.append(i)
        common_data.final_layout.clear_widgets()
        common_data.final_layout.add_widget(self.parent) 
        
        for i in range (common_var.NUM_OF_LANGS):
            self.choose_langs.check_boxes_for_lang[i].active = False
        self.choose_langs.check_boxes_for_lang[common_var.lang].active = True
        self.volume_ind.value = common_data.my_stats.volume_of_music
        
    
        
#common nasts are for game
common_nast = ScrollView(pos = (sizes.Width_of_screen*0.08, sizes.Height_of_screen*0.05), size_hint=(.84, .9), do_scroll_x=False, 
                                      bar_color = [.35, .35, .25, 1], bar_width = 15, scroll_type = ['bars', 'content'])
nast = Additional_Menu(size_hint = (.9, None), pos = (sizes.Width_of_screen*0.9, sizes.Height_of_screen*0.1))
nast.bind(minimum_height=nast.setter('height'))
common_nast.add_widget(nast)