import checkboxer
import common_data as cd
import common_var
import game_modes
import info_layouts
import sizes
import uix_classes
import widget_of_common_par


list_of_aval_modes = []

common_var.Current_mode = game_modes.numbers_in_menu[common_var.lang][0].name[common_var.lang]

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class Mode_choiser_layout(FloatLayout):
    def __init__(self, **kwargs): 
        super(Mode_choiser_layout, self).__init__(**kwargs) 
    @staticmethod
    def update_mode_menu():
        global list_of_aval_modes
        list_of_aval_modes = []
        #common_var.num_of_lands = 0
        
        for i in game_modes.numbers_in_menu[common_var.lang]:
           
            if cd.stats.stars >= i.min_rep_stars and cd.stats.goldreserves >= i.min_goldreserves:
                list_of_aval_modes.append(i)
                
    def open_layout(self, instance=None):
        self.update_mode_menu()       
        self.outer_folders = []
        for i in cd.final_layout.children:
            self.outer_folders.append(i)
        
        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(self)         
        
        self.lab_choose = uix_classes.Label_with_tr(text_source=["Выберите режим игры:", 
                                                               "Choose the game mode:"], size_hint = (.35, .1), pos_hint = {'left': .95, 'top':.99}, 
                                      font_size = (sizes.width_res/50), halign = 'left')
        #self.lab_choose.bind(size=self.lab_choose.setter('text_size'))  
        self.add_widget(self.lab_choose)
        
        self.checkbox = checkboxer.Universal_CheckBox(type = "mode", 
                                                      item_list = list_of_aval_modes, text_size = sizes.width_res/50,
                                                      size_hint = [.7, .8], pos_hint = {"center_x": .36,  'center_y': 0.45})
        self.add_widget(self.checkbox)   
        
        self.btn_confirm = uix_classes.Button_with_image(text_source = ["Начать игру!", "Start the game!"], size_hint_x = None, width = sizes.width_res/4.5, size_hint_y = .15,
                                             pos_hint = {"center_x": .83,  'center_y': .5}, font_size = (sizes.width_res/55))
        
        self.add_widget(self.btn_confirm)
        
    
        
        self.btn_modes_info = uix_classes.Button_with_image(text_source = ["Информация\nо режимах", "Modes info"], size_hint_x = None, size_hint_y = .15, width = sizes.width_res / 4.5,
                                           pos_hint = {'center_x': .83, 'center_y': .85}, font_size = (sizes.width_res/55))
        self.btn_modes_info.bind(on_press = info_layouts.modes_info_pannel.open_manual)
        self.add_widget(self.btn_modes_info)
        
        self.btn_return_to_start_page = uix_classes.Button_with_image(text_source=["Выйти в главное меню", "Exit to main menu"], size_hint_x = None, size_hint_y = .15, 
                                                                       width = sizes.width_res / 4.5,
                                           pos_hint = {'center_x': .83, 'center_y': .15}, font_size = (sizes.width_res/55))
        self.btn_return_to_start_page.bind(on_press=self.close_layout)        
        
        self.add_widget(self.btn_return_to_start_page)
        common_var.Current_mode = list_of_aval_modes[0].name[common_var.lang]
        
    def close_layout(self, instance):
        cd.final_layout.remove_widget(self)
        for i in self.outer_folders:
            cd.final_layout.add_widget(i)
        print("Choicer closed")
        
        if widget_of_common_par.opened_ask_panel != None:
            widget_of_common_par.opened_ask_panel.close_ask_panel(instance=5)
            
        App.get_running_app().close_game_space(instance=5)
        
        for i in self.children:
            del i
        del self
            
        



