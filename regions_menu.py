import widget_of_common_par
import common_func
import common_var
import graph_maker
import icon_func
import textures
import common_data as cd
import tech_info
import sizes
import uix_classes

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label

     
Current_tech = -1
def region_menu():
    if widget_of_common_par.opened_ask_panel != None:
        widget_of_common_par.opened_ask_panel.close_ask_panel(instance = 3) 
    
    widget_of_common_par.choose_tech_for_activation = widget_of_common_par.AskPanel()
    several_reg = len(cd.mg.list_of_chosen)>1
    if several_reg:
        
        if common_var.lang == 0:
            widget_of_common_par.choose_tech_for_activation.open_ask_panel(texture = textures.texture_questions, 
                                                                            messages = ["Вы выбрали регионы", "№" + str(cd.mg.list_of_chosen), "Что будем делать?"], color_texture = (1, 1, 1, .6))
        elif common_var.lang == 1:
            widget_of_common_par.choose_tech_for_activation.open_ask_panel(texture = textures.texture_questions, 
                                                                            messages = ["You chose regions", "#" + str(cd.mg.list_of_chosen), "What do you want to do?"], color_texture = (1, 1, 1, .6))
    else:
        if common_var.lang == 0:
            widget_of_common_par.choose_tech_for_activation.open_ask_panel(texture = textures.texture_questions, 
                                                                            messages = ["Вы выбрали регион №" + str(cd.mg.list_of_chosen[0]), "Что будем делать?"], color_texture = (1, 1, 1, .6))
        elif common_var.lang == 1:
            widget_of_common_par.choose_tech_for_activation.open_ask_panel(texture = textures.texture_questions, 
                                                                            messages = ["You chose region #" + str(cd.mg.list_of_chosen[0]), "What do you want to do?"], color_texture = (1, 1, 1, .6))
    list_of_tech = [0]*len(cd.mg.list_of_tech_tr)
    for i in range(len(list_of_tech)):
        list_of_tech[i] = cd.mg.list_of_tech_tr[i][common_var.lang]
        
    widget_of_common_par.spinner_for_tech = uix_classes.SpinnerWidget(sync_height = True, text = cd.mg.str_of_probably_activating_tech[common_var.lang])
    widget_of_common_par.spinner_for_tech.font_size = sizes.ASK_SIZE
    widget_of_common_par.spinner_for_tech.values = list_of_tech
    
    widget_of_common_par.choose_tech_for_activation.add_widget(widget_of_common_par.spinner_for_tech)
    widget_of_common_par.spinner_for_tech.size_hint = (.2, .1)
    widget_of_common_par.spinner_for_tech.pos=(widget_of_common_par.choose_tech_for_activation.active_zone.pos[0]+widget_of_common_par.choose_tech_for_activation.active_zone.size[0]*0.17, 
                                               widget_of_common_par.choose_tech_for_activation.active_zone.pos[1]+ widget_of_common_par.choose_tech_for_activation.active_zone.size[1]*0.38)
    mes = ["Применить!", "Apply!"]
    size_hint = [.11, .1]
    if common_var.lang == 0:
        size_hint = [.125, .1]
    btn_ask = Button(text = mes[common_var.lang], size_hint = size_hint, 
                     pos=[widget_of_common_par.choose_tech_for_activation.active_zone.pos[0]+widget_of_common_par.choose_tech_for_activation.active_zone.size[0]*0.6, 
                          widget_of_common_par.choose_tech_for_activation.active_zone.pos[1]+widget_of_common_par.choose_tech_for_activation.active_zone.size[1]*(0.38+(0.1-size_hint[1])/2)], 
                    font_size = sizes.ASK_SIZE, on_press = make_pay_for_tech, halign = 'center')
    
    widget_of_common_par.choose_tech_for_activation.add_widget(btn_ask)

    
    if len(cd.mg.list_of_chosen) == 1:
        cd.mg.is_chosen_only_one = cd.mg.list_of_chosen[0]
        btn_info = Button(text = ['Графики для региона', 'Region charts'][common_var.lang], size_hint = (.2, .1), 
                          pos=(widget_of_common_par.choose_tech_for_activation.active_zone.pos[0]+widget_of_common_par.choose_tech_for_activation.active_zone.size[0]*0.1, 
                               widget_of_common_par.choose_tech_for_activation.active_zone.pos[1]+ widget_of_common_par.choose_tech_for_activation.active_zone.size[1]*0.08), 
                          font_size = sizes.ASK_SIZE, on_press = choose_graph)
        widget_of_common_par.choose_tech_for_activation.add_widget(btn_info)    
    else:
        btn_info = Button(text = ['Графики для страны', 'Country charts'][common_var.lang], size_hint = (.2, .1), pos=(widget_of_common_par.choose_tech_for_activation.active_zone.pos[0]+widget_of_common_par.choose_tech_for_activation.active_zone.size[0]*0.1, 
                                                                                 widget_of_common_par.choose_tech_for_activation.active_zone.pos[1]+ widget_of_common_par.choose_tech_for_activation.active_zone.size[1]*0.1), 
                                                                            font_size = sizes.ASK_SIZE, on_press = choose_graph)
        widget_of_common_par.choose_tech_for_activation.add_widget(btn_info) 

