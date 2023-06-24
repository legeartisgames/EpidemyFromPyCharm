import time

import common_data
import frases
import icon_func
import regions_menu
import sizes
import spec_func
import textures
import uix_classes

from kivy.clock import Clock
from kivy.graphics import Color, Instruction, InstructionGroup, Line, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.input.motionevent import MotionEvent


#система кодировки такая: первая координата по горизонатли, вторая по вертикали (причём 1;0 ниже чем 0;0) Начинаем слева сверху
#Приведённая схема верна для России

#start_point_y = 6 #чтобы координаты для y меньше нуля также были бы определены

coords_of_hexes = []
coords_of_centers = []
    
class Widget_Hex2(Widget):   #really all land 
    def __init__(self, **kwargs):
        super(Widget_Hex2, self).__init__(**kwargs)
        global side, height, x_start, y_start
        side = min(1.87*(1-.28)*sizes.Width_of_screen*(1-0.07*common_data.my_stats.is_shown_real_sizes_of_country)/(common_data.my_game.My_Country.sizes[0]), 
                           1.87*sizes.Height_of_screen*(1-0.09*common_data.my_stats.is_shown_real_sizes_of_country)/(common_data.my_game.My_Country.sizes[1]*1.732))
        height = side*1.732        
            
        with self.canvas:
            Color(0.5, 0.5, 0.5, 0.3)
            Color(0.6, 0.8, 0.5, 1)
            
            sizes.SIZE_OF_TEXT_FOR_LABEL = round(height*0.16/50*17.5)
            dx = ((1-.28)*sizes.Width_of_screen*2 - common_data.my_game.My_Country.sizes[0]*side)/2 #.28 is size_hint of left table, *1.8 is because of s2 scale
           
        x_start = side*0.05+0.05*common_data.my_stats.is_shown_real_sizes_of_country*sizes.Width_of_screen + dx 
        y_start = (1.9-0.09*common_data.my_stats.is_shown_real_sizes_of_country)*sizes.Height_of_screen-common_data.my_game.My_Country.dy*height
        Draw_country2(x_start, y_start, side, height)

    
def define_hex(x, y):
    global coords_of_centers, side, height
    optim_hex = 0
    min_dist2 = (x - coords_of_centers[0][0])**2 + (y - coords_of_centers[0][1])**2
    for i in range(1, common_data.my_game.My_Country.number_of_regions):
        dist = (x - coords_of_centers[i][0])**2 + (y - coords_of_centers[i][1])**2

        if dist < min_dist2:
            optim_hex = i
            min_dist2 = dist
    xc = coords_of_centers[optim_hex][0]
    yc = coords_of_centers[optim_hex][1]
    is_hit = True
    #дальше идёт проверка на то, что точка лежит внутри гекса
    #левая нижняя прямая
    x1 = xc-side
    y1 = yc
    x2 = xc-side/2
    y2 = yc-height/2
    y_theor = (x-x1)*(y2-y1)/(x2-x1)+y1
    if y < y_theor:
        is_hit = False

    #левая верхняя прямая
    x1 = xc-side
    y1 = yc
    x2 = xc-side/2
    y2 = yc+height/2
    y_theor = (x-x1)*(y2-y1)/(x2-x1)+y1
    if y > y_theor:
        is_hit = False

    if y > yc+height/2:
        is_hit = False
    #правая верхняя прямая
    x1 = xc+side
    y1 = yc
    x2 = xc+side/2
    y2 = yc+height/2
    y_theor = (x-x1)*(y2-y1)/(x2-x1)+y1
    if y > y_theor:
        is_hit = False
    #правая нижняя прямая
    x1 = xc+side
    y1 = yc
    x2 = xc+side/2
    y2 = yc-height/2
    y_theor = (x-x1)*(y2-y1)/(x2-x1)+y1
    if y < y_theor:
        is_hit = False
    if y < yc-height/2:
        is_hit = False
    return optim_hex, is_hit
    
