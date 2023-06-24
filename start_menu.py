import os.path
import random

import common_data
import common_var
import e_settings
import interact_rules
import sizes
import textures
import uix_classes
import widget_of_common_par

menu_size = round(sizes.Width_of_screen/40)
from kivy.animation import Animation, AnimationTransition
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView

from kivy.lang import Builder
Builder.load_string('''                               
<RotatingImage2>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix
''')

'''
class RotatingImage(Image):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        import random
        super(RotatingImage, self).__init__(**kwargs)
        transition_variants = ['in_back', 'in_bounce', 'in_circ', 'in_cubic', 
                               'in_elastic', 'in_expo',
                               'in_out_back', 'in_out_bounce', 'in_out_circ', 'in_out_cubic',
                               'in_out_elastic', 'in_out_expo',
                               'in_out_quad', 'in_out_elastic']
        
        anim = Animation()
        self.rotating_by_clock =  Animation(angle = -360, duration=4, transition = random.choice(transition_variants))
        anim+=self.rotating_by_clock
        self.moving_right = Animation(pos = [self.pos[0] + 0.25*sizes.Width_of_screen, self.pos[1]], 
                                      duration = 7, transition = random.choice(transition_variants))
        anim&=self.moving_right
        self.rotating_counter_clock = Animation(angle = 360, duration=4, transition = random.choice(transition_variants))
        self.moving_left = Animation(pos = [self.pos[0] - 0.25*sizes.Width_of_screen, self.pos[1]], duration = 7,
                                     transition = random.choice(transition_variants))
        anim += (self.rotating_counter_clock&self.moving_left)
        
        anim.repeat = True
        anim.start(self)
    

    def on_angle(self, item, angle):
        if angle == 360 or angle == -360:
            item.angle = 0            
 '''   
       
class RotatingImage2(Image):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
       
        
        super(RotatingImage2, self).__init__(**kwargs)
        self.transition_variants = ['in_back', 'in_bounce', 'in_circ', 'in_cubic', 
                               'in_elastic', 'in_expo',
                               'in_out_back', 'in_out_bounce', 'in_out_circ', 'in_out_cubic',
                               'in_out_elastic', 'in_out_expo',
                               'in_out_quad', 'in_out_elastic']
        
        self.start_pos = (self.pos[0], self.pos[1])
        #self.list_of_anim = []
        self.is_animating = True
        self.generate_rotating_transition(instance=0, animation=0)
        self.generate_horizontal_moving(instance=0, animation=0)
        self.generate_vertical_moving(instance=0, animation=0)
    def on_angle(self, item, angle):
        if angle == 360 or angle == -360:
            item.angle = 0
    def generate_horizontal_moving(self, instance, animation):
        self.anim_moving_hor = Animation()
        
        
        self.moving_right = Animation(x = self.start_pos[0] + 0.6*random.uniform(0.6, 1.4)*sizes.Width_of_screen, 
                                      duration = random.randint(8, 12), transition = random.choice(self.transition_variants))
        self.anim_moving_hor+=self.moving_right
        
        
        self.moving_left = Animation(x = self.start_pos[0] - 0.11*random.uniform(0.6, 1.4)*sizes.Width_of_screen, duration = random.randint(6, 10),
                                     transition = random.choice(self.transition_variants))
        self.anim_moving_hor += (self.moving_left)
        
        self.anim_moving_hor.repeat = True
        #self.list_of_anim.append(self.anim_moving_hor)
        self.anim_moving_hor.start(self)
    def generate_vertical_moving(self, instance, animation):
        self.anim_moving_ver = Animation()
        
        
        self.moving_down = Animation(y = self.start_pos[1]+ 0.12*random.uniform(0.6, 1.4)*sizes.Height_of_screen, 
                                      duration = random.randint(6, 10), transition = random.choice(self.transition_variants))
        self.anim_moving_ver+=self.moving_down
        
        
        self.moving_up = Animation(y = self.start_pos[1]- 0.5*random.uniform(0.6, 1.4)*sizes.Height_of_screen, duration = random.randint(9, 12),
                                     transition = random.choice(self.transition_variants))
        self.anim_moving_ver += (self.moving_up)
        
        self.anim_moving_ver.repeat = False
        self.anim_moving_ver.bind(on_complete=self.generate_vertical_moving)
        #self.list_of_anim.append(self.anim_moving_ver)
        self.anim_moving_ver.start(self)  
        
        
    def generate_rotating_transition(self, instance, animation):

        self.anim_rotating = Animation()
        
        self.rotating_by_clock =  Animation(angle = -360, duration=random.randint(3, 5), transition = random.choice(self.transition_variants))
        self.anim_rotating+=self.rotating_by_clock
        
        self.rotating_counter_clock = Animation(angle = 360, duration=random.randint(3, 5), transition = random.choice(self.transition_variants))
        self.anim_rotating += self.rotating_counter_clock
        
        self.anim_rotating.repeat = False
        self.anim_rotating.bind(on_complete=self.generate_rotating_transition)
        #self.list_of_anim.append(self.anim_rotating)
        self.anim_rotating.start(self)

