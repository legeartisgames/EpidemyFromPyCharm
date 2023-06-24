import common_data
import common_func
import common_var
import draw_for_epidemy
import icon_func
import math
import sizes
import spec_func
import widget_of_common_par

from kivy.app import App
from kivy.clock import Clock
k_sigma = 0.1 #for Gauss deviation

def mode_time_callback(dt):
    
    if spec_func.date_go(common_data.my_game.game_pars.date, days=1)[0]==1:
        if sizes.platform == 'android':
            sizes.plyer.vibrator.pattern(pattern = (0, .04, .015, .04))         
        Step_Make(instance=0, why = "need")
        common_data.my_game_frontend.game_pars.labels.str_of_date.color=[1,1,1]
    if common_data.my_game.game_pars.date[0]==15:
        #music_module.My_switch.load_and_play_music(name = '5beep', loop=False)
        if sizes.platform == 'android':
            sizes.plyer.vibrator.pattern(pattern = (0, .04, .015, .04)) 
        common_data.my_game_frontend.game_pars.labels.str_of_date.color = [219/256, 145/256, 15/256]

    if common_data.my_game.game_pars.date[0]==27:
        common_data.my_game_frontend.game_pars.labels.str_of_date.color = [224/256, 31/256, 9/256]
    common_data.my_game.game_pars.date = spec_func.date_go(common_data.my_game.game_pars.date, days=1)
    common_data.my_game_frontend.game_pars.labels.str_of_date.text = str(spec_func.generate_str_date(common_data.my_game.game_pars.date))
    
