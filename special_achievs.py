import common_data
import common_var
import country_variants
import diseases
import sizes
import tech_info
import textures
import web_goer

from kivy.graphics import Canvas, Color, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class Special_Achievements_Label(Label):
    def __init__(self, achieves = [], color = "gold", **kwargs): 
        super(Special_Achievements_Label, self).__init__(**kwargs)     
        #achieves[type][value]
        
        self.text = " "
        self.font_size = sizes.WIN_SIZE
        self.halign = 'center'
        self.markup = True
        
        for i in range(len(achieves)):
            if achieves[i][0] == "first_text":
                self.text+=achieves[i][1]
            if achieves[i][0] == "rate_app":
                self.text+=['Не забудьте написать отзыв на [u][ref='+achieves[i][1]+']Google Play[/ref][/u]\nи поставить оценку приложению (желательно 5 звёзд :) )!\n\nЭто будет Ваша лучшая помошь "Эпидемии".\n', 
                            "Don't forget to rate our app in [u][ref="+achieves[i][1]+"]Google Play[/ref][/u]!\n\n"][common_var.lang]
            if achieves[i][0] == "victory_by_new_disease":
                self.text+= ("[b][color=cf4432]"+achieves[i][1][common_var.lang]+"[/color][/b]"+\
                             [" впервые остановлен"+achieves[i][2]*'а'+" благодаря Вам!\n\n", 
                              " has stopped for the first time because of you!\n\n"][common_var.lang] )
            if achieves[i][0] == "victory_by_new_country":
                #австр, арг, браз, инд, кан, кит, мекс, рос, сша, уни, яп, турц
                letter = ''
                if achieves[i][2] in {0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12}:
                    letter = 'а'
                if achieves[i][2] in {5}:#China
                    letter = ''
                if achieves[i][2] in {8}:#USA
                    letter = 'и'
                self.text+= ("[b][color=cf34eb]"+achieves[i][1][common_var.lang]+"[/color][/b]"+\
                             [" впервые победил" +letter+" с Вами эпидемию!\n\n", 
                              " has defeated the epidemic for the first time with you!\n\n"][common_var.lang] )
            
            if achieves[i][0] == "new_tech":
                self.text+= (["Разблокирован новый метод: ", 
                              "New method is unblocked: ", 
                            ][common_var.lang] +  "[b][color=ff0066]"+tech_info.names_of_tech[achieves[i][1]][common_var.lang]+"[/color][/b]\n\n")
            
            if achieves[i][0] == "new_disease":
                self.text+= (["Разблокирована новая инфекция: ", 
                              "New infection is unblocked: ", 
                            ][common_var.lang] +  "[b][color=ed1313]"+diseases.diseases_list[achieves[i][1][0]].name[common_var.lang]+"[/color][/b]\n\n")
            
            if achieves[i][0] == "new_techs":
                if len(achieves[i][1]) == 1:
                    
                    self.text+= (["Разблокирован новый метод: ", 
                                  "New method is unblocked: ", 
                                  ][common_var.lang] +  "[b][color=ff0066]"+tech_info.names_of_tech[achieves[i][1][0]][common_var.lang]+"[/color][/b]\n\n")
                else:
                    add = ["Разблокированы новые методы: ", "New methods are unblocked: "][common_var.lang]
                    for k in range(len(achieves[i][1])):
                        add+="[b][color=ff0066]"+tech_info.names_of_tech[achieves[i][1][k]][common_var.lang]
                        if k == len(achieves[i][1])-1:
                            add+=".[/b][/color]\n\n"
                        else:
                            add+=', [/b][/color]'
                            if k%4 == 2:
                                add+="\n"
                    self.text+=add
            if achieves[i][0] == "new_countries":
                if len(achieves[i][1]) == 1:
                    
                    self.text+= (["Разблокирована новая страна: ", 
                                  "New country is unblocked: ", 
                                  ][common_var.lang] +  "[b][color="+country_variants.Country_lands[achieves[i][1][0]].color_of_name+"]"+country_variants.Country_lands[achieves[i][1][0]].name[common_var.lang]+"[/color][/b]\n\n")
                else:
                    add = ["Разблокированы новые страны: ", "New countries are unblocked: "][common_var.lang]
                    for k in range(len(achieves[i][1])):
                        add+="[b][color="+country_variants.Country_lands[achieves[i][1][k]].color_of_name+"]"+country_variants.Country_lands[achieves[i][1][k]].name[common_var.lang]
                        if k == len(achieves[i][1])-1:
                            add+=".[/b][/color]\n\n"
                        else:
                            add+=',[/b][/color] '
                            if k%4 == 2:
                                add+='\n'
                    self.text+=add
                
            if achieves[i][0] == "rep_status":
                self.text+=(["У Вас новый статус репутации: ", 
                             "You've got new reputation status: "][common_var.lang] + "[b][color=14BADB]" + str(common_var.statuses_stars[achieves[i][1]][common_var.lang]) +'\n\n[/b][/color]')
            if achieves[i][0] == "gold_status":
                self.text+=(["У Вас новый статус благостояния: ", 
                             "You've got new wealth status: "][common_var.lang] +"[b][color=fbc503]" +str(common_var.statuses_coins[achieves[i][1]][common_var.lang]) +'\n\n[/b][/color]')            
            if achieves[i][0] == "link_vk_page" and len(achieves) < 3:
                if common_var.lang == 1:
                    self.text+='Join us: [u][ref=https://www.facebook.com/epidemy_outbreak]Facebook community of "Epidemy"[/ref][/u]\n\n'
                if common_var.is_victory == 1 and common_var.lang == 0:
                    self.text+="Если играть слишком легко, пишите:\n\n[u][ref="+achieves[i][1]+']ВК-сообщество "Эпидемии"[/ref][/u]\n\n'
                if common_var.is_victory == 0 and common_var.lang == 0:
                    self.text+="Если никак не получается победить, гляньте сюда:\n\n[u][ref="+achieves[i][1]+"]Наше ВК-сообщество[/ref][/u]\n\n"
            
        if common_var.is_victory == 1:
            self.text+=["[color=00ff00]Поздравляем!", "[color=00ff00]Congratulations!"][common_var.lang]
        self.bind(on_ref_press = lambda *args: web_goer.go_to_link(*args))
        
       