class Start_Menu(FloatLayout):
    def __init__(self, **kwargs): 
        super(Start_Menu, self).__init__(**kwargs)   
    
    def filling(self):
        
        self.stats_pannel = ScrollView(pos = (sizes.Width_of_screen*0.08, sizes.Height_of_screen*0.05), size_hint=(.84, .9), do_scroll_x=False, bar_color = [.35, .35, .25, 1], bar_width = 15, 
                                       scroll_type = ['bars', 'content'])
        self.stats_pannel_in = e_settings.Additional_Menu(size_hint = (.9, None), pos = (sizes.Width_of_screen*0.1, sizes.Height_of_screen*0.1), 
                                                          type_of_nast="common_stats")
        
        self.stats_pannel_in.bind(minimum_height=self.stats_pannel_in.setter('height'))
        self.stats_pannel.add_widget(self.stats_pannel_in)        
        
        hi_text = ['Добро пожаловать в мир "Эпидемии"!', 'Welcome to the world of "Epidemy"!']
        today = common_data.datetime.date.today()
        
        if (today.weekday() == 6 and today.day > 14 and today.day < 22) or today.weekday() == 0:
            common_var.IS_PREMIUM = True
            hi_text = ["Сегодня день без рекламы!", 
                       "Today is day without ads!"]
            
        elif today.weekday() == 6\
             or (today.weekday() == 5 and today.day > 13 and today.day < 21):
            hi_text = ["Завтра будет день без рекламы!", 
                       "Tomorrow is no-ads day of Epidemy!"]
        
        self.hi_label = uix_classes.Label_with_tr(text_source=hi_text, size_hint = (1, .1), 
                                                  font_size = menu_size, pos = (sizes.Width_of_screen*0, sizes.Height_of_screen*.87), markup = True)        
        self.add_widget(self.hi_label)                  
        self.button_start_game = uix_classes.Button_with_image(text_source=["Играть!", "Start gaming!"], size_hint = (.25, .3), 
                                                   font_size = menu_size, pos = (sizes.Width_of_screen*0.05, sizes.Height_of_screen*0.1), on_press = start_gaming)
        self.add_widget(self.button_start_game)
        
        
        self.button_open_stats = uix_classes.Button_with_image(text_source=["Моя статистика", "My statistics"], size_hint = (.25, .3), 
                                                   font_size = menu_size, 
                                                   pos = (sizes.Width_of_screen*0.35, sizes.Height_of_screen*0.3),
                                                   on_press = self.open_stats)
        self.add_widget(self.button_open_stats)
        
        self.button_open_manual = uix_classes.Button_with_image(text_source=["Правила игры", "Game guide"], size_hint = (.25, .3), 
                                                   font_size = menu_size, 
                                                   pos = (sizes.Width_of_screen*0.65, sizes.Height_of_screen*0.5),
                                                   on_press = self.open_manual)
        self.add_widget(self.button_open_manual)
        
        self.covid_image = RotatingImage2(source = "different_images/covid.png", pos = (sizes.Width_of_screen*0.1, sizes.Height_of_screen*0.6), 
                              size_hint = (.1, .2))
        self.add_widget(self.covid_image)
        
        
    def open_stats(self, instance):
        self.stats_pannel_in.open_nast(instance=1)
        
    def open_manual(self, instance):
        interact_rules.rp.open_self(instance=0)  
        