def scatter_touch_multichoice(self, touch):
       
    xs = common_data.s2.pos[0]
    ys = common_data.s2.pos[1]
    
    x = (touch.pos[0]-xs)/common_data.s2.scale
    y = (touch.pos[1]-ys)/common_data.s2.scale
        
    optim_hex, is_hit = define_hex(x, y)
    if is_hit == False:
        return

    if common_data.my_game.multichoice_list[optim_hex]==0:
        common_data.my_game_frontend.hexes_chosen[optim_hex].show_circle()
        common_data.my_game.list_of_chosen.append(optim_hex)
        common_data.my_game.multichoice_list[optim_hex] = 1
    else:
        common_data.my_game_frontend.hexes_chosen[optim_hex].hide_circle()
        common_data.my_game.list_of_chosen.remove(optim_hex)
        common_data.my_game.multichoice_list[optim_hex] = 0
    
def on_scatter_move(self, touch):
    if self.collide_point(*touch.pos):
        global active_zone
        x = self.pos[0]
        y = self.pos[1]
       
        if x < (sizes.normal_s2_pos_x-active_zone[1][0]*self.scale):
            #print("надо тащить вправо")
            self.pos = (sizes.normal_s2_pos_x-active_zone[1][0]*self.scale, self.pos[1])
        if x > (sizes.Width_of_screen-active_zone[0][0]*self.scale):
            #print("надо тащить влево")
            self.pos = (sizes.Width_of_screen-active_zone[0][0]*self.scale, self.pos[1])
                
        if y < (-active_zone[1][1]*self.scale):
            #print("надо тащить вниз")
            self.pos = (self.pos[0], -active_zone[1][1]*self.scale)
        if y > (sizes.Height_of_screen-active_zone[0][1]*self.scale):
            #print("надо тащить вверх")
            self.pos = (self.pos[0], sizes.Height_of_screen-active_zone[0][1]*self.scale)
        
def on_scatter_touch_down(self, touch):
    if self.collide_point(*touch.pos):
        if common_data.my_game.multichoice_ind == 1:
            scatter_touch_multichoice(self, touch)
        if touch.is_double_tap:
            xs = common_data.s2.pos[0]
            ys = common_data.s2.pos[1]
        
            x = (touch.pos[0]-xs)/common_data.s2.scale
            y = (touch.pos[1]-ys)/common_data.s2.scale
            
            optim_hex, is_hit = define_hex(x, y)
                
            print(optim_hex, is_hit)
            if is_hit == False:
                return
            
            common_data.my_game.is_chosen_only_one = optim_hex        
            for i in range(common_data.my_game.n):
                common_data.my_game_frontend.hexes_chosen[i].hide_circle()
            common_data.my_game_frontend.hexes_chosen[optim_hex].show_circle()
            common_data.my_game.list_of_chosen= [optim_hex]
            common_data.my_game.multichoice_list = [0]*21
            common_data.my_game.multichoice_list[optim_hex] = 1
    
    
            regions_menu.region_menu()  
            common_data.my_game_frontend.hexes_chosen[optim_hex].hide_circle()
            common_data.my_game.list_of_chosen= []
            common_data.my_game.multichoice_list = [0]*21              
            return True            


        
