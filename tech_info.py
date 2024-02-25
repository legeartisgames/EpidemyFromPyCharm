'''
Номера технологий таковы:
Инвестиции в производство 0
Инвестиции в больницы 1
Инвестиции в НИИ 2
Маски и перчатки 3
Карантин в столице 4
Ограничение сообщения 5
Изолировать! 6
Жёсткий карантин 7
Массовые тесты 8
Научная коммуникация 9
Вакцина 10
Лекарство 11

Цена исследования технологий:
Инвестиции в производство 15
Инвестиции в больницы 10
Инвестиции в НИИ 12
Маски и перчатки 5
Карантин в столице 8
Ограничение сообщения 12
Изолировать! 10
Жёсткий карантин 15
Массовые тесты 12
Научная коммуникация 30
Вакцина 180
Лекарство 180

Возможность Активации/Деактивации (за бесплатно):
Инвестиции в производство Нет
Инвестиции в больницы Нет
Инвестиции в НИИ Нет
Маски и перчатки Нет
Карантин в столице Да
Ограничение сообщения Да
Изолировать! Нет
Жёсткий карантин Нет
Массовые тесты Нет
Научная коммуникация Нет
Вакцина Нет
Лекарство Нет

Возможное число приобретений технологии:
Инвестиции в производство бесконечно.\n - Там, куда попали больные, дополнительно заболевает '+str(cd.mg.parameters_of_tech[24][2][1][0]*100)+'% от числа попавших больных
Инвестиции в больницы бесконечно
Инвестиции в НИИ бесконечно
Маски и перчатки 1 раз
Карантин в столице 1 раз
Ограничение сообщения 1 раз
Изолировать! 1 раз
Жёсткий карантин 1 раз
Массовые тесты 1 раз
Научная коммуникация 1 раз
Вакцина 1 раз
Лекарство 1 раз
'''

prices_of_tech = [0]*100

prices_of_tech[0] = [-25]
prices_of_tech[1] = [-12]
prices_of_tech[2] = [-12]
prices_of_tech[3] = [-12]
prices_of_tech[4] = [-5, 0] #activation
prices_of_tech[5] = [-12, 0] #activation
prices_of_tech[6] = [-18, -2]
prices_of_tech[7] = [-15, -5]
prices_of_tech[8] = [-12, -1]
prices_of_tech[9] = [-30]
prices_of_tech[10] = [-150, 0]
prices_of_tech[11] = [-200]
prices_of_tech[12] = [-15]
prices_of_tech[13] = [-10]
prices_of_tech[14] = [-15]
prices_of_tech[15] = [-5, 0] #0 для применения - исключительно ради удобства
prices_of_tech[16] = [-5, 0] #0 для применения - исключительно ради удобства
prices_of_tech[17] = [-5, 0]
prices_of_tech[18] = [-10, -1]
prices_of_tech[19] = [-10]
prices_of_tech[20] = [-5]
prices_of_tech[21] = [-8, -1]
prices_of_tech[22] = [-12, -5]
prices_of_tech[23] = [-20]
prices_of_tech[24] = [-10, -2]
prices_of_tech[25] = [-20, -2]
prices_of_tech[26] = [-5, -2]
prices_of_tech[27] = [-5]
prices_of_tech[28] = [-5]
prices_of_tech[29] = [-30]
prices_of_tech[30] = [-5]
prices_of_tech[31] = [-7]

parameters_of_tech = [0]*32
parameters_of_tech[0] =  ['income', -1, [1, "+"], [3, "+"]] 
parameters_of_tech[1] = ["zd", -1, [[0.9, "*"], [0.85, "*"]], [0, "+"]] 
parameters_of_tech[2] = [2, -1, 1, [0, "+"]] 
parameters_of_tech[3] = [3, -1, [[0.8, "*"], [3, "+"]], [0, "+"]] #z_out и число штрафных очков
parameters_of_tech[4] = ["z_in_z_out", 0, [[0.8, "*"], [0.9, "*"]], [-1, "+"]] 
parameters_of_tech[5] = ["coef_of_perenos_z_out", -1, [[1/50, "*"], [0.75, "*"]], [-3, "+"]] 
parameters_of_tech[6] = ["ill", 0, [[-20000, "+"], [1/10, "*"]], [0, "+"]]
parameters_of_tech[7] = [7, 0, [1/12, "*"], [0, "*"]]
parameters_of_tech[8] = ["z_dop", 0, [0.6, "*"], [0, "+"]]
parameters_of_tech[9] = ["coef_skidka_na_tech", -1, [[3, "*"], [0.7, "*"]], [0, "+"]]
parameters_of_tech[10] = [10, 0, [[5*10**6, "+"], [10**6, "+"], [2, "+"]], [0, "+"]]#новые дозы, уже имеющиеся дозы, цена изготовления
parameters_of_tech[11] = ["zd", -1, [[0.5, "*"], [0.001, "*"]], [0, "+"]] 

