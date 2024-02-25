import common_data as cd
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
    if cd.mg.pars.coins - cd.mg.parameters_of_tech[10][2][2][0] >= 0:
        cd.mg.parameters_of_tech[10][2][1][0] += cd.mg.parameters_of_tech[10][2][0][0]
        
        cd.mg.pars.coins -= cd.mg.parameters_of_tech[10][2][2][0]
        cd.frontend.pars.labels.cash_label.text = icon_func.add_money_icon(string = str(cd.mg.pars.coins), size = cd.frontend.pars.labels.cash_label.font_size)
        
        text_for_tech_generator.generate_texts_for_tech()
        cd.frontend.wid[10].label_of_tech.update_text()
    else:
        if common_var.lang == 0:
            widget_of_common_par.info_message("У Вас не хватает денег\nна данное действие", 'bad', 2)
        elif common_var.lang == 1:
            widget_of_common_par.info_message("You haven't enough\nmoney for this action", 'bad', 2)


def Action_in_end_step():
    for i in cd.mg.actions_end_step:
        if i == 19:
            cd.mg.pars.earned_straph_b += cd.mg.parameters_of_tech[19][2][1][0]
            cd.stats.goldreserves += cd.mg.parameters_of_tech[19][2][0][0]
            
            x = cd.stats.level_coins
            cd.stats.level_coins = spec_func.status_finder('coins', cd.stats.goldreserves)[0]
            cd.stats.save_to_file()
            
            if x != cd.stats.level_coins:
                mes = ["Ваш статус благосостояния вырос (из-за коррупции)",
                       "Your wealth status has just grown (because of money laundering)."]
                widget_of_common_par.info_message(mes[common_var.lang], 'good', 3)
            
            common_var.need_c = spec_func.status_finder('coins', cd.stats.goldreserves)[1] 

            e_settings.nast.str_of_reserves.text = icon_func.add_money_icon(string = str(cd.stats.goldreserves), size = e_settings.nast.str_of_reserves.font_size)
            
            e_settings.nast.lab_need_coins_for_next_status.text = icon_func.add_money_icon(string = str(common_var.need_c), size = e_settings.nast.lab_need_coins_for_next_status.font_size)
            
            e_settings.nast.coins_progress_bar.value = int(cd.stats.goldreserves) 
            e_settings.nast.coins_progress_bar.max = cd.stats.goldreserves + common_var.need_c
        
            e_settings.nast.lab_status_of_rich.text_source = common_var.statuses_coins[cd.stats.level_coins]
            e_settings.nast.lab_status_of_rich.text = common_var.statuses_coins[cd.stats.level_coins][common_var.lang]
        
        if i == 20:  # transferts
            cd.stats.stars += cd.mg.parameters_of_tech[20][2][0][0]
            cd.stats.stars = round(cd.stats.stars, 1)
            last_level_stars = cd.stats.level_stars
            cd.stats.level_stars = spec_func.status_finder('stars', cd.stats.stars)[0]
            cd.stats.save_to_file()
            
            if last_level_stars != cd.stats.level_stars:
                mes = ["Ваш статус репутации вырос (из-за трансфертов)",
                       "Your reputation status has just grown (because of transferts)."]
                widget_of_common_par.info_message(mes[common_var.lang], 'good', 3)
            
            common_var.need_s = spec_func.status_finder('stars', cd.stats.stars)[1] 

            e_settings.nast.num_stars_label.text = \
                icon_func.add_star_icon(string=str(cd.stats.stars),
                                        size=e_settings.nast.num_stars_label.font_size)
            
            e_settings.nast.lab_need_for_s.text = icon_func.add_star_icon(string=str(common_var.need_s), size = e_settings.nast.lab_need_for_s.font_size)
            
            e_settings.nast.stars_progress_bar.value = int(cd.stats.stars) 
            e_settings.nast.stars_progress_bar.max = cd.stats.stars + common_var.need_s
        
            e_settings.nast.stars_status_label.text_source = common_var.stars_statuses[cd.stats.level_stars]
            e_settings.nast.stars_status_label.text = common_var.stars_statuses[cd.stats.level_stars][common_var.lang]
            
    udal_crit = cd.random.randint(0, 10)
    
    if cd.mg.is_activated[14] and udal_crit >= 4:
        # когда удалёнка активирована в конце хода, то в следующем ходу доход сильнее падает.
        cd.mg.parameters_of_tech[14][3][0] -= 1 #доход ещё сильней должен упасть
        cd.mg.pars.income -=1
        cd.frontend.pars.labels.str_of_income.text = icon_func.add_money_icon(string = str(cd.mg.pars.income), 
                                                                                                    size = cd.frontend.pars.labels.str_of_income.font_size)        
        text_for_tech_generator.generate_texts_for_tech()
        cd.frontend.wid[14].label_of_tech.update_text()
        widget_of_common_par.info_message(["Работа на удалёнке дополнительно понизила доход страны", 
                                                 "Remote working is more decreasing country income"][common_var.lang], 'info', 3)
    
    elif cd.mg.counter_of_buys[14][0] > 0 and cd.mg.is_activated[14] == False and cd.mg.parameters_of_tech[14][3][0] < -2 + cd.mg.counter_of_buys[23][0]:
        cd.mg.parameters_of_tech[14][3][0] = -2 + cd.mg.counter_of_buys[23][0]#на удалёнку точно влияет оптимизация
        text_for_tech_generator.generate_texts_for_tech()
        cd.frontend.wid[14].label_of_tech.update_text()
        widget_of_common_par.info_message(["Дела на работе наладились: удалёнка сменила параметры!", 
                                                 "Remote working parameters were changed for the better!"][common_var.lang], 'good', 3)