def make_pay_for_tech(instance):
    global Current_tech
    widget_of_common_par.choose_tech_for_activation.close_ask_panel(instance = 3)
    Current_tech = widget_of_common_par.spinner_for_tech.text
    
    del widget_of_common_par.spinner_for_tech
    
    ind = -1
    for i in {6, 7, 8, 10, 18,  21, 22, 24, 25}:
        if Current_tech == tech_info.names_of_tech[i][common_var.lang]:
            ind = i
            break
        if Current_tech in {"Вакцинация", "Vaccination"}:
            ind = 10
            break
    
    if ind != -1:
        cd.mg.str_of_probably_activating_tech = tech_info.names_of_tech[ind]
        if ind == 10:
            cd.mg.str_of_probably_activating_tech = ["Вакцинация", "Vaccination"]

    if ind == -1:      
        cd.mg.str_of_probably_activating_tech = ["Пока нет методов\nдля региона", "No methods\nfor region yet"]
        tex = ["Вы ещё не освоили методов для применения в регионах", "Yet you haven't got methods for using in regions"]
        widget_of_common_par.info_message(tex[common_var.lang], 'bad', 2.5)
                
    else:
        if (len(cd.mg.list_of_chosen) > 1): #если активируем на несколько гексов
            
            skidka = 0
            if cd.mg.prices_of_tech[ind][1] < -1:
                for i in range(common_var.n):
                    if cd.mg.multichoice_list[i]==1:
                        skidka += cd.mg.pars.reg_automatisated[i]*cd.mg.parameters_of_tech[22][2][0]
            statement = -cd.mg.prices_of_tech[ind][1]*len(cd.mg.list_of_chosen) <= cd.mg.pars.coins+skidka
            if ind == 25:
                skidka = min(skidka, 1)
                statement = -cd.mg.prices_of_tech[ind][1] <= cd.mg.pars.coins+skidka
                archive_par = cd.mg.parameters_of_tech[25][2][0]
                cd.mg.parameters_of_tech[25][2][0] = 1-(1-cd.mg.parameters_of_tech[25][2][0])/len(cd.mg.list_of_chosen)
            
            if statement:
                
                for i in range(common_var.n):
                    if cd.mg.multichoice_list[i]==1:
                        
                        
                        common_func.Mult_on_par((cd.mg.parameters_of_tech[ind][0], i, cd.mg.parameters_of_tech[ind][2], cd.mg.parameters_of_tech[ind][3]), ind)
                        cd.frontend.hexes_chosen[i].hide_circle()
                
                
                if ind != 25:
                    
                    cd.mg.pars.coins += (cd.mg.prices_of_tech[ind][1]*len(cd.mg.list_of_chosen)+skidka)
                else:
                    cd.mg.pars.coins += (cd.mg.prices_of_tech[ind][1]+skidka)
                    cd.mg.parameters_of_tech[25][2][0] = archive_par
                cd.frontend.pars.labels.cash_label.text = icon_func.add_money_icon(string = str(cd.mg.pars.coins), size = cd.frontend.pars.labels.cash_label.font_size)
                
                cd.mg.multichoice_list = [0]*21
                cd.mg.list_of_chosen = []
                
        
            else:            
                tex = ["У вас не хватает денег на данное действие", "You haven't enough money for this action"]
                widget_of_common_par.info_message(tex[common_var.lang], 'bad', 2)            
        
        else: #если на один гекс
            skidka = 0
            if cd.mg.prices_of_tech[ind][1] < -1:
                for i in range(cd.mg.n):
                    if i == cd.mg.is_chosen_only_one:               
                        skidka = cd.mg.pars.reg_automatisated[i]*cd.mg.parameters_of_tech[22][2][0]
                
            if -cd.mg.prices_of_tech[ind][1] <= cd.mg.pars.coins + skidka:
                
                for i in range(cd.mg.n):
                    if i == cd.mg.is_chosen_only_one:
                        common_func.Mult_on_par((cd.mg.parameters_of_tech[ind][0], 
                                                 i, cd.mg.parameters_of_tech[ind][2], cd.mg.parameters_of_tech[ind][3], 1), ind)
                        cd.frontend.hexes_chosen[i].hide_circle()
                        cd.mg.pars.coins += (cd.mg.prices_of_tech[ind][1]+skidka)
                        
                        cd.frontend.pars.labels.cash_label.text = icon_func.add_money_icon(string = str(cd.mg.pars.coins), size = cd.frontend.pars.labels.cash_label.font_size)                        
                cd.mg.multichoice_list = [0]*21
                cd.mg.list_of_chosen = []
            else:         
                tex = ["У вас не хватает денег на данное действие", "You haven't enough money for this action"]
                widget_of_common_par.info_message(tex[common_var.lang], 'bad', 2) 
                
            cd.mg.is_chosen_only_one = 'not exists'
            
            
            