parameters_of_tech[12] = [12, -1, [.85, "*"], [0, "+"]] #parameters_of_tech[12][0] really is z_out, but very specific
parameters_of_tech[13] = [13, -1, [1.5, "*"], [-2, "+"]]
parameters_of_tech[14] = ["z", -1, [.67, "*"], [-2, "+"]]

parameters_of_tech[15] = [15, -1, [[12, "+"], [1, "+"], [1, "+"]], [0, "+"]] #первый параметр - кол-во полученных монет, второй - подорожание технологий, третий - насколько повысилось число штрафных очков 
parameters_of_tech[16] = [16, -1, [[12, "+"], [1, "+"]], [-1, "+"]] #первый параметр - кол-во полученных монет, второй - насколько повысилось число штрафных очков 
parameters_of_tech[17] = [17, -1, [[2, "+"]], [+1, "+"]] #[2] - число штрафных очков

parameters_of_tech[18] = [18, 0, [0, "*"], [0, "+"]]
parameters_of_tech[19] = [19, 0, [[2, "+"], [1, "+"]], [-3, "+"]] #первое - число монет, уходящих в золотовалютыне резервы каждый ход, число штрафных очков, получаемых каждый ход
parameters_of_tech[20] = [20, 0, [[0.5, "+"], [1, "+"]], [-2, "+"]] #первое - число звёзд репутации, получаемых каждый ход, второе - дополнительное число победных очков, которое есть, пока технология активирована

parameters_of_tech[21] = [21, -1, [1, "+"], [0, "+"]]#параметр - число штрафных очков, получаемых за применённый гекс
parameters_of_tech[22] = [22, -1, [1, "+"], [0, "+"]]#параметр показывает понижение стоимости применения технологии для региона
parameters_of_tech[23] = [23, 0, [[1, "+"], [.95, "*"]], [0, "+"]]#первый параметр показывает, какое минимальное число монет падения дохода должно быть у технологии, чтобы была скидка в 1 монету, второй - уменьшение z_out

parameters_of_tech[24] = [24, -1, [[-5000, "+"], [0, "*"]], [0, "+"]] #первый параметр - до скольки больных можно импортировать в данный регион из соседнего, второй - доп. увеличение числа больных при импортировании
parameters_of_tech[25] = [25, -1, [.3, "*"], [0, "+"]] #параметр показывает, во сколько раз понижается смертность
parameters_of_tech[26] = [26, -1, 1, [0, "+"]]

parameters_of_tech[27] = [27, -1, [[7, "+"], 7, [3, "+"]], [0, "+"]]#первый параметр показывает, не более чем на какую величину растёт число штрафных очков за ход, второй - какой статус надо иметь, чтобы было как в третьем параметре.
parameters_of_tech[28] = [28, -1, [[1/10, "%"], [1/15, "%"]], [0, "+"]]#первый параметр показывает вероятность открыть вакцину, второй - лекарство 
parameters_of_tech[29] = [29, -1, [[1.5, "*"], [2, "*"]], [0, "+"]]#первое - повышение вероятности найти вакцину, второе - лекарство
parameters_of_tech[30] = [30, -1, [4, 3, -5, 1], [0, "+"]]#максимальный возможный уровень благосостояния для получения помощи; увеличение дохода при этом; падение дохода, если мы богаче определённого; возрастание штрафных баллов при этом
parameters_of_tech[31] = [31, -1, [0.97, 0.95, 1], [0, "+"]]#умножение d_out; увеличение предела числа штрафных очков