def Draw_hex2 (x, y, side, height, i):       
    
    with common_data.s2.canvas:
        
        Color(0.6, 0.8, 0.5, 1)
        points = (x, y, x-side/2, y+height/2, x, y+height, x+side, y+height, x + 3/2*side, y+height/2, x+side, y)
        #22 к 15 соотношение размеров области карты страны
        if (common_data.my_game.My_Country.sizes[0] / common_data.my_game.My_Country.sizes[1]/1.732 > 1.47): #тогда нормируем на ширину страны
            coef_of_width = 8/common_data.my_game.My_Country.sizes[0]
        else:
            coef_of_width = 3.5/common_data.my_game.My_Country.sizes[1]
        
        Line(points = tuple(points), close = True, 
             width = sizes.Height_of_screen/120*coef_of_width, joint = 'round') 
        
        
        color_of_ti_r = (1, 1, 1, 1)
        color_of_text_input = (.07, .1, .1, 1)
        delta_y = side*0.19
        delta_x = side*0.06

        common_data.my_game_frontend.carta_labels.z_in_label[i] = Hex_par_Label(text = icon_func.letters_to_icons("z_in"), size = (side/3, height*0.16), pos = (x-delta_x, y+height*0.8-delta_y), font_size = sizes.SIZE_OF_TEXT_FOR_LABEL*2.5, 
                                               index = i, color_r = (0.5, 0.3, 0.5, 0.3), parent = 's2', markup = True, 
                                               typ = "z_in")
       
        common_data.my_game_frontend.game_pars.labels.array_of_z_in[i] =  Hex_par_Label(size = (side*0.5+delta_x, height*0.16), pos = (x+side/3-delta_x*0.75, y+height*0.8-delta_y), font_size = sizes.SIZE_OF_TEXT_FOR_LABEL, 
                                                                   text = str(round(common_data.my_game.game_pars.z_ins[i]*common_data.my_game.game_pars.z_ins_dop[i], 3)), parent = 's2',
                                                  index = i, color_r = color_of_ti_r, color = (color_of_text_input[0], color_of_text_input[1], color_of_text_input[2], color_of_text_input[3]),
                                                  typ = "z_in")
        if abs(common_data.my_game.game_pars.z_ins_dop[i] - (common_data.my_game.My_population[i]-common_data.my_game.game_pars.immunated[i])/(common_data.my_game.My_population[i]+1)) > 0.01:
            common_data.my_game_frontend.game_pars.labels.array_of_z_in[i].color = [1,0,0,1]
        
        common_data.my_game_frontend.carta_labels.ill_label[i] = Hex_par_Label(text = icon_func.letters_to_icons("Ill"), parent = 's2', size = (side/3, height*0.16), pos = (x-delta_x, y+height*0.63-delta_y), font_size = sizes.SIZE_OF_TEXT_FOR_LABEL*2.5, 
                                index = i, color_r = (0.3, 0.3, 0.5, 0.3), markup = True,
                                typ = "ill")
        
        common_data.my_game_frontend.game_pars.labels.array_of_ill[i]= Hex_par_Label(parent = 's2', size = (side*0.5+delta_x, height*0.16), pos = (x+side/3-delta_x*0.75, y+height*0.63-delta_y), font_size = sizes.SIZE_OF_TEXT_FOR_LABEL, 
                                                 text = spec_func.tri_sep(common_data.my_game.game_pars.quant_of_ill[i]), 
                                               index = i, color_r = color_of_ti_r, color = (color_of_text_input[0], color_of_text_input[1], color_of_text_input[2], color_of_text_input[3]),
                                               typ = "ill")
        
        if common_data.my_game.game_pars.is_stats_right[i]==False:
            draw_change_points(draw="draw", i=i)
            
        if common_data.my_game.game_pars.is_automatisated[i]==True:
            draw_automatisated(draw="draw", i=i)

        common_data.my_game_frontend.carta_labels.d_in_label[i] = Hex_par_Label(parent = 's2', text = icon_func.letters_to_icons("d_in"), 
                                                                                size = (side/3, height*0.16), pos = (x-delta_x, y+height*0.46-delta_y), 
                                                                                font_size = sizes.SIZE_OF_TEXT_FOR_LABEL*2.5, 
                                                                                index = i, color_r = (0.8, 0.3, 0.5, 0.3), markup = True,
                                                                                typ = "d_in")
        
        common_data.my_game_frontend.game_pars.labels.array_of_d_in[i] = Hex_par_Label(parent = 's2', size = (side*0.5+delta_x, height*0.16), 
                                                                                       pos = (x+side/3-delta_x*0.75, y+height*0.46-delta_y), 
                                                                                       font_size = sizes.SIZE_OF_TEXT_FOR_LABEL, 
                                                                                       text = str(common_data.my_game.game_pars.d_ins[i]*common_data.my_game.game_pars.d_ins_dop[i]),
                                                   index = i, color_r = color_of_ti_r, color = (color_of_text_input[0], color_of_text_input[1], color_of_text_input[2], color_of_text_input[3]),
                                                   typ = "d_in")
        
        if common_data.my_game.game_pars.d_ins_dop[i]!=1:
            common_data.my_game_frontend.game_pars.labels.array_of_d_in[i].color = [1,0,0,1]
        
        common_data.my_game_frontend.carta_labels.dead_label[i] = Hex_par_Label(parent = 's2', text = icon_func.letters_to_icons("Dead"), 
                                                                                size = (side/3, height*0.16), pos = (x-delta_x, y+height*0.29-delta_y), 
                                                                                font_size = sizes.SIZE_OF_TEXT_FOR_LABEL*2.5, 
                                                                                index = i, color_r = (1, 0.2, 0, 0.25), markup = True,
                                                                                typ = "dead")
        common_data.my_game_frontend.game_pars.labels.array_of_dead[i]= Hex_par_Label(parent = 's2', size = (side*0.5+delta_x, height*0.16), pos = (x+side/3-delta_x*0.75, y+height*0.29-delta_y), font_size = sizes.SIZE_OF_TEXT_FOR_LABEL, 
                                                  text = spec_func.tri_sep(common_data.my_game.game_pars.quant_of_dead[i]), 
                                                index = i, color_r = color_of_ti_r, color = (color_of_text_input[0], color_of_text_input[1], color_of_text_input[2], color_of_text_input[3]),
                                                typ = "dead")
        
        common_data.s2.add_widget(common_data.my_game_frontend.game_pars.labels.array_of_z_in[i])
        common_data.s2.add_widget(common_data.my_game_frontend.carta_labels.z_in_label[i])
        
        common_data.s2.add_widget(common_data.my_game_frontend.carta_labels.ill_label[i])
        common_data.s2.add_widget(common_data.my_game_frontend.game_pars.labels.array_of_ill[i]) 
        
        common_data.s2.add_widget(common_data.my_game_frontend.carta_labels.d_in_label[i])
        common_data.s2.add_widget(common_data.my_game_frontend.game_pars.labels.array_of_d_in[i])
        
        common_data.s2.add_widget(common_data.my_game_frontend.carta_labels.dead_label[i])        
        common_data.s2.add_widget(common_data.my_game_frontend.game_pars.labels.array_of_dead[i])        
        
        
       
        
        common_data.my_game_frontend.hexes_chosen[i] = Circle_Multichoice2((x+side*0.9, y+height*0.1), side/30, i, parent = 's2')
    
    common_data.my_game_frontend.circles_situation_in_hexes[i][0] = CircleWidget2(pos=(x+side*0.95+delta_x, y+height*0.87-delta_y), radius = side/20, ind = i, ty = 0, parent = 's2')
    common_data.my_game_frontend.circles_situation_in_hexes[i][1] = CircleWidget2(pos=(x+side*0.95+delta_x, y+height*0.70-delta_y), radius = side/20, ind = i, ty = 1, parent = 's2') 
    common_data.my_game_frontend.circles_situation_in_hexes[i][2] = CircleWidget2(pos=(x+side*0.95+delta_x, y+height*0.53-delta_y), radius = side/20, ind = i, ty = 2, parent = 's2') 
    common_data.my_game_frontend.circles_situation_in_hexes[i][3] = CircleWidget2(pos=(x+side*0.95+delta_x, y+height*0.36-delta_y), radius = side/20, ind = i, ty = 3, parent = 's2')
    common_data.s2.add_widget(common_data.my_game_frontend.circles_situation_in_hexes[i][0]) 
    common_data.s2.add_widget(common_data.my_game_frontend.circles_situation_in_hexes[i][1])
    common_data.s2.add_widget(common_data.my_game_frontend.circles_situation_in_hexes[i][2])
    common_data.s2.add_widget(common_data.my_game_frontend.circles_situation_in_hexes[i][3])
    with common_data.s2.canvas:
        Color(0.3, 1, 1, 1)
        
    if i == common_data.my_game.index_of_capital:
        common_data.my_game_frontend.carta_labels.capital_label = uix_classes.Label_with_tr(text_source = frases.str_capital, size = (side*0.7, height/4), pos = (x, y-side*0.1), font_size = int(14/11*sizes.SIZE_OF_TEXT_FOR_LABEL), bold = True)
             
              
    #common_data.my_game_frontend.carta_labels.region = uix_classes.Label_with_tr(text_source = ["Регион", "Region"], size = (side/3, height/7), pos = (x+side*0.3, y+height*0.85), font_size = round(sizes.SIZE_OF_TEXT_FOR_LABEL)*1.2)
    name_font_size = round(sizes.SIZE_OF_TEXT_FOR_LABEL)*1.2
    add_for_name = 0.3
    if len(common_data.my_game.My_Country.names_of_provinces[i][common_data.common_var.lang]) >= 10:
        add_for_name = 0.28
        name_font_size -= 1 
    if len(common_data.my_game.My_Country.names_of_provinces[i][common_data.common_var.lang]) >= 12:
        add_for_name = 0.25
        name_font_size -= 1
    if len(common_data.my_game.My_Country.names_of_provinces[i][common_data.common_var.lang]) >= 15:
        add_for_name = 0.24
    common_data.my_game_frontend.carta_labels.region = uix_classes.Label_with_tr(text_source = common_data.my_game.My_Country.names_of_provinces[i], size = (side/3, height/7), pos = (x+side*add_for_name, y+height*0.85), 
                                                                                 font_size = name_font_size)
    
    common_data.s2.add_widget(common_data.my_game_frontend.carta_labels.region)
    add_for_hash = 0.735
    if i < 10:
        add_for_hash = 0.75
    common_data.my_game_frontend.carta_labels.number_of_region = Label(text = "#"+str(i), size = (side/3, height/7), pos = (x+side*add_for_hash, y+height*0.85), font_size = name_font_size)
    common_data.s2.add_widget(common_data.my_game_frontend.carta_labels.number_of_region)
        
    common_data.my_game_frontend.game_pars.labels.str_of_naselenie[i] = Label(text = spec_func.tri_sep(common_data.my_game.My_population[i]), size = (side/3, height/7), pos = (x+side*0.2, y+height*0.05), font_size = sizes.SIZE_OF_TEXT_FOR_LABEL)    
        
    if i == common_data.my_game.index_of_capital:        
        common_data.s2.add_widget(common_data.my_game_frontend.carta_labels.capital_label)
        
