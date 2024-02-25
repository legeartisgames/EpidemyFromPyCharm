import checkboxer
import common_data as cd
import common_var
import country_variants
import frases
import info_layouts
import sizes
import uix_classes
import widget_of_common_par


list_of_all_countries=[]
aval_state_countries = []
fir_av = 0

common_var.Current_country = country_variants.numbers_in_menu[common_var.lang][0].name[common_var.lang]

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class Country_choiser_layout(FloatLayout):
    def __init__(self, **kwargs): 
        super(Country_choiser_layout, self).__init__(**kwargs) 
    @staticmethod
    def update_country_menu():
        global list_of_all_countries, aval_state_countries, fir_av
        list_of_all_countries = []
        aval_state_countries = []      
        common_var.num_of_lands = 0
        
        for i in country_variants.numbers_in_menu[common_var.lang]:
            list_of_all_countries.append(i)
            if cd.stats.stars >= i.min_rep_stars and cd.stats.goldreserves >= i.min_goldreserves:
                common_var.num_of_lands+=1
                aval_state_countries.append(True)
            else:
                if cd.stats.stars < i.min_rep_stars:
                    aval_state_countries.append([False, 'stars', - cd.stats.stars + i.min_rep_stars])
                else:
                    aval_state_countries.append([False, 'coins', - cd.stats.goldreserves + i.min_goldreserves])
                    
        for i in range(len(aval_state_countries)):
            if aval_state_countries[i] == True:
                fir_av = i
                break        
                
    def open_layout(self, instance=None):
        self.update_country_menu()       
        self.outer_folders = []
        for i in cd.final_layout.children:
            self.outer_folders.append(i)
        
        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(self)         
        
        self.add_widget(uix_classes.Label_with_tr(text_source=["Выберите страну, за которую будете играть:", "Choose the country to play with:"], 
                                                  size_hint = (.5, .1), pos_hint = {'left':.95, 'top':.95}, 
                                                  font_size = (sizes.width_res/53)))
        
        self.checkbox = checkboxer.Universal_CheckBox(type = "country", item_list = list_of_all_countries, availabilites = aval_state_countries, 
                                                      fir_av=fir_av, size_hint = [.7, .7], pos_hint = {"center_x": .36,  'center_y': .47})
        self.add_widget(self.checkbox)   
        
        self.btn_remake_country = uix_classes.Button_with_image(text_source = ["Подтвердить выбор", "Confirm choice"], size_hint_x = None, width = sizes.width_res/4.5, size_hint_y = .15,
                                             pos_hint = {"center_x": .83,  'center_y': .5}, font_size = (sizes.width_res/55))
        
        self.add_widget(self.btn_remake_country)
        
    
        
        self.btn_country_info = uix_classes.Button_with_image(text_source=frases.str_open_country_info, size_hint_x = None, size_hint_y = .15, width = sizes.width_res / 4.5,
                                           pos_hint = {'center_x': .83, 'center_y': .85}, font_size = (sizes.width_res/55))
        self.btn_country_info.bind(on_press = info_layouts.country_info_pannel.open_manual)
        self.add_widget(self.btn_country_info)
        
        self.btn_return_to_start_page = uix_classes.Button_with_image(text_source=["Выйти в главное меню", "Exit to main menu"], size_hint_x = None, size_hint_y = .15, 
                                                                       width = sizes.width_res / 4.5,
                                           pos_hint = {'center_x': .83, 'center_y': .15}, font_size = (sizes.width_res/55))
        self.btn_return_to_start_page.bind(on_press=self.close_layout)        
        
        self.add_widget(self.btn_return_to_start_page)
        common_var.Current_country = list_of_all_countries[fir_av].name[common_var.lang]
        
    def close_layout(self, instance):
        cd.final_layout.remove_widget(self)
        for i in self.outer_folders:
            cd.final_layout.add_widget(i)
        print("Country choicer was closed")
        
        if widget_of_common_par.opened_ask_panel != None:
            widget_of_common_par.opened_ask_panel.close_ask_panel(instance=5)
            
        App.get_running_app().close_game_space(instance=5)
        
        for i in self.children:
            del i
        del self
            
        