names_of_tech = [0]*32
names_of_tech[0] = ["Инвестиции в производство", "Production Investments"]
names_of_tech[1] = ["Инвестиции в больницы", "Hospital Investments"]
names_of_tech[2] = ["Инвестиции в исследования: старое", "Research Investments: old"]
names_of_tech[3] = ["Маски и перчатки", "Masks&Gloves"]
names_of_tech[4] = ["Запрет авиаперевозок", "Airflights cancellation"]
names_of_tech[5] = ["Ограничение сообщения", "Reduce of communication"]
names_of_tech[6] = ["Изолировать!", "Isolate!"]
names_of_tech[7] = ["Жёсткий карантин", "Strict quarantine"]
names_of_tech[8] = ["Массовые тесты", "Mass tests"]
names_of_tech[9] = ["Научная коммуникация: старое", "Scientific communication: old"]
names_of_tech[10] = ["Вакцина", "Vaccine"]
names_of_tech[11] = ["Дешёвое лекарство", "Medicine"]
names_of_tech[12] = ["Дистанционное образование", "Distance education"]
names_of_tech[13] = ["Пропаганда", "Propaganda"]
names_of_tech[14] = ["Работа на удалёнке", "Remote working"]
names_of_tech[15] = ["Денежная эмиссия", "Money emmission"] 
names_of_tech[16] = ["Продажа госкомпании", "Sale of state company"] 
names_of_tech[17] = ["Повышение налогов", "Increasing of taxes"]
names_of_tech[18] = ["Блокада региона", "Region blockade"]
names_of_tech[19] = ["Коррупция", "Money laundering"]
names_of_tech[20] = ["Трансферты", "Transferts"]
names_of_tech[21] = ["Искажение фактов", "Distortion of stats"]
names_of_tech[22] = ["Автоматизация", "Automatisation"]
names_of_tech[23] = ["Оптимизация", "Optimisation"]
names_of_tech[24] = ["Своз больных", "Collecting of ill people"]
names_of_tech[25] = ["Сыворотка", "Plasma"]
names_of_tech[26] = ["Законотворчество", "Lawmaking"]
names_of_tech[27] = ["Сила убеждения", "Power of persuasion"]
names_of_tech[28] = ["Инвестиции в исследования", "Investments in research"]
names_of_tech[29] = ["Научная коммуникация", "Scientific communication"]
names_of_tech[30] = ["Гуманитарная помощь", "Humanitarian Aid"]
names_of_tech[31] = ["Здоровый образ жизни", "Healthy lifestyle"]

possible_of_activation = [False, False, False, 
                          True, True, True, 
                          False, False, False, 
                          False, False, False, 
                          True, True, True, 
                          False, False, False, 
                          False, True, True, 
                          False, False, False, 
                          False, False, False,
                          False, False, False,
                          False, False] #массив с активациями для технологий

possible_of_paying_to_action = [False, False, False, 
                                False, False, False, 
                                True, True, True, 
                                False, True, False, 
                                False, False, False, 
                                False, False, False, 
                                True, False, False, 
                                True, True, False, 
                                True, True, False,
                                False, False, False,
                                False, False] #pay for do something in hex

quant_of_buys = ([-1, None], [-1, None], [-1, None], 
                 [1, None], [1, None], [1, None], 
                 [1, None], [1, None], [1, None], 
                 [1, None], [1, None], [1, None], 
                 [1, None], [1, None], [1, None], 
                 [1, None], [1, 5], [1, None], 
                 [1, None], [1, None], [1, None], 
                 [1, None], [1, None], [1, None], 
                 [1, None], [1, None], [1, None],
                 [1, None], [-1, None], [1, None],
                 [1, None], [-1, None]) # в этом кортеже хранится информация о максимальном возможном числе покупок данной технологии
'''
type of get - как будем называть процесс получения чего-то. Записываем числами:
0 - цена инвестиции
1 - цена исследования
2 - цена освоения
3 - цена применения
'''
type_of_get = [0, 0, 0, 
               2, 2, 2, 
               2, 2, 2, 
               2, 1, 1, 
               2, 2, 2, 
               2, 2, 2, 
               2, 2, 2, 
               2, 2, 2, 
               2, 1, 2,
               2, 0, 2,
               2, 0]

what_counting = [0]*32#список, в котором храним информацию о том, о чём пишем "применено столько-то раз"
what_counting[15] = 1#считаем применение emission
what_counting[16] = 1#считаем применение goscompany
what_counting[17] = 1#increasing of nalogy
what_counting[26] = 1#lawmaking

min_goldreserves_for_tech = [0]*32
min_goldreserves_for_tech[12] = 55 #distant
min_goldreserves_for_tech[13] = 250
min_goldreserves_for_tech[14] = 80
min_goldreserves_for_tech[20] = 140
min_goldreserves_for_tech[22] = 800
min_goldreserves_for_tech[24] = 900
min_goldreserves_for_tech[25] = 1000
min_goldreserves_for_tech[26] = 23
min_goldreserves_for_tech[27] = 6#power of persuasion


min_stars_for_tech = [0]*32
min_stars_for_tech[2] = 10000000#old sci-investments
min_stars_for_tech[9] = 10000000#old sci-communication
min_stars_for_tech[15] = 120
min_stars_for_tech[16] = 215
min_stars_for_tech[17] = 1.5
min_stars_for_tech[18] = 80
min_stars_for_tech[19] = 300
min_stars_for_tech[21] = 400
min_stars_for_tech[23] = 600
min_stars_for_tech[30] = 13#humanitarian aid
min_stars_for_tech[31] = 450#healthy


