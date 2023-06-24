import common_data
import common_var
import draw_for_epidemy
import e_settings
import icon_func
import init_of_tech
import spec_func
import text_for_tech_generator
import widget_of_common_par
import tech_info

def make_new_vac_dozes(inctance):
    if common_data.my_game.game_pars.coins - common_data.my_game.parameters_of_tech[10][2][2][0] >= 0:
        common_data.my_game.parameters_of_tech[10][2][1][0] += common_data.my_game.parameters_of_tech[10][2][0][0]
        
        common_data.my_game.game_pars.coins -= common_data.my_game.parameters_of_tech[10][2][2][0]
        common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)
        
        text_for_tech_generator.generate_texts_for_tech()
        common_data.my_game_frontend.wid[10].label_of_tech.update_text()
        
    else:
        if common_var.lang == 0:
            widget_of_common_par.inform_about_error("У Вас не хватает денег\nна данное действие", 'bad', 2)
        elif common_var.lang == 1:
            widget_of_common_par.inform_about_error("You haven't enough\nmoney for this action", 'bad', 2)
    
def Action_in_end_step():
    for i in common_data.my_game.actions_end_step:
        if i == 19:
            common_data.my_game.game_pars.earned_straph_b += common_data.my_game.parameters_of_tech[19][2][1][0]
            common_data.my_stats.goldreserves += common_data.my_game.parameters_of_tech[19][2][0][0]
            
            x = common_data.my_stats.level_coins
            common_data.my_stats.level_coins = spec_func.status_finder('coins', common_data.my_stats.goldreserves)[0]
            common_data.my_stats.save_to_file()
            
            if x != common_data.my_stats.level_coins:
                mes = ["Ваш статус благосостояния вырос (из-за коррупции)", "Your wealth status has just grown (because of money laundering)."]
                widget_of_common_par.inform_about_error(mes[common_var.lang], 'good', 3)
            
            common_var.need_c = spec_func.status_finder('coins', common_data.my_stats.goldreserves)[1] 

            e_settings.nast.str_of_reserves.text = icon_func.add_money_icon(string = str(common_data.my_stats.goldreserves), size = e_settings.nast.str_of_reserves.font_size)
            
            e_settings.nast.lab_need_coins_for_next_status.text = icon_func.add_money_icon(string = str(common_var.need_c), size = e_settings.nast.lab_need_coins_for_next_status.font_size)
            
            e_settings.nast.progress_c.value = int(common_data.my_stats.goldreserves) 
            e_settings.nast.progress_c.max = common_data.my_stats.goldreserves + common_var.need_c
        
            e_settings.nast.lab_status_of_rich.text_cource = common_var.statuses_coins[common_data.my_stats.level_coins]
            e_settings.nast.lab_status_of_rich.text = common_var.statuses_coins[common_data.my_stats.level_coins][common_var.lang]
        
        if i == 20: #transferts
            
            common_data.my_stats.stars += common_data.my_game.parameters_of_tech[20][2][0][0]
            common_data.my_stats.stars = round(common_data.my_stats.stars, 1)
            x = common_data.my_stats.level_stars
            common_data.my_stats.level_stars = spec_func.status_finder('stars', common_data.my_stats.stars)[0]
            common_data.my_stats.save_to_file()
            
            if x != common_data.my_stats.level_stars:
                mes = ["Ваш статус репутации вырос (из-за трансфертов)", "Your reputation status has just grown (because of transferts)."]
                widget_of_common_par.inform_about_error(mes[common_var.lang], 'good', 3)
            
            common_var.need_s = spec_func.status_finder('stars', common_data.my_stats.stars)[1] 

            e_settings.nast.lab_quant_of_stars.text = icon_func.add_star_icon(string = str(common_data.my_stats.stars), 
                                                                        size = e_settings.nast.lab_quant_of_stars.font_size)
            
            e_settings.nast.lab_need_for_s.text = icon_func.add_star_icon(string = str(common_var.need_s), size = e_settings.nast.lab_need_for_s.font_size)
            
            e_settings.nast.progress_s.value = int(common_data.my_stats.stars) 
            e_settings.nast.progress_s.max = common_data.my_stats.stars + common_var.need_s
        
            e_settings.nast.lab_status_of_rep.text_cource = common_var.statuses_stars[common_data.my_stats.level_stars]
            e_settings.nast.lab_status_of_rep.text = common_var.statuses_stars[common_data.my_stats.level_stars][common_var.lang]
            
    udal_crit = common_data.random.randint(0, 10)
    
    if common_data.my_game.is_activated[14] == True and udal_crit >= 4: #когда удалёнка активирована в конце хода, то в следующем ходу доход сильнее падает.
        common_data.my_game.parameters_of_tech[14][3][0]-=1 #доход ещё сильней должен упасть
        common_data.my_game.game_pars.income -=1
        common_data.my_game_frontend.game_pars.labels.str_of_income.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.income), 
                                                                                                    size = common_data.my_game_frontend.game_pars.labels.str_of_income.font_size)        
        text_for_tech_generator.generate_texts_for_tech()
        common_data.my_game_frontend.wid[14].label_of_tech.update_text()
        widget_of_common_par.inform_about_error(["Работа на удалёнке дополнительно понизила доход страны", 
                                                 "Remote working is more decreasing country income"][common_var.lang], 'info', 3)
    
    elif common_data.my_game.counter_of_buys[14][0] > 0 and common_data.my_game.is_activated[14] == False and common_data.my_game.parameters_of_tech[14][3][0] < -2 + common_data.my_game.counter_of_buys[23][0]:
        common_data.my_game.parameters_of_tech[14][3][0] = -2 + common_data.my_game.counter_of_buys[23][0]#на удалёнку точно влияет оптимизация
        text_for_tech_generator.generate_texts_for_tech()
        common_data.my_game_frontend.wid[14].label_of_tech.update_text()
        widget_of_common_par.inform_about_error(["Дела на работе наладились: удалёнка сменила параметры!", 
                                                 "Remote working parameters were changed for the better!"][common_var.lang], 'good', 3)
