
import common_data
import common_func
import common_var

import frases
import icon_func
import sizes
import spec_func
import tech_info
import text_for_tech_generator
import tech_sm
import uix_classes
import widget_of_common_par

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

class SpecialLabel(uix_classes.WrappedLabel, Widget):
    def __init__(self, index_of_current_tech, **kwargs):
        super(SpecialLabel, self).__init__(**kwargs)
          
        self.index_of_current_tech = index_of_current_tech
        self.update_text()
        common_var.list_of_btns.append(self)
        
    def update_text(self, do_generate = False):
        if do_generate:
            text_for_tech_generator.generate_texts_for_tech()
        self.text_source = [text_for_tech_generator.texts_of_tech[self.index_of_current_tech][0],
                            text_for_tech_generator.texts_of_tech[self.index_of_current_tech][1]]        
        self.text_source = [icon_func.letter_to_icons_increasing_size(size= size_of_name_of_tech, coef = 1.6, string = self.text_source[0]), 
                            icon_func.letter_to_icons_increasing_size(size= size_of_name_of_tech, coef = 1.6, string = self.text_source[1])]
        
        self.text = self.text_source[common_var.lang]   
        
size_of_name_of_tech = round(21/15*0.013*sizes.Width_of_screen*common_var.K)
size_of_button_of_tech = round(13/15*0.013*sizes.Width_of_screen*common_var.K)