td = {
  "politics": ["Политика", "Politics"],
  "economics": ["Экономика", "Economics"],
  "society": ["Общество", "Society"],
  "activation": ["С активацией", "With activation"],
  "regional": ["Региональный", "Regional"],
  "investition": ["Инвестиции", "Investition"],
  "z_reduction": ["Уменьшает распространение инфекции", "Reduces spread of infection"],
  "d_reduction": ["Понижает смертность", "Reduces letality"],
  "transfer_c": ["Коэффициент переноса", "Spread coefficient"],
  "income_rises": ["Доход растёт", "Income rises"],
  "income_drops": ["Доход падает", "Income drops"],
  "money_flows": ["Бюджет пополняется", "Proficiency of budget"],
  "reg_interaction": ["Взаимодействие регионов", "Regional interaction"],
  "manipulation": ["Манипуляции", "Manipulations"],
  "status": ["Имеет значение статус репутации или благосостояния", "Your reputation or wealth status matters"]
}
tech_tags = [[['пусто', 'empty']]]*32
tech_tags[0] = [td['economics'], td['investition']]
tech_tags[1] = [td['z_reduction'], td['d_reduction'], td['investition']]

tech_tags[12] = [td['z_reduction'], td['activation']]
tech_tags[13] = [td['manipulation'], td['activation']]#propaganda
tech_tags[14] = [td['z_reduction'], td['economics'], td['activation']]#distant working

tech_tags[15] = [td['economics'], td['money_flows']]#emission
tech_tags[16] = [td['economics'], td['income_drops'], td['money_flows']]#sale of state company
tech_tags[17] = [td['economics'], td['income_rises']]#increasing of taxes

tech_tags[18] = [td['transfer_c'], td['regional']]#regional isolation
tech_tags[19] = [td['manipulation'], td['activation']]#corruption
tech_tags[20] = [td['society'], td['activation']]#transferts

tech_tags[21] = [td['manipulation'], td['regional']]#distortion of facts
tech_tags[22] = [td['regional']]#automatisation
tech_tags[23] = [td['economics'], td['income_rises']]#optimisation

tech_tags[24] = [td['reg_interaction']]#transporting of ill
tech_tags[25] = [td['d_reduction']]#plasma
tech_tags[26] = [td['politics']]#lawmaking

tech_tags[27] = [td['manipulation'], td['status']]#power of persuasion
tech_tags[30] = [td['economics'], td['society'], td['status']]#humanitarian aid
tech_tags[31] = [td['society'], td['z_reduction'], td['d_reduction'], td['investition']]#healthy lifestyle

'''
идеи для новых технологий:
быстрые больницы: тратите 3 монеты на регион. В результате: для около 5000 человек каждый ход смертность понижается в 2 раза.
объявление о победе: не более 5 применений. За каждое применение на 2 хода: z_out больше в 1.6 раза, +1 победный балл, лимит штрафных очков выше на 5.
закупка зарубежных препаратов: тратите 2 монету на регион, понижаете в нём смертность в этот ход на 30% (это число растёт со временем). Можно применять не раньше сентября 2020 (определяем случайным образом отклонением, это обусловлено ситуацией в других странах)
продажа земли в аренду: если активировано, то +3 к доходу, но и rewarded interstitial video каждый ход.
чрезвычайная ситуация: доход = -нормальный доход страны/3, z_out падает в 5 раз, деактивирует все методы, лимит штрафных очков больше на четверть.

закрытие общественных пространств: пока активировано:
в тех регионах, где базовое z_in больше 2 или проживает более 1/(число гексов в стране - 2) населения, z_in меньше в 1.5 раза

контролируемая вариоляция: (вводят маленькие дозы живого вируса. 

От оспы смерность при вариоляции 2%). Вроде как есть вариоляция только для оспы
заразите 10000 больных в регионе за 1 монету. Из них около 1-5% (от заболевания зависит) умрёт, остальные тут же выздоровят и получат иммунитет. 
живая вакцина: аналог вариоляции, только стоимость 50 монет, а смертность только раз в 10 ниже, чем от болезни (и определяется случайным образом).
коммендантский час: пока активно, получаете 2 штрафных балла, z_out падает на 5%. Цена: 5 монет.
track-and-trace app: понижает z_out. z_out*=(1-d_out).
подсчёты: только для режима неизвестной инфекции за 1 монетку на данный ход можно узнать параметры z_out, d_out и коэф. переноса. стоимость: 5 монет.
если есть паника: если слишком много штрафных очков в регионе (больше 3), то не работает большинство методов к этому региону.
60 Мб python bundle,  в том числе 10 Мб numpy, 15 Mb matplotlib


#улучшение: инвестциии в исследования сделать нормальными: вкладываем что-то каждый ход, и когда-то получаем лекарство или вакцину. А то, что сейчас, переименовываем в инвестиции в бизнес
Идея.
"Эпидемия" была игрой о борьбе с эпидемией в отдельной стране, поэтому там нельзя было ждать помощи от других стран.
Можно сделать режим, в котором надо будет победить эпидемию за конечные сроки (год-полтора), но при этом страна может получать помощь от других стран: вакцины, деньги (для развивающихся стран).
'''