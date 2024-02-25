import common_data as cd
import frases
import spec_func
import tech_info

attach_font = ''
texts_of_tech = 0
def append_cost(i):
    if tech_info.type_of_get[i] == 2:
        
        return ['[i]'+frases.str_price_of_get[0]+ '[/i] = ' + str(-cd.mg.prices_of_tech[i][0]) + ' '  + frases.str_coins[0] +'[sup]\n\n[/sup]' + attach_font,
                          '[i]'+frases.str_price_of_get[1]+ '[/i] = '+ str(-cd.mg.prices_of_tech[i][0]) + ' '  + frases.str_coins[1] +'\n\n' + attach_font]    
    
    elif tech_info.type_of_get[i] == 0: #for investition
     
        return ['[i]'+frases.str_price_of_invest[0]+ '[/i] = ' + str(-cd.mg.prices_of_tech[i][0]) + ' '  + frases.str_coins[0] +'\n\n' + attach_font,
                      '[i]'+frases.str_price_of_invest[1]+ '[/i] = ' + str(-cd.mg.prices_of_tech[i][0]) + ' '  + frases.str_coins[1] +'\n\n' + attach_font]     
    
    elif tech_info.type_of_get[i] == 1: #for research
        
        return ['[i]'+frases.str_price_of_research[0]+ '[/i] = ' + str(-cd.mg.prices_of_tech[i][0]) + ' '  + frases.str_coins[0] +'\n\n' + attach_font,
                      '[i]'+frases.str_price_of_research[1]+ '[/i] = ' + str(-cd.mg.prices_of_tech[i][0]) + ' '  + frases.str_coins[1] +'\n\n' + attach_font]         