def redraw_undraw_real_sizes():
    if common_data.my_stats.is_shown_real_sizes_of_country == True:
        common_data.my_stats.is_shown_real_sizes_of_country = False
        common_data.s2.canvas.remove_group("real_sizes")        
        common_data.s2.remove_widget(common_data.my_game_frontend.lab_of_real_sizes_hor)
        common_data.s2.canvas.remove(common_data.my_game_frontend.lab_of_real_sizes_hor.canvas)
        common_data.s2.remove_widget(common_data.my_game_frontend.lab_of_real_sizes_ver)
    else:
        common_data.my_stats.is_shown_real_sizes_of_country = True
          
        with common_data.s2.canvas:
            Color(38/256, 112/256, 110/256, 1)  
            common_data.s2.canvas.add(common_data.s2.line_of_real_sizes_hor)
            common_data.s2.canvas.add(common_data.s2.line_of_real_sizes_ver)
        common_data.s2.add_widget(common_data.my_game_frontend.lab_of_real_sizes_hor)
        common_data.s2.add_widget(common_data.my_game_frontend.lab_of_real_sizes_ver)        


            
def Draw_real_sizes_on_cart(x, y, side, height):
    with common_data.s2.canvas:
        Color(r = 38/256, g = 112/256, b = 110/256, a = 1, group = "real_sizes") 
        global active_zone
        active_zone = [0, 0] 
        active_zone[0] = (x-side*0.7  +side, 
                          y-common_data.my_game.My_Country.ups_by_y*height+height-height*common_data.my_game.My_Country.sizes[1]   +side/2)
        active_zone[1] = (x-side/2+side*common_data.my_game.My_Country.sizes[0]  -side, 
                         y-common_data.my_game.My_Country.ups_by_y*height+1.2*height  -side)
        
        common_data.s2.line_of_real_sizes_hor = Line(points=(x-side/2, 
                                                             y-common_data.my_game.My_Country.ups_by_y*height+1.2*height, 
                                                             x-side/2+side*common_data.my_game.My_Country.sizes[0], 
                                                             y-common_data.my_game.My_Country.ups_by_y*height+1.2*height), 
                                                     width = 5*sizes.Height_of_screen/1000, group = "real_sizes")#ups< 0; 1 height из-за того, что хотим нарисовать сверху гекса
        
        Color(38/256, 112/256, 110/256, 1)    
        common_data.s2.line_of_real_sizes_ver = Line(points=(x-side*0.7, 
                                                             y-common_data.my_game.My_Country.ups_by_y*height+height, 
                                                             x-side*0.7, 
                                                             y-common_data.my_game.My_Country.ups_by_y*height+height-height*common_data.my_game.My_Country.sizes[1]), 
                                                     width = 5*sizes.Height_of_screen/1000, group = "real_sizes")#ups< 0; 1 height из-за того, что хотим нарисовать сверху гекса
    
    common_data.my_game_frontend.lab_of_real_sizes_hor = Label(pos = (common_data.s2.line_of_real_sizes_hor.points[0], common_data.s2.line_of_real_sizes_hor.points[1]+height*0.05), size = (side*common_data.my_game.My_Country.sizes[0], sizes.Height_of_screen/20), 
                     text = str(round(common_data.my_game.My_Country.sizes[0]*common_data.my_game.My_Country.real_size_of_hex/100)*100)+ " km", 
                     font_size = sizes.TEXT_SIZE_OF_COMMON_PAR*1.25)

     
    common_data.my_game_frontend.lab_of_real_sizes_ver = Label(size = (side*1.1, height*common_data.my_game.My_Country.sizes[1]), 
                                                        text = str(100*round(height/side*common_data.my_game.My_Country.sizes[1]*common_data.my_game.My_Country.real_size_of_hex/100)) + " km", font_size = sizes.TEXT_SIZE_OF_COMMON_PAR*1.25, halign = 'right')
    common_data.my_game_frontend.lab_of_real_sizes_ver.pos = (common_data.s2.line_of_real_sizes_ver.points[0]-common_data.my_game_frontend.lab_of_real_sizes_ver.size[0], 
                                                        common_data.s2.line_of_real_sizes_ver.points[1]-common_data.my_game_frontend.lab_of_real_sizes_ver.size[1]) 
    if common_data.my_stats.is_shown_real_sizes_of_country == True:
        common_data.s2.add_widget(common_data.my_game_frontend.lab_of_real_sizes_hor)   
        common_data.s2.add_widget(common_data.my_game_frontend.lab_of_real_sizes_ver)   
    else:
        common_data.s2.canvas.remove_group("real_sizes") 
        