def Mult_on_par (parameters, method_id, do_notify=True):
    typ = parameters[0]
    index = parameters[1] 
    coef = parameters[2]
     
    delta_income = parameters[3]  
    cd.mg.pars.income += delta_income[0]  # второй показатель - + или * , тип увеличения
    cd.frontend.pars.labels.str_of_income.text = \
        icon_func.add_money_icon(string=str(cd.mg.pars.income),
                                 size=cd.frontend.pars.labels.str_of_income.font_size)
    if typ == "income":
        cd.mg.pars.earned_win_b += 1
        cd.mg.pars.victory_points += 1    
        cd.frontend.pars.labels.str_of_win.text = \
            str(cd.mg.pars.victory_points)+ '/[color=00ff00][b]' + \
            str(cd.mg.pars.crit_victory_points)+'[/color][/b]'

    if typ == "z":
        if index == -1:
            cd.mg.pars.z_out *= coef[0]
            cd.mg.pars.z_out = round(cd.mg.pars.z_out, 3)
            cd.to_str_dis_par(obj="z_out")
        else:
            cd.mg.pars.z_ins[index] *= coef[0]
            cd.mg.pars.z_ins[index] = round(cd.mg.pars.z_ins[index], 3)
            cd.frontend.pars.labels.array_of_z_in[index].text = str(cd.mg.pars.z_ins[index])

    elif typ == "z_dop":
        if index == -1:
            pass
        else:
            cd.mg.pars.z_ins_dop[index] = coef[0]*cd.mg.pars.z_ins_dop[index]
            cd.frontend.pars.labels.array_of_z_in[index].text = str(round(float(cd.mg.pars.z_ins[index]*cd.mg.pars.z_ins_dop[index]), 4))
            cd.frontend.pars.labels.array_of_z_in[index].color = [1, 0, 0, 1]
            
    elif typ == 7:  # в случае введения жёсткого карантина
        cd.mg.pars.z_ins_dop[index] = coef[0]*cd.mg.pars.z_ins_dop[index]
        cd.frontend.pars.labels.array_of_z_in[index].text = str(round(float(cd.mg.pars.z_ins[index]*cd.mg.pars.z_ins_dop[index]), 4))
        cd.frontend.pars.labels.array_of_z_in[index].color = [1, 0, 0, 1]
        cd.mg.pars.reg_quarantine[index] = True
        
        draw_for_epidemy.draw_reg_isolation(
            draw_for_epidemy.coords_of_hexes[index][0], draw_for_epidemy.coords_of_hexes[index][1],
            draw_for_epidemy.side, draw_for_epidemy.height, draw=True)
    elif typ == "d":
        if index == -1:
            cd.mg.pars.d_out *= coef[0]
            cd.mg.pars.d_out = round(cd.mg.pars.d_out, 3)
            cd.to_str_dis_par(obj="d_out")
        else:
            cd.mg.pars.d_ins[index] *= coef[0]
            cd.mg.pars.d_ins[index] = round(cd.mg.pars.d_ins[index], 3)
            cd.frontend.pars.labels.array_of_d_in[index].text = str(cd.mg.pars.d_ins[index])
            
    elif typ == "coef_of_perenos_z_out":
        cd.mg.pars.spread_coeff *= coef[0][0]
        cd.mg.pars.spread_coeff = round(cd.mg.pars.spread_coeff, 4)

        cd.mg.pars.z_out*=coef[1][0]
        cd.mg.pars.z_out = round(cd.mg.pars.z_out, 3)

        cd.to_str_dis_par(obj="transfer_c")
        cd.to_str_dis_par(obj="z_out")
        
    elif typ == "coef_skidka_na_tech":
        cd.mg.coef_skidka_na_tech *=coef[0][0]

    elif typ == "ill":
        a = cd.mg.pars.ill_nums[index]
        
        if a >= 500:
            cd.mg.pars.ill_nums[index] += coef[0][0]
            cd.mg.pars.ill_nums[index] = max(int(coef[1][0]*a), cd.mg.pars.ill_nums[index])
            cd.frontend.pars.labels.array_of_ill[index].text = spec_func.tri_sep(int(cd.mg.pars.ill_nums[index]))
            cd.mg.pars.dead_nums[index] += (a-cd.mg.pars.ill_nums[index])*cd.mg.pars.d_out*cd.mg.pars.d_ins[index]
            cd.frontend.pars.labels.array_of_dead[index].text = spec_func.tri_sep(int(cd.mg.pars.dead_nums[index]))
        else:
            if do_notify:
                if common_var.lang == 0:
                    widget_of_common_par.info_message(
                        "Больных для изоляции в регионе №" + str(index) +
                        " не смогли обнаружить\n(их слишком мало)", 'bad', 2)
                elif common_var.lang == 1:
                    widget_of_common_par.info_message("Too small quantity of ill in region №" + str(index), 'bad', 2)
    elif typ == "zd":
        if index == -1:
            cd.mg.pars.d_out *= coef[1][0]
            cd.mg.pars.d_out = round(cd.mg.pars.d_out, 3)
            cd.to_str_dis_par(obj="d_out")
            cd.mg.pars.z_out *= coef[0][0]
            cd.mg.pars.z_out = round(cd.mg.pars.z_out, 4)
            cd.to_str_dis_par(obj="z_out")

    elif typ == "z_in_z_out":
        cd.mg.pars.z_ins[index] *= coef[0][0]
        cd.mg.pars.z_ins[index] = round(cd.mg.pars.z_ins[index], 3)

        cd.frontend.pars.labels.array_of_z_in[index].text = str(cd.mg.pars.z_ins[index]) 
        cd.mg.pars.z_out *= coef[1][0]
        cd.mg.pars.z_out = round(cd.mg.pars.z_out, 3)
        cd.to_str_dis_par(obj="z_out")   
        
    elif typ == 3:  # masks
        cd.mg.pars.z_out *= coef[0][0]
        cd.mg.pars.z_out = round(cd.mg.pars.z_out, 3)
        cd.to_str_dis_par(obj="z_out") 
        
        cd.mg.pars.earned_straph_b += coef[1][0]
        cd.mg.pars.penalty_points += coef[1][0]
        cd.frontend.pars.labels.str_of_straph.text = \
            str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' +\
            str(cd.mg.pars.crit_penalty_points)+'[/color][/b]'

        cd.frontend.wid[3].label_of_tech.update_text(do_generate=True)

    elif typ == 10:  # vaccine
        if cd.mg.pars.immunated[index] == cd.mg.My_population[index]:
            if common_var.lang == 0:
                widget_of_common_par.info_message("Всё население в регионе №" + str(index) +
                                                        " иммунно к инфекции!", 'good', 2)
            elif common_var.lang == 1:
                widget_of_common_par.info_message("All population in region #" + str(index) +
                                                        " is immune for the disease!", 'good', 2)
            do_notify = False
            return
        cd.mg.pars.z_ins_dop[index] /= \
            (cd.mg.My_population[index]-cd.mg.pars.immunated[index])/\
            (cd.mg.My_population[index]+0.01)
        delta = cd.mg.My_population[index] - cd.mg.pars.immunated[index]
        
        if delta > cd.mg.My_population[index]*0.25:
            delta = cd.mg.My_population[index]*0.25
            
        if cd.mg.parameters_of_tech[10][2][1][0] - delta >= 0:
            cd.mg.pars.immunated[index] += delta  # а как быть с уже больными?
            remain = cd.mg.parameters_of_tech[10][2][1][0] - delta
            cd.mg.parameters_of_tech[10][2][1][0] = 1000*round(remain/1000)
        else:
            cd.mg.pars.immunated[index] += cd.mg.parameters_of_tech[10][2][1][0] 
            cd.mg.parameters_of_tech[10][2][1][0] = 0
            if common_var.lang == 0:
                widget_of_common_par.info_message("Закончились дозы вакцины (не хватило для вакцинации региона №"+str(index)+")", 'bad', 2)
            elif common_var.lang == 1:
                widget_of_common_par.info_message("Vaccine doses have run out!", 'bad', 2)
            do_notify = False
        
        cd.mg.archive_proc_immunated[len(cd.mg.archive_proc_immunated)-1][index] = cd.mg.pars.immunated[index]/cd.mg.My_population[index]*100
        
        cd.mg.archive_proc_immunated_sum[len(cd.mg.archive_proc_immunated_sum)-1] = sum(cd.mg.pars.immunated)/sum(cd.mg.My_population)*100
        
        cd.mg.pars.z_ins_dop[index] *= (cd.mg.My_population[index]-cd.mg.pars.immunated[index])/(cd.mg.My_population[index]+0.01)
        cd.frontend.pars.labels.array_of_z_in[index].text = str(round(float(cd.mg.pars.z_ins[index]*cd.mg.pars.z_ins_dop[index]), 4))
        
        text_for_tech_generator.generate_texts_for_tech()
        cd.frontend.wid[10].label_of_tech.update_text()
        
    elif typ == 12:  # distant
        if coef[0] > 1:
            cd.mg.pars.earned_straph_b -= 1
            cd.mg.pars.penalty_points -= 1
            cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]' 
        else:
            cd.mg.pars.earned_straph_b += 1
            cd.mg.pars.penalty_points += 1
            cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]' 
                                    
        cd.mg.pars.z_out *= coef[0]
        cd.mg.pars.z_out = round(cd.mg.pars.z_out, 3)
        cd.to_str_dis_par(obj="z_out")            
    
    elif typ == 13:  # propaganda
        cd.mg.pars.crit_penalty_points = round(coef[0]*cd.mg.pars.crit_penalty_points)
        cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]' 

    elif typ == 15:  # coin emission
        cd.mg.pars.coins += coef[0][0]
        cd.frontend.pars.labels.cash_label.text = icon_func.add_money_icon(string = str(cd.mg.pars.coins), size = cd.frontend.pars.labels.cash_label.font_size)
        if cd.mg.parameters_of_tech[15][2][1][0] < 2:
            cd.mg.parameters_of_tech[15][2][1][0]+=1
        
        cd.mg.pars.earned_straph_b += coef[2][0]
        cd.mg.pars.penalty_points += coef[2][0]

        if cd.mg.My_Country.index == 8:
            if cd.mg.parameters_of_tech[15][2][2][0] == 0:
                cd.mg.parameters_of_tech[15][2][2][0] = cd.random.randint(0, 2)
            else:
                cd.mg.parameters_of_tech[15][2][2][0] += cd.random.randint(0, 2)>0
        else:
            cd.mg.parameters_of_tech[15][2][2][0] *= 1.3
        if cd.mg.parameters_of_tech[15][2][2][0]%1 < 0.2:
            cd.mg.parameters_of_tech[15][2][2][0] = cd.math.floor(cd.mg.parameters_of_tech[15][2][2][0])
        else:
            cd.mg.parameters_of_tech[15][2][2][0] = cd.math.ceil(cd.mg.parameters_of_tech[15][2][2][0])
        if cd.mg.parameters_of_tech[15][2][2][0] > 5:
            cd.mg.parameters_of_tech[15][2][2][0] = 5 
        cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]' 
        for i in range(common_var.QUANT_OF_TECH):
            if cd.mg.counter_of_buys[i][0] < tech_info.quant_of_buys[i][0] or tech_info.quant_of_buys[i][0] == -1:
                cd.mg.prices_of_tech[i][0] -= coef[1][0]  # как обычно, цены меньше нуля, поэтому падают
        text_for_tech_generator.generate_texts_for_tech()
        for i in range(common_var.QUANT_OF_TECH):
            if hasattr(cd.frontend.wid[i], "label_of_tech"):  # unlocked haven't that attribute
                cd.frontend.wid[i].label_of_tech.update_text()
            
    elif typ == 16:  # govcompany
        cd.mg.pars.coins += coef[0][0]
        cd.frontend.pars.labels.cash_label.text = icon_func.add_money_icon(string = str(cd.mg.pars.coins), size = cd.frontend.pars.labels.cash_label.font_size)
        
        cd.mg.pars.earned_straph_b += coef[1][0]
        cd.mg.pars.penalty_points += coef[1][0]
        cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]' 
        
        cd.mg.parameters_of_tech[16][2][0][0] -= 1
        if cd.mg.parameters_of_tech[16][2][0][0] < 1:
            cd.mg.parameters_of_tech[16][2][0][0] = 1
        
        cd.mg.parameters_of_tech[16][2][1][0] += 1*(cd.random.randint(0, 5) > 2)
        # народ ещё сильнее недоволен, но непонятно как
        
        cd.frontend.wid[16].label_of_tech.update_text(do_generate=True)
        if cd.mg.counter_of_buys[16][1] >= cd.mg.quant_of_buys[16][1]:
            print("All goscompanies were sold")

    elif typ == 17:  # taxes increasing
        cd.mg.pars.earned_straph_b += coef[0][0]
        cd.mg.pars.penalty_points += coef[0][0]
        cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]' 

        cd.mg.parameters_of_tech[17][2][0][0] += 1*(cd.random.randint(0, 3) > 0)
        # народ ещё сильнее недоволен, но непонятно как
        
        cd.frontend.wid[17].label_of_tech.update_text(do_generate=True)
        
    elif typ == 18:  # region isolation
        cd.mg.pars.reg_quarantine[index] = True  # it counts quarantine
        draw_for_epidemy.draw_reg_isolation(
            draw_for_epidemy.coords_of_hexes[index][0], draw_for_epidemy.coords_of_hexes[index][1],
            draw_for_epidemy.side, draw_for_epidemy.height, draw=True)

    elif typ == 19:  # money laundering
        if 19 not in cd.mg.actions_end_step:
            cd.mg.actions_end_step.append(19)
        else:
            cd.mg.actions_end_step.remove(19)
    
    elif typ == 20:  # transferts
        if 20 not in cd.mg.actions_end_step:
            cd.mg.actions_end_step.append(20)
        else:
            cd.mg.actions_end_step.remove(20)    
        cd.mg.pars.earned_win_b += coef[1][0]
 
        cd.mg.pars.victory_points += coef[1][0]        
        cd.frontend.pars.labels.\
            str_of_win.text = str(cd.mg.pars.victory_points) + '/[color=00ff00][b]' +\
                              str(cd.mg.pars.crit_victory_points)+'[/color][/b]'
        
    elif typ == 21 and not cd.mg.pars.reg_stats_distortion[index]:  # distortion of stats
        cd.mg.pars.reg_stats_distortion[index] = True
        draw_for_epidemy.draw_reg_distortion(draw=True, reg_id=index)
        
        cd.frontend.circles_situation_in_hexes[index][1].update_color()
        cd.frontend.circles_situation_in_hexes[index][3].update_color()
        
    elif typ == 22:  # automatisation
        if not cd.mg.pars.reg_automatisated[index]:
            cd.mg.pars.reg_automatisated[index] = True
            draw_for_epidemy.draw_automation(draw=True, reg_id=index)
        else:
            widget_of_common_par.info_message(["Автоматизация в этом регионе была проведена ранее", "Automatisation was made in this region earlier"][common_var.lang], typ="bad", t=2)
            do_notify = False

    elif typ == 23:  # optimisation
        for i in range(len(cd.mg.parameters_of_tech)):
            if cd.mg.parameters_of_tech[i][3][0] < -cd.mg.parameters_of_tech[23][2][0][0]:
                cd.mg.parameters_of_tech[i][3][0] += 1
                if cd.mg.is_activated[i]:
                    cd.mg.pars.income += 1
                    cd.frontend.pars.labels.str_of_income.text =\
                        icon_func.add_money_icon(string=str(cd.mg.pars.income),
                                                 size=cd.frontend.pars.
                                                 labels.str_of_income.font_size)
        cd.mg.pars.z_out *= cd.mg.parameters_of_tech[23][2][1][0]
        cd.mg.pars.z_out = round(cd.mg.pars.z_out, 3)
        cd.to_str_dis_par(obj="z_out")
        
        text_for_tech_generator.generate_texts_for_tech()
        for i in range(len(cd.mg.parameters_of_tech)):
            if hasattr(cd.frontend.wid[i], "label_of_tech"):  # unlocked haven't that attribute
                cd.frontend.wid[i].label_of_tech.update_text()
            
    elif typ == 24:  # import of ill
        a_ind = None
        b_ind = None
        do_stop = False
        for a in range(20):
            for b in range(20):
                if cd.mg.Existing_of_hexes[a][b][0] == 1 and cd.mg.Existing_of_hexes[a][b][1] == index:
                    a_ind = a
                    b_ind = b
                    do_stop = True
                    break
            if do_stop:
                break

        candidats = [(a_ind, b_ind-1), (a_ind, b_ind+1), (a_ind-1, b_ind-1+a_ind % 2),
                     (a_ind-1, b_ind+a_ind % 2), (a_ind+1, b_ind-1+a_ind % 2), (a_ind+1, b_ind+a_ind % 2)]
        ind_candidats = []
        for i in candidats:
            if cd.mg.Existing_of_hexes[i[0]][i[1]][0] == 1:
                i_can = cd.mg.Existing_of_hexes[i[0]][i[1]][1]
                if not cd.mg.pars.reg_quarantine[i_can]:  # i.e. no quarantine
                    ind_candidats.append(i_can)
        delta = 0       
        for i in ind_candidats:
            c = cd.mg.pars.ill_nums[i]
            cd.mg.pars.ill_nums[i] = max(0.05*c, c+cd.mg.parameters_of_tech[24][2][0][0])
            delta += c - cd.mg.pars.ill_nums[i]
            cd.frontend.pars.labels.array_of_ill[i].text = spec_func.tri_sep(int(cd.mg.pars.ill_nums[i]))

        cd.mg.pars.ill_nums[index] += delta
        cd.frontend.pars.labels.array_of_ill[index].text = spec_func.tri_sep(int(cd.mg.pars.ill_nums[index]))

    elif typ == 25:  # plasma
        cd.mg.pars.d_ins_dop[index]*=cd.mg.parameters_of_tech[25][2][0]
        cd.frontend.pars.labels.array_of_d_in[index].text = str(round(float(cd.mg.pars.d_ins[index]\
                                                                                                  *cd.mg.pars.d_ins_dop[index]), 4))
        cd.frontend.pars.labels.array_of_d_in[index].color = [1,0,0,1]
                
    elif typ == 26:  # lawmaking
        variants = []
        for i in range(common_var.QUANT_OF_TECH):
            if cd.frontend.wid[i].is_available != True and tech_info.min_goldreserves_for_tech[i] < 2000 and tech_info.min_stars_for_tech[i] < 2000:
                variants.append(i)
        print("New methods variants", variants)
        if len(variants) != 0:
            num = cd.random.choice(variants)
            cd.frontend.wid[num].is_available = True
            cd.mg.techs_avail_bool[num] = True
            init_of_tech.init_tech_card(num, changing_content=True)
            print(num, "was chosen")
        else:
            widget_of_common_par.info_message(["Нет недоступных методов", "All methods are avalibale"][common_var.lang], typ="bad", t=2)
            do_notify = False
        
    elif typ == 27:  # power of persuasion
        if cd.stats.level_stars >= coef[1]:
            cd.mg.pars.lim_penalty_increase = coef[2][0]
            stat = cd.common_var.stars_statuses[spec_func.status_finder(value=cd.stats.stars, typ = 'stars')[0]]
            stat = [stat[0][:stat[0].find(' (')], stat[1][:stat[1].find(' (')]]
            widget_of_common_par.info_message(["Вы как "+stat[0]+ ' умеете убеждать людей в чём угодно', 
                                                     "You as "+stat[1]+ ' have perfect skill of misleading people'][common_var.lang], 
                                                    'good', 3)
            do_notify = False
        else:
            cd.mg.pars.lim_penalty_increase = coef[0][0]

    elif typ == 28:  # new investments in research
        was_invented = False
        print(cd.mg.counter_of_buys[10][0])
        if cd.mg.counter_of_buys[10][0] == 0:
            
            if cd.random.randint(0, int(1/coef[0][0])-1) == 0:
                was_invented = True
                print("VACCINE RESEARCHHED!")
                cd.mg.result_of_research = "vaccine"
        else:
            pass
        if cd.mg.counter_of_buys[11][0] == 0:
            if cd.random.randint(0, int(1/coef[1][0])-1) == 0:
                
                was_invented = True
                print("CURE RESEARCHHED!")
                if cd.mg.result_of_research == "vaccine":
                    cd.mg.result_of_research = 'vaccine+medicine'                
                else:
                    cd.mg.result_of_research = 'medicine'
        else:
            pass
        if not was_invented:
            cd.mg.result_of_research = 'no results'
            
        cd.mg.was_purchased_in_this_month[28] = True
        ob = cd.frontend.wid[28]
        ob.label_using_now = \
            cd.uix_classes.Label_with_tr(
                text_source=['Исследования\nуже ведутся!', 'Researches\nare conducting!'], font_size=ob.button_buy.font_size,
                pos_hint=ob.button_buy.pos_hint, size_hint=ob.button_buy.size_hint, color=[52/256, 235/256, 158/256, 1],
                bold=True, halign='center')
        cd.frontend.wid[28].add_widget(cd.frontend.wid[28].label_using_now)
            
        cd.frontend.wid[28].remove_widget(cd.frontend.wid[28].button_buy)
        if cd.mg.counter_of_buys[28][0] == 1: # в первый раз инвестиции
            frases = [0, 0, 0]
            frases[0] = ["Исследования начались!\nЖдите результатов в конце месяца",
                         "Researches have started!\nWait results in the end of this month!"]
            frases[1] = ["Исследования начались.\nОтчёт будет в конце месяца.",
                         "Research have started.\nReport will be in the end of the month!"]
            frases[2] = ["НИИ начали/продолжили разработку вакцины и лекарства",
                                     "Institutes commenced/continued to develop vaccine and cure"]
            frase = cd.random.choice(frases)
        
            widget_of_common_par.info_message(frase[common_var.lang], 'good', 2)
        
        do_notify = False

    elif typ == 29:  # new scientific communication
        cd.mg.parameters_of_tech[28][2][0][0]*=coef[0][0]
        cd.mg.parameters_of_tech[28][2][1][0]*=coef[1][0]
        text_for_tech_generator.generate_texts_for_tech()
        
        cd.frontend.wid[28].label_of_tech.update_text()
        
    elif typ == 30:  # humanitarian aid
        if cd.stats.level_stars <= coef[0]:
            hum_text = [cd.mg.My_Country.name[0] + ' получила гуманитарную помощь ',
                        cd.mg.My_Country.name[1] + ' has received humanitarian aid']
            cd.mg.pars.income += coef[1]
            
        else:
            hum_text = [cd.mg.My_Country.name[0] +
                        ' будет оказывать гуманитарную помощь\nразвивающимся странам',
                        cd.mg.My_Country.name[1] +
                        ' will be providing humanitarian aid\nto developing countries']

            cd.mg.pars.earned_win_b += 1
            cd.mg.pars.victory_points += 1    
            cd.frontend.pars.labels.str_of_win.text = str(cd.mg.pars.victory_points)+ '/[color=00ff00][b]' + str(cd.mg.pars.crit_victory_points)+'[/color][/b]'
            
            cd.mg.pars.income +=coef[2]
            
        cd.frontend.pars.labels.str_of_income.text = icon_func.add_money_icon(string = str(cd.mg.pars.income), 
                                                                                                            size = cd.frontend.pars.labels.str_of_income.font_size)        
        widget_of_common_par.info_message(hum_text[common_var.lang], 'good', 3)
        do_notify = False

    elif typ == 31:  # health lifestyle

        cd.mg.pars.z_out*=coef[0]
        cd.mg.pars.z_out = round(cd.mg.pars.z_out, 3)
        cd.to_str_dis_par(obj="z_out")
        
        cd.mg.pars.d_out*=coef[1]
        cd.mg.pars.d_out = round(cd.mg.pars.d_out, 3)
        cd.to_str_dis_par(obj="d_out")
        
        cd.mg.pars.crit_penalty_points +=coef[2]
        cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]'        
        
        cd.mg.was_purchased_in_this_month[31] = True
        ob = cd.frontend.wid[31]
        ob.label_using_now = cd.uix_classes.Label_with_tr(text_source=['Оздоровление\nудалсоь!',
                                                                                'We are now\nhealthier!'], 
                                                                    font_size=ob.button_buy.font_size,
                                                                    pos_hint=ob.button_buy.pos_hint,
                                                                    size_hint=ob.button_buy.size_hint,
                                                                    color=[32/256, 187/256, 214/256, 1],
                                                                    bold=True, halign='center')
        cd.frontend.wid[31].add_widget(cd.frontend.wid[31].label_using_now)
            
        cd.frontend.wid[31].remove_widget(cd.frontend.wid[31].button_buy)
        
        cd.mg.parameters_of_tech[31][2][0] = 0.98
        cd.mg.parameters_of_tech[31][2][1] = 0.99
        text_for_tech_generator.generate_texts_for_tech()
        cd.frontend.wid[31].label_of_tech.update_text()
                
        #for i in range(len(cd.mg.parameters_of_tech)): I don't know why I should correct all wid[i]; I commented this otherwise it would break (label of tech doesn't exist in unlocked methods)
        #    cd.frontend.wid[i].label_of_tech.update_text()
    for i in range (0, cd.mg.n):
        cd.mg.update_situations(i)    
 
    if do_notify:
        if common_var.lang == 0:
            widget_of_common_par.info_message("Операция выполнена", 'good', 2)
        elif common_var.lang == 1:
            widget_of_common_par.info_message("Operation is completed", 'good', 2)


