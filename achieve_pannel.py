from kivy.clock import Clock
from kivy.graphics import Canvas, Color, Rectangle, Triangle 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from custom_kivy.my_scrollview import ScrollView

import common_data as cd
import common_var
import country_variants
import diseases
import icon_func
import sizes
import spec_func
import tech_info
import uix_classes

def custom_log(x):
    return (x**0.56)*2

class Achieve_pannel(FloatLayout):
    def __init__(self, size_of_rec = (50*sizes.width_res/1100, 10000*sizes.height_res/780), max_value = 10000, 
                 points = [cd.stats.goldreserves], text_sources = [
                                                        ["У Вас: " + str(cd.stats.goldreserves) + " монет",
                                                        "You have: " + str(cd.stats.goldreserves) + " coins"]
                                                        ],
                types = ["mine"], type_of_pannel = "gold",
                                                            
                **kwargs): 
        super(Achieve_pannel, self).__init__(**kwargs)
        is_above = [True]
        #values are normalized
        self.size_hint = (None, None)
        self.size = (sizes.width_res, size_of_rec[1]*1.03)
        with self.canvas:
            #Color(.9, .8, .5,1)
            if type_of_pannel == 'gold':
                Color(.15, .22, .42)
            elif type_of_pannel == 'stars':
                Color(.15, .22, .42)
            self.bar_rec = Rectangle(size = size_of_rec, pos = (sizes.width_res/7, self.size[1]*0.005))
            
        max_value = custom_log(max_value)
        
        if type_of_pannel == "gold":
            
            for i in range(len(common_var.statuses_coins)):
                points.append(common_var.thresh_hold_coins[i])
                text_sources.append(common_var.statuses_coins[i])
                types.append("coins_status")
              
                is_above.append(True)
            for i in range(len(country_variants.Country_lands)):
                if country_variants.Country_lands[i].min_goldreserves > 0:
                    points.append(country_variants.Country_lands[i].min_goldreserves)
                    text_sources.append(["Новая страна: "+ country_variants.Country_lands[i].name[0],
                                        "New country: " + country_variants.Country_lands[i].name[1]])
                    types.append("new_country")      
                    is_above.append(True)
            for i in range(len(tech_info.min_goldreserves_for_tech)):
                if tech_info.min_goldreserves_for_tech[i] > 0:
                    points.append(tech_info.min_goldreserves_for_tech[i])
                    text_sources.append(["Метод: " + tech_info.names_of_tech[i][0],
                                        "Method: " + tech_info.names_of_tech[i][1]])
                    types.append("new_tech")      
                    is_above.append(True)
            for i in diseases.diseases_list:
                if i.min_gold > 0 and i.name[0]!="Неизвестная инфекция":
                    points.append(i.min_gold)
                    text_sources.append(["Инфекция: " + i.name[0],
                                        "Infection: " + i.name[1]])
                    types.append("new_disease")      
                    is_above.append(True)
            
            
        elif type_of_pannel == "stars":
            for i in range(len(common_var.stars_statuses)):
                points.append(common_var.thresh_hold_stars[i])
                text_sources.append(common_var.stars_statuses[i])
                types.append("stars_status")      
                
                is_above.append(True)
            for i in range(len(country_variants.Country_lands)):
                if country_variants.Country_lands[i].min_rep_stars > 0:
                    points.append(country_variants.Country_lands[i].min_rep_stars)
                    text_sources.append(["Новая страна: "+ country_variants.Country_lands[i].name[0],
                                        "New country: " + country_variants.Country_lands[i].name[1]])
                    types.append("new_country")      
                    is_above.append(True)    
            for i in range(len(tech_info.min_stars_for_tech)):
                if tech_info.min_stars_for_tech[i] > 0:
                    points.append(tech_info.min_stars_for_tech[i])
                    text_sources.append(["Метод: " + tech_info.names_of_tech[i][0],
                                        "Method: " + tech_info.names_of_tech[i][1]])
                    types.append("new_tech")      
                    is_above.append(True)
            
            
        
            
        real_achieve_points_coords = [0]*len(points)    
        for i in range(len(points)):
            real_achieve_points_coords[i] = self.bar_rec.pos[1]+self.bar_rec.size[1] - custom_log(points[i])/max_value*self.bar_rec.size[1]
        
        min_to_last_goal = 10000000000
        min_to_next_goal = 10000000000
        ind_of_next = 100000000000
        for i in range(1, len(points)):
            delta = real_achieve_points_coords[i]-real_achieve_points_coords[0]
            if -delta < min_to_next_goal and delta <= 0: 
                min_to_next_goal = -real_achieve_points_coords[i]+real_achieve_points_coords[0]
                ind_of_next = i
            if delta < min_to_last_goal and delta > 0: 
                min_to_last_goal = real_achieve_points_coords[i]-real_achieve_points_coords[0]
        
        if min_to_last_goal <= min_to_next_goal and min_to_next_goal < 100000:#canvas works naoborot
            is_above[0] = False
            
        if ind_of_next < 1000000000:
            is_above[ind_of_next] = False
        
        for i in range(len(points)):
            with self.canvas:
                if types[i] == "mine":
                    
                    Color(.2, .5, .6, 1)
                    self.mine_coord_hint = custom_log(points[i])/max_value
                    self.point_rec = Rectangle(size = (size_of_rec[0]*1.2, 
                                                  (custom_log(self.bar_rec.size[1]/50))), 
                                           pos = (self.bar_rec.pos[0]-size_of_rec[0]*0.1, real_achieve_points_coords[i]))
            
                    self.point_rec.pos = (self.point_rec.pos[0], 
                                      self.point_rec.pos[1] - self.point_rec.size[1]/2)
                    Arrow_with_text(parent = self, text_source = text_sources[i],
                                    pos_of_ar = (self.bar_rec.pos[0] + self.bar_rec.size[0]*3/4, real_achieve_points_coords[i]),
                                    width = 300*sizes.width_res/1200, is_text_above = is_above[i])                    
            
                elif types[i] == "coins_status":
                    
                    Line_with_text(parent = self, text_source = text_sources[i], typ = types[i],
                            pos_of_ar = (self.bar_rec.pos[0] + self.bar_rec.size[0]*3/4, real_achieve_points_coords[i]),
                            is_text_above = is_above[i])
                elif types[i] == "stars_status":
                    
                    Line_with_text(parent = self, text_source = text_sources[i], typ = types[i], 
                            pos_of_ar = (self.bar_rec.pos[0] + self.bar_rec.size[0]*3/4, real_achieve_points_coords[i]),
                            is_text_above = is_above[i]) 
                elif types[i] in {"new_country", "new_tech", "new_disease"} :
                    
                    Line_with_text(parent = self, text_source = text_sources[i], typ = types[i], 
                            pos_of_ar = (self.bar_rec.pos[0] + self.bar_rec.size[0]*3/4, real_achieve_points_coords[i]),
                            is_text_above = is_above[i])                 
        
            