class Widget_of_tech(FloatLayout):
    def __init__(self, index_of_current_tech, **kwargs):
        super(Widget_of_tech, self).__init__(**kwargs)
        self.real_init(index_of_current_tech)
    def reinit(self):
        
        self.canvas.before.remove(self.rect_wid)
        self.canvas.before.remove(self.rect_wid_card)
        self.clear_widgets()
        self.real_init(self.index_of_current_tech)
        
    def real_init(self, index_of_current_tech):
        self.index_of_current_tech = index_of_current_tech
        i = self.index_of_current_tech
        if common_data.my_stats.goldreserves >= tech_info.min_goldreserves_for_tech[i] and\
            common_data.my_stats.stars >= tech_info.min_stars_for_tech[i]:
            self.is_avaliable = True
        else:
            self.is_avaliable = False
        if common_data.my_game.My_mode.index == 5:#режим "с нуля"
            if self.index_of_current_tech in {10, 11, 26}:
                self.is_avaliable = True
            else:
                self.is_avaliable = 'no in mode lack of methods'
                
        if common_data.my_game.is_tech_avaliable[self.index_of_current_tech] == None:
            common_data.my_game.is_tech_avaliable[self.index_of_current_tech] = self.is_avaliable
            
        else:
            self.is_avaliable = common_data.my_game.is_tech_avaliable[self.index_of_current_tech]
            
        
        
        if self.index_of_current_tech == 0:
            text_for_tech_generator.generate_texts_for_tech()
            
        self.rect_wid_card = None
        self.rect_wid = None
        
        self.pm_buttons = [None, None]
        self.str_of_input_for_tech = ['']*common_var.QUANT_OF_TECH #для активации технологии за монетки, первый элемент - вывеска, второй - окно ввода, третий - кнопка применения эффекта
        for i in range(common_var.QUANT_OF_TECH):
            self.str_of_input_for_tech[i] = [0, 0, 0]
        tech_name = tech_info.names_of_tech[self.index_of_current_tech]
        if common_data.my_game.My_Country.index == 12 and self.index_of_current_tech == 3:#if Germany
            tech_name = ["Респираторы", "Respirators"]
        str_font_on = ['[font=fonts/Tahoma.ttf]', '[font=fonts/MuseoSlab.ttf]'][common_var.lang]
        self.label_name_of_tech = uix_classes.WrappedLabel_with_tr(text_source=['[b]'+'[size='+str(size_of_name_of_tech)+']' + str_font_on + tech_name[0]+'[/font]'+'[/b]'+ '\n' +'[/size]',
                                                                                '[b]'+'[size='+str(size_of_name_of_tech)+']' + str_font_on + tech_name[1]+ '[/font]'+'[/b]'+ '\n' +'[/size]'],
                                                                   font_size = int(1.2*0.013*sizes.Width_of_screen*common_var.K), 
                                                                   pos_hint={'center_x': .5, 'center_y': .87}, valign = 'center', halign = 'center', size_hint_x = .75,
                                                           markup = True, color = [1, 1, 1, 1])
        self.add_widget(self.label_name_of_tech)
        
        font_size = int(1.2*0.013*sizes.Width_of_screen*common_var.K)
            
        if self.is_avaliable == False:
            i = self.index_of_current_tech
            tags_text = ['[i]Теги метода[/i]: ', '[i]Tags[/i]: ']
            for j in range(len(tech_info.tech_tags[i])):
                if j!=0:
                    tags_text[0]+=', '
                    tags_text[1]+=', '                    
                tags_text[0]+=tech_info.tech_tags[i][j][0]
                tags_text[1]+=tech_info.tech_tags[i][j][1]
                
            self.label_of_tags = uix_classes.WrappedLabel(size_hint=(.9, None),
                    font_size = font_size, 
                    pos_hint={'center_x': .5, 'top': .55}, valign = 'top', halign = 'center', 
                    markup = True, color = [1, 1, 1, 1], text=tags_text[common_var.lang])
            self.label_of_tags.text_source = tags_text
            
            common_var.list_of_btns.append(self.label_of_tags)    
            self.add_widget(self.label_of_tags)
            
            resource_need = '?'
            quant_need = '?'
            if common_data.my_stats.goldreserves < tech_info.min_goldreserves_for_tech[i]:
                resource_need = 'coins'
                quant_need = round(-common_data.my_stats.goldreserves + tech_info.min_goldreserves_for_tech[i])
            if common_data.my_stats.stars < tech_info.min_stars_for_tech[i]:
                resource_need = 'stars'
                quant_need = round(-common_data.my_stats.stars + tech_info.min_stars_for_tech[i], 1)
                
            if quant_need !='?':
                
                text_s = ['[i]До получения[/i] ещё '+str(quant_need)+' ' + resource_need, '[i]Need[/i] extra '+str(quant_need)+' ' + resource_need]
            
                text_s[0] = icon_func.letter_to_icons_increasing_size(size = sizes.Width_of_screen/53, coef = 1.6, string = text_s[0])    
                text_s[1] = icon_func.letter_to_icons_increasing_size(size = sizes.Width_of_screen/53, coef = 1.6, string = text_s[1])    
        
            else:
                text_s = ["В следующей партии этот метод будет разблокирован",
                          "This method will be unlocked in the next game"]
            self.label_need = uix_classes.WrappedLabel(size_hint=(.9, None),
                    font_size = font_size, 
                    pos_hint={'center_x': .5, 'top': .85}, valign = 'top', halign = 'center', 
                    markup = True, color = [1, 1, 1, 1], text=text_s[common_var.lang])
            self.label_need.text_source = text_s
            
            if quant_need == '?':
                self.label_need.pos_hint = {'center_x': .5, 'top': .8}
            
            common_var.list_of_btns.append(self.label_need)    
            self.add_widget(self.label_need)
            
            return
        
        
        self.label_of_tech = SpecialLabel(size_hint=(.9, None),
                font_size = font_size, 
                pos_hint={'center_x': .5, 'top': .83}, valign = 'top', halign = 'center', 
        markup = True, color = [1, 1, 1, 1], index_of_current_tech = self.index_of_current_tech)
        
        self.label_of_tech.outline_color = (1,1,0,1)
            
        self.add_widget(self.label_of_tech)

        self.button_buy = uix_classes.Button_asfalt(
            text_source = frases.str_get_tech,
            size_hint=(.4, .12),
            pos_hint={'right': 0.95, 'top': 0.145},
            on_press = self.Multiply_on_parameter,
            font_size = size_of_button_of_tech)
        
        if tech_info.type_of_get[self.index_of_current_tech] == 1:
            self.button_buy.text = frases.str_research_tech[common_var.lang]
            self.button_buy.text_source = frases.str_research_tech
            self.button_buy.pos_hint={'right': 0.98, 'top': 0.17}
            self.button_buy.size_hint= (.4, .15)
            
        if self.index_of_current_tech in {0, 1, 2, 28, 31}:
            self.button_buy.text_source = frases.str_proinvest
            self.button_buy.text = self.button_buy.text_source[common_var.lang]
            if common_var.lang == 0:
                self.button_buy.size_hint = (.5, .15)
                self.button_buy.pos_hint={'right': 0.98, 'top': 0.17}
            else:
                self.button_buy.size_hint = (.4, .12)
                self.button_buy.pos_hint={'right': 0.96, 'top': 0.14}
            self.button_buy.halign = 'center'
            
       
        self.add_widget(self.button_buy)
        
        if tech_info.possible_of_activation[self.index_of_current_tech] == True\
           and common_data.my_game.is_activated[self.index_of_current_tech] != True:
            
            self.button_of_activation = uix_classes.Button_asfalt(
                text_source=frases.str_activate_tech,
                size_hint=(.42, .15),
                pos_hint={'right': 0.44, 'top': 0.17}, 
                on_press = self.Activate_Deactivate,
                halign = 'center',
                font_size = size_of_button_of_tech)
            
        elif tech_info.possible_of_activation[self.index_of_current_tech] == True\
             and common_data.my_game.is_activated[self.index_of_current_tech] == True:
            
            self.button_of_activation = uix_classes.Button_asfalt(
                text_source=frases.str_deactivate_tech,
                size_hint=(.42, .15),
                pos_hint={'right': 0.44, 'top': 0.17}, 
                on_press = self.Activate_Deactivate,
                halign = 'center',
                font_size = size_of_button_of_tech)
       
        if tech_info.quant_of_buys[self.index_of_current_tech][0] != -1\
           and common_data.my_game.counter_of_buys[self.index_of_current_tech][0] >= 1:
            self.set_btn_to_researched()      
            
            
        if ((tech_info.quant_of_buys[self.index_of_current_tech][0]>common_data.my_game.counter_of_buys[self.index_of_current_tech][0] or tech_info.quant_of_buys[self.index_of_current_tech][0]<=-1) and common_data.my_game.counter_of_buys[self.index_of_current_tech][0] > 0)\
           or common_data.my_game.counter_of_buys[self.index_of_current_tech][1] > 0:
            self.set_done_x_times()
        
        if tech_info.possible_of_activation[self.index_of_current_tech] == True and common_data.my_game.counter_of_buys[self.index_of_current_tech][0] > 0:
            self.add_widget(self.button_of_activation)
        
        self.spec_methods_button_preparing()        
        
    def Activate_Deactivate(self, instance, do_notify = True):
        
        if common_data.my_game.is_activated[self.index_of_current_tech]==True:
            par = common_data.my_game.parameters_of_tech[self.index_of_current_tech]
            answer = ["0"]*4
            answer[0] = par[0]
            answer[1] = par[1]
            if type(par[2][0]) == float or type(par[2][0]) == int:
                if par[2][1] == "*": 
                    answer[2] = [1/par[2][0], "*"]
                elif par[2][1] == "+": 
                    answer[2] = [-par[2][0], "+"]
            else:
                answer[2] = []
                for i in range(len(par[2])):
                    if par[2][i][1] == "*": 
                        answer[2].append([1/par[2][i][0], "*"])
                    elif par[2][i][1] == "+": 
                        answer[2].append([-par[2][i][0], "+"])
            answer[3] = [-par[3][0], "+"]
            common_func.Mult_on_par(answer, self.index_of_current_tech, do_notify = do_notify)
            self.button_of_activation.text_source = frases.str_activate_tech 
            common_data.my_game.is_activated[self.index_of_current_tech] = False
            self.button_of_activation.text= frases.str_activate_tech[common_var.lang]
    
                
        else:
        
            common_func.Mult_on_par(common_data.my_game.parameters_of_tech[self.index_of_current_tech], self.index_of_current_tech, do_notify = do_notify)
            common_data.my_game.is_activated[self.index_of_current_tech] = True
            self.button_of_activation.text_source = frases.str_deactivate_tech

            self.button_of_activation.text = frases.str_deactivate_tech[common_var.lang] 
            
            
            
    def Multiply_on_parameter (self, instance, do_notify = True):
        global size_of_button_of_tech
        
        if common_data.my_game.game_pars.coins + common_data.my_game.prices_of_tech[self.index_of_current_tech][0] >=0: #if we have enough money
            was_counter_of_buys = common_data.my_game.counter_of_buys[self.index_of_current_tech][0]
            
            common_data.my_game.counter_of_buys[self.index_of_current_tech][0] +=1
    
            common_data.my_game.game_pars.coins += (common_data.my_game.prices_of_tech[self.index_of_current_tech][0])
            common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)
                        
            if self.index_of_current_tech == 4: #delay of airlines
                common_data.my_game.parameters_of_tech[4][1] = common_data.my_game.index_of_capital
            
            if self.index_of_current_tech == 9: #science communication
                #update of skidka to vakzine and cure
                x = common_data.my_game.prices_of_tech[10][0]
                coef = common_data.my_game.parameters_of_tech[9][2][1][0]
                common_data.my_game.prices_of_tech[10][0] = round(common_data.my_game.prices_of_tech[10][0]*coef)
                
                x = common_data.my_game.prices_of_tech[11][0]
                common_data.my_game.prices_of_tech[11][0] = round(common_data.my_game.prices_of_tech[11][0]*coef)
                text_for_tech_generator.generate_texts_for_tech()
                common_data.my_game_frontend.wid[10].label_of_tech.update_text()
                common_data.my_game_frontend.wid[11].label_of_tech.update_text()
                
            if (self.index_of_current_tech in {6, 7, 8, 10, 18, 21, 22, 24, 25}) and was_counter_of_buys == 0:
                
               
                if common_data.my_game.list_of_tech_tr[0][0] == "Пока нет методов\nдля региона":
                    del common_data.my_game.list_of_tech_tr[0] #for spinner of technologies 
                name = tech_info.names_of_tech[self.index_of_current_tech]
                if self.index_of_current_tech == 10:
                    name = ["Вакцинация", "Vaccination"]
                common_data.my_game.str_of_probably_activating_tech = name
                
                common_data.my_game.list_of_tech_tr.append(name)
                print("New region method was gotten")
            
            elif self.index_of_current_tech in {15, 16, 17, 26}: #coin emission or goscompany
                print("New economical tech was gotten")
            else:
                common_func.Mult_on_par (common_data.my_game.parameters_of_tech[self.index_of_current_tech], self.index_of_current_tech)
                
            if self.index_of_current_tech == 2: #для инвестиций в науку
                for i in range(common_var.QUANT_OF_TECH):
                    if tech_info.quant_of_buys[i][0] > 0 and common_data.my_game.counter_of_buys[i][0] < tech_info.quant_of_buys[i][0]: #if did't buy, and it isn't investition
                        #we make skidka for tech
                        
                        if i == 10 or i == 11:
            
                            common_data.my_game.prices_of_tech[i][0]+=5*common_data.my_game.coef_skidka_na_tech
                        else:
                            common_data.my_game.prices_of_tech[i][0]+=common_data.my_game.coef_skidka_na_tech
                        if common_data.my_game.prices_of_tech[i][0] > 0: #цена всегда меньше 0, т.к. число монет при покупке падает
                            common_data.my_game.prices_of_tech[i][0] = 0
                        
                text_for_tech_generator.generate_texts_for_tech()
                
                for i in range(common_var.QUANT_OF_TECH):
                    
                    common_data.my_game_frontend.wid[i].label_of_tech.update_text()
                
                
            if tech_info.possible_of_activation[self.index_of_current_tech] == True: # if tech can be activated
                self.set_btn_activate()
            
            if self.index_of_current_tech == 12:
                
                if common_data.my_game.game_pars.date[1] in {6, 7, 8}: #if summer and researched distant 
                    self.Activate_Deactivate(instance=3, do_notify=False)
                    common_data.my_game_frontend.wid[12].label_summer = common_data.uix_classes.Label_with_tr(text_source=['Лето!','Summer'], 
                                                                                    font_size = common_data.my_game_frontend.wid[12].button_of_activation.font_size*1.2,
                                                                                    pos_hint={'right': 0.44, 'top': 0.18},
                                                                                    size_hint = common_data.my_game_frontend.wid[12].button_of_activation.size_hint,
                                                                                    color = [52/256, 235/256, 158/256, 1], bold = True)
                    common_data.my_game_frontend.wid[12].add_widget(common_data.my_game_frontend.wid[12].label_summer)
                    
                    if common_data.my_game_frontend.wid[12].button_of_activation in common_data.my_game_frontend.wid[12].children:
                        common_data.my_game_frontend.wid[12].remove_widget(common_data.my_game_frontend.wid[12].button_of_activation)
                            
            if tech_info.quant_of_buys[self.index_of_current_tech][0]==common_data.my_game.counter_of_buys[self.index_of_current_tech][0]: # if tech is researched    
                self.set_btn_to_researched()
                
            elif tech_info.quant_of_buys[self.index_of_current_tech][0]>common_data.my_game.counter_of_buys[self.index_of_current_tech][0] or tech_info.quant_of_buys[self.index_of_current_tech][0]<=-1:
               
                self.set_done_x_times()
                
                
                if self.index_of_current_tech == 0:
                    common_data.my_game.prices_of_tech[self.index_of_current_tech][0] -= 5
                else:
                    common_data.my_game.prices_of_tech[self.index_of_current_tech][0] -= 1
                    
                self.label_of_tech.update_text(do_generate=True)
                if self.index_of_current_tech == 1: #for bolnitsy
                    
                    common_data.my_game.parameters_of_tech[1][2][0][0] += (1-common_data.my_game.parameters_of_tech[1][2][0][0])*0.25
                    common_data.my_game.parameters_of_tech[1][2][1][0] += (1-common_data.my_game.parameters_of_tech[1][2][1][0])*0.25
                    text_for_tech_generator.generate_texts_for_tech()
                    common_data.my_game_frontend.wid[1].label_of_tech.update_text()
        elif do_notify == True:
            if common_var.lang == 0:
                widget_of_common_par.inform_about_error("У Вас не хватает денег\nна данное действие", 'no money', 2)
            elif common_var.lang == 1:
                widget_of_common_par.inform_about_error("You haven't enough\nmoney for this action", 'no money', 2)
    
    def make_paid_option(self, instance):
        ind = -1
        if self.index_of_current_tech in {6, 7, 8, 10, 18, 21, 22, 24, 25}:
            ind = int(self.str_of_input_for_tech[1].text)
            common_data.my_game.parameters_of_tech[self.index_of_current_tech][1] = ind
                    
        if common_data.my_game.prices_of_tech[self.index_of_current_tech][1] >= -1 or ind == -1:
            skidka = 0
        else:
            skidka = common_data.my_game.game_pars.is_automatisated[ind]*common_data.my_game.parameters_of_tech[22][2][0]
                
        if common_data.my_game.game_pars.coins + skidka + common_data.my_game.prices_of_tech[self.index_of_current_tech][1] >=0: #if we have enough money for paid option
            
            common_data.my_game.game_pars.coins += common_data.my_game.prices_of_tech[self.index_of_current_tech][1]+skidka
            
            common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), 
                                                                                                       size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)
            
            if self.index_of_current_tech in {15, 16, 17, 26}:
                common_data.my_game.counter_of_buys[self.index_of_current_tech][1]+=1
                self.set_done_x_times()
            common_func.Mult_on_par(common_data.my_game.parameters_of_tech[self.index_of_current_tech], self.index_of_current_tech)
        else:
            if common_var.lang == 0:
                widget_of_common_par.inform_about_error("У Вас не хватает денег\nна данное действие", 'no money', 2)
            elif common_var.lang == 1:
                widget_of_common_par.inform_about_error("You haven't enough\nmoney for this action", 'no money', 2)
    
    
    def set_done_x_times(self):
        dobavka_k_stroke = ' '
        
        times = common_data.my_game.counter_of_buys[self.index_of_current_tech][tech_info.what_counting[self.index_of_current_tech]]
        if times%10 < 5 and times%10>1 and times>20:
            dobavka_k_stroke = 'а'
            
        elif times < 5 and times >1:
            dobavka_k_stroke = 'а'    
        max_d = ['', '']
        if common_data.my_game.quant_of_buys[self.index_of_current_tech][1] != None:
            max_d = [' из ' + str(common_data.my_game.quant_of_buys[self.index_of_current_tech][1]),
                     ' of ' + str(common_data.my_game.quant_of_buys[self.index_of_current_tech][1])]
            
        mes = ['Уже применено\n'+ str(times) +' раз'+ dobavka_k_stroke + max_d[0],
                'Already done\n'+ str(times) +' time' + 's'*(times>1) + max_d[1]]
        
        if hasattr(self, 'btn_already_done_x_times') == False:
            self.btn_already_done_x_times = uix_classes.WrappedLabel_with_tr(text_source = mes,
                                                                      size_hint=(.3, None),
                                                                      font_size = int(0.011*sizes.Width_of_screen*common_var.K), 
                                                                      pos_hint={'center_x': .2, 'top': .15}, 
                                                                      valign = 'top', halign = 'center'
                                                                      )
            self.add_widget(self.btn_already_done_x_times)
            if self.index_of_current_tech in {15, 16, 17, 26}: #emission or goscompany
                self.remove_widget(self.button_buy)
        else:
            self.btn_already_done_x_times.text_source = mes
            self.btn_already_done_x_times.text = mes[common_var.lang]
        if common_data.my_game.quant_of_buys[self.index_of_current_tech][1] != None \
           and self.index_of_current_tech in  {16}\
           and common_data.my_game.quant_of_buys[self.index_of_current_tech][1] <= common_data.my_game.counter_of_buys[self.index_of_current_tech][1]:
            self.remove_widget(self.button_make)
            self.button_make = uix_classes.WrappedLabel_with_tr(
                text_source = ["Метод исчерпан", "Method is used"],
                size_hint=(.4, .13),
                pos_hint={'right': 0.98, 'top': 0.17},
                on_press = self.make_paid_option,
                font_size = size_of_button_of_tech,
                color = [66/256, 245/256, 188/256, 1], bold = False)
            self.add_widget(self.button_make)
    
    def set_btn_activate(self):
            
        self.add_widget(self.button_of_activation)
        self.button_of_activation.text_source = frases.str_deactivate_tech
        self.button_of_activation.text = self.button_of_activation.text_source[common_var.lang]
        common_data.my_game.is_activated[self.index_of_current_tech] = True
        
    def set_btn_to_researched(self):

        self.remove_widget(self.button_buy)
        if tech_info.type_of_get[self.index_of_current_tech] == 1:
            button_buy_text_source = frases.str_researched
        if tech_info.type_of_get[self.index_of_current_tech] == 2:
            button_buy_text_source = frases.str_gotten_tech
            
        self.button_buy = uix_classes.Label_with_tr(
                text_source=button_buy_text_source,
                size_hint=(.25, .1),
                pos_hint={'right': 0.9, 'top': 0.15},
                font_size = size_of_button_of_tech 
                        )
        
        self.add_widget(self.button_buy)  
        
        if self.index_of_current_tech in {6, 7, 8, 10, 18, 21, 22, 24, 25}: #if we can use tech for region
            self.button_buy.pos_hint={'right': 0.9, 'top': 0.11}
            self.remove_widget(self.button_buy)                          
            level_of_btn_for_pay = 0.08
            
            self.str_of_input_for_tech[1] = TextInput(
            text="0",
            size_hint=(.115, .08),
            #height = sizes.Height_of_screen/23,
            pos_hint={'right': 0.458, 'center_y': level_of_btn_for_pay},
            readonly = True, halign = "center", 
            font_size = int(size_of_button_of_tech*1.3)
                    )
            
            self.pm_buttons[0] = Button(
            text="-", font_size = size_of_button_of_tech*1.5,
            size_hint=(.12, .08), valign = 'center', halign = 'center', bold = True,
            pos_hint={'right': 0.35, 'center_y': level_of_btn_for_pay},
            on_press = lambda *args: widget_of_common_par.change_input(-1, self.str_of_input_for_tech[1], 
                                                                       common_data.my_game.n-1, *args)
                    )
           
            
            self.pm_buttons[1] = Button(
            text="+", font_size = size_of_button_of_tech*1.5,
            size_hint=(.12, .08), valign = 'center', halign = 'center', bold = True,
            pos_hint={'right': 0.575, 'center_y': level_of_btn_for_pay},
            on_press = lambda *args: widget_of_common_par.change_input(+1, self.str_of_input_for_tech[1], common_data.my_game.n-1,*args)
                    )
            self.add_widget(self.pm_buttons[0])           
            self.add_widget(self.pm_buttons[1])           
            
            self.str_of_input_for_tech[0] = uix_classes.Label_with_tr(
            text_source=["Введите\nномер\nрегиона", "Enter\nregion\nindex"],
            size_hint=(.35, .15),
            pos_hint={'right': 0.30, 'center_y': level_of_btn_for_pay},
            font_size = size_of_button_of_tech
                    )   
            
            enter_ts = ["Применить!", "Apply!"]
            enter_sh = [.35, .09]
            enter_ph = .95
            
            if self.index_of_current_tech == 10:
                enter_ts = ["Вакцинировать!", "Vaccinise!"]
                enter_sh = [.393, .105]
                enter_ph = .98
                
            self.str_of_input_for_tech[2] = uix_classes.Button_asfalt(
            text_source = enter_ts,
            size_hint=enter_sh,
            pos_hint={'right': enter_ph, 'center_y': level_of_btn_for_pay},
            on_press = self.make_paid_option,
            font_size = size_of_button_of_tech                    
                )
        
            self.add_widget(self.str_of_input_for_tech[0])
            self.add_widget(self.str_of_input_for_tech[1])
            self.add_widget(self.str_of_input_for_tech[2])  
            
            if self.index_of_current_tech == 10:
                self.btn_make_vaccine = uix_classes.Button_asfalt(
                text_source = ["Произвести дозы!", "Make doses!"],
                size_hint=(.47, .105),
                pos_hint={'center_x': 0.5, 'top': 0.28},
                on_press = common_func.make_new_vac_dozes,
                font_size = size_of_button_of_tech                    
                    )
            
                self.add_widget(self.btn_make_vaccine)
                
        
            
        if self.index_of_current_tech in {15, 16, 17, 26}: #coin emission or goscompany
            
            self.button_make = uix_classes.Button_asfalt(
                text_source = ["Применить!", "Make!"],
                size_hint=(.4, .13),
                pos_hint={'right': 0.98, 'top': 0.17},
                on_press = self.make_paid_option,
                font_size = size_of_button_of_tech)
            
            self.add_widget(self.button_make)
            self.button_buy.pos_hint={'center_x': .2, 'top': .15}
    
    def on_touch_up(self, touch): # can go to viewer mode
        if self.collide_point(*touch.pos): 
            
            if touch.is_double_tap == True:
                if hasattr(self, "button_buy"):
                    if self.button_buy.collide_point(touch.pos[0], touch.pos[1]):
                        return
                if hasattr(self, "str_of_input_for_tech"):
                    if hasattr(self.str_of_input_for_tech[2], "collide_point"):
                        if self.str_of_input_for_tech[2].collide_point(touch.pos[0], touch.pos[1]):
                            return
                        if self.pm_buttons[0].collide_point(touch.pos[0], touch.pos[1]):
                            return
                        if self.pm_buttons[1].collide_point(touch.pos[0], touch.pos[1]):
                            return   
                if hasattr(self, "button_of_activation"):
                    if self.button_of_activation.collide_point(touch.pos[0], touch.pos[1]):
                        return
                if hasattr(self, "btn_make_vaccine"):
                    if self.btn_make_vaccine.collide_point(touch.pos[0], touch.pos[1]):
                        return      
                if common_data.my_game_frontend.mode_of_tech_panel == "panel":
                    tech_sm.TechViewer().open_self(ind_tech=self.index_of_current_tech, instance = 0)
                    return
                if common_data.my_game_frontend.mode_of_tech_panel == "viewer":
                    tech_sm.tech_viewer.close_self(instance = 5)
    
    def spec_methods_button_preparing(self):
        if self.index_of_current_tech == 12 and common_data.my_game.counter_of_buys[12][0] > 0: # if distant
            print("SUMMER")
            if common_data.my_game.game_pars.date[1] in {6, 7, 8} and self.button_of_activation in self.children: #if summer and researched distant 
                
                self.label_summer = common_data.uix_classes.Label_with_tr(text_source=['Лето!','Summer'], 
                                                                        font_size = self.button_of_activation.font_size*1.2,
                                                                        pos_hint={'right': 0.44, 'top': 0.18},
                                                                        size_hint = self.button_of_activation.size_hint,
                                                                        color = [52/256, 235/256, 158/256, 1], bold = True)
                self.add_widget(self.label_summer)
                
                self.remove_widget(self.button_of_activation)
                
                if common_data.my_game.is_activated[12]==True:
                    self.Activate_Deactivate(instance = 5)
                    
                    common_data.my_game_game.must_be_activated_distant = True
        if self.index_of_current_tech == 28 and common_data.my_game.was_purchased_in_this_month[28] == True:
                
            self.label_using_now = common_data.uix_classes.Label_with_tr(text_source=['Исследования\nуже ведутся!',
                                                                                       'Researches\nare conducting!'], 
                                                                          font_size = self.button_buy.font_size,
                                                                          pos_hint = self.button_buy.pos_hint,
                                                                          size_hint = self.button_buy.size_hint,
                                                                          color = [52/256, 235/256, 158/256, 1], 
                                                                          bold = True, halign = 'center')
            self.add_widget(self.label_using_now)
                
            self.remove_widget(self.button_buy)
        if self.index_of_current_tech == 31 and common_data.my_game.was_purchased_in_this_month[31] == True:
                
            self.label_using_now = common_data.uix_classes.Label_with_tr(text_source=['Оздоровление\nудалось!',
                                                                                'We are now\nhealthier!'], 
                                                                    font_size = self.button_buy.font_size,
                                                                    pos_hint = self.button_buy.pos_hint,
                                                                    size_hint = self.button_buy.size_hint,
                                                                    color = [32/256, 187/256, 214/256, 1], 
                                                                    bold = True, halign = 'center')
            self.add_widget(self.label_using_now)
                
            self.remove_widget(self.button_buy)
                
    def update_rect(self, instance, value):
        self.rect_wid_card.pos = self.pos
        self.rect_wid_card.size = self.size    
        self.rect_wid.pos = self.pos
        self.rect_wid.size = self.size 
    