def Draw_country2 (x, y, side, height):
    Draw_real_sizes_on_cart(x, y, side, height)
    global coords_of_hexes, coords_of_centers
    coords_of_hexes = [0]*common_data.my_game.My_Country.number_of_regions
    coords_of_centers = [0]*common_data.my_game.My_Country.number_of_regions
    with common_data.s2.canvas:
            for i in range(common_data.my_game.n):
                coords_of_hexes[i] = [x+3/2*side*common_data.my_game.My_land[i][0]+common_data.my_stats.is_shown_real_sizes_of_country*0.2*side,
                          y-(common_data.my_game.My_land[i][0]%2)*height/2-common_data.my_game.My_land[i][1]*height-common_data.my_stats.is_shown_real_sizes_of_country*0.2*side]
                Draw_hex2(coords_of_hexes[i][0], coords_of_hexes[i][1],
                          side, height, i)
                coords_of_centers[i] = [coords_of_hexes[i][0] + side/2, coords_of_hexes[i][1] + height/2]
                
class CircleWidget2(Widget):
    def __init__(self, radius, ind, ty, parent = 's2', **kwargs):
        super().__init__(**kwargs)
        
        self.index  = ind
        self.ty = ty
        self.points = self.pos
        self.r = min(common_data.my_game.situation_in_hexes[self.index][self.ty], 1)
        self.g = 1- min(common_data.my_game.situation_in_hexes[self.index][self.ty],1)
        self.radius = radius
        
        self.l2 = None
            
        with self.canvas:
            
            Color(self.r, self.g , 0, 1)
            self.l = Line(circle= (self.points[0], self.points[1], self.radius), width = self.radius)
            if common_data.my_game.situation_in_hexes[self.index][self.ty]**2>=1 and (ty == 1 or ty ==3):
                Color(.5,0,.8,1)
                Line(circle= (self.points[0], self.points[1], self.radius/10*common_data.my_game.situation_in_hexes[self.index][self.ty]), 
                     width = self.radius/10*common_data.my_game.situation_in_hexes[self.index][self.ty])        
        self.update_color()
    def update_color(self):
        self.canvas.remove(self.l)
        with self.canvas:
            Color(min(common_data.my_game.situation_in_hexes[self.index][self.ty], 1), 1-min(common_data.my_game.situation_in_hexes[self.index][self.ty], 1) ,0,1)    
            self.l = (Line(circle= (self.points[0], self.points[1], self.radius), width = self.radius)) 
            if self.l2 in self.canvas.children:
                self.canvas.remove(self.l2)
                
        if common_data.my_game.region_straphs[self.index][self.ty]>=1 and self.ty in {1, 3}:
            
            if hasattr(self, "label_straph_b"):
                self.label_straph_b.text = str(common_data.my_game.region_straphs[self.index][self.ty])
                if self.label_straph_b not in self.children:
                    self.add_widget(self.label_straph_b)
                if common_data.my_game.game_pars.is_stats_right[self.index] == True and self.label_straph_b.color != (.5, 0, .8, 1):
                    self.label_straph_b.color = (.5, 0, .8, 1)
                elif common_data.my_game.game_pars.is_stats_right[self.index] == False:
                    self.label_straph_b.color = (.2, 1, .2, 1)
            else:
                if common_data.my_game.game_pars.is_stats_right[self.index] == True:
                    color_straph = (.5, 0, .8, 1)
                else:
                    color_straph = (.2, 1, .2, 1)
                self.label_straph_b = Label(text = str(common_data.my_game.region_straphs[self.index][self.ty]), halign = 'left', 
                                            pos = [self.pos[0]+self.radius*1.7, self.pos[1]+self.radius*1.9], size = (self.radius*0.8, self.radius),
                                            font_size = 15, color = color_straph)
                self.add_widget(self.label_straph_b)
                
            with self.canvas:
                
                Color(.5, 0, .8, 1)
                self.l2 = Line(circle= (self.points[0], self.points[1], min(self.radius/8*common_data.my_game.situation_in_hexes[self.index][self.ty], self.radius*1.2)), 
                               width = min(self.radius/8*common_data.my_game.situation_in_hexes[self.index][self.ty], self.radius*1.2))        
        
        elif (self.ty==1 or self.ty==3):#если надо удалять штрафную вывеску, т.к. штрафных баллов нет
            if hasattr(self, "label_straph_b"):
                if self.label_straph_b in self.children:
                    self.label_straph_b.canvas.clear()
                    del self.label_straph_b
                                     