def generate_texts_for_tech():
    global texts_of_tech
    if True:
        texts_of_tech = [' ']*cd.common_var.QUANT_OF_TECH
        
        texts_of_tech[0] = [append_cost(0)[0] + 'Ваш доход растёт на '+str(cd.mg.parameters_of_tech[0][3][0]) +' монеты\n\nПолучите 1 победный балл', 
                            append_cost(0)[1] + 'Your income grows by '+ str(cd.mg.parameters_of_tech[0][3][0])+' coins\n\nGet 1 victory point']
        
        texts_of_tech[1] = [append_cost(1)[0] + 'За каждую инвестицию в больницы:\n- z_out меньше на '+str(round((1-cd.mg.parameters_of_tech[1][2][0][0])*100, 1))+'%\n- d_out меньше на '+str(round((1-cd.mg.parameters_of_tech[1][2][1][0])*100, 1))+'%', 
                            append_cost(1)[1] +'For each investment in hospitals:\n- z_out is '+str(round((1-cd.mg.parameters_of_tech[1][2][0][0])*100, 1))+'% less\n- d_out is '+str(round((1-cd.mg.parameters_of_tech[1][2][1][0])*100, 1))+'% less']
        
                    
        texts_of_tech[2] = [append_cost(2)[0] +'За эту инвестицию Вы получаете 1 монету скидки на исследование методов (но не инвестиций)\nИвестиции в исследования оказывают в 5 раз более сильный эффект на лекарство и вакцину',
                            append_cost(2)[1] +'After this investition you get 1 coin discount for methods development (except investments)\nYour investments in research get in 5 times more intense effect on medicine and vaccine']
        
        texts_of_tech[3] = [append_cost(3)[0] +'Когда этот метод активирован:\n- z_out меньше на ' + str(round((1-cd.mg.parameters_of_tech[3][2][0][0])*100)) +'%\n- Число штрафных очков больше на '+ str(cd.mg.parameters_of_tech[3][2][1][0]) + '.', 
                            append_cost(3)[1] +'When this method is activated:\n- z_out is '+ str(round((1-cd.mg.parameters_of_tech[3][2][0][0])*100)) +'% less\n- Number of penalty points is more by '+ str(cd.mg.parameters_of_tech[3][2][1][0]) + '.']
        
        texts_of_tech[4] = [append_cost(4)[0] +'Когда этот метод активирован:\n- z_in в столице меньше на ' + str(round((1-cd.mg.parameters_of_tech[4][2][0][0])*100))+'%\n- z_out меньше на '+str(round((1-cd.mg.parameters_of_tech[4][2][1][0])*100))+'%\n- Доход меньше на '+ str(-cd.mg.parameters_of_tech[4][3][0]) + ' монету', 
                            append_cost(4)[1] +'When this method is activated:\n- z_in in capital is '+str(round((1-cd.mg.parameters_of_tech[4][2][0][0])*100))+'% less\n- z_out is '+str(round((1-cd.mg.parameters_of_tech[4][2][1][0])*100))+'% less\n- Your income reduces by '+ str(-cd.mg.parameters_of_tech[4][3][0]) + ' coin']
        
        texts_of_tech[5] = [append_cost(5)[0] +'Когда этот метод активирован:\n- Коэффициент переноса в стране меньше в '+ str(1/cd.mg.parameters_of_tech[5][2][0][0])+ ' раз' + spec_func.fin_of_word(val = 1/cd.mg.parameters_of_tech[5][2][0][0], rod = 1)+ '\n- z_out меньше на '+ str(round((1-cd.mg.parameters_of_tech[5][2][1][0])*100)) + '%\n- Доход меньше на '+ str(-cd.mg.parameters_of_tech[5][3][0]) + ' монету', 
                            append_cost(5)[1] +'When this method is activated:\n- Spread coefficient in country is '+ str(1/cd.mg.parameters_of_tech[5][2][0][0])+ ' times lower\n- z_out is '+ str(round((1-cd.mg.parameters_of_tech[5][2][1][0])*100)) + '% less \n- Income reduces by '+ str(-cd.mg.parameters_of_tech[5][3][0]) + ' coin']
        
        texts_of_tech[6] = [append_cost(6)[0] +'Потратив '+ str(-cd.mg.prices_of_tech[6][1])+' монеты на регион:\n- Если число больных в регионе > 500, то уменьшите его на ' + str(spec_func.tri_sep(-cd.mg.parameters_of_tech[6][2][0][0])) + ' (но не более, чем в '+ str(round(1/cd.mg.parameters_of_tech[6][2][1][0], 1))+' раз). При этом соотвествующая часть\nбольных умрёт', 
                            append_cost(6)[1] +'If you spend '+ str(-cd.mg.prices_of_tech[6][1])+' coin on a region:\n- If number of ill in chosen region > 500, reduce it by ' + str(spec_func.tri_sep(-cd.mg.parameters_of_tech[6][2][0][0])) + '\n(but less than in '+ str(round(1/cd.mg.parameters_of_tech[6][2][1][0], 1))+' times) Remember that some isolated ill pepople will die']
        
        
        texts_of_tech[7] = [append_cost(7)[0] +'Если потратите '+ str(-cd.mg.prices_of_tech[7][1])+' монет на регион:\n - Только на этот ход z_in в этом регионе упадёт в '+ str(round(1/cd.mg.parameters_of_tech[7][2][0], 1))+' раз'+spec_func.fin_of_word(val = 1/cd.mg.parameters_of_tech[7][2][0], rod=1)+'\n- Коэффициент переноса из данного региона и в него упадёт до 0',
                            append_cost(7)[1] +'If you spend '+ str(-cd.mg.prices_of_tech[7][1])+' coins on region:\n - Only on current turn z_in in current region reduces '+str(round(1/cd.mg.parameters_of_tech[7][2][0], 1))+' times\n- Spread coefficient from and in current region = 0']
        
        
        texts_of_tech[8] = [append_cost(8)[0] +'Если потратите '+ str(-cd.mg.prices_of_tech[8][1])+' монету на регион:\n - Только на этот ход z_in в этом регионе упадёт на ' +  str((1-cd.mg.parameters_of_tech[8][2][0])*100) +'%',
                            append_cost(8)[1] +'If you spend '+ str(-cd.mg.prices_of_tech[8][1])+' coin on a region:\n - Only on current turn z_in in current region is ' +  str((1-cd.mg.parameters_of_tech[8][2][0])*100) +'% less']
        
        texts_of_tech[9] = [append_cost(9)[0] +'Ваши инвестции в исследования оказывают тройной эффект\n\nЦена лекарства или вакцины\nпадает на '+str(round(100-cd.mg.parameters_of_tech[9][2][1][0]*100))+'%',
                            append_cost(9)[1] +'Your investitions in research get a 3 times more intense effect\n\nPrice of vaccine or medicine is '+str(round(100-cd.mg.parameters_of_tech[9][2][1][0]*100))+'% less']
        
        text_ru = 'Доступно '+str(spec_func.tri_sep(cd.mg.parameters_of_tech[10][2][1][0]))+' доз\nЗа '+str(cd.mg.parameters_of_tech[10][2][2][0]) +' монеты делаете '+str(spec_func.tri_sep(cd.mg.parameters_of_tech[10][2][0][0]))+' доз\nВакцинация: + 25% населения региона становится иммунным (если хватает доз)'
        text_en = 'Avaliable: '+str(spec_func.tri_sep(cd.mg.parameters_of_tech[10][2][1][0]))+' doses\nFor '+str(cd.mg.parameters_of_tech[10][2][2][0]) +' coins make '+str(spec_func.tri_sep(cd.mg.parameters_of_tech[10][2][0][0]))+' doses\nVaccination: + 25% of region population become immune (if you have enough doses)'
        
        texts_of_tech[10] = [append_cost(10)[0] + text_ru,
                             append_cost(10)[1] + text_en]
        
        texts_of_tech[11] = [append_cost(11)[0] +"d_out падает в " + str(round(1/cd.mg.parameters_of_tech[11][2][1][0], 1)) + " раз" + spec_func.fin_of_word(val = 1/cd.mg.parameters_of_tech[11][2][1][0], rod = 1) + "\nz_out падает в " + str(round(1/cd.mg.parameters_of_tech[11][2][0][0], 1)) +" раз" + spec_func.fin_of_word(val = 1/cd.mg.parameters_of_tech[11][2][0][0], rod = 1), 
                             append_cost(11)[1] +"d_out reduces in " + str(round(1/cd.mg.parameters_of_tech[11][2][1][0], 1)) + " times\nz_out reduces in " + str(round(1/cd.mg.parameters_of_tech[11][2][0][0], 1)) +" times"]
        
        texts_of_tech[12] = [append_cost(12)[0] +'Когда этот метод активирован:\n- НЕ летом z_out меньше на ' + str(round((1-cd.mg.parameters_of_tech[12][2][0])*100))+'%.\n- Число штрафных очков больше на 1.', 
                            append_cost(12)[1] +'When this method is activated:\n- z_out is '+str(round((1-cd.mg.parameters_of_tech[12][2][0])*100))+'% less Not in summer.\n- Number of penalty points is more by 1.']
        
        texts_of_tech[13] = [append_cost(13)[0] +'Когда этот метод активирован:\n- На этот ход число штрафных очков, приводящее к проигрышу, больше в '+str(cd.mg.parameters_of_tech[13][2][0])+' раза' + spec_func.fin_of_word(val = cd.mg.parameters_of_tech[13][2][0], rod = 1)+'.\n- Доход на '+str(-cd.mg.parameters_of_tech[13][3][0])+' монету меньше', 
                             append_cost(13)[1] +'When this method is activated:\n- Only on current turn number of penalty points leading to lose is more in '+str(cd.mg.parameters_of_tech[13][2][0])+' times.\n- Income is less by '+str(-cd.mg.parameters_of_tech[13][3][0])+' coins']   
        
        texts_of_tech[14] = [append_cost(14)[0] +'Когда этот метод активирован:\n- z_out меньше на '+str(round((1-cd.mg.parameters_of_tech[14][2][0])*100))+'%.\n- Доход на '+str(-cd.mg.parameters_of_tech[14][3][0])+' монету меньше\n (может меняться со временем)', 
                             append_cost(14)[1] +'When this method is activated:\n- z_out is '+str(round((1-cd.mg.parameters_of_tech[14][2][0])*100))+'% less.\n- Income is less by '+str(-cd.mg.parameters_of_tech[14][3][0])+' coins\n(it may change)']   
        
        texts_of_tech[15] = [append_cost(15)[0] +'За каждое применение:\n- Получите '+ str(cd.mg.parameters_of_tech[15][2][0][0]) + ' монет.\n- Цена каждого метода растёт на ' +str(cd.mg.parameters_of_tech[15][2][1][0])+' монет.\n- Число штрафных очков растёт на ' + str(cd.mg.parameters_of_tech[15][2][2][0]), 
                             append_cost(15)[1] + 'For every use:\n- Get '+ str(cd.mg.parameters_of_tech[15][2][0][0]) + ' coins.\n\n- Cost of every method or investition increase by ' +str(cd.mg.parameters_of_tech[15][2][1][0])+' coins.\n\n- Get ' + str(cd.mg.parameters_of_tech[15][2][2][0]) + ' penalty point' + 's'*(cd.mg.parameters_of_tech[15][2][2][0]>1)]   
        
        if cd.mg.parameters_of_tech[15][2][2][0] == 0:
            texts_of_tech[15] = [append_cost(15)[0] +'За каждое применение:\n- Получите '+ str(cd.mg.parameters_of_tech[15][2][0][0]) + ' монет.\n- Цена каждого метода растёт на ' +str(cd.mg.parameters_of_tech[15][2][1][0])+' монет.', 
                                 append_cost(15)[1] + 'For every use:\n- Get '+ str(cd.mg.parameters_of_tech[15][2][0][0]) + ' coins.\n\n- Cost of every method or investition increase by ' +str(cd.mg.parameters_of_tech[15][2][1][0])+' coins.']   
        
        texts_of_tech[16] = [append_cost(16)[0] +'За каждое применение (их не более '+str(cd.mg.quant_of_buys[16][1])+'):\n- Получите '+ str(cd.mg.parameters_of_tech[16][2][0][0]) + ' монет.\n- Доход навсегда падает на ' +str(-cd.mg.parameters_of_tech[16][3][0])+' монет.\n- Число штрафных очков растёт на ' + str(cd.mg.parameters_of_tech[16][2][1][0]), 
                             append_cost(16)[1] + 'For every use (max '+str(cd.mg.quant_of_buys[16][1])+'):\n\n- Get '+ str(cd.mg.parameters_of_tech[16][2][0][0]) + ' coins.\n- Income reduces by ' +str(-cd.mg.parameters_of_tech[16][3][0])+' coins.\n\n- Get ' + str(cd.mg.parameters_of_tech[16][2][1][0]) + ' penalty point' + 's'*(cd.mg.parameters_of_tech[16][2][1][0]>1)]   
        
        texts_of_tech[17] = [append_cost(17)[0] +'За каждое применение:\n- Доход навсегда растёт на ' +str(cd.mg.parameters_of_tech[17][3][0])+' монет.\n- Число штрафных очков растёт на ' + str(cd.mg.parameters_of_tech[17][2][0][0]), 
                             append_cost(17)[1] + 'For every use:\n\n- Income grows by ' + str(cd.mg.parameters_of_tech[17][3][0])+' coins.\n\n- Get ' + str(cd.mg.parameters_of_tech[17][2][0][0]) + ' penalty point' + 's'*(cd.mg.parameters_of_tech[17][2][0][0]>1)]   
    
        
        texts_of_tech[18] = [append_cost(18)[0]+'Если потратите ' +str(-cd.mg.prices_of_tech[18][1])+' монеты на регион:\n\n - Коээфициент переноса из него и в него равен 0 на этот ход.',
                             append_cost(18)[1]+'If you spend '+ str(-cd.mg.prices_of_tech[18][1])+ ' coin on region:\n\n- Spread coefficient from and in current region is 0 while this turn.']
        
            
        texts_of_tech[19] = [append_cost(19)[0] +'Когда этот метод активирован:\n- Доход меньше на '+str(-cd.mg.parameters_of_tech[19][3][0])+' coins\n- В конце каждого хода:\n* Получите ' + str(cd.mg.parameters_of_tech[19][2][0][0]) + ' coins золотовалютных резервов\n * Получите ' + str(cd.mg.parameters_of_tech[19][2][1][0]) + ' штрафной балл',
                             append_cost(19)[1] +'When this method is activated:\n- Income is less by '+str(-cd.mg.parameters_of_tech[19][3][0])+' coins\n- For every turn:\n* Get ' + str(cd.mg.parameters_of_tech[19][2][0][0]) + ' coins to gold reserves\n * Get ' + str(cd.mg.parameters_of_tech[19][2][1][0]) + ' penalty point']   
        
        texts_of_tech[20] = [append_cost(20)[0] +'Когда этот метод активирован:\n\n- Число победных очков больше на ' + str(cd.mg.parameters_of_tech[20][2][1][0]) + '\n- Доход меньше на '+str(-cd.mg.parameters_of_tech[20][3][0])+' coins\n- В конце каждого хода Вы получаете ' + str(cd.mg.parameters_of_tech[20][2][0][0]) + ' sstar',
                             append_cost(20)[1] +'When this method is activated:\n\n- Number of victory points is more by ' + str(cd.mg.parameters_of_tech[20][2][1][0]) + '\n- Income is less by '+str(-cd.mg.parameters_of_tech[20][3][0])+' coins\n- At the end of each turn you get ' + str(cd.mg.parameters_of_tech[20][2][0][0]) + ' sstar']   
        
        
        texts_of_tech[21] = [append_cost(21)[0]+'Если потратите ' +str(-cd.mg.prices_of_tech[21][1])+' монеты на регион:\n\n - В конце данного хода вы получаете за этот регион '+str(cd.mg.parameters_of_tech[21][2][0])+' штрафной балл, а не сколько положено \n(см. правую часть гекса)',
                             append_cost(21)[1]+'If you spend '+ str(-cd.mg.prices_of_tech[21][1])+ ' coin on region:\n\n- In the end of turn you get '+str(cd.mg.parameters_of_tech[21][2][0])+' penalty point for the region instead of penalty points you must get\n(see the right corner of hex)']
        
        texts_of_tech[22] = [append_cost(22)[0]+'Если потратите ' +str(-cd.mg.prices_of_tech[22][1])+' монеты на регион:\n - Методы с участием этого региона (см. букву "А" слева) стоят на '+str(cd.mg.parameters_of_tech[22][2][0])+' монету меньше, но не менее 1 монеты',
                             append_cost(22)[1]+'If you spend '+ str(-cd.mg.prices_of_tech[22][1])+ ' coin on region:\n- It is cheaper by '+str(cd.mg.parameters_of_tech[22][2][0])+' coin to use methods for this region\n(but cost of use is still greater than 0)']
        
        texts_of_tech[23] = [append_cost(23)[0] +'- Ваш доход падает на 1 монету меньше из-за методов, в которых падение дохода больше '+str(cd.mg.parameters_of_tech[23][2][0][0])+' монет\n - z_out меньше на '+str(round((1-cd.mg.parameters_of_tech[23][2][1][0])*100, 1))+'%',
                            append_cost(23)[1] +'- Your income decreases 1 coin less because of methods with decrease of income more than ' +str(cd.mg.parameters_of_tech[23][2][0][0])+' coins\n - z_out is '+str(round((1-cd.mg.parameters_of_tech[23][2][1][0])*100, 1))+'% less']
        
        
        texts_of_tech[24] = [append_cost(24)[0] +'Если потратите '+str(-cd.mg.prices_of_tech[24][1])+' монет для региона:\n\n - До '+str(-cd.mg.parameters_of_tech[24][2][0][0])+' больных (но не более 95% всех больных) из каждого соседнего неизолированного региона перемещаются в данный регион',
                            append_cost(24)[1] +'If you spend '+str(-cd.mg.prices_of_tech[24][1])+' coin on region:\n\n - Up to '+str(-cd.mg.parameters_of_tech[24][2][0][0])+' ill (but less than 95%) from the non-isolated adjournal region get transported to the region']
        texts_of_tech[25] = [append_cost(25)[0] +'Если потратите '+str(-cd.mg.prices_of_tech[25][1])+' монет на X регионов:\n- В каждом из этих регионов d_in на этот ход меньше на '+str((1-cd.mg.parameters_of_tech[25][2][0])*100)+'/X%',
                            append_cost(25)[1] +'If you spend '+str(-cd.mg.prices_of_tech[25][1])+' coins on X regions:\n- In each of these regions d_in is less on '+str((1-cd.mg.parameters_of_tech[25][2][0])*100)+'/X% for this turn']
        texts_of_tech[26] = [append_cost(26)[0] +'Если потратите '+str(-cd.mg.prices_of_tech[26][1])+' монет:\n- Панель методов на данную партию пополняется 1 методом из числа пока недоступных',
                            append_cost(26)[1] +'If you spend '+str(-cd.mg.prices_of_tech[26][1])+" coins :\n- You will get a new not-avaliable now method up to the end of current game"]
        
        texts_of_tech[27] = [append_cost(27)[0] + 'С вероятностью 67% вы за ход не можете получить более '+ str(cd.mg.parameters_of_tech[27][2][0][0])+' штрафных очков\n(несгораемые не в счёт)'\
                             + '\n\nЕсли вы по stars хотя бы ' + cd.common_var.stars_statuses[cd.mg.parameters_of_tech[27][2][1]][0] + ', то не более, чем '+ str(cd.mg.parameters_of_tech[27][2][2][0])+'.',
                             append_cost(27)[1] + "With 67% probability you can't get more than "+ str(cd.mg.parameters_of_tech[27][2][0][0])+" (non-fireproof) penalty points in one turn"\
                             + '\n\nIf your stars is less than ' + cd.common_var.stars_statuses[cd.mg.parameters_of_tech[27][2][1]][1] + " - not more than "+ str(cd.mg.parameters_of_tech[27][2][2][0])+" points in one turn."]
        add=["", ""]
        if cd.mg.opened_by_research != []:
            add = ["Открыто учёными: ", "Created by scientists: "]
            if 10 in cd.mg.opened_by_research:
                add[0]+="[color=17eb9a][b]Вакцина[/b][/color]"
                add[1]+="[color=17eb9a][b]Vaccine[/b][/color]"
                if 11 in cd.mg.opened_by_research:
                    add[0]+=", [color=4bd2db][b]Лекарство[/b][/color]"
                    add[1]+=", [color=4bd2db][b]Cure[/b][/color]"
            elif 11 in cd.mg.opened_by_research:
                    add[0]+="[color=4bd2db][b]Лекарство[/b][/color]"
                    add[1]+="[color=4bd2db][b]Cure[/b][/color]"
        
        texts_of_tech[28] = [append_cost(28)[0] + "- С вероятностью "+ str(round(100*cd.mg.parameters_of_tech[28][2][0][0], 1))+ "% Вы открываете вакцину, "\
                             "с вероятностью "+ str(round(100*cd.mg.parameters_of_tech[28][2][1][0], 1))+ "% - лекарство.\n\n- Результат будет в конце месяца\n\n"+add[0],
                             append_cost(28)[1] + "- With "+ str(round(100*cd.mg.parameters_of_tech[28][2][0][0], 1))+ "% probability you invent vaccine, "\
                             "with "+ str(round(100*cd.mg.parameters_of_tech[28][2][1][0], 1))+ "% - medicine.\n\n- Results will be in the end of the month\n\n"+add[1]]
        
        texts_of_tech[29] = [append_cost(29)[0] +'Вероятность открытия лекарства или вакцины при исследованиях повышается в 1.5 раза.',
                            append_cost(29)[1] +'Probability of inventing vaccine or medicine during researches increases in 1.5 times.']
        
        texts_of_tech[30] = [append_cost(30)[0]+'Если вы по coins не более, чем ' + cd.common_var.statuses_coins[cd.mg.parameters_of_tech[30][2][0]][0] + \
                             ', то доход растёт на '+str(cd.mg.parameters_of_tech[30][2][1]) +' coins.\n\n'+\
                             'В противном случае доход падает на '+str(-cd.mg.parameters_of_tech[30][2][2]) +' coins'
                             '  и вы получаете '+str(cd.mg.parameters_of_tech[30][2][3]) +' победный балл',
                             append_cost(30)[1]+"If your coins status isn't more than " + cd.common_var.statuses_coins[cd.mg.parameters_of_tech[30][2][0]][1] + \
                             ', then your income will grow by '+str(cd.mg.parameters_of_tech[30][2][1]) +' coins\n\n'+\
                             'Else income will drop by '+str(-cd.mg.parameters_of_tech[30][2][2]) +' coins'+\
                              '  and you will get '+str(cd.mg.parameters_of_tech[30][2][3]) +' victory point']
        texts_of_tech[31] = [append_cost(31)[0] +'Можете использовать лишь раз за ход:\n- z_out уменьшается на '+str(round((1-cd.mg.parameters_of_tech[31][2][0])*100))+ '%\n- d_out уменьшается на '+str(round((1-cd.mg.parameters_of_tech[31][2][1])*100))+ '%\n- Лимит штрафных очков растёт на '+str(cd.mg.parameters_of_tech[31][2][2]),
                            append_cost(31)[1] +'You can use it only once per turn:\n- z_out reduces on '+str(round((1-cd.mg.parameters_of_tech[31][2][0])*100))+ '%\n- d_out reduces on '+str(round((1-cd.mg.parameters_of_tech[31][2][1])*100))+ '%\n- Limit of penalty points increases on '+str(cd.mg.parameters_of_tech[31][2][2])+' point']
        
        print("Texts for tech were generated")
    
generate_texts_for_tech()