def start_gaming(instance):
    
    Animation.cancel_all(Main_menu.covid_image)
    Main_menu.covid_image.is_animating = False
    
    if common_data.my_stats.possible_of_continue_game == True and os.path.isfile("game_exemplar_data.pkl") == False:#if game-containing file was lost
        common_data.my_stats.possible_of_continue_game = False 
    
    if common_data.my_stats.possible_of_continue_game == False:
        App.get_running_app().choosing_of_disease(instance=4)
    else:
        
        file_prev_game = open('game_exemplar_data.pkl', 'rb')
        
        last_game = common_data.pickle.load(file_prev_game)
        str_game_description = ['Вы боролись с ' + last_game.My_disease.padezhi[4] + ' в ' + last_game.My_Country.pp_name + '.',
                                'You were coping with ' + last_game.My_disease.small_name[1] + ' in ' + last_game.My_Country.name[1] + '.']
        
        file_prev_game.close()
        
        pannel = widget_of_common_par.Ask_pannel()
        pannel.open_ask_pannel(messages = [[str_game_description[0],'',
                                            "Вы хотите продолжить предыдущую", 
                                            "партию или начать новую?"], 
                                           [str_game_description[1], '',
                                            "Do you want to continue previous game", 
                                            "or start new one?"]][common_var.lang], 
                               texture=textures.texture_questions, color_texture=(1, 1, 1, .6))
  
        
        
        widget_of_common_par.opened_ask_pannel_is.btn_new = Button(text = (["Начать\nновую игру", "Start new game"][common_var.lang]), 
                                              size_hint = (.3*widget_of_common_par.opened_ask_pannel_is.size_zone[0]/sizes.Width_of_screen, .16*widget_of_common_par.opened_ask_pannel_is.size_zone[1]/sizes.Height_of_screen), 
                                              pos=(widget_of_common_par.opened_ask_pannel_is.left_edge_pos[0]+widget_of_common_par.opened_ask_pannel_is.size_zone[0]*0.6, widget_of_common_par.opened_ask_pannel_is.left_edge_pos[1]+ widget_of_common_par.opened_ask_pannel_is.size_zone[1]*0.3),                                              
                                              font_size = sizes.ASK_SIZE, 
                                              on_press = App.get_running_app().choosing_of_disease, halign = 'center',
                                              background_color = [1, 0, 0, 1])
                
        widget_of_common_par.opened_ask_pannel_is.add_widget(widget_of_common_par.opened_ask_pannel_is.btn_new)
        
        widget_of_common_par.opened_ask_pannel_is.btn_prev = Button(text= (["Продолжить\nстарую", "Continue previous"][common_var.lang]), 
                                              size_hint = (.3*widget_of_common_par.opened_ask_pannel_is.size_zone[0]/sizes.Width_of_screen, .16*widget_of_common_par.opened_ask_pannel_is.size_zone[1]/sizes.Height_of_screen), 
                                              pos=(widget_of_common_par.opened_ask_pannel_is.left_edge_pos[0]+widget_of_common_par.opened_ask_pannel_is.size_zone[0]*0.1, widget_of_common_par.opened_ask_pannel_is.left_edge_pos[1]+ widget_of_common_par.opened_ask_pannel_is.size_zone[1]*0.3),                                                                                            
                                              font_size = sizes.ASK_SIZE, 
                                              on_press = App.get_running_app().continue_saved_game, halign = 'center',
                                              background_color = [0, 1, 0, 1])
        
        widget_of_common_par.opened_ask_pannel_is.add_widget(widget_of_common_par.opened_ask_pannel_is.btn_prev)

Main_menu = Start_Menu()