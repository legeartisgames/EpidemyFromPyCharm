import common_data
import common_var
import sizes
import spec_func 

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image as UImage
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
current_graph = None

import io


plt = None
datetime = None
mdates = None

import numpy as np
class Graph_shower(FloatLayout):
    def __init__(self, database = None, text_of_title = ["empty", "empty"], typ = 'typ?', for_country = False, **kwargs): 
        super(Graph_shower, self).__init__(**kwargs)
        global current_graph
        if current_graph != None:
            del current_graph
        current_graph = self
    
        self.text_of_title = text_of_title
        self.typ = typ
        self.database = eval(database)
        self.for_country = for_country
        self.size_hint = [1, 1]
        
        
    def make_graph(self, dt):
           
        
        global datetime, plt, current_graph, mdates
        
        if datetime == None:
            import datetime
        if plt == None:
            import matplotlib.pyplot as plt  
            import matplotlib.dates as mdates

        marker_size = 15
        x = list()
        y = list()
        
    
        x = [i for i in range(len(self.database))]
            
        if len(common_data.my_game.list_of_chosen) > 1 or self.for_country == True:
            print("Warning with graph: not one region (may be graph for total country?)")
            y = list(self.database)
        else:
            y = [self.database[i][common_data.my_game.is_chosen_only_one] for i in range(len(self.database))]     
            
        if len(x)!=1:
            marker_size = 0
        
        figsize = (16, 9)
        plt.figure(num=None, figsize = figsize, facecolor='w', edgecolor='k', dpi = 100)    
        figure = plt.subplot() 
        
        lw = 7*figsize[0]/16
        if len(x) > 70:
            lw = 6*figsize[0]/16 
        
        if len(x) == 1:
            figure.plot(x, y, '-o', linewidth = lw, markersize = marker_size, color = 'r') 
        else:
            if self.typ == 'pen_points_sum':
                figure.plot(x, y, '-o', linewidth = lw, markersize = marker_size, color='#d1151e') 
            else:
                figure.plot(x, y, '-o', linewidth = lw, markersize = marker_size) 
        
        if len(x) == 0:
            self.text_of_title+=["\n(пока нет данных)", "\n(we have no data yet)"][common_var.lang]
        
        text_size_of_title = 30*figsize[0]/16
        plt.title(self.text_of_title, y = 1.05, fontsize = text_size_of_title)
        
        text_size_of_tick = 23*figsize[0]/16
        for tick in figure.xaxis.get_major_ticks() + figure.yaxis.get_major_ticks():
            tick.label.set_fontsize(text_size_of_tick) 
        
        figure.ticklabel_format(axis = 'y', style='plain')#чтобы не было 1e10
        yloc = plt.MaxNLocator(7)
        figure.yaxis.set_major_locator(yloc) 
        
        '''if len(x) >= 4 or len(x) == 1:
            if len(x) > 1:
                xloc = plt.MaxNLocator(min(8, len(x)+2))
                figure.xaxis.set_major_formatter(mdates.DateFormatter('%b, %Y'))#названия месяцев
            else:
                sd = common_data.my_game.My_disease.start_date
                sd_pre = spec_func.month_back(sd)
                sd_pre = spec_func.month_back(sd_pre)
                sd_fut = spec_func.two_weeks_go(sd)
                sd_fut = spec_func.two_weeks_go(sd_fut)
                plt.xlim([datetime.date(year=sd_pre[2], month = sd_pre[1], day = 1), 
                          datetime.date(year=sd_fut[2], month = sd_fut[1], day = 1)])
                plt.ylim([y[0]*0.9, y[0]*1.1])
                xloc = plt.MaxNLocator(6)
                figure.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))#названия месяцев
            
        elif len(x) == 3:
            xloc = mdates.WeekdayLocator(interval=2)#шаг по 2 недели
            figure.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
            
        elif len(x) > 1 and len(x) < 3:
            xloc = mdates.WeekdayLocator()
            figure.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
        
        elif len(x) == 0:
            xloc = plt.MaxNLocator(8)
        
        figure.xaxis.set_major_locator(xloc)  
        plt.gcf().autofmt_xdate()'''
                        
        for axis in ['top','bottom','left','right']:
            figure.spines[axis].set_linewidth(2*figsize[0]/16)        
        
        figure.tick_params(axis='both', which='major', pad=11*figsize[0]/16)
    
        
        color_theme = 'gainsboro'
        figure.tick_params(axis='x', colors=color_theme)
        figure.tick_params(axis='y', colors=color_theme)
        figure.yaxis.label.set_color(color_theme)
        figure.xaxis.label.set_color(color_theme)
        figure.title.set_color(color_theme)
        figure.spines['bottom'].set_color(color_theme)
        figure.spines['left'].set_color(color_theme)
        figure.spines['right'].set_color(color_theme)
        figure.spines['top'].set_color(color_theme)
        
        figure.grid(True, color = 'dimgray', linewidth = 1.5*figsize[0]/16, linestyle = 'dashed')
        
        plt.tight_layout()
        
        labels = [item.get_text() for item in figure.get_yticklabels()]
        
        if len(y) > 0 and max(y) > 10**9:
    
            for i in range(1, len(labels)):
                labels[i] = float(labels[i])
                labels[i]/=10**9
            if [int(j) for j in labels[1:]] == labels[1:]:
                labels2 = [0]*len(labels)
                for i in range(len(labels)):
                    if i!=0:
                        labels2[i] = int(labels[i])
                    else:
                        labels2[i]= labels[i]
                labels = labels2
    
            for i in range(1, len(labels)):      
                if labels[i] == 0:
                    labels[i] = '0'
                else:
                    labels[i] = str(labels[i]) + ([' млрд.', 'G'][common_var.lang])       
        
        elif len(y) > 0 and max(y) > 10**6:
            
            for i in range(1, len(labels)):
                labels[i] = float(labels[i])
                labels[i]/=10**6
            if [int(j) for j in labels[1:]] == labels[1:]:
                labels2 = [0]*len(labels)
                for i in range(len(labels)):
                    if i!=0:
                        labels2[i] = int(labels[i])
                    else:
                        labels2[i]= labels[i]
                labels = labels2
                
            for i in range(1, len(labels)):      
                if labels[i] == 0:
                    labels[i] = '0'
                else:
                    labels[i] = str(labels[i]) + ([' млн.', 'M'][common_var.lang])       
        elif len(y) > 0 and max(y) > 1000:
            for i in range(1, len(labels)):
                labels[i] = float(labels[i])
                labels[i]/=1000
            
            if [int(j) for j in labels[1:]] == labels[1:]:
                labels2 = [0]*len(labels)
                for i in range(len(labels)):
                    if i!=0:
                        labels2[i] = int(labels[i])
                    else:
                        labels2[i]= labels[i]
                labels = labels2
            for i in range(1, len(labels)):
                if labels[i] == 0:
                    labels[i] = '0'
                else:
                    labels[i] = str(labels[i]) + [' тыс.', 'K'][common_var.lang]
                
        ylabels = labels
        figure.set_yticklabels(ylabels)
        
        s_month = common_data.my_game.My_disease.start_date[1]-1#путаница: start_date меряет месяцы от 1 до 12, а мы тут от 0 до 11
        s_year = common_data.my_game.My_disease.start_date[2]
        if self.typ != 'z_in':
            s_month+=1
            if s_month == 12:
                s_month = 0
                s_year +=1
            
        if len(x) < 7:
            xticks=[i for i in range(len(x))]
            figure.set_xticks(xticks)
        elif len(x) < 14:
            xticks=[(2*i-(s_month%2)) for i in range(len(x)//2+len(x)%2)]
            figure.set_xticks(xticks)
        elif len(x) < 20:
            xticks=[(3*i-(s_month%3)) for i in range(len(x)//3+(len(x)%3>0))]
            figure.set_xticks(xticks)
        elif len(x) < 36:
            xticks=[(6*i-(s_month%6)) for i in range(len(x)//6+1)]
            figure.set_xticks(xticks)
        else:
            xticks=[(12*i-(s_month%12)) for i in range(len(x)//12+1)]
            figure.set_xticks(xticks)
                
        
        
        names_ru = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        names_en = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        names = [names_ru, names_en][common_var.lang]
        xtickslabels = []
        for i in xticks:
            st = (names[(i+s_month)%12]+', ')*(len(x)<36)+str(s_year+(i+s_month)//12)
            xtickslabels.append(st)
        #labelsx = [item.get_text() for item in figure.get_xticklabels()]
        #print(labelsx)
        #labelsx[1] = 'Testing'
        figure.set_xticklabels(xtickslabels)
        if len(x)<36:
            plt.xticks(rotation=20)
        
        plt.tight_layout()
        self.graph = plt.gcf()
        
        #сохраяем график в буфер
        buf = io.BytesIO()
        self.graph.savefig(buf, edgecolor = 'b', transparent = True, dpi = 100)
        buf.seek(0)
   
        imgData = io.BytesIO(buf.read())
          
        self.graph_texture = CoreImage(imgData, ext='png').texture 
        self.graph_im = UImage(texture = self.graph_texture, size_hint = [.9, .9], pos_hint = {'center_x': .5, 'center_y': .5}, allow_stretch = True)
        
        self.add_widget(self.graph_im)
        
        if self.lab_loading in self.children:
            self.remove_widget(self.lab_loading)
        
    def open(self, instance):
        self.outer_folders = []
        for i in common_data.final_layout.children:
            self.outer_folders.append(i)
        common_data.final_layout.clear_widgets()
        common_data.final_layout.add_widget(self)   
        self.lab_loading = Label(text = ["Строим график... (подождите пару секунд)\nВ первый раз график будет строиться медленнее", "Buiding graph in progress... (wait ~ 2-3 sec)\nFor the first time it may be slower"][common_var.lang],
                                 font_size = sizes.WIN_SIZE*1.2)
        self.add_widget(self.lab_loading)
        Clock.schedule_once(self.make_graph, 0.03)
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap == True:
                self.close(instance=5)
    
    def close (self, instance):
        common_data.final_layout.remove_widget(self)
        for i in self.outer_folders:
            common_data.final_layout.add_widget(i)  
        




def make_graph(typ, for_country = False):
    type = typ
    print('graph type: ', type)
    text_of_title = ''
    database = []
    reg_ind = common_data.my_game.is_chosen_only_one
    name_ru = common_data.my_game.My_Country.names_of_provinces[reg_ind][0]
    name_en = common_data.my_game.My_Country.names_of_provinces[reg_ind][1]
    if type =='ill':
      
        database = 'common_data.my_game.archieve_quant_of_ill'
        text_of_title = ['Больные '+common_data.my_game.My_disease.padezhi[4]+' в регионе №'+ str(reg_ind) + ' ('+name_ru+')', 
                         'Sick with ' +common_data.my_game.My_disease.small_name[1]+' people in '+ name_en +' (region #'+ str(reg_ind) + ')']
        
    elif type == 'dead' or type == 'd_in':
        database = 'common_data.my_game.archieve_quant_of_dead'
        text_of_title = ['Умершие от '+common_data.my_game.My_disease.padezhi[1]+' в регионе №'+ str(reg_ind)  + ' (' + name_ru + ')', 
                         'Deceased from '+common_data.my_game.My_disease.small_name[1]+' in '+ name_en +' (region #'+ str(reg_ind) + ')']
            
    elif type == 'z_in':
        database = 'common_data.my_game.archieve_z_in_out'
        text_of_title = ['z_in*z_out в регионе №' + str(reg_ind) +' (' + name_ru + ')' + ' от времени', 
                         'z_in*z_out in '+ name_en +' (region #'+ str(reg_ind) + ')' + ' versus time graph']
                   
    elif type == 'recovered':
        database = 'common_data.my_game.archieve_recovered'
        text_of_title = ['Случаи выздоровления от '+common_data.my_game.My_disease.padezhi[1]+' в регионе №' + str(reg_ind) + ' (' + name_ru +')' , 
                         'Cases of recovery from ' + common_data.my_game.My_disease.small_name[1] + ' in ' + name_en + ' (region #'+ str(reg_ind) + ')']
            
    elif type == 'new_ill':
        text_of_title = ['Заболевающие за день ' + common_data.my_game.My_disease.padezhi[4] +' в регионе №' + str(reg_ind) + ' (' + name_ru +')' , 
                         'Daily cases of ' +common_data.my_game.My_disease.small_name[1]+' in ' + name_en + ' (region #'+ str(reg_ind) + ')']
          
        database = 'common_data.my_game.archieve_new_ill'
    elif type == 'new_dead':
        database = 'common_data.my_game.archieve_new_dead'
        text_of_title = ['Умирающие за день в регионе №' + str(reg_ind) + ' (' + name_ru +')' +' от ' + common_data.my_game.My_disease.padezhi[1], 
                         'Daily deceased from ' + common_data.my_game.My_disease.small_name[1] + ' in '+ name_en +' (region #'+ str(reg_ind) + ')']
            
    elif type == 'new_recovered':
        database = 'common_data.my_game.archieve_new_recovered'
        text_of_title = ['Выздоровевшие от '+common_data.my_game.My_disease.padezhi[1]+' в регионе №' + str(reg_ind) + ' (' + name_ru +')' + ' за день', 
                         'Daily cases of recovery from ' + common_data.my_game.My_disease.small_name[1] + ' in '+ name_en +' (region #'+ str(reg_ind) + ')']
    elif type == 'pr_immune':
        database = 'common_data.my_game.archieve_proc_immunated'
        
        text_of_title = ['Процент иммунных к '+common_data.my_game.My_disease.padezhi[2]+' в регионе №' + str(reg_ind) + ' (' + name_ru +')' , 
                         'Percent of immune for ' + common_data.my_game.My_disease.small_name[1]+ ' people in '+ name_en +' (region #'+ str(reg_ind) + ')']
        
    elif type == 'pen_points':
        database = 'common_data.my_game.archieve_penalty_points'
        
        text_of_title = ['Число штрафных баллов в регионе №' + str(reg_ind), 
                         'Penalty points in region #'+ str(reg_ind)]
    
    if len(common_data.my_game.list_of_chosen) > 1 or for_country == True:
        print('total country graph')    
        type+='_sum'
        database+='_sum'
        if len(text_of_title[0].split(')'))>1:
            text_of_title[0] = text_of_title[0].split('регионе')[0] + common_data.my_game.My_Country.pp_name + text_of_title[0].split(')')[1]
        else:
            text_of_title[0] = text_of_title[0].split('регионе')[0] + common_data.my_game.My_Country.pp_name      
        text_of_title[1] = text_of_title[1].split(' in')[0] + ' in ' + common_data.my_game.My_Country.name[1]
        text_of_title = [text_of_title[0],
                        text_of_title[1]]
        print(text_of_title)
    
    
    if type != None:
        text_of_title = text_of_title[common_var.lang]    
        global current_graph
        current_graph = Graph_shower(text_of_title = text_of_title, database = database, for_country = for_country, typ = type)
        current_graph.open(instance=0)
    
    