class Arrow_with_text():
    def __init__(self, parent, pos_of_ar = (0,0), text_source = ["Test_text" , "Test_text"],  
                 width = 300*sizes.width_res/1200, height_of_cap = 15*sizes.height_res/700, width_of_cap = 60*sizes.width_res/1200,  
                 height_of_line = 7*sizes.height_res/700, is_text_above = True,
                 **kwargs): 
        super(Arrow_with_text, self).__init__(**kwargs) 
        self.parent = parent
        with self.parent.canvas.after:
            Color(135/256, 16/256, 16/256, 1)
            Triangle(points = [pos_of_ar[0], pos_of_ar[1], 
                               pos_of_ar[0]+width_of_cap, pos_of_ar[1] + height_of_cap/2,
                               pos_of_ar[0]+width_of_cap, pos_of_ar[1] - height_of_cap/2]
                     )
            self.rec = Rectangle(pos = (pos_of_ar[0]+width_of_cap, pos_of_ar[1]-height_of_line/2), 
                      size = (width - width_of_cap, height_of_line))
            
        self.parent.text_lab = uix_classes.Label_with_tr(text_source = text_source, 
                                                         pos = (pos_of_ar[0]+width_of_cap, 
                                                                pos_of_ar[1]+height_of_line*1.5),
                                                         
                                                         size = (width - width_of_cap, height_of_line*5), color = (1,1,1,1),
                                                         font_size = sizes.ACHIEVE_SIZE, 
                                                         halign = 'center',  valign = 'bottom', markup = True,
                                                         text_size = (width - width_of_cap, height_of_line*7),
                                                         size_hint = [None, None])
        if is_text_above == False:
            self.parent.text_lab.pos[1] = self.rec.pos[1]-height_of_line*4.5
            self.parent.text_lab.valign = 'top'
            
        self.parent.add_widget(self.parent.text_lab, canvas = 'after')
        
        