def Step_Make(instance, why = "btn"):
    global k_sigma
    #music_module.My_switch.load_and_play_music(name = 'click', loop=False)
    #последовательность действий: начисляются деньги, люди умирают, число больных внутри региона увеличивается, болезнь разносится (коэффициент переноса)
    
    common_data.my_game.archieve_game_pars_before_step()
    print ("Step was made")
    
    common_data.my_game_frontend.game_pars.labels.str_of_date.color=[1,1,1]
    common_data.my_game.game_pars.coins+=common_data.my_game.game_pars.income
    
    if common_data.my_game.game_pars.coins < 0:
        mes = ["Дефицит бюджета! (получаете + 1 несгораемеый штрафной балл)", "Budget deficite! (get 1 penalty point)"]
        widget_of_common_par.inform_about_error(mes[common_var.lang], 'bad', 1.6)
        common_data.my_game.game_pars.earned_straph_b += 1
    
    
    common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)
    
    common_data.my_game.game_pars.numer_step+=1
   
    if common_data.my_game.My_mode.index in {0, 4, 5, 6} or (common_data.my_game.My_mode.index in {1, 2, 3} and why == "btn"):
        common_data.my_game.game_pars.date = spec_func.two_weeks_go(common_data.my_game.game_pars.date)
        common_data.my_game_frontend.game_pars.labels.str_of_date.text = str(spec_func.generate_str_date(common_data.my_game.game_pars.date))
        
    
    for i in range(common_data.my_game.n):
        
        common_data.my_game.game_pars.quant_of_dead[i] += common_data.my_game.game_pars.quant_of_ill[i]*common_data.my_game.game_pars.d_ins[i]*common_data.my_game.game_pars.d_out*common_data.my_game.game_pars.d_ins_dop[i]
        common_data.my_game.game_pars.quant_of_dead[i] = round(common_data.my_game.game_pars.quant_of_dead[i])
        
        
       
        common_data.my_game_frontend.game_pars.labels.array_of_dead[i].text = spec_func.tri_sep(common_data.my_game.game_pars.quant_of_dead[i])             
        
        common_data.my_game.My_population[i] = common_data.my_game.My_Country.population[i]-common_data.my_game.game_pars.quant_of_dead[i]
        
        
        if common_data.my_game.My_population[i] < 0:
            print("Population in region #", i, "is less 0:", common_data.my_game.My_population[i])            
            common_data.my_game.My_population[i] = 0
    
        common_data.my_game.game_pars.recovered[i] += common_data.my_game.game_pars.quant_of_ill[i]*(1-common_data.my_game.game_pars.d_ins[i]*common_data.my_game.game_pars.d_out*common_data.my_game.game_pars.d_ins_dop[i])
        common_data.my_game.game_pars.recovered[i] = round(common_data.my_game.game_pars.recovered[i])
            
        common_data.my_game.game_pars.immunated[i]+= common_data.my_game.game_pars.quant_of_ill[i]*(1-common_data.my_game.game_pars.d_ins[i]*common_data.my_game.game_pars.d_out*common_data.my_game.game_pars.d_ins_dop[i])
        time_again = common_data.my_game.game_pars.numer_step-1 - common_data.my_game.My_disease.immunity_term
        if time_again >= 0: #если кто-то из переболевших уже снова может заболеть
            common_data.my_game.game_pars.immunated[i] -= (common_data.my_game.archieve_quant_of_ill[time_again-1][i] - common_data.my_game.archieve_new_dead[time_again][i])#нас интересуют больные на начало хода и умершие в конце  
        
        common_data.my_game.game_pars.immunated[i] = round(common_data.my_game.game_pars.immunated[i])    
        
        if common_data.my_game.game_pars.immunated[i] < 0:
            print("Immunated < 0:", common_data.my_game.game_pars.immunated[i], "why?")
            common_data.my_game.game_pars.immunated[i] = 0
                
        if common_data.my_game.game_pars.immunated[i] > common_data.my_game.My_population[i]:
            print("Immunated > population:", common_data.my_game.game_pars.immunated[i], "why?")
            common_data.my_game.game_pars.immunated[i] = common_data.my_game.My_population[i] 
        
        
    coef_mult = [0]*common_data.my_game.n
    for a in range(20):
        for b in range(20):
            if common_data.my_game.Existing_of_hexes[a][b][0]== 1 and common_data.my_game.game_pars.is_hard_carantin_in_current_region[common_data.my_game.Existing_of_hexes[a][b][1]] ==1:
                cur_ind = common_data.my_game.Existing_of_hexes[a][b][1]
                if common_data.my_game.Existing_of_hexes[a][b-1][0] == 1 :
                    
                    if common_data.my_game.game_pars.is_hard_carantin_in_current_region[common_data.my_game.Existing_of_hexes[a][b-1][1]] ==1:
                        
                        coef_mult[cur_ind]+=common_data.my_game.game_pars.z_ins[cur_ind]*common_data.my_game.game_pars.z_ins_dop[cur_ind]*float(common_data.my_game.game_pars.quant_of_ill[common_data.my_game.Existing_of_hexes[a][b-1][1]])*math.sqrt(
                              common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b-1][1]]*common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b][1]])\
                            /(common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b-1][1]]\
                              +common_data.my_game.My_population[cur_ind]+1)                            
                
                if common_data.my_game.Existing_of_hexes[a][b+1][0] == 1 :
                    if common_data.my_game.game_pars.is_hard_carantin_in_current_region[common_data.my_game.Existing_of_hexes[a][b+1][1]] ==1:
                        
                        coef_mult[cur_ind]+=common_data.my_game.game_pars.z_ins[cur_ind]*common_data.my_game.game_pars.z_ins_dop[cur_ind]*\
                            float(common_data.my_game.game_pars.quant_of_ill[common_data.my_game.Existing_of_hexes[a][b+1][1]])*math.sqrt(
                            common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b+1][1]]*common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b][1]])/(common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b+1][1]]+common_data.my_game.My_population[cur_ind]+1)                 
                
                if common_data.my_game.Existing_of_hexes[a-1][b-1+a%2][0] == 1:
                    if common_data.my_game.game_pars.is_hard_carantin_in_current_region[common_data.my_game.Existing_of_hexes[a-1][b-1+a%2][1]] ==1:
                        
                        coef_mult[cur_ind]+=common_data.my_game.game_pars.z_ins[cur_ind]*common_data.my_game.game_pars.z_ins_dop[cur_ind]*\
                            float(common_data.my_game.game_pars.quant_of_ill[common_data.my_game.Existing_of_hexes[a-1][b-1+a%2][1]])*math.sqrt(
                            common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a-1][b-1+a%2][1]]*common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b][1]])/(common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a-1][b-1+a%2][1]]+common_data.my_game.My_population[cur_ind]+1)                            
                
                if common_data.my_game.Existing_of_hexes[a-1][b+a%2][0] == 1 :
                    if common_data.my_game.game_pars.is_hard_carantin_in_current_region[common_data.my_game.Existing_of_hexes[a-1][b+a%2][1]] ==1:
                        
                        coef_mult[cur_ind]+=common_data.my_game.game_pars.z_ins[cur_ind]*common_data.my_game.game_pars.z_ins_dop[cur_ind]*\
                            float(common_data.my_game.game_pars.quant_of_ill[common_data.my_game.Existing_of_hexes[a-1][b+a%2][1]])*math.sqrt(
                                                    common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a-1][b+a%2][1]]*common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b][1]])/(common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a-1][b+a%2][1]]+common_data.my_game.My_population[cur_ind]+1)                            
                        
                if common_data.my_game.Existing_of_hexes[a+1][b-1+a%2][0] == 1 :
                    if common_data.my_game.game_pars.is_hard_carantin_in_current_region[common_data.my_game.Existing_of_hexes[a+1][b-1+a%2][1]] ==1:
                        
                        coef_mult[cur_ind]+=common_data.my_game.game_pars.z_ins[cur_ind]*common_data.my_game.game_pars.z_ins_dop[cur_ind]*\
                            float(common_data.my_game.game_pars.quant_of_ill[common_data.my_game.Existing_of_hexes[a+1][b-1+a%2][1]])*math.sqrt(
                                                    common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a+1][b-1+a%2][1]]*common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b][1]])/(common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a+1][b-1+a%2][1]]+common_data.my_game.My_population[cur_ind]+1)                            
                        
                if common_data.my_game.Existing_of_hexes[a+1][b+a%2][0] == 1:
                    if common_data.my_game.game_pars.is_hard_carantin_in_current_region[common_data.my_game.Existing_of_hexes[a+1][b+a%2][1]] ==1:
                
                        coef_mult[cur_ind]+=common_data.my_game.game_pars.z_ins[cur_ind]*common_data.my_game.game_pars.z_ins_dop[cur_ind]*\
                            float(common_data.my_game.game_pars.quant_of_ill[common_data.my_game.Existing_of_hexes[a+1][b+a%2][1]])*math.sqrt(
                                                    common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a+1][b+a%2][1]]*common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a][b][1]])/(common_data.my_game.My_population[common_data.my_game.Existing_of_hexes[a+1][b+a%2][1]]+common_data.my_game.My_population[cur_ind]+1)                            
                        
            
   
    for i in range (common_data.my_game.n):
        were_ill = common_data.my_game.game_pars.quant_of_ill[i]
         
        common_data.my_game.game_pars.d_ins[i] = round(common_data.my_game.game_pars.d_ins[i], 4)       
        common_data.my_game_frontend.game_pars.labels.array_of_d_in[i].text = str(round(common_data.my_game.game_pars.d_ins[i], 4))
        common_data.my_game_frontend.game_pars.labels.array_of_d_in[i].color = [0,0,0,1]
        
        common_data.my_game.game_pars.quant_of_ill[i]+=round(
            common_data.my_game.game_pars.coef_of_perenos*coef_mult[i]*2)
        
        
        common_data.my_game_frontend.game_pars.labels.str_of_naselenie[i].text = spec_func.tri_sep(round(common_data.my_game.My_population[i]))
        
        common_data.my_game.game_pars.quant_of_ill[i] *= common_data.random.gauss(1, k_sigma) 
        common_data.my_game.game_pars.quant_of_ill[i] *= common_data.my_game.game_pars.z_ins[i]*common_data.my_game.game_pars.z_out*common_data.my_game.game_pars.z_ins_dop[i]
        
        
        if common_data.my_game.game_pars.is_hard_carantin_in_current_region[i] == 1:#if no qarantine
            ad_v = int(common_data.my_game.game_pars.coef_of_perenos/0.1*common_data.random.gauss(0, 20))
            #print(ad_v)
            common_data.my_game.game_pars.quant_of_ill[i] = ad_v + common_data.my_game.game_pars.quant_of_ill[i]
           
        if common_data.my_game.game_pars.quant_of_ill[i]>=common_data.my_game.My_population[i]-common_data.my_game.game_pars.immunated[i]:
            common_data.my_game.game_pars.quant_of_ill[i] = common_data.my_game.My_population[i]-common_data.my_game.game_pars.immunated[i]
        
        common_data.my_game.game_pars.quant_of_ill[i] = max(int(common_data.my_game.game_pars.quant_of_ill[i]), 0)
        
    
        common_data.my_game_frontend.game_pars.labels.array_of_ill[i].text = spec_func.tri_sep(common_data.my_game.game_pars.quant_of_ill[i])
        
        if common_data.my_game.game_pars.quant_of_ill[i] >= 100*10**6:
            common_data.my_game_frontend.game_pars.labels.array_of_ill[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL/1.1
        
        elif common_data.my_game_frontend.game_pars.labels.array_of_ill[i].font_size != sizes.SIZE_OF_TEXT_FOR_LABEL:
            common_data.my_game_frontend.game_pars.labels.array_of_ill[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL
        if common_data.my_game.game_pars.quant_of_dead[i] >= 100*10**6:
            common_data.my_game_frontend.game_pars.labels.array_of_dead[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL/1.1
        
        elif common_data.my_game_frontend.game_pars.labels.array_of_dead[i].font_size != sizes.SIZE_OF_TEXT_FOR_LABEL:
            common_data.my_game_frontend.game_pars.labels.array_of_dead[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL
        
        common_data.my_game.game_pars.z_ins_dop[i]=(common_data.my_game.My_population[i]-common_data.my_game.game_pars.immunated[i])/(common_data.my_game.My_population[i]+0.01)  
        common_data.my_game.game_pars.d_ins_dop[i]=1 
        
        if common_data.my_game.game_pars.is_hard_carantin_in_current_region[i] == 0:
            common_data.my_game.game_pars.is_hard_carantin_in_current_region[i] = 1
            draw_for_epidemy.draw_carantine(draw ="undraw")
        
        common_data.my_game_frontend.game_pars.labels.array_of_z_in[i].text = str(round(common_data.my_game.game_pars.z_ins[i] * common_data.my_game.game_pars.z_ins_dop[i], 3))
        common_data.my_game_frontend.game_pars.labels.array_of_z_in[i].color = [0,0,0,1]
        
        
    for i in range(common_data.my_game.n):
        common_data.my_game.update_situations(i)  
    
    
    common_func.Action_in_end_step()
    
    were_straph_b = common_data.my_game.game_pars.straph_b
    common_data.my_game.game_pars.straph_b = common_data.my_game.game_pars.earned_straph_b
    for i in range(common_data.my_game.n):
        ind = True
        if common_data.my_game.game_pars.is_stats_right[i] == False:
            common_data.my_game.game_pars.is_stats_right[i] = True
            draw_for_epidemy.draw_change_points(draw="undraw", i=i)
            common_data.my_game.game_pars.straph_b += common_data.my_game.parameters_of_tech[21][2][0]
            ind = False
        total_pen_points_for_reg = 0
        counter = 0
        if common_data.my_game.game_pars.quant_of_ill[i] >=common_data.my_game.My_population[i]/20:
            counter+=1        
            print("ill: " + str(i))
        
        if common_data.my_game.game_pars.quant_of_ill[i] >=common_data.my_game.My_Country.population[i]/10:
            counter+=math.floor(common_data.my_game.game_pars.quant_of_ill[i]*5/common_data.my_game.My_Country.population[i])

        common_data.my_game.region_straphs[i][1] = counter
        
        if ind == True:
            common_data.my_game.game_pars.straph_b += counter
        total_pen_points_for_reg+=counter
        
        counter = 0
        if common_data.my_game.game_pars.quant_of_dead[i]>=common_data.my_game.My_Country.population[i]/200:
            counter+=1
            print("dead: " + str(round(common_data.my_game.game_pars.quant_of_dead[i]*50/common_data.my_game.My_Country.population[i])) + ' ' + str(i))
        if common_data.my_game.game_pars.quant_of_dead[i]>=common_data.my_game.My_Country.population[i]/50:
            counter+=math.floor(common_data.my_game.game_pars.quant_of_dead[i]*50/common_data.my_game.My_Country.population[i])
            
        common_data.my_game.region_straphs[i][3] = counter
        if ind == True:
            common_data.my_game.game_pars.straph_b += counter
        total_pen_points_for_reg+=counter
        if common_data.my_game.My_mode.index == 6 and i == common_data.my_game.My_Country.capital_index:
            if total_pen_points_for_reg >= 3: 
                ft_rus = "[b][color=ff0000]Причина поражения[/b][/color]: Столица получила " + str(total_pen_points_for_reg) + " штрафных очков\n(" + str(total_pen_points_for_reg-counter) + " штрафных баллов за число больных и " +str(counter) + " за число умерших).\n\n"
                ft_en = "[b][color=ff0000]Cause of defeat[/b][/color]: Capital added " + str(total_pen_points_for_reg) + " penalty points\n(" + str(total_pen_points_for_reg-counter) + " points because of ill people and " +str(counter) + " because of dead).\n\n" 
                go_to_lose(first_text = [ft_rus, ft_en][common_var.lang])
            elif total_pen_points_for_reg >=2 and total_pen_points_for_reg - counter > 0: #вторая проверка сделана на число больных: если весь штраф только от умерших, то игрок ничего с этим не может сделать 
                widget_of_common_par.inform_about_error(["В столице может быть бунт!", "There may be a riot in the capital!"][common_var.lang], typ='info', t=2)
    if common_data.my_game.game_pars.straph_b - common_data.my_game.archieve_penalty_points_sum[common_data.my_game.game_pars.numer_step-2] > common_data.my_game.game_pars.lim_penalty_increase:
        if common_data.random.randint(0, 2) == 0:
            widget_of_common_par.inform_about_error(["На этот раз Вы оказались неубедительны:(", "This time you weren't persuasive:("][common_var.lang], 'bad', 1.6)
        else:
            was_pen_p = common_data.my_game.game_pars.straph_b 
            common_data.my_game.game_pars.straph_b = common_data.my_game.archieve_penalty_points_sum[common_data.my_game.game_pars.numer_step-2] + common_data.my_game.game_pars.lim_penalty_increase        
        
            #mes = ["Ораторское мастерство вам помогло\nпредотвратить начисление " + str(was_pen_p-common_data.my_game.game_pars.straph_b) + " "+ spec_func.rp_pen_poins(val=was_pen_p-common_data.my_game.game_pars.straph_b) + "!", 
            #       "Oratory helped you to prevent\n " + str(was_pen_p-common_data.my_game.game_pars.straph_b) + " penalty points!"]
            mes = ["Ораторское мастерство выручило Вас!", "Oratory has helped you!"]
            widget_of_common_par.inform_about_error(mes[common_var.lang], 'good', 1.6)
            
    common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]'       
    
    if common_data.my_game.game_pars.straph_b >= common_data.my_game.game_pars.crit_straph_b:
        go_to_lose()
        return
    
    common_data.my_game_frontend.game_pars.labels.str_of_straph.color = [1, 1, 1, 1]
    common_data.my_game_frontend.game_pars.labels.str_of_straph.bold = False
    if common_data.my_game.game_pars.straph_b >= 5:
        common_data.my_game_frontend.game_pars.labels.str_of_straph.color = [1, .5, .2, 1]
        common_data.my_game_frontend.game_pars.labels.str_of_straph.bold = True
        
    if common_data.my_game.game_pars.straph_b >= common_data.my_game.game_pars.crit_straph_b - 5\
       or ((common_data.my_game.game_pars.straph_b-were_straph_b)>=4*common_data.my_game.game_pars.crit_straph_b/25 and common_data.my_game.game_pars.straph_b >= common_data.my_game.game_pars.crit_straph_b*2/3):
        mes = ["Вы близки к проигрышу", "You are about to lose"]
        common_data.my_game_frontend.game_pars.labels.str_of_straph.color = [1, 0, 0, 1]
        widget_of_common_par.inform_about_error(mes[common_var.lang], 'bad', 1.6)
 
    
    common_data.my_game_frontend.game_pars.labels.str_of_win.bold = True
    common_data.my_game_frontend.game_pars.labels.str_of_win.color = [0, 1, 0, 1]
    for i in range(common_data.my_game.n):
        if (common_data.my_game.game_pars.quant_of_ill[i] >= 100 and\
           common_data.my_game.counter_of_buys[10][0] < 1 and common_data.my_game.counter_of_buys[11][0] < 1)\
           or (common_data.my_game.game_pars.quant_of_ill[i] >= common_data.my_game.My_population[i]/10000 and common_data.my_game.game_pars.quant_of_ill[i] > 50):
            common_data.my_game.game_pars.win_b = -1 + common_data.my_game.game_pars.earned_win_b
            common_data.my_game_frontend.game_pars.labels.str_of_win.color = [1, 1, 1, 1]
            common_data.my_game_frontend.game_pars.labels.str_of_win.bold = False
            break
        
    common_data.my_game.game_pars.win_b+=1
    common_data.my_game_frontend.game_pars.labels.str_of_win.text = str(common_data.my_game.game_pars.win_b)+ '/[color=00ff00][b]' + str(common_data.my_game.game_pars.crit_win_b)+'[/color][/b]'
    
    if common_data.my_game.game_pars.win_b >= common_data.my_game.game_pars.crit_win_b:
        common_var.is_victory = 1
        
        try:
            day_event.cancel()
        except:
            print("no day event")
        App.get_running_app().end_of_game()
        return
        
    if common_data.my_game.game_pars.date[1] in {6, 7, 8} and common_data.my_game.counter_of_buys[12][0] > 0 and common_data.my_game_frontend.wid[12].button_of_activation in common_data.my_game_frontend.wid[12].children: #if summer and researched distant 
        common_data.my_game_frontend.wid[12].label_summer = common_data.uix_classes.Label_with_tr(text_source=['Лето!','Summer'], 
                                                                        font_size = common_data.my_game_frontend.wid[12].button_of_activation.font_size*1.2,
                                                                        pos_hint={'right': 0.44, 'top': 0.18},
                                                                        size_hint = common_data.my_game_frontend.wid[12].button_of_activation.size_hint,
                                                                        color = [52/256, 235/256, 158/256, 1], bold = True)
        common_data.my_game_frontend.wid[12].add_widget(common_data.my_game_frontend.wid[12].label_summer)
        
        common_data.my_game_frontend.wid[12].remove_widget(common_data.my_game_frontend.wid[12].button_of_activation)
        
        if common_data.my_game.is_activated[12]==True:
            common_data.my_game_frontend.wid[12].Activate_Deactivate(instance = 5, do_notify = False)
            
            common_data.my_game.must_be_activated_distant = True
            
    elif common_data.my_game.game_pars.date[1] not in {6, 7, 8} and common_data.my_game.counter_of_buys[12][0] > 0 and common_data.my_game_frontend.wid[12].button_of_activation not in common_data.my_game_frontend.wid[12].children:
        if hasattr(common_data.my_game_frontend.wid[12], "label_summer"):
            common_data.my_game_frontend.wid[12].remove_widget(common_data.my_game_frontend.wid[12].label_summer)
        if hasattr(common_data.my_game, "must_be_activated_distant"):
            common_data.my_game_frontend.wid[12].Activate_Deactivate(instance = 5, do_notify = False)
            delattr(common_data.my_game, "must_be_activated_distant")
        common_data.my_game_frontend.wid[12].add_widget(common_data.my_game_frontend.wid[12].button_of_activation)
    
    
    
    for i in range(common_var.QUANT_OF_TECH):
        
        if common_data.my_game.was_purchased_in_this_month[i] == True: 
        
            if i == 28: 
                common_func.research_results()
            common_data.my_game.was_purchased_in_this_month[i] = False
            if i == 28:
                common_data.my_game.result_of_research = 'no result'           
        
            if hasattr(common_data.my_game_frontend.wid[i], "label_using_now"):
                common_data.my_game_frontend.wid[i].remove_widget(common_data.my_game_frontend.wid[i].label_using_now)
        
            common_data.my_game_frontend.wid[i].add_widget(common_data.my_game_frontend.wid[i].button_buy)
    
    
    
    eff_month = (common_data.my_game.game_pars.date[1] - 1 + 6*(common_data.my_game.My_Country.half_ball-1) )%12
    
    common_data.my_game.game_pars.z_out *= (1+(common_data.my_game.My_disease.z_out_seasonal[eff_month]-1)*common_data.my_game.My_Country.fluct_z_out) #-6+6 из-за северного и южного полушарий
    common_data.my_game.game_pars.z_out /= (1+(common_data.my_game.My_disease.z_out_seasonal[(eff_month-1)%12]-1)*common_data.my_game.My_Country.fluct_z_out)
    common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 5)
    common_data.to_str_dis_par(obj="z_out")
    
    for i in range(common_data.my_game.n):
        common_data.my_game.update_situations(i)  
    common_data.my_game.archieve_previous_game_pars_after_step()
    
    
    common_data.my_game.save_to_file()
    
    if spec_func.is_internet() == False:
        print('No internet')
    
    else:
        print("Internet Ok!")  
        
        if common_var.IS_PREMIUM == False:
            if App.get_running_app().ads.is_interstitial_loaded() == False:
                App.get_running_app().ads.request_interstitial()
        
            if common_data.my_game.game_pars.numer_step%5 == 0:
                Clock.schedule_once(show_inter, .1)
                        
def show_inter(dt): 
    App.get_running_app().ads.show_interstitial()
    
def go_to_lose(first_text = ""):
    common_var.is_victory = 0
    try:
        day_event.cancel()
    except:
        print("no day event")        
    App.get_running_app().end_of_game(first_text = first_text)
    return    