def research_results():
    if cd.mg.result_of_research == 'vaccine':
        cd.mg.opened_by_research.append(10)
        cd.mg.pars.coins -= cd.mg.prices_of_tech[10][0] #цены всё ещё меньше нуля
        cd.frontend.wid[10].Multiply_on_parameter(instance = 20)
        text_from = [cd.mg.My_disease.padezhi[1], cd.mg.My_disease.small_name[1]]
        frases = [0, 0, 0, 0]
        frases[0] = ["Поздравляем! Ваши учёные создали вакцину от " + text_from[0]+ "!",
                     "Congratulations! Your scientists inventioned vaccine against " + text_from[1] + "!"]
        frases[1] = ["Вакцина от " + text_from[0] + " изобретена!",
                     "Vaccine against " + text_from[1]+" is invented!"]
        frases[2] = ["Вакцина от " + text_from[0] + " созадана",
                     "Scinentists finally invented vaccine against " + text_from[1]+"!"]
        frases[3] = ["Вакцина от " +text_from[0]+" готова!\nМожете начинать вакцинацию!",
                     "Vaccine against "+text_from[1]+" is ready!\nYou can start vaccination right now!"]
        frase = cd.random.choice(frases)
        widget_of_common_par.info_message(frase[common_var.lang], 'good', 2)
        
    if cd.mg.result_of_research == 'medicine' or\
            cd.mg.result_of_research == "vaccine+medicine":
        cd.mg.opened_by_research.append(11)
        cd.mg.pars.coins -= cd.mg.prices_of_tech[11][0]  # цены всё ещё меньше нуля
        cd.frontend.wid[11].Multiply_on_parameter(instance=20)
        
        text_from = [cd.mg.My_disease.padezhi[1], cd.mg.My_disease.small_name[1]]
        frases = [0, 0, 0, 0]
        frases[0] = ["Поздравляем! Ваши учёные создали лекарство от " + text_from[0]+ "!",
                     "Congratulations! Your scientists inventioned a cure for " + text_from[1] + "!"]
        frases[1] = ["Лекарство от " + text_from[0] + " изобретено!",
                     "Medicine against " + text_from[1]+" is invented!"]
        frases[2] = ["Лекарство от " + text_from[0] + " создано",
                     "Scinentists finally invented cure against " + text_from[1]]
        frases[3] = ["Лекарство от " +text_from[0]+" готово!\nНа горизонте победа в игре!",
                     "Cure against "+text_from[1]+"is ready!\nYou can start vaccination right now!"]
        frase = cd.random.choice(frases)
        widget_of_common_par.info_message(frase[common_var.lang], 'good', 5)
        
    if cd.mg.result_of_research == 'no results':
        '''frases = [0, 0, 0, 0, 0, 0]
        
        frases[0] = ["Не всегда получается так, как Вы хотите :(\nНо продвижения в исследованиях имеются", 
                     "It's not always as you want :(\nContinue researchers and next time you will do your best!"]
        frases[1] = ["Учёным необходимо провести дополнительные эксперименты", 
                     "Scieintists need more experiments"]
        frases[2] = ["Разработка идёт полным ходом, но ещё далеко до завершения!",
                     "Developing is goint at full speed\nbut it's pretty long time for final"]
        frases[3] = ["Нужно больше времени на исследования!",
                     "Think-tanks need more time for researches!"]
        frases[4] = ["Исследования в " + cd.mg.My_Country.prepositional_case + " идут медленно :(",
                     "Researches in " + cd.mg.My_Country.name[1]+ " are quite slow :("]
        frases[5] = ["Нет новых открытий.",
                     "No inventions."]
        frase = cd.random.choice(frases)
        
        widget_of_common_par.info_message(frase[common_var.lang], 'info', 2.5)
        '''
        frase = ["ничего не было открыто", "nothing was discovered"]
        wdate = spec_func.month_back(cd.mg.pars.date)
        # -1 в дате за то, что нумерация с 0, а не с 1, и ещё -1, так как за прошлый месяц.
        frase_res_ru = "Результаты за " + common_var.months_names[wdate[1]-1][0] + ':\n' + frase[0]
        frase_res_en = "Results for " + common_var.months_names[wdate[1]-1][1] + ':\n' + frase[1]
        pr_str_28 = cd.frontend.wid[28].label_of_tech.text
        
        disc_by_sc = ''
        if common_var.lang == 0:
            if pr_str_28.find('учёными') != -1:
                disc_by_sc = pr_str_28[pr_str_28.find('Открыто учёными'):]
            
            pr_str_28 = pr_str_28[:pr_str_28.find('Результат')]
            
        if common_var.lang == 1:
            if pr_str_28.find('Created by')!=-1:
                disc_by_sc = pr_str_28[pr_str_28.find('Created by'):]
            
            pr_str_28 = pr_str_28[:pr_str_28.find('Result')]
            
        cd.frontend.wid[28].label_of_tech.text=pr_str_28+[frase_res_ru, frase_res_en][common_var.lang]+disc_by_sc
    else:
        text_for_tech_generator.generate_texts_for_tech()
        cd.frontend.wid[28].label_of_tech.update_text()
