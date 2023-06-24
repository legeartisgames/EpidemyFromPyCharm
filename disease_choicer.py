import checkboxer
import common_data
import common_var
import diseases
import info_layouts
import sizes
import uix_classes
import widget_of_common_par


list_of_all_diseases = []
avail_state_diseases = []
fir_av = 0
common_var.Current_dis = diseases.numbers_in_menu[common_var.lang][0].name[common_var.lang]

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class Disease_choiser_layout(FloatLayout):
    def __init__(self, **kwargs): 
        super(Disease_choiser_layout, self).__init__(**kwargs) 
    @staticmethod
    def update_disease_menu():
        global list_of_all_diseases, aval_state_diseases, fir_av
        list_of_all_diseases = []
        aval_state_diseases = []
        common_var.num_of_dis = 0
        
        for i in diseases.numbers_in_menu[common_var.lang]:
            list_of_all_diseases.append(i)
            if common_data.my_stats.goldreserves >= i.min_gold:
                common_var.num_of_dis+=1
                avail_state_diseases.append(True)
            else:
                if common_data.my_stats.goldreserves < i.min_gold:
                    avail_state_diseases.append([False, 'coins', - common_data.my_stats.goldreserves + i.min_gold])
            
            for i in range(len(avail_state_diseases)):
                if avail_state_diseases[i] == True:
                    fir_av = i
                    break        

                
    def open_layout(self, instance):
        self.update_disease_menu()       
        self.outer_folders = []
        for i in common_data.final_layout.children:
            self.outer_folders.append(i)
        
        common_data.final_layout.clear_widgets()
        common_data.final_layout.add_widget(self)         
        
        self.add_widget(uix_classes.Label_with_tr(text_source=["Выберите инфекцию, с которой будете бороться:", 
                                                               "Choose the disease to play against:"], size_hint = (.5, .1), pos_hint = {'left':.95, 'top':.95}, 
                                      font_size = (sizes.Width_of_screen/50)))
        
        self.checkbox = checkboxer.Universal_CheckBox(type = "disease", 
                                                      item_list = list_of_all_diseases, availabilites = avail_state_diseases, fir_av = fir_av,
                                                      text_size = sizes.Width_of_screen/50,
                                                      size_hint = [.7, .7], pos_hint = {"center_x": .36,  'top': 0.8})
        self.add_widget(self.checkbox)   
        
        self.btn_confirm = uix_classes.Button_with_image(text_source = ["Подтвердить выбор", "Confirm choice"], size_hint_x = None, width = sizes.Width_of_screen/4.5, size_hint_y = .15, 
                                             pos_hint = {"center_x": .83,  'center_y': .5}, font_size = (sizes.Width_of_screen/55))
        
        self.add_widget(self.btn_confirm)
        
    
        
        self.btn_country_info = uix_classes.Button_with_image(text_source = ["Информация\nоб инфекциях", "Diseases info"], size_hint_x = None, size_hint_y = .15, width = sizes.Width_of_screen / 4.5, 
                                           pos_hint = {'center_x': .83, 'center_y': .85}, font_size = (sizes.Width_of_screen/55))        
        self.btn_country_info.bind(on_press = info_layouts.diseases_info_pannel.open_manual)
        self.add_widget(self.btn_country_info)
        
        self.btn_return_to_start_page = uix_classes.Button_with_image(text_source=["Выйти в главное меню", "Exit to main menu"], size_hint_x = None, size_hint_y = .15, 
                                                                       width = sizes.Width_of_screen / 4.5, 
                                           pos_hint = {'center_x': .83, 'center_y': .15}, font_size = (sizes.Width_of_screen/55))        
        self.btn_return_to_start_page.bind(on_press=self.close_layout)        
        
        self.add_widget(self.btn_return_to_start_page)
        common_var.Current_dis = list_of_all_diseases[fir_av].name[common_var.lang]
        
    def close_layout(self, instance):
        common_data.final_layout.remove_widget(self)
        for i in self.outer_folders:
            common_data.final_layout.add_widget(i)
        print("Disease choicer was closed")
        
        if widget_of_common_par.opened_ask_pannel_is != None:
            widget_of_common_par.opened_ask_pannel_is.close_ask_pannel(instance=5)
            
        App.get_running_app().close_game_space(instance=5)
        
        for i in self.children:
            del i
        del self    
        