class Line_with_text():
    def __init__(self, parent, pos_of_ar = (0,0), text_source = ["Test_text" , "Test_text"],  
                 width = 350*sizes.width_res/1200, height_of_line = 7*sizes.height_res/700, typ = 'gold_status', 
                 is_text_above = True,
                 **kwargs):
        
        super(Line_with_text, self).__init__(**kwargs)    
        self.parent = parent
        with self.parent.canvas:
            if typ == 'coins_status':
                Color(.98, .77, .01)
            elif typ == 'stars_status':
                Color(20/256,186/256,219/256)
            elif typ == 'new_country':
                Color(36/256,219/256,20/256)   
            elif typ == 'new_tech':
                Color(256/256, 0/256, 66/256, 1)
            elif typ == 'new_disease':
                Color(237/256, 19/256, 19/256, 1)
           
            self.rec = Rectangle(pos = (pos_of_ar[0], pos_of_ar[1] - height_of_line/2), 
                      size = (width, height_of_line))
            
        self.parent.text_lab = uix_classes.Label_with_tr(text_source = text_source, 
                                                         pos = [self.rec.pos[0]+width*0.1, 
                                                                self.rec.pos[1]+self.rec.size[1]+height_of_line*2],
                                                         
                                         size = (width*.8, height_of_line*7), color = (1,1,1,1),
                                         font_size = sizes.ACHIEVE_SIZE,
                                         text_size = (width, height_of_line*10),
                                         halign = 'center', valign = 'bottom', 
                                         size_hint = [None, None])
        if is_text_above == False:
            self.parent.text_lab.pos[1] = self.rec.pos[1]-self.rec.size[1]-height_of_line*7.5
            self.parent.text_lab.valign = 'top'
        
        self.parent.add_widget(self.parent.text_lab)
        