def choose_graph(instance):
    
    widget_of_common_par.graph_menu = widget_of_common_par.AskPanel()
    
    if common_var.lang == 0:
        widget_of_common_par.graph_menu.open_ask_panel(texture = textures.texture_questions, 
                                                                        messages = ["Какой график Вы хотите увидеть?", "Выберите величину для оси Y, на оси X будет время"], color_texture = (1, 1, 1, .6))
    elif common_var.lang == 1:
        widget_of_common_par.graph_menu.open_ask_panel(texture = textures.texture_questions, 
                                                                        messages = ["What graph do you want to see?", "Choose what will be on y-axis, on x-axis is time"], color_texture = (1, 1, 1, .6))
    
    widget_of_common_par.spinner_for_graph = uix_classes.SpinnerWidget(sync_height = True, text = ["Нажмите для выбора", "Press to open menu"][common_var.lang], markup=True)
    widget_of_common_par.spinner_for_graph.font_size = sizes.ASK_SIZE
    widget_of_common_par.spinner_for_graph.values = [["Больные", "Умершие", "Выздоровевшие", "z_in*z_out", "Процент иммунных", "Заболевающие\n за день", "Умирающие\nза день", "Выздоровевшие\n за день"], 
                                                     ["[font=fonts/Verdana.ttf]Ill[/font]", "Dead", "Recovered", "z_in*z_out", "Percent of immune", "Ill per day", "Dead per day", "Recovered\n per day"]][common_var.lang]

    if len(cd.mg.list_of_chosen) > 1:
        widget_of_common_par.spinner_for_graph.values.remove('z_in*z_out')
        widget_of_common_par.spinner_for_graph.values.append(['Штрафные баллы', 'Penalty points'][common_var.lang])
        
        
    widget_of_common_par.graph_menu.add_widget(widget_of_common_par.spinner_for_graph)
    widget_of_common_par.spinner_for_graph.size_hint = (.2, .1)
    widget_of_common_par.spinner_for_graph.pos=(widget_of_common_par.graph_menu.active_zone.pos[0]+widget_of_common_par.graph_menu.active_zone.size[0]*0.17, 
                                               widget_of_common_par.graph_menu.active_zone.pos[1]+ widget_of_common_par.graph_menu.active_zone.size[1]*0.4)
    mes = ["Построить!", "Plot!"]
    btn_ask = Button(text = mes[common_var.lang], size_hint = (.13, .1), pos=(widget_of_common_par.graph_menu.active_zone.pos[0]+widget_of_common_par.graph_menu.active_zone.size[0]*0.6, 
                                                                             widget_of_common_par.graph_menu.active_zone.pos[1]+ widget_of_common_par.graph_menu.active_zone.size[1]*0.4), 
                                                                        font_size = sizes.ASK_SIZE, on_press = to_make_graph)
    widget_of_common_par.graph_menu.add_widget(btn_ask)

    

def to_make_graph(instance):
    text_in_spinner = widget_of_common_par.spinner_for_graph.text
    text_in_spinner = text_in_spinner.replace('[font=fonts/Verdana.ttf]', '')
    text_in_spinner = text_in_spinner.replace('[/font]', '')
    
    type = None
    
    if text_in_spinner in {"Ill", "Больные"}:
        type = 'ill'
        
    if text_in_spinner in {"Dead", "Умершие"}:
        type = 'dead'
        
    if text_in_spinner in {'z_in*z_out'}:
        type = 'z_in' #really z_in*z_out
        
    if text_in_spinner in {"Выздоровевшие", "Recovered"}:
        type = 'recovered'
        
    if text_in_spinner in {"Заболевающие\n за день", "Ill per day"}:
        type = 'new_ill'
        
    if text_in_spinner in {"Умирающие\nза день", "Dead per day"}:
        type = 'new_dead'
    
    if text_in_spinner in {"Выздоровевшие\n за день", "Recovered\n per day"}:
        type = 'new_recovered'
        
    if text_in_spinner in {"Процент иммунных", "Percent of immune"}:
        type = 'pr_immune'
    
    if text_in_spinner in {"Штрафные баллы", "Penalty points"}:
        type = 'pen_points'
        
    if type != None:
        graph_maker.make_graph(typ=type)
        