class Circle_Multichoice2(Line):
    def __init__(self, poi, radius, ind, parent = 's', **kwargs):
        super(Circle_Multichoice2).__init__(**kwargs)
        
        self.widget_parent = 0
        
        if parent == 's2':
            self.widget_parent = common_data.s2    
        self.index  = ind
        self.points = poi
        self.b = 1
        self.radius = radius
        
        Color(0, 0, 0, 1)
        self.l = Line(circle= (self.points[0], self.points[1], self.radius), width = self.radius)
        if common_data.my_game.multichoice_list[self.index] == 1:
            self.show_circle() 
    
    def show_circle(self):
        self.widget_parent.canvas.remove(self.l)
        with self.widget_parent.canvas:
            Color(0, 1, 1, 1)   
            self.l = (Line(circle= (self.points[0], self.points[1], self.radius), width = self.radius)) 
    def hide_circle(self):
        self.widget_parent.canvas.remove(self.l)
        with self.widget_parent.canvas:
            Color(0, 0, 0, 1)   
            self.l = (Line(circle= (self.points[0], self.points[1], self.radius), width = self.radius))    
            
            
         
class Hex_par_Label(Label):

    def __init__(self, index, color_r, typ, parent = 's', type_of_icon = "none",  **kwargs):
        super(Hex_par_Label, self).__init__(**kwargs)  
        self.index = index #number_of_region
        self.typ = typ #z_in, d_in, ill, dead
        self.widget_parent = 0
        
        if parent == 's2':
            self.widget_parent = common_data.s2
        with self.widget_parent.canvas:
            Color(color_r[0], color_r[1], color_r[2], color_r[3])
            Rectangle(pos=self.pos, size=self.size, texture = textures.tex_ramka)
     
        self.was_touch = False
        
    def do_make_graph(self, dt):
    
        vec = [common_data.s2.pos[0]-self.down_s2_pos[0], 
               common_data.s2.pos[1]-self.down_s2_pos[1]]
    
        if vec[0]**2+vec[1]**2 < 1000:
            self.go_to_graph()
       
                
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.was_touch == True:
            try:
                self.graph_event.cancel()
            except:
                print("Event was cancelled earlier")
            
            self.was_touch = False
            
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
        
            self.was_touch = True 
           
            self.down_s2_pos = tuple(common_data.s2.pos)
            if common_data.my_game.multichoice_ind == -1 or self.typ!="z_in":
                self.graph_event = Clock.schedule_once(self.do_make_graph, timeout=1.5)
    
            return super(Hex_par_Label, self).on_touch_down(touch)
        
    def go_to_graph(self):
        common_data.my_game.is_chosen_only_one = self.index
        regions_menu.graph_maker.make_graph(typ = self.typ)
       
            