class Widget_with_texture(Widget):
    def __init__(self, **kwargs):
        super(Widget_with_texture, self).__init__(**kwargs)
    def update_rect(self, instance, value):
        self.rec.pos = self.pos
        self.rec.size = self.size    
        self.rect.pos = self.pos
        self.rect.size = self.size    
    
class Special_Achievements_Pannel(common_data.FloatLayout):
    def __init__(self, achieves = [], color = "gold", **kwargs): 
        super(Special_Achievements_Pannel, self).__init__(**kwargs)
        with self.canvas:
            Color(.98, .77, .01)
            if color == "green":
                Color(22/256, 186/256, 91/256)
            Line(rectangle=(.03*sizes.Width_of_screen, .05*sizes.Height_of_screen, .94*sizes.Width_of_screen, .9*sizes.Height_of_screen),
                 width = sizes.Height_of_screen/720*3)
            
        self.bind(on_touch_down = self.touched_to_close)
        
        self.bl = BoxLayout(size_hint = [.7, .2], pos_hint = {'center_x': .5, 'center_y': .17},
                            orientation = "horizontal", spacing = sizes.Width_of_screen/50)
        
        self.lab = Special_Achievements_Label(achieves=achieves, color=color, 
                                            pos_hint = {'center_x': .5, 'top': .9}, size_hint = [1, .5])
        self.add_widget(self.lab)
        txt = self.lab.text
        
        new_strokes = txt.count("\n")
        print(new_strokes)
        if new_strokes <= 4:
            self.bl.size_hint_y = .4
            self.bl.pos_hint = {'center_x': .5, 'center_y': .28}             
        if new_strokes <= 7:
            self.bl.size_hint_y = .31
            self.bl.pos_hint = {'center_x': .5, 'center_y': .235}        
        elif new_strokes < 10:
            self.bl.size_hint_y = .24
            self.bl.pos_hint = {'center_x': .5, 'center_y': .22}
        if new_strokes > 10:
            self.lab.font_size-=1
            self.lab.size_hint_y = .6    
        if new_strokes > 12:
            self.lab.font_size-=3
            self.lab.size_hint_y=.75
        
        valign = 'center'
        im = list()
        for i in achieves:
            if i[0] == "new_techs":
                for j in range(len(i[1])):
                    im2 = Widget_with_texture(size_hint_y = None, height = self.bl.size_hint_y*sizes.Height_of_screen,
                                              size_hint_x = None, width = self.bl.size_hint_y*sizes.Height_of_screen*8/10)
                    
                    with im2.canvas:
                        Color(.56, .58, .13, .6)
                        im2.rec = Rectangle(size = im2.size, pos = im2.pos, texture = textures.texture_of_tech)
                        im2.bind(size = im2.update_rect, pos = im2.update_rect)
                        Color(1, 1, 1, .7)
                        im2.rect = Rectangle(size = im2.size, pos = im2.pos, texture = textures.textures_of_tech[i[1][j]])
                        im2.bind(size = im2.update_rect, pos = im2.update_rect)
                        
                    im.append(im2)    
                    
                valign = 'top'
                    
            if i[0] == "new_countries":
    
                for j in range(len(i[1])):
                    im1 = Widget_with_texture(size_hint_y = None, height = self.bl.size_hint_y*sizes.Height_of_screen,
                                              size_hint_x = None, width = self.bl.size_hint_y*sizes.Height_of_screen*1.6)
                    
                    with im1.canvas:
                        Color(.56, .58, .13, .6)
                        im1.rec = Rectangle(size = im1.size, pos = im1.pos, texture = textures.texture_of_tech)
                        im1.bind(size = im1.update_rect, pos = im1.update_rect)
                        Color(1, 1, 1, .8)
                        im1.rect = Rectangle(size = im1.size, pos = im1.pos, texture = textures.CoreImage("flags_images/" + common_data.country_variants.flags_source[i[1][j]] + ".jpg").texture)
                        im1.bind(size = im1.update_rect, pos = im1.update_rect)
                        
                    im.append(im1)    
                valign = 'top'
                
            
        counter = 0
        for i in range(len(im)):
            counter+=im[i].size[0]

        self.bl.size_hint_x = counter/sizes.Width_of_screen+0
        self.bl.pos_hint['center_x'] = .5
        
        
        common_data.random.shuffle(im)
        for i in im:
            self.bl.add_widget(i)
                
        self.add_widget(self.bl, index = 0)
        
        if valign != 'top':
            self.lab.pos_hint = {'center_x': .5, 'center_y': .5}
        
        
        
    def open_pannel(self, instance):
        self.outer_folders = []
        for i in common_data.final_layout.children:
            self.outer_folders.append(i)
        common_data.final_layout.clear_widgets()
        common_data.final_layout.add_widget(self)
        
    def touched_to_close(self, touch, instance):
        if self.collide_point(*touch.pos):
            self.close_pannel(instance=3)
            
    def close_pannel (self, instance):
        common_data.final_layout.remove_widget(self)
        for i in self.outer_folders:
            common_data.final_layout.add_widget(i) 
        
win_pannel = Special_Achievements_Pannel()