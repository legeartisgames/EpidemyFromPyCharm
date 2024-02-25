import common_data as cd
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
auto_end_step_clock = None
k_sigma = 0.1  # for Gauss deviation


def mode_time_callback(dt):
    if spec_func.date_go(cd.mg.pars.date, days=1)[0] == 1:
        if sizes.platform == 'android':
            sizes.plyer.vibrator.pattern(pattern=(0, .04, .015, .04))
        Step_Make(instance=0, why="need")
        cd.frontend.pars.labels.str_of_date.color = [1, 1, 1]
    if cd.mg.pars.date[0] == 15:
        # music_module.My_switch.load_and_play_music(name = '5beep', loop=False)
        if sizes.platform == 'android':
            sizes.plyer.vibrator.pattern(pattern=(0, .04, .015, .04))
        cd.frontend.pars.labels.str_of_date.color = [219/256, 145/256, 15/256]

    if cd.mg.pars.date[0] == 27:
        cd.frontend.pars.labels.str_of_date.color = [224/256, 31/256, 9/256]
    cd.mg.pars.date = spec_func.date_go(cd.mg.pars.date, days=1)
    cd.frontend.pars.labels.str_of_date.text = \
        str(spec_func.generate_str_date(cd.mg.pars.date))


def Step_Make(instance, why="btn"):
    global k_sigma
    # music_module.My_switch.load_and_play_music(name = 'click', loop=False)
    # последовательность действий: начисляются деньги, люди умирают, число больных внутри региона увеличивается,
    # болезнь разносится (коэффициент переноса)
    
    cd.mg.archive_game_pars_before_step()
    print ("Step was made")
    
    cd.frontend.pars.labels.str_of_date.color=[1,1,1]
    cd.mg.pars.coins+=cd.mg.pars.income
    
    if cd.mg.pars.coins < 0:
        mes = ["Дефицит бюджета! (получаете + 1 несгораемеый штрафной балл)", "Budget deficite! (get 1 penalty point)"]
        widget_of_common_par.info_message(mes[common_var.lang], 'bad', 1.6)
        cd.mg.pars.earned_straph_b += 1

    cd.frontend.pars.labels.cash_label.text = \
        icon_func.add_money_icon(string=str(cd.mg.pars.coins),
                                 size=cd.frontend.pars.labels.cash_label.font_size)
    
    cd.mg.pars.step_num += 1
   
    if cd.mg.My_mode.index in {0, 4, 5, 6} or (cd.mg.My_mode.index in {1, 2, 3} and why == "btn"):
        cd.mg.pars.date = spec_func.two_weeks_go(cd.mg.pars.date)
        cd.frontend.pars.labels.str_of_date.text = str(spec_func.generate_str_date(cd.mg.pars.date))

    for i in range(cd.mg.n):
        cd.mg.pars.dead_nums[i] += cd.mg.pars.ill_nums[i]*cd.mg.pars.d_ins[i]*cd.mg.pars.d_out*cd.mg.pars.d_ins_dop[i]
        cd.mg.pars.dead_nums[i] = round(cd.mg.pars.dead_nums[i])

        cd.frontend.pars.labels.array_of_dead[i].text = spec_func.tri_sep(cd.mg.pars.dead_nums[i])             
        
        cd.mg.My_population[i] = cd.mg.My_Country.population[i]-cd.mg.pars.dead_nums[i]

        if cd.mg.My_population[i] < 0:
            print("Population in region #", i, "is less 0:", cd.mg.My_population[i])            
            cd.mg.My_population[i] = 0
    
        cd.mg.pars.recovered[i] += cd.mg.pars.ill_nums[i]*(1-cd.mg.pars.d_ins[i]*cd.mg.pars.d_out*cd.mg.pars.d_ins_dop[i])
        cd.mg.pars.recovered[i] = round(cd.mg.pars.recovered[i])
            
        cd.mg.pars.immunated[i] += cd.mg.pars.ill_nums[i]*(1-cd.mg.pars.d_ins[i]*cd.mg.pars.d_out*cd.mg.pars.d_ins_dop[i])
        time_again = cd.mg.pars.step_num-1 - cd.mg.My_disease.immunity_term
        if time_again >= 0: # если кто-то из переболевших уже снова может заболеть
            cd.mg.pars.immunated[i] -= (cd.mg.archive_quant_of_ill[time_again-1][i] - cd.mg.archive_new_dead[time_again][i])#нас интересуют больные на начало хода и умершие в конце
        
        cd.mg.pars.immunated[i] = round(cd.mg.pars.immunated[i])    
        
        if cd.mg.pars.immunated[i] < 0:
            print("Immunated < 0:", cd.mg.pars.immunated[i], "why?")
            cd.mg.pars.immunated[i] = 0
                
        if cd.mg.pars.immunated[i] > cd.mg.My_population[i]:
            print("Immunated > population:", cd.mg.pars.immunated[i], "why?")
            cd.mg.pars.immunated[i] = cd.mg.My_population[i] 

    coef_mult = [0]*cd.mg.n
    for a in range(20):
        for b in range(20):
            if cd.mg.Existing_of_hexes[a][b][0] == 0:
                break
            if cd.mg.pars.reg_quarantine[cd.mg.Existing_of_hexes[a][b][1]]:
                break
            cur_ind = cd.mg.Existing_of_hexes[a][b][1]
            if cd.mg.Existing_of_hexes[a][b-1][0] == 1:
                if not cd.mg.pars.reg_quarantine[cd.mg.Existing_of_hexes[a][b-1][1]]:
                    coef_mult[cur_ind] += cd.mg.pars.z_ins[cur_ind]*cd.mg.pars.z_ins_dop[cur_ind]*float(cd.mg.pars.ill_nums[cd.mg.Existing_of_hexes[a][b-1][1]])*math.sqrt(
                          cd.mg.My_population[cd.mg.Existing_of_hexes[a][b-1][1]]*cd.mg.My_population[cd.mg.Existing_of_hexes[a][b][1]])\
                        /(cd.mg.My_population[cd.mg.Existing_of_hexes[a][b-1][1]]\
                          +cd.mg.My_population[cur_ind]+1)

            if cd.mg.Existing_of_hexes[a][b+1][0] == 1:
                if not cd.mg.pars.reg_quarantine[cd.mg.Existing_of_hexes[a][b+1][1]]:
                    coef_mult[cur_ind]+=cd.mg.pars.z_ins[cur_ind]*cd.mg.pars.z_ins_dop[cur_ind]*\
                        float(cd.mg.pars.ill_nums[cd.mg.Existing_of_hexes[a][b+1][1]])*math.sqrt(
                        cd.mg.My_population[cd.mg.Existing_of_hexes[a][b+1][1]]*cd.mg.My_population[cd.mg.Existing_of_hexes[a][b][1]])/(cd.mg.My_population[cd.mg.Existing_of_hexes[a][b+1][1]]+cd.mg.My_population[cur_ind]+1)

            if cd.mg.Existing_of_hexes[a-1][b-1+a%2][0] == 1:
                if not cd.mg.pars.reg_quarantine[cd.mg.Existing_of_hexes[a-1][b-1+a%2][1]]:

                    coef_mult[cur_ind]+=cd.mg.pars.z_ins[cur_ind]*cd.mg.pars.z_ins_dop[cur_ind]*\
                        float(cd.mg.pars.ill_nums[cd.mg.Existing_of_hexes[a-1][b-1+a%2][1]])*math.sqrt(
                        cd.mg.My_population[cd.mg.Existing_of_hexes[a-1][b-1+a%2][1]]*cd.mg.My_population[cd.mg.Existing_of_hexes[a][b][1]])/(cd.mg.My_population[cd.mg.Existing_of_hexes[a-1][b-1+a%2][1]]+cd.mg.My_population[cur_ind]+1)

            if cd.mg.Existing_of_hexes[a-1][b+a%2][0] == 1:
                if not cd.mg.pars.reg_quarantine[cd.mg.Existing_of_hexes[a-1][b+a%2][1]]:
                    coef_mult[cur_ind] += cd.mg.pars.z_ins[cur_ind]*cd.mg.pars.z_ins_dop[cur_ind]*\
                        float(cd.mg.pars.ill_nums[cd.mg.Existing_of_hexes[a-1][b+a%2][1]])*math.sqrt(
                                                cd.mg.My_population[cd.mg.Existing_of_hexes[a-1][b+a%2][1]]*cd.mg.My_population[cd.mg.Existing_of_hexes[a][b][1]])/(cd.mg.My_population[cd.mg.Existing_of_hexes[a-1][b+a%2][1]]+cd.mg.My_population[cur_ind]+1)

            if cd.mg.Existing_of_hexes[a+1][b-1+a%2][0] == 1:
                if not cd.mg.pars.reg_quarantine[cd.mg.Existing_of_hexes[a+1][b-1+a%2][1]]:

                    coef_mult[cur_ind]+=cd.mg.pars.z_ins[cur_ind]*cd.mg.pars.z_ins_dop[cur_ind]*\
                        float(cd.mg.pars.ill_nums[cd.mg.Existing_of_hexes[a+1][b-1+a%2][1]])*math.sqrt(
                                                cd.mg.My_population[cd.mg.Existing_of_hexes[a+1][b-1+a%2][1]]*cd.mg.My_population[cd.mg.Existing_of_hexes[a][b][1]])/(cd.mg.My_population[cd.mg.Existing_of_hexes[a+1][b-1+a%2][1]]+cd.mg.My_population[cur_ind]+1)

            if cd.mg.Existing_of_hexes[a+1][b+a % 2][0] == 1:
                if not cd.mg.pars.reg_quarantine[cd.mg.Existing_of_hexes[a+1][b+a%2][1]]:

                    coef_mult[cur_ind] += cd.mg.pars.z_ins[cur_ind]*cd.mg.pars.z_ins_dop[cur_ind]*\
                        float(cd.mg.pars.ill_nums[cd.mg.Existing_of_hexes[a+1][b+a%2][1]])*math.sqrt(
                                                cd.mg.My_population[cd.mg.Existing_of_hexes[a+1][b+a%2][1]]*cd.mg.My_population[cd.mg.Existing_of_hexes[a][b][1]])/(cd.mg.My_population[cd.mg.Existing_of_hexes[a+1][b+a%2][1]]+cd.mg.My_population[cur_ind]+1)

    for i in range(cd.mg.n):
        were_ill = cd.mg.pars.ill_nums[i]
         
        cd.mg.pars.d_ins[i] = round(cd.mg.pars.d_ins[i], 4)       
        cd.frontend.pars.labels.array_of_d_in[i].text = str(round(cd.mg.pars.d_ins[i], 4))
        cd.frontend.pars.labels.array_of_d_in[i].color = [0, 0, 0, 1]
        
        cd.mg.pars.ill_nums[i] += round(
            cd.mg.pars.spread_coeff*coef_mult[i]*2)

        cd.frontend.pars.labels.str_of_naselenie[i].text = spec_func.tri_sep(round(cd.mg.My_population[i]))
        
        cd.mg.pars.ill_nums[i] *= cd.random.gauss(1, k_sigma) 
        cd.mg.pars.ill_nums[i] *= cd.mg.pars.z_ins[i]*cd.mg.pars.z_out*cd.mg.pars.z_ins_dop[i]

        if not cd.mg.pars.reg_quarantine[i]:  # if no quarantine
            ad_v = int(cd.mg.pars.spread_coeff/0.1*cd.random.gauss(0, 20))
            cd.mg.pars.ill_nums[i] = ad_v + cd.mg.pars.ill_nums[i]
           
        if cd.mg.pars.ill_nums[i] >= cd.mg.My_population[i]-cd.mg.pars.immunated[i]:
            cd.mg.pars.ill_nums[i] = cd.mg.My_population[i]-cd.mg.pars.immunated[i]
        
        cd.mg.pars.ill_nums[i] = max(int(cd.mg.pars.ill_nums[i]), 0)

        cd.frontend.pars.labels.array_of_ill[i].text = \
            spec_func.tri_sep(cd.mg.pars.ill_nums[i])
        
        if cd.mg.pars.ill_nums[i] >= 100*10**6:
            cd.frontend.pars.labels.array_of_ill[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL/1.1
        
        elif cd.frontend.pars.labels.array_of_ill[i].font_size != sizes.SIZE_OF_TEXT_FOR_LABEL:
            cd.frontend.pars.labels.array_of_ill[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL
        if cd.mg.pars.dead_nums[i] >= 100*10**6:
            cd.frontend.pars.labels.array_of_dead[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL/1.1
        
        elif cd.frontend.pars.labels.array_of_dead[i].font_size != sizes.SIZE_OF_TEXT_FOR_LABEL:
            cd.frontend.pars.labels.array_of_dead[i].font_size = sizes.SIZE_OF_TEXT_FOR_LABEL
        
        cd.mg.pars.z_ins_dop[i]=(cd.mg.My_population[i]-cd.mg.pars.immunated[i])/(cd.mg.My_population[i]+0.01)  
        cd.mg.pars.d_ins_dop[i]=1 
        
        if cd.mg.pars.reg_quarantine[i]:
            cd.mg.pars.reg_quarantine[i] = False
            draw_for_epidemy.draw_reg_isolation(draw=False)  # nota bene: it discards all isolation marks!
        
        cd.frontend.pars.labels.array_of_z_in[i].text = str(round(cd.mg.pars.z_ins[i] * cd.mg.pars.z_ins_dop[i], 3))
        cd.frontend.pars.labels.array_of_z_in[i].color = [0, 0, 0, 1]

    for i in range(cd.mg.n):
        cd.mg.update_situations(i)  

    common_func.Action_in_end_step()
    
    were_straph_b = cd.mg.pars.penalty_points
    cd.mg.pars.penalty_points = cd.mg.pars.earned_straph_b
    for i in range(cd.mg.n):
        ind = True
        if cd.mg.pars.reg_stats_distortion[i]:
            cd.mg.pars.reg_stats_distortion[i] = False
            draw_for_epidemy.draw_reg_distortion(draw=False, reg_id=i)
            cd.mg.pars.penalty_points += cd.mg.parameters_of_tech[21][2][0]
            ind = False
        total_pen_points_for_reg = 0
        counter = 0
        if cd.mg.pars.ill_nums[i] >= cd.mg.My_population[i]/20:
            counter += 1
            print("ill: " + str(i))
        
        if cd.mg.pars.ill_nums[i] >= cd.mg.My_Country.population[i]/10:
            counter += math.floor(cd.mg.pars.ill_nums[i]*5/cd.mg.My_Country.population[i])

        cd.mg.region_straphs[i][1] = counter
        
        if ind:
            cd.mg.pars.penalty_points += counter
        total_pen_points_for_reg += counter
        
        counter = 0
        if cd.mg.pars.dead_nums[i]>=cd.mg.My_Country.population[i]/200:
            counter += 1
            print("dead: " + str(round(cd.mg.pars.dead_nums[i]*50/cd.mg.My_Country.population[i])) + ' ' + str(i))
        if cd.mg.pars.dead_nums[i]>=cd.mg.My_Country.population[i]/50:
            counter += math.floor(cd.mg.pars.dead_nums[i]*50/cd.mg.My_Country.population[i])
            
        cd.mg.region_straphs[i][3] = counter
        if ind:
            cd.mg.pars.penalty_points += counter
        total_pen_points_for_reg += counter
        if cd.mg.My_mode.index == 6 and i == cd.mg.My_Country.capital_index:
            if total_pen_points_for_reg >= 3: 
                ft_rus = "[b][color=ff0000]Причина поражения[/b][/color]: Столица получила " + str(total_pen_points_for_reg) + " штрафных очков\n(" + str(total_pen_points_for_reg-counter) + " штрафных баллов за число больных и " +str(counter) + " за число умерших).\n\n"
                ft_en = "[b][color=ff0000]Cause of defeat[/b][/color]: Capital added " + str(total_pen_points_for_reg) + " penalty points\n(" + str(total_pen_points_for_reg-counter) + " points because of ill people and " +str(counter) + " because of dead).\n\n" 
                go_to_lose(first_text = [ft_rus, ft_en][common_var.lang])
            elif total_pen_points_for_reg >=2 and total_pen_points_for_reg - counter > 0: #вторая проверка сделана на число больных: если весь штраф только от умерших, то игрок ничего с этим не может сделать 
                widget_of_common_par.info_message(["В столице может быть бунт!", "There may be a riot in the capital!"][common_var.lang], typ='info', t=2)
    if cd.mg.pars.penalty_points - cd.mg.archive_penalty_points_sum[cd.mg.pars.step_num-2] > cd.mg.pars.lim_penalty_increase:
        if cd.random.randint(0, 2) == 0:
            widget_of_common_par.info_message(["На этот раз Вы оказались неубедительны:(", "This time you weren't persuasive:("][common_var.lang], 'bad', 1.6)
        else:
            was_pen_p = cd.mg.pars.penalty_points 
            cd.mg.pars.penalty_points = cd.mg.archive_penalty_points_sum[cd.mg.pars.step_num-2] + cd.mg.pars.lim_penalty_increase
        
            mes = ["Ораторское мастерство выручило Вас!", "Oratory has helped you!"]
            widget_of_common_par.info_message(mes[common_var.lang], 'good', 1.6)
            
    cd.frontend.pars.labels.str_of_straph.text = str(cd.mg.pars.penalty_points) + '/[color=ff0000][b]' + str(cd.mg.pars.crit_penalty_points)+'[/color][/b]'       
    
    if cd.mg.pars.penalty_points >= cd.mg.pars.crit_penalty_points:
        go_to_lose()
        return
    
    cd.frontend.pars.labels.str_of_straph.color = [1, 1, 1, 1]
    cd.frontend.pars.labels.str_of_straph.bold = False
    if cd.mg.pars.penalty_points >= 5:
        cd.frontend.pars.labels.str_of_straph.color = [1, .5, .2, 1]
        cd.frontend.pars.labels.str_of_straph.bold = True
        
    if cd.mg.pars.penalty_points >= cd.mg.pars.crit_penalty_points - 5\
       or ((cd.mg.pars.penalty_points-were_straph_b) >= 4*cd.mg.pars.crit_penalty_points/25 and cd.mg.pars.penalty_points >= cd.mg.pars.crit_penalty_points*2/3):
        mes = ["Вы близки к проигрышу", "You are about to lose"]
        cd.frontend.pars.labels.str_of_straph.color = [1, 0, 0, 1]
        widget_of_common_par.info_message(mes[common_var.lang], 'bad', 1.6)

    cd.frontend.pars.labels.str_of_win.bold = True
    cd.frontend.pars.labels.str_of_win.color = [0, 1, 0, 1]
    for i in range(cd.mg.n):
        if (cd.mg.pars.ill_nums[i] >= 100 and\
           cd.mg.counter_of_buys[10][0] < 1 and cd.mg.counter_of_buys[11][0] < 1)\
           or (cd.mg.pars.ill_nums[i] >= cd.mg.My_population[i]/10000 and cd.mg.pars.ill_nums[i] > 50):
            cd.mg.pars.victory_points = -1 + cd.mg.pars.earned_win_b
            cd.frontend.pars.labels.str_of_win.color = [1, 1, 1, 1]
            cd.frontend.pars.labels.str_of_win.bold = False
            break
        
    cd.mg.pars.victory_points += 1
    cd.frontend.pars.labels.str_of_win.text = str(cd.mg.pars.victory_points)+ '/[color=00ff00][b]' + str(cd.mg.pars.crit_victory_points)+'[/color][/b]'
    
    if cd.mg.pars.victory_points >= cd.mg.pars.crit_victory_points:
        common_var.is_victory = 1
        if auto_end_step_clock is not None:
            auto_end_step_clock.cancel()
        else:
            print("No auto end step clock ")
        App.get_running_app().end_of_game()
        return
        
    if cd.mg.pars.date[1] in {6, 7, 8} and cd.mg.counter_of_buys[12][0] > 0 \
            and cd.frontend.wid[12].button_of_activation in cd.frontend.wid[12].children:
        # if summer and distant is researched
        cd.frontend.wid[12].label_summer = cd.uix_classes.Label_with_tr(text_source=['Лето!', 'Summer'],
                                                                        font_size=cd.frontend.wid[12].button_of_activation.font_size*1.2,
                                                                        pos_hint={'right': 0.44, 'top': 0.18},
                                                                        size_hint=cd.frontend.wid[12].button_of_activation.size_hint,
                                                                        color=[52/256, 235/256, 158/256, 1], bold=True)
        cd.frontend.wid[12].add_widget(cd.frontend.wid[12].label_summer)
        
        cd.frontend.wid[12].remove_widget(cd.frontend.wid[12].button_of_activation)
        
        if cd.mg.is_activated[12]:
            cd.frontend.wid[12].Activate_Deactivate(instance=5, do_notify=False)
            cd.mg.must_be_activated_distant = True
            
    elif cd.mg.pars.date[1] not in {6, 7, 8} and cd.mg.counter_of_buys[12][0] > 0 and cd.frontend.wid[12].button_of_activation not in cd.frontend.wid[12].children:
        if hasattr(cd.frontend.wid[12], "label_summer"):
            cd.frontend.wid[12].remove_widget(cd.frontend.wid[12].label_summer)
        if hasattr(cd.mg, "must_be_activated_distant"):
            cd.frontend.wid[12].Activate_Deactivate(instance = 5, do_notify = False)
            delattr(cd.mg, "must_be_activated_distant")
        cd.frontend.wid[12].add_widget(cd.frontend.wid[12].button_of_activation)

    for i in range(common_var.QUANT_OF_TECH):
        if cd.mg.was_purchased_in_this_month[i]:
            if i == 28: # new investments in research
                common_func.research_results()
            cd.mg.was_purchased_in_this_month[i] = False
            if i == 28:
                cd.mg.result_of_research = 'no result'           
        
            if hasattr(cd.frontend.wid[i], "label_using_now"):
                cd.frontend.wid[i].remove_widget(cd.frontend.wid[i].label_using_now)
        
            cd.frontend.wid[i].add_widget(cd.frontend.wid[i].button_buy)

    eff_month = (cd.mg.pars.date[1] - 1 + 6 * (cd.mg.My_Country.hemisphere-1)) % 12
    
    cd.mg.pars.z_out *= \
        (1+(cd.mg.My_disease.z_out_seasonal[eff_month]-1)*cd.mg.My_Country.fluct_z_out)
    # -6+6 из-за северного и южного полушарий
    cd.mg.pars.z_out /= \
        (1+(cd.mg.My_disease.z_out_seasonal[(eff_month-1) % 12]-1)*cd.mg.My_Country.fluct_z_out)
    cd.mg.pars.z_out = round(cd.mg.pars.z_out, 5)
    cd.to_str_dis_par(obj="z_out")
    
    for i in range(cd.mg.n):
        cd.mg.update_situations(i)  
    cd.mg.archive_previous_game_pars_after_step()

    cd.mg.save_to_file()
    
    if not spec_func.is_internet():
        print('No internet')
    else:
        print("Internet Ok!")
        if not common_var.IS_PREMIUM:
            if not App.get_running_app().ads.is_interstitial_loaded():
                App.get_running_app().ads.request_interstitial()
        
            if cd.mg.pars.step_num % 5 == 0:
                Clock.schedule_once(show_inter, .1)


def show_inter(dt): 
    App.get_running_app().ads.show_interstitial()


def go_to_lose(first_text=""):
    common_var.is_victory = 0
    if auto_end_step_clock is not None:
        auto_end_step_clock.cancel()
    else:
        print("No auto end day clock")
    App.get_running_app().end_of_game(first_text=first_text)
    return