def draw_carantine(x=0, y=0, side=100, height=100, draw = "draw"):
    
    
    if draw == "undraw":
        common_data.s2.canvas.remove_group("carant")    
    if draw == "draw":
        with common_data.s2.canvas:
            
            points = (x, y, x-side/2, y+height/2, x, y+height, x+side, y+height, x + 3/2*side, y+height/2, x+side, y)
            
            center = [x+side/2, y+height/2]
            k = 0.93        
            new_points = [0]*12
            for j in range (len(points)):
                new_points[j] = center[j%2]*(1-k)+k*points[j]
               
            Color(1, 0.2, 0.5, 1, group = "carant")    
            
            Line(points = tuple(new_points), close = True, 
                width = 1, dash_length = 20, dash_offset = 10, group = "carant") 
            


def draw_change_points(draw = "draw", i = 0):
    global side
    global height
    global coords_of_hexes
    x = coords_of_hexes[i][0]
    y = coords_of_hexes[i][1]
    
    if draw == "draw":
        with common_data.s2.canvas:
            Color(.5, 0, .8, .3, group = "change_points")
            rec = Rectangle(size = (side/6.5, side/6.5), pos=(x+side*1.23-side*0.06*0.75, y+height*0.585-side*0.19), group = "change_points")
            common_data.my_game_frontend.change_points_labs[i] = Label(text = str(common_data.my_game.parameters_of_tech[21][2][0]), 
                                                                       pos = rec.pos, size = rec.size, font_size = sizes.SIZE_OF_TEXT_FOR_LABEL*1.45, 
                                                                       color = (217/256, 172/256, 26/256), halign = 'center')
            common_data.s2.add_widget(common_data.my_game_frontend.change_points_labs[i])
            
    elif draw == "undraw":
        common_data.s2.canvas.remove_group("change_points")
        common_data.s2.remove_widget(common_data.my_game_frontend.change_points_labs[i])
        common_data.my_game_frontend.change_points_labs[i].canvas.clear()

def draw_automatisated(draw = "draw", i = 0):
    global side
    global height
    global coords_of_hexes
    x = coords_of_hexes[i][0]
    y = coords_of_hexes[i][1]
    
    if draw == "draw":
        with common_data.s2.canvas:
            Color(97/256, 93/256, 40/256, .3, group = "autom")
            #Color(.5, 0, .8, .3, group = "autom")
            rec = Rectangle(size = (side/6.5, side/6.5), pos=(x-side*0.28-side*0.06*0.75, y+height*0.585-side*0.19), group = "autom")
            common_data.my_game_frontend.autom_labs[i] = Label(text = str("A"), pos = rec.pos, size = rec.size, font_size = sizes.SIZE_OF_TEXT_FOR_LABEL*1.45, color = (16/256, 185/256, 232/256), halign = 'center')
            common_data.s2.add_widget(common_data.my_game_frontend.autom_labs[i])
            
    elif draw == "undraw":
        common_data.s2.canvas.remove_group("autom")
        common_data.s2.remove_widget(common_data.my_game_frontend.autom_labs[i])
        common_data.my_game_frontend.autom_labs[i].canvas.clear()