class Achieve_Layout(FloatLayout):
    def __init__(self, **kwargs):
        super(Achieve_Layout, self).__init__(**kwargs) 
        self.size_hint = [1, 1] 
        
        self.init_gold_pannel()
        self.init_stars_pannel()
        self.add_widget(uix_classes.Label_with_tr(text_source=["Шкала благосостояния:", 
                                                               "Scale of wealth:"], 
                                                  size_hint = (.5, .1), pos_hint = {'right':.5, 'top':.96}, halign = 'center',
                                      font_size = (sizes.width_res/50)))
        
        self.add_widget(uix_classes.Label_with_tr(text_source=["Шкала репутации:", 
                                                               "Scale of reputation:"], 
                                                  size_hint = (.5, .1), pos_hint = {'right': .98, 'top':.96}, halign = 'center',
                                      font_size = (sizes.width_res/50)))
        
        self.btn_close_pannel = uix_classes.Button_with_image(text_source = ["Закрыть панель", "Close bar"],
                                                           on_press = self.close_layout, font_size = (sizes.width_res/50),
                                                           halign = 'center',
                                                           size_hint = (2/9, .15), pos_hint = {'right': .5+1/9, 'top':.96})
        self.add_widget(self.btn_close_pannel)
        
    def update_content(self):
        self.achieve_pan_gold.clear_widgets()
        self.achieve_pan_gold.canvas.clear()
        self.achieve_pan_gold.parent.remove_widget(self.achieve_pan_gold)
        del self.achieve_pan_gold
        self.achieve_pan_gold = Achieve_pannel(max_value = 8000,
                                               points = [cd.stats.goldreserves], text_sources = [
                                                        [icon_func.add_money_icon("У Вас: " + str(cd.stats.goldreserves), 
                                                                                  sizes.ACHIEVE_SIZE),
                                                        icon_func.add_money_icon("You have: " + str(cd.stats.goldreserves),
                                                                                 sizes.ACHIEVE_SIZE)]
                                                        ], types = ["mine"], type_of_pannel = "gold")
        #self.achieve_pan.bind(height = self.achieve_pan.setter('height'))
        self.achieve_scroll_gold.add_widget(self.achieve_pan_gold)
        
        self.achieve_pan_stars.clear_widgets()
        self.achieve_pan_stars.canvas.clear()
        self.achieve_pan_stars.parent.remove_widget(self.achieve_pan_stars)
        del self.achieve_pan_stars
        self.achieve_pan_stars = Achieve_pannel(max_value = 5000,
                                                points = [cd.stats.stars], text_sources = [
                                                        [icon_func.add_star_icon("У Вас: " + str(cd.stats.stars),
                                                                                 sizes.ACHIEVE_SIZE),
                                                        icon_func.add_star_icon("You have: " + str(cd.stats.stars),
                                                                                sizes.ACHIEVE_SIZE)]
                                                        ], types = ["mine"], type_of_pannel = "stars")
        #self.achieve_pan.bind(height = self.achieve_pan.setter('height'))
        self.achieve_scroll_stars.add_widget(self.achieve_pan_stars)
            
    def init_gold_pannel(self):
        self.achieve_scroll_gold = ScrollView(do_scroll_x = False, size_hint = (None, None),
                                         size = (sizes.width_res/2, sizes.height_res*0.8), 
                                         pos = (0, sizes.height_res*0.04),
                               scroll_type = ['bars', 'content'], bar_width = 8, bar_margin = 10, bar_pos_y = 'left')
        
        self.achieve_pan_gold = Achieve_pannel(max_value = 5500,
                                               points = [cd.stats.goldreserves], text_sources = [
                                                        [icon_func.add_money_icon("У Вас: " + str(cd.stats.goldreserves), 
                                                                                  sizes.ACHIEVE_SIZE),
                                                        icon_func.add_money_icon("You have: " + str(cd.stats.goldreserves),
                                                                                 sizes.ACHIEVE_SIZE)]
                                                        ], types = ["mine"], type_of_pannel = "gold")
        #self.achieve_pan.bind(height = self.achieve_pan.setter('height'))
        self.achieve_scroll_gold.add_widget(self.achieve_pan_gold)
        self.add_widget(self.achieve_scroll_gold)       
    def init_stars_pannel(self):
        self.achieve_scroll_stars = ScrollView(do_scroll_x = False, size_hint = (None, None),
                                         size = (sizes.width_res/2, sizes.height_res*0.8), 
                                         pos = (sizes.width_res/2, sizes.height_res*0.04),
                               scroll_type = ['bars', 'content'], bar_width = 8, bar_margin = 10)
        
        self.achieve_pan_stars = Achieve_pannel(max_value = 3000,
                                                points = [cd.stats.stars], text_sources = [
                                                        [icon_func.add_star_icon("У Вас: " + str(cd.stats.stars),
                                                                                 sizes.ACHIEVE_SIZE),
                                                        icon_func.add_star_icon("You have: " + str(cd.stats.stars),
                                                                                sizes.ACHIEVE_SIZE)]
                                                        ], types = ["mine"], type_of_pannel = "stars")
        #self.achieve_pan.bind(height = self.achieve_pan.setter('height'))
        self.achieve_scroll_stars.add_widget(self.achieve_pan_stars)
        self.add_widget(self.achieve_scroll_stars)       
        
    def open_layout(self, instance=None):
        self.update_content()
      
        self.outer_folders = []
        for i in cd.final_layout.children:
            self.outer_folders.append(i)
            
        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(self)
        self.achieve_scroll_gold.scroll_y = max(1 - self.achieve_pan_gold.mine_coord_hint, 0)
        self.achieve_scroll_stars.scroll_y = max(1 - self.achieve_pan_stars.mine_coord_hint, 0)
        
    def close_layout(self,instance):
        cd.final_layout.remove_widget(self)
        for i in self.outer_folders:
            cd.final_layout.add_widget(i)  
        #for i in self.children:
         #   del i

achieve_p = Achieve_Layout()