import common_data
import common_var
import e_settings
import frases
import icon_func
import sizes
import spec_func
import textures
import widget_of_common_par

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label

def load_videos(instance):
    if spec_func.is_internet() == True:
        print("Wait for rewarded video")
        App.get_running_app().ads.show_rewarded_ad()
    else:
        mes = ["Нет интернета!", "No internet connection!"]
        widget_of_common_par.inform_about_error(mes[common_var.lang], 'good', 2) 
   
        
  
def after_rewarded_ads(instance):
   
    common_data.my_game.game_pars.coins+=10
    common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)
    
    widget_of_common_par.opened_ask_pannel_is.close_ask_pannel(instance = 5)
    widget_of_common_par.gold_ask = widget_of_common_par.Ask_pannel()
     
    create_gold_menu(pannel=widget_of_common_par.opened_ask_pannel_is)
    
def create_gold_menu(pannel = widget_of_common_par.opened_ask_pannel_is):
    
    widget_of_common_par.gold_ask = widget_of_common_par.Ask_pannel()
    if common_var.lang == 0:
        widget_of_common_par.gold_ask.open_ask_pannel(messages=[icon_func.letters_to_icons("У Вас сейчас "+str(common_data.my_stats.goldreserves)+" монет\nзолотовалютных резервов"), 
                                                                "\nХотите часть их перевести в активы?",
                                                                icon_func.letters_to_icons("\n[b]У страны уже "+str(common_data.my_game.game_pars.coins) + " монет активов")], 
                                                                texture = textures.tex_gold_res, color_texture = (1,1,1,.6))
    elif common_var.lang == 1:
        widget_of_common_par.gold_ask.open_ask_pannel(messages=[icon_func.letters_to_icons("Goldexchange\nreserves contain "+str(common_data.my_stats.goldreserves)+" coins"), 
                                                                icon_func.letters_to_icons("\nDo you want to convert some gold coins to actives?"),
                                                                icon_func.letters_to_icons("\n[b]You have already "+str(common_data.my_game.game_pars.coins) + " coins")], 
                                                                texture = textures.tex_gold_res, color_texture = (1,1,1,.6))
    
    pannel = widget_of_common_par.gold_ask
    mes = ["Перевести!", "Convert it!"]
    btn_ask = Button(text = mes[common_var.lang], 
                                          size_hint = (.23*pannel.size_zone[0]/sizes.Width_of_screen, pannel.size_zone[1]/sizes.Height_of_screen*0.14), 
                                          pos=(pannel.left_edge_pos[0]+pannel.size_zone[0]*0.6, pannel.left_edge_pos[1]+ pannel.size_zone[1]*0.33), 
                                          font_size = sizes.ASK_SIZE, 
                                          on_press = lambda *args: reserves_to_actives(pannel, *args), markup = True)
    pannel.add_widget(btn_ask)
    
    if common_var.IS_PREMIUM == False:
        mes = [icon_func.letters_to_icons("Получить 10 монет\nза просмотр рекламы"), 
               icon_func.letters_to_icons("Get 10 coins by\n watching ads")]
        btn_rew_video = Button(text = mes[common_var.lang], size_hint = (.25, .1), pos=(pannel.left_edge_pos[0]+pannel.size_zone[0]*0.1, pannel.left_edge_pos[1]+ pannel.size_zone[1]*0.1), 
                                               font_size = sizes.ASK_SIZE, on_release = load_videos, markup = True)
     
            
        pannel.add_widget(btn_rew_video)    

    pannel.input_mes = Label(text = icon_func.add_money_icon_simple("0"), size_hint = (.17*pannel.size_zone[0]/sizes.Width_of_screen, pannel.size_zone[1]/sizes.Height_of_screen*0.1), 
                                pos=(pannel.left_edge_pos[0]+pannel.size_zone[0]*0.199, pannel.left_edge_pos[1]+ pannel.size_zone[1]*0.35), font_size = sizes.ASK_SIZE, markup = True, color = (0,0,0,1))
    
    with pannel.canvas:
        Color(1,1,1,1)
        Rectangle(size = (pannel.input_mes.size_hint[0]*common_data.final_layout.size[0], pannel.input_mes.size_hint[1]*common_data.final_layout.size[1]), pos = pannel.input_mes.pos, texture = textures.tex_ramka)    
    
    pannel.add_widget(pannel.input_mes)     
    btn_p = Button(text = "+", size_hint = (.068*pannel.size_zone[0]/sizes.Width_of_screen, pannel.size_zone[1]/sizes.Height_of_screen*0.1), 
                   pos=(pannel.left_edge_pos[0]+pannel.size_zone[0]*0.37, pannel.left_edge_pos[1]+ pannel.size_zone[1]*0.35), font_size = sizes.ASK_SIZE, 
                   on_press = lambda *args: widget_of_common_par.change_input(+1, pannel.input_mes, 1000, typ = "coin", *args))
    pannel.add_widget(btn_p)
    btn_m = Button(text = "-", size_hint = (.068*pannel.size_zone[0]/sizes.Width_of_screen, pannel.size_zone[1]/sizes.Height_of_screen*0.1), 
                   pos=(pannel.left_edge_pos[0]+pannel.size_zone[0]*0.13, pannel.left_edge_pos[1]+ pannel.size_zone[1]*0.35), font_size = sizes.ASK_SIZE, 
                   on_press = lambda *args: widget_of_common_par.change_input(-1, pannel.input_mes, 1000, typ = "coin", *args))
    pannel.add_widget(btn_m)       
        
    