def Mult_on_par (parameters, index_of_current_tech, do_notify = True):
    
    
        
    typ = parameters[0]
    index = parameters[1] 
    coef = parameters[2]
     
    delta_income = parameters[3]  
    common_data.my_game.game_pars.income += delta_income[0] #второй показатель - + или * , тип увеличения
    common_data.my_game_frontend.game_pars.labels.str_of_income.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.income), 
                                                                                                    size = common_data.my_game_frontend.game_pars.labels.str_of_income.font_size)
    if typ == "income":
        common_data.my_game.game_pars.earned_win_b += 1
        common_data.my_game.game_pars.win_b += 1    
        common_data.my_game_frontend.game_pars.labels.str_of_win.text = str(common_data.my_game.game_pars.win_b)+ '/[color=00ff00][b]' + str(common_data.my_game.game_pars.crit_win_b)+'[/color][/b]'

    if typ == "z":
        if index == -1:
            common_data.my_game.game_pars.z_out*=coef[0]
            common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 3)
            common_data.to_str_dis_par(obj="z_out")
        else:
            common_data.my_game.game_pars.z_ins[index]*=coef[0]
            common_data.my_game.game_pars.z_ins[index] = round(common_data.my_game.game_pars.z_ins[index], 3)
            common_data.my_game_frontend.game_pars.labels.array_of_z_in[index].text = str(common_data.my_game.game_pars.z_ins[index])

    elif typ == "z_dop":
        if index == -1:
            pass
        else:
            common_data.my_game.game_pars.z_ins_dop[index] = coef[0]*common_data.my_game.game_pars.z_ins_dop[index]
            common_data.my_game_frontend.game_pars.labels.array_of_z_in[index].text = str(round(float(common_data.my_game.game_pars.z_ins[index]*common_data.my_game.game_pars.z_ins_dop[index]), 4))
            common_data.my_game_frontend.game_pars.labels.array_of_z_in[index].color = [1,0,0,1]
            
    elif typ == 7: #в случае введения жёсткого карантина
        common_data.my_game.game_pars.z_ins_dop[index] = coef[0]*common_data.my_game.game_pars.z_ins_dop[index]
        common_data.my_game_frontend.game_pars.labels.array_of_z_in[index].text = str(round(float(common_data.my_game.game_pars.z_ins[index]*common_data.my_game.game_pars.z_ins_dop[index]), 4))
        common_data.my_game_frontend.game_pars.labels.array_of_z_in[index].color = [1,0,0,1]
        common_data.my_game.game_pars.is_hard_carantin_in_current_region[index] = 0
        
        draw_for_epidemy.draw_carantine(draw_for_epidemy.coords_of_hexes[index][0], draw_for_epidemy.coords_of_hexes[index][1], 
                              draw_for_epidemy.side, draw_for_epidemy.height, draw = "draw")        
    elif typ == "d":
        if index == -1:
            common_data.my_game.game_pars.d_out*=coef[0]
            common_data.my_game.game_pars.d_out = round(common_data.my_game.game_pars.d_out, 3)
            common_data.to_str_dis_par(obj="d_out")
        else:
            common_data.my_game.game_pars.d_ins[index]*=coef[0]
            common_data.my_game.game_pars.d_ins[index] = round(common_data.my_game.game_pars.d_ins[index], 3)
            common_data.my_game_frontend.game_pars.labels.array_of_d_in[index].text = str(common_data.my_game.game_pars.d_ins[index])
            
    elif typ == "coef_of_perenos_z_out":
        common_data.my_game.game_pars.coef_of_perenos*=coef[0][0]
        common_data.my_game.game_pars.coef_of_perenos = round(common_data.my_game.game_pars.coef_of_perenos, 4)

        common_data.my_game.game_pars.z_out*=coef[1][0]
        common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 3)

        common_data.to_str_dis_par(obj="transfer_c")
        common_data.to_str_dis_par(obj="z_out")
        
    elif typ == "coef_skidka_na_tech":
        common_data.my_game.coef_skidka_na_tech *=coef[0][0]


    elif typ == "ill":
        a = common_data.my_game.game_pars.quant_of_ill[index]
        
        if a >= 500:
            common_data.my_game.game_pars.quant_of_ill[index]+=coef[0][0]
            common_data.my_game.game_pars.quant_of_ill[index] = max(int(coef[1][0]*a), common_data.my_game.game_pars.quant_of_ill[index])
            common_data.my_game_frontend.game_pars.labels.array_of_ill[index].text = spec_func.tri_sep(int(common_data.my_game.game_pars.quant_of_ill[index]))
            common_data.my_game.game_pars.quant_of_dead[index]+=(a-common_data.my_game.game_pars.quant_of_ill[index])*common_data.my_game.game_pars.d_out*common_data.my_game.game_pars.d_ins[index]
            common_data.my_game_frontend.game_pars.labels.array_of_dead[index].text = spec_func.tri_sep(int(common_data.my_game.game_pars.quant_of_dead[index]))
        else:
            if do_notify == True:
                
                if common_var.lang == 0:
                    widget_of_common_par.inform_about_error("Больных для изоляции в регионе №" + str(index)+" не смогли обнаружить\n(их слишком мало)", 'bad', 2)
                elif common_var.lang == 1:
                    widget_of_common_par.inform_about_error("Too small quantity of ill in region №" + str(index), 'bad', 2)
    elif typ == "zd":
        if index == -1:
            common_data.my_game.game_pars.d_out*=coef[1][0]
            common_data.my_game.game_pars.d_out = round(common_data.my_game.game_pars.d_out, 3)
            common_data.to_str_dis_par(obj="d_out")
            common_data.my_game.game_pars.z_out*=coef[0][0]
            common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 4)
            common_data.to_str_dis_par(obj="z_out")

    elif typ == "z_in_z_out":
        common_data.my_game.game_pars.z_ins[index]*=coef[0][0]
        common_data.my_game.game_pars.z_ins[index] = round(common_data.my_game.game_pars.z_ins[index], 3)

        common_data.my_game_frontend.game_pars.labels.array_of_z_in[index].text = str(common_data.my_game.game_pars.z_ins[index]) 
        common_data.my_game.game_pars.z_out*=coef[1][0]
        common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 3)
        common_data.to_str_dis_par(obj="z_out")   
        
    elif typ == 3:#masks
        common_data.my_game.game_pars.z_out*=coef[0][0]
        common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 3)
        common_data.to_str_dis_par(obj="z_out") 
        
        common_data.my_game.game_pars.earned_straph_b += coef[1][0]
        common_data.my_game.game_pars.straph_b += coef[1][0]
        common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]' 
        
       
        common_data.my_game_frontend.wid[3].label_of_tech.update_text(do_generate=True)
       
    
    elif typ == 10:#vaccine
        if common_data.my_game.game_pars.immunated[index] == common_data.my_game.My_population[index]:
            if common_var.lang == 0:
                widget_of_common_par.inform_about_error("Всё население в регионе №"+ str(index) + " иммунно к инфекции!", 'good', 2)
            elif common_var.lang == 1:
                widget_of_common_par.inform_about_error("All population in region #"+ str(index) + " is immune for the disease!", 'good', 2)
            do_notify = False
            return
        common_data.my_game.game_pars.z_ins_dop[index]/=(common_data.my_game.My_population[index]-common_data.my_game.game_pars.immunated[index])/(common_data.my_game.My_population[index]+0.01)
        delta = common_data.my_game.My_population[index] - common_data.my_game.game_pars.immunated[index]
        
        if delta > common_data.my_game.My_population[index]*0.25:
            delta = common_data.my_game.My_population[index]*0.25
            
        if common_data.my_game.parameters_of_tech[10][2][1][0] - delta >= 0:
            common_data.my_game.game_pars.immunated[index] += delta#а как быть с уже больными?
            remain = common_data.my_game.parameters_of_tech[10][2][1][0] - delta
            common_data.my_game.parameters_of_tech[10][2][1][0] = 1000*round(remain/1000)
        else:
            common_data.my_game.game_pars.immunated[index] += common_data.my_game.parameters_of_tech[10][2][1][0] 
            common_data.my_game.parameters_of_tech[10][2][1][0]= 0
            if common_var.lang == 0:
                widget_of_common_par.inform_about_error("Закончились дозы вакцины (не хватило для вакцинации региона №"+str(index)+")", 'bad', 2)
            elif common_var.lang == 1:
                widget_of_common_par.inform_about_error("Vaccine doses have run out!", 'bad', 2)
            do_notify = False
        
        common_data.my_game.archieve_proc_immunated[len(common_data.my_game.archieve_proc_immunated)-1][index] = common_data.my_game.game_pars.immunated[index]/common_data.my_game.My_population[index]*100 
        
        common_data.my_game.archieve_proc_immunated_sum[len(common_data.my_game.archieve_proc_immunated_sum)-1] = sum(common_data.my_game.game_pars.immunated)/sum(common_data.my_game.My_population)*100
        
        common_data.my_game.game_pars.z_ins_dop[index]*=(common_data.my_game.My_population[index]-common_data.my_game.game_pars.immunated[index])/(common_data.my_game.My_population[index]+0.01)
        common_data.my_game_frontend.game_pars.labels.array_of_z_in[index].text = str(round(float(common_data.my_game.game_pars.z_ins[index]*common_data.my_game.game_pars.z_ins_dop[index]), 4))
        
        text_for_tech_generator.generate_texts_for_tech()
        common_data.my_game_frontend.wid[10].label_of_tech.update_text()
        
    elif typ == 12: #distant
           
        if coef[0]>1:
            common_data.my_game.game_pars.earned_straph_b -= 1
            common_data.my_game.game_pars.straph_b-=1
            common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]' 
        else:
            common_data.my_game.game_pars.earned_straph_b +=1
            common_data.my_game.game_pars.straph_b+=1
            common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]' 
                                    
        common_data.my_game.game_pars.z_out*=coef[0]
        common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 3)
        common_data.to_str_dis_par(obj="z_out")            
    
    elif typ == 13: #propaganda
        common_data.my_game.game_pars.crit_straph_b = round(coef[0]*common_data.my_game.game_pars.crit_straph_b)
        common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]' 
    elif typ == 15:#coin emission
        common_data.my_game.game_pars.coins += coef[0][0]
        common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)
        if common_data.my_game.parameters_of_tech[15][2][1][0] < 2:
            common_data.my_game.parameters_of_tech[15][2][1][0]+=1
        
        common_data.my_game.game_pars.earned_straph_b += coef[2][0]
        common_data.my_game.game_pars.straph_b += coef[2][0]

        if common_data.my_game.My_Country.index == 8:
            if common_data.my_game.parameters_of_tech[15][2][2][0] == 0:
                common_data.my_game.parameters_of_tech[15][2][2][0] = common_data.random.randint(0, 2)
            else:
                common_data.my_game.parameters_of_tech[15][2][2][0] += common_data.random.randint(0, 2)>0
        else:
            common_data.my_game.parameters_of_tech[15][2][2][0] *= 1.3
        if common_data.my_game.parameters_of_tech[15][2][2][0]%1 < 0.2:
            common_data.my_game.parameters_of_tech[15][2][2][0] = common_data.math.floor(common_data.my_game.parameters_of_tech[15][2][2][0])
        else:
            common_data.my_game.parameters_of_tech[15][2][2][0] = common_data.math.ceil(common_data.my_game.parameters_of_tech[15][2][2][0])
        if common_data.my_game.parameters_of_tech[15][2][2][0] > 5:
            common_data.my_game.parameters_of_tech[15][2][2][0] = 5 
        common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]' 
        for i in range(common_var.QUANT_OF_TECH):
            if common_data.my_game.counter_of_buys[i][0] < tech_info.quant_of_buys[i][0] or tech_info.quant_of_buys[i][0] == -1:
                common_data.my_game.prices_of_tech[i][0]-=coef[1][0] #как обычно, цены меньше нуля, поэтому падают
        text_for_tech_generator.generate_texts_for_tech()
        for i in range(common_var.QUANT_OF_TECH):
            if hasattr(common_data.my_game_frontend.wid[i], "label_of_tech"):#unlocked haven't that attribute
                common_data.my_game_frontend.wid[i].label_of_tech.update_text()
            
    elif typ == 16:#goscompany
        common_data.my_game.game_pars.coins += coef[0][0]
        common_data.my_game_frontend.game_pars.labels.str_of_money.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.coins), size = common_data.my_game_frontend.game_pars.labels.str_of_money.font_size)
        
        common_data.my_game.game_pars.earned_straph_b += coef[1][0]
        common_data.my_game.game_pars.straph_b += coef[1][0]
        common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]' 
        
        common_data.my_game.parameters_of_tech[16][2][0][0]-=1
        if common_data.my_game.parameters_of_tech[16][2][0][0] < 1:
            common_data.my_game.parameters_of_tech[16][2][0][0] = 1
        
        common_data.my_game.parameters_of_tech[16][2][1][0]+=1*(common_data.random.randint(0, 5)>2) #народ ещё сильнее недоволен, но непонятно как
        
        common_data.my_game_frontend.wid[16].label_of_tech.update_text(do_generate=True)
        if common_data.my_game.counter_of_buys[16][1] >= common_data.my_game.quant_of_buys[16][1]:
            print("All goscompanies were sold")
    elif typ == 17:#taxes increasing
        common_data.my_game.game_pars.earned_straph_b += coef[0][0]
        common_data.my_game.game_pars.straph_b += coef[0][0]
        common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]' 

        common_data.my_game.parameters_of_tech[17][2][0][0]+=1*(common_data.random.randint(0, 3)>0) #народ ещё сильнее недоволен, но непонятно как
        
        common_data.my_game_frontend.wid[17].label_of_tech.update_text(do_generate=True)
        
    elif typ == 18:#region isolation
        common_data.my_game.game_pars.is_hard_carantin_in_current_region[index] = 0
        
        draw_for_epidemy.draw_carantine(draw_for_epidemy.coords_of_hexes[index][0], draw_for_epidemy.coords_of_hexes[index][1], 
                              draw_for_epidemy.side, draw_for_epidemy.height, draw = "draw")        
   
    
    elif typ == 19:#money laundering
        if 19 not in common_data.my_game.actions_end_step:
            common_data.my_game.actions_end_step.append(19)
        else:
            common_data.my_game.actions_end_step.remove(19)
    
    elif typ == 20:#transferts
        if 20 not in common_data.my_game.actions_end_step:
            common_data.my_game.actions_end_step.append(20)
        else:
            common_data.my_game.actions_end_step.remove(20)    
        common_data.my_game.game_pars.earned_win_b += coef[1][0]
 
        common_data.my_game.game_pars.win_b += coef[1][0]        
        common_data.my_game_frontend.game_pars.labels.str_of_win.text = str(common_data.my_game.game_pars.win_b)+ '/[color=00ff00][b]' + str(common_data.my_game.game_pars.crit_win_b)+'[/color][/b]'
        
    elif typ == 21 and common_data.my_game.game_pars.is_stats_right[index] == True:#distortion of stats
        common_data.my_game.game_pars.is_stats_right[index] = False 
        draw_for_epidemy.draw_change_points(i = index, draw = "draw")
        
        common_data.my_game_frontend.circles_situation_in_hexes[index][1].update_color()
        common_data.my_game_frontend.circles_situation_in_hexes[index][3].update_color()
        
    elif typ == 22: #automatisation
        if common_data.my_game.game_pars.is_automatisated[index] == False:
            common_data.my_game.game_pars.is_automatisated[index] = True
        
            draw_for_epidemy.draw_automatisated(i = index, draw = "draw")        
        else:
            widget_of_common_par.inform_about_error(["Автоматизация в этом регионе была проведена ранее", "Automatisation was made in this region earlier"][common_var.lang], typ="bad", t=2)
            do_notify = False
    elif typ == 23:#optimisation
        for i in range (len(common_data.my_game.parameters_of_tech)):
            if common_data.my_game.parameters_of_tech[i][3][0] < -common_data.my_game.parameters_of_tech[23][2][0][0]:
                common_data.my_game.parameters_of_tech[i][3][0] += 1
                if common_data.my_game.is_activated[i] == True:
                    common_data.my_game.game_pars.income+=1
                    common_data.my_game_frontend.game_pars.labels.str_of_income.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.income), 
                                                                                                                size = common_data.my_game_frontend.game_pars.labels.str_of_income.font_size)                    
        common_data.my_game.game_pars.z_out*=common_data.my_game.parameters_of_tech[23][2][1][0]
        common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 3)
        common_data.to_str_dis_par(obj="z_out")
        
        text_for_tech_generator.generate_texts_for_tech()
        for i in range(len(common_data.my_game.parameters_of_tech)):
            if hasattr(common_data.my_game_frontend.wid[i], "label_of_tech"):#unlocked haven't that attribute
                common_data.my_game_frontend.wid[i].label_of_tech.update_text()
            
    elif typ == 24:#import of ill
        a_ind = None
        b_ind = None
        do_stop = False
        for a in range(20):
            for b in range(20):
                if common_data.my_game.Existing_of_hexes[a][b][0] == 1 and common_data.my_game.Existing_of_hexes[a][b][1] == index:
                    a_ind = a
                    b_ind = b
                    do_stop = True
                    break
            if do_stop:
                break
          
        
        candidats = [(a_ind, b_ind-1), (a_ind, b_ind+1), (a_ind-1, b_ind-1+a_ind%2), (a_ind-1, b_ind+a_ind%2), (a_ind+1, b_ind-1+a_ind%2), (a_ind+1, b_ind+a_ind%2)] 
        ind_candidats = []
        for i in candidats:
            if common_data.my_game.Existing_of_hexes[i[0]][i[1]][0] == 1:
                i_can = common_data.my_game.Existing_of_hexes[i[0]][i[1]][1]
                if common_data.my_game.game_pars.is_hard_carantin_in_current_region[i_can] == 1: #i.e. no quarantine
                    ind_candidats.append(i_can)
        delta = 0       
        for i in ind_candidats:
            c = common_data.my_game.game_pars.quant_of_ill[i]
            common_data.my_game.game_pars.quant_of_ill[i] = max(0.05*c, c+common_data.my_game.parameters_of_tech[24][2][0][0])
            delta += c - common_data.my_game.game_pars.quant_of_ill[i]
            common_data.my_game_frontend.game_pars.labels.array_of_ill[i].text = spec_func.tri_sep(int(common_data.my_game.game_pars.quant_of_ill[i]))
            
            
        
        common_data.my_game.game_pars.quant_of_ill[index] += delta
        common_data.my_game_frontend.game_pars.labels.array_of_ill[index].text = spec_func.tri_sep(int(common_data.my_game.game_pars.quant_of_ill[index]))
                
           
    elif typ == 25:#plasma
        common_data.my_game.game_pars.d_ins_dop[index]*=common_data.my_game.parameters_of_tech[25][2][0]
        common_data.my_game_frontend.game_pars.labels.array_of_d_in[index].text = str(round(float(common_data.my_game.game_pars.d_ins[index]\
                                                                                                  *common_data.my_game.game_pars.d_ins_dop[index]), 4))
        common_data.my_game_frontend.game_pars.labels.array_of_d_in[index].color = [1,0,0,1]
                
    elif typ == 26:#lawmaking
        variants = []
        for i in range(common_var.QUANT_OF_TECH):
            if common_data.my_game_frontend.wid[i].is_avaliable != True and tech_info.min_goldreserves_for_tech[i] < 2000 and tech_info.min_stars_for_tech[i] < 2000:
                variants.append(i)
        print("New methods variants", variants)
        if variants!=[]:
            num = common_data.random.choice(variants)
            common_data.my_game_frontend.wid[num].is_avaliable = True
            common_data.my_game.is_tech_avaliable[num] = True
            init_of_tech.init_tech_card(num, changing_content=True)
            print(num, "was chosen")
        else:
            widget_of_common_par.inform_about_error(["Нет недоступных методов", "All methods are avalibale"][common_var.lang], typ="bad", t=2)
            do_notify = False
        
    elif typ == 27:#power of persuasion
        if common_data.my_stats.level_stars >= coef[1]:
            common_data.my_game.game_pars.lim_penalty_increase = coef[2][0]
            stat = common_data.common_var.statuses_stars[spec_func.status_finder(value=common_data.my_stats.stars, typ = 'stars')[0]]
            stat = [stat[0][:stat[0].find(' (')], stat[1][:stat[1].find(' (')]]
            widget_of_common_par.inform_about_error(["Вы как "+stat[0]+ ' умеете убеждать людей в чём угодно', 
                                                     "You as "+stat[1]+ ' have perfect skill of misleading people'][common_var.lang], 
                                                    'good', 3)
            do_notify = False
        else:
            common_data.my_game.game_pars.lim_penalty_increase = coef[0][0]
    elif typ == 28:#new investments in research
        was_invented = False
        print(common_data.my_game.counter_of_buys[10][0])
        if common_data.my_game.counter_of_buys[10][0] == 0:
            
            if common_data.random.randint(0, int(1/coef[0][0])-1) == 0:
                
                was_invented = True
                print("VACCINE RESEARCHHED!")
                common_data.my_game.result_of_research = "vaccine"
        else:
            pass
        if common_data.my_game.counter_of_buys[11][0] == 0:
            if common_data.random.randint(0, int(1/coef[1][0])-1) == 0:
                
                was_invented = True
                print("CURE RESEARCHHED!")
                if common_data.my_game.result_of_research == "vaccine":
                    common_data.my_game.result_of_research = 'vaccine+medicine'                
                else:
                    common_data.my_game.result_of_research = 'medicine'
        else:
            pass
        if was_invented == False:
            common_data.my_game.result_of_research = 'no results'
            
        common_data.my_game.was_purchased_in_this_month[28] = True
        ob = common_data.my_game_frontend.wid[28]
        ob.label_using_now = common_data.uix_classes.Label_with_tr(text_source=['Исследования\nуже ведутся!',
                                                                                'Researches\nare conducting!'], 
                                                                    font_size = ob.button_buy.font_size,
                                                                    pos_hint = ob.button_buy.pos_hint,
                                                                    size_hint = ob.button_buy.size_hint,
                                                                    color = [52/256, 235/256, 158/256, 1], 
                                                                    bold = True, halign = 'center')
        common_data.my_game_frontend.wid[28].add_widget(common_data.my_game_frontend.wid[28].label_using_now)
            
        common_data.my_game_frontend.wid[28].remove_widget(common_data.my_game_frontend.wid[28].button_buy)
        if common_data.my_game.counter_of_buys[28][0]==1: #в первый раз инвестиции
            frases = [0, 0, 0]
            frases[0] = ["Исследования начались!\nЖдите результатов в конце месяца",
                         "Researches have started!\nWait results in the end of this month!"]
            frases[1] = ["Исследования начались.\nОтчёт будет в конце месяца.",
                         "Research have started.\nReport will be in the end of the month!"]
            frases[2] = ["НИИ начали/продолжили разработку вакцины и лекарства",
                                     "Institutes commenced/continued to develop vaccine and cure"]
            frase = common_data.random.choice(frases)
        
            widget_of_common_par.inform_about_error(frase[common_var.lang], 'good', 2)
        
        do_notify = False
    elif typ == 29:#new scientific communication
        common_data.my_game.parameters_of_tech[28][2][0][0]*=coef[0][0]
        common_data.my_game.parameters_of_tech[28][2][1][0]*=coef[1][0]
        text_for_tech_generator.generate_texts_for_tech()
        
        common_data.my_game_frontend.wid[28].label_of_tech.update_text()
        
    elif typ == 30:#humanitarian aid
        
        if common_data.my_stats.level_stars <= coef[0]:
            hum_text = [common_data.my_game.My_Country.name[0]+ ' получила гуманитарную помощь ', common_data.my_game.My_Country.name[1] + ' has received humanitarian aid']
            common_data.my_game.game_pars.income +=coef[1]
            
        else:
            hum_text = [common_data.my_game.My_Country.name[0]+ ' будет оказывать гуманитарную помощь\nразвивающимся странам', common_data.my_game.My_Country.name[1] + ' will be providing humanitarian aid\nto developing countries']

            common_data.my_game.game_pars.earned_win_b += 1
            common_data.my_game.game_pars.win_b += 1    
            common_data.my_game_frontend.game_pars.labels.str_of_win.text = str(common_data.my_game.game_pars.win_b)+ '/[color=00ff00][b]' + str(common_data.my_game.game_pars.crit_win_b)+'[/color][/b]'
            
            common_data.my_game.game_pars.income +=coef[2]
            
        common_data.my_game_frontend.game_pars.labels.str_of_income.text = icon_func.add_money_icon(string = str(common_data.my_game.game_pars.income), 
                                                                                                            size = common_data.my_game_frontend.game_pars.labels.str_of_income.font_size)        
        widget_of_common_par.inform_about_error(hum_text[common_var.lang], 'good', 3)
        do_notify = False
    elif typ == 31:#health lifestyle

        common_data.my_game.game_pars.z_out*=coef[0]
        common_data.my_game.game_pars.z_out = round(common_data.my_game.game_pars.z_out, 3)
        common_data.to_str_dis_par(obj="z_out")
        
        common_data.my_game.game_pars.d_out*=coef[1]
        common_data.my_game.game_pars.d_out = round(common_data.my_game.game_pars.d_out, 3)
        common_data.to_str_dis_par(obj="d_out")
        
        common_data.my_game.game_pars.crit_straph_b +=coef[2]
        common_data.my_game_frontend.game_pars.labels.str_of_straph.text = str(common_data.my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(common_data.my_game.game_pars.crit_straph_b)+'[/color][/b]'        
        
        common_data.my_game.was_purchased_in_this_month[31] = True
        ob = common_data.my_game_frontend.wid[31]
        ob.label_using_now = common_data.uix_classes.Label_with_tr(text_source=['Оздоровление\nудалсоь!',
                                                                                'We are now\nhealthier!'], 
                                                                    font_size = ob.button_buy.font_size,
                                                                    pos_hint = ob.button_buy.pos_hint,
                                                                    size_hint = ob.button_buy.size_hint,
                                                                    color = [32/256, 187/256, 214/256, 1], 
                                                                    bold = True, halign = 'center')
        common_data.my_game_frontend.wid[31].add_widget(common_data.my_game_frontend.wid[31].label_using_now)
            
        common_data.my_game_frontend.wid[31].remove_widget(common_data.my_game_frontend.wid[31].button_buy)
        
        common_data.my_game.parameters_of_tech[31][2][0] = 0.98
        common_data.my_game.parameters_of_tech[31][2][1] = 0.99
        text_for_tech_generator.generate_texts_for_tech()
        common_data.my_game_frontend.wid[31].label_of_tech.update_text()
                
        #for i in range(len(common_data.my_game.parameters_of_tech)): I don't know why I should correct all wid[i]; I commented this otherwise it would break (label of tech doesn't exist in unlocked methods)
        #    common_data.my_game_frontend.wid[i].label_of_tech.update_text()
        
        
    for i in range (0, common_data.my_game.n):
        common_data.my_game.update_situations(i)    
 
    if do_notify == True:
        if common_var.lang == 0:
            widget_of_common_par.inform_about_error("Операция выполнена", 'good', 2)
        elif common_var.lang == 1:
            widget_of_common_par.inform_about_error("Operation is completed", 'good', 2)

def research_results():
    if common_data.my_game.result_of_research == 'vaccine':
        common_data.my_game.opened_by_research.append(10)
        common_data.my_game.game_pars.coins -= common_data.my_game.prices_of_tech[10][0] #цены всё ещё меньше нуля
        common_data.my_game_frontend.wid[10].Multiply_on_parameter(instance = 20)
        text_from = [common_data.my_game.My_disease.padezhi[1], common_data.my_game.My_disease.small_name[1]]
        frases = [0, 0, 0, 0]
        frases[0] = ["Поздравляем! Ваши учёные создали вакцину от " + text_from[0]+ "!",
                     "Congratulations! Your scientists inventioned vaccine against " + text_from[1] + "!"]
        frases[1] = ["Вакцина от " + text_from[0] + " изобретена!",
                     "Vaccine against " + text_from[1]+" is invented!"]
        frases[2] = ["Вакцина от " + text_from[0] + " созадана",
                     "Scinentists finally invented vaccine against " + text_from[1]+"!"]
        frases[3] = ["Вакцина от " +text_from[0]+" готова!\nМожете начинать вакцинацию!",
                     "Vaccine against "+text_from[1]+" is ready!\nYou can start vaccination right now!"]
        frase = common_data.random.choice(frases)
        widget_of_common_par.inform_about_error(frase[common_var.lang], 'good', 2)
        
    if common_data.my_game.result_of_research == 'medicine' or common_data.my_game.result_of_research == "vaccine+medicine":
        common_data.my_game.opened_by_research.append(11)
        common_data.my_game.game_pars.coins -= common_data.my_game.prices_of_tech[11][0] #цены всё ещё меньше нуля
        common_data.my_game_frontend.wid[11].Multiply_on_parameter(instance = 20)
        
        text_from = [common_data.my_game.My_disease.padezhi[1], common_data.my_game.My_disease.small_name[1]]
        frases = [0, 0, 0, 0]
        frases[0] = ["Поздравляем! Ваши учёные создали лекарство от " + text_from[0]+ "!",
                     "Congratulations! Your scientists inventioned a cure for " + text_from[1] + "!"]
        frases[1] = ["Лекарство от " + text_from[0] + " изобретено!",
                     "Medicine against " + text_from[1]+" is invented!"]
        frases[2] = ["Лекарство от " + text_from[0] + " создано",
                     "Scinentists finally invented cure against " + text_from[1]]
        frases[3] = ["Лекарство от " +text_from[0]+" готово!\nНа горизонте победа в игре!",
                     "Cure against "+text_from[1]+"is ready!\nYou can start vaccination right now!"]
        frase = common_data.random.choice(frases)
        widget_of_common_par.inform_about_error(frase[common_var.lang], 'good', 5)
        
    if common_data.my_game.result_of_research == 'no results':
        '''frases = [0, 0, 0, 0, 0, 0]
        
        frases[0] = ["Не всегда получается так, как Вы хотите :(\nНо продвижения в исследованиях имеются", 
                     "It's not always as you want :(\nContinue researchers and next time you will do your best!"]
        frases[1] = ["Учёным необходимо провести дополнительные эксперименты", 
                     "Scieintists need more experiments"]
        frases[2] = ["Разработка идёт полным ходом, но ещё далеко до завершения!",
                     "Developing is goint at full speed\nbut it's pretty long time for final"]
        frases[3] = ["Нужно больше времени на исследования!",
                     "Think-tanks need more time for researches!"]
        frases[4] = ["Исследования в " + common_data.my_game.My_Country.pp_name + " идут медленно :(",
                     "Researches in " + common_data.my_game.My_Country.name[1]+ " are quite slow :("]
        frases[5] = ["Нет новых открытий.",
                     "No inventions."]
        frase = common_data.random.choice(frases)
        
        widget_of_common_par.inform_about_error(frase[common_var.lang], 'info', 2.5)
        '''
        frase = ["ничего не было открыто", "nothing was discovered"]
        wdate = spec_func.month_back(common_data.my_game.game_pars.date)
        #-1 в дате за то, что нумерация с 0, а не с 1, и ещё -1, так как за прошлый месяц.
        frase_res_ru = "Результаты за " + common_var.months_names[wdate[1]-1][0] + ':\n' + frase[0]
        frase_res_en = "Results for " + common_var.months_names[wdate[1]-1][1] + ':\n' + frase[1]
        pr_str_28 = common_data.my_game_frontend.wid[28].label_of_tech.text
        
        disc_by_sc = ''
        if common_var.lang == 0:
            if pr_str_28.find('учёными')!=-1:
                disc_by_sc = pr_str_28[pr_str_28.find('Открыто учёными'):]
            
            pr_str_28 = pr_str_28[:pr_str_28.find('Результат')]
            
        if common_var.lang == 1:
            if pr_str_28.find('Created by')!=-1:
                disc_by_sc = pr_str_28[pr_str_28.find('Created by'):]
            
            pr_str_28 = pr_str_28[:pr_str_28.find('Result')]
            
        common_data.my_game_frontend.wid[28].label_of_tech.text=pr_str_28+[frase_res_ru, frase_res_en][common_var.lang]+disc_by_sc
    else:
        text_for_tech_generator.generate_texts_for_tech()
        common_data.my_game_frontend.wid[28].label_of_tech.update_text()        