def reserves_to_actives (pannel, instance):
    
    if widget_of_common_par.opened_ask_pannel_is != None:
        
        delta_c = int(pannel.input_mes.text.replace(icon_func.add_money_icon_simple(""), ""))
        
        if common_data.my_stats.goldreserves < delta_c:
            tex = ["У вас не хватает резервов на данное действие", "You haven't enough money for this action"]
            widget_of_common_par.inform_about_error(tex[common_var.lang], 'bad', 2)
    
        elif delta_c > 0:          
            
            common_data.my_game.game_pars.coins+=delta_c
            common_data.my_stats.goldreserves-= delta_c
            
            common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)     
            
            x = common_data.my_stats.level_coins
            common_data.my_stats.level_coins = spec_func.status_finder('coins', common_data.my_stats.goldreserves)[0]
            common_data.my_stats.save_to_file()
            
            common_var.need_c = spec_func.status_finder('coins', common_data.my_stats.goldreserves)[1] 
            
            e_settings.nast.str_of_reserves.text = icon_func.add_money_icon(string = str(common_data.my_stats.goldreserves), size = e_settings.nast.str_of_reserves.font_size)
            
            e_settings.nast.lab_need_coins_for_next_status.text = icon_func.add_money_icon(string = str(common_var.need_c), size = e_settings.nast.lab_need_coins_for_next_status.font_size)
            
            e_settings.nast.progress_c.value = int(common_data.my_stats.goldreserves) 
            e_settings.nast.progress_c.max = common_data.my_stats.goldreserves + common_var.need_c
        
            e_settings.nast.lab_status_of_rich.text_cource = common_var.statuses_coins[common_data.my_stats.level_coins]
            e_settings.nast.lab_status_of_rich.text = common_var.statuses_coins[common_data.my_stats.level_coins][common_var.lang]

            pannel.close_ask_pannel(instance = 5)            
            
            create_gold_menu()
            if x > common_data.my_stats.level_coins:
                tex = ["Операция выполнена.\nВаш статус благосостояния упал.", 
                       "Transaction was completed.\nYour wealth status decreased."]
                typ='bad'
            
            else:
                tex = ["Операция выполнена", "Transaction was completed"]
                typ='good'
            widget_of_common_par.inform_about_error(tex[common_var.lang], typ, 2)
            
            
    
            
