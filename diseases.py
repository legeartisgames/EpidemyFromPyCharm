'''class Disease():
    def __init__(self, day_look_ill = 2, day_infectious = 1, length_of_illness = 14, day_start_isolating = 3, 
                 d_disease = .1, z_disease = 2, possibility_to_get_ill = 1):
        self.day_look_ill = day_look_ill
        self.day_infectious = day_infectious
        self.day_start_isolating = day_start_isolating
        self.length_of_illness = length_of_illness
        self.possibility_to_ill = 1
        self.d = d_disease
        self.z = z_disease
        
covid_disease = Disease(day_look_ill = 7, day_infectious = 4, length_of_illness = 14, day_start_isolating = 5)'''
import copy
import datetime
import random

date_now = datetime.datetime.now()
now_year = date_now.year
now_month = date_now.month


class Disease:
    def __init__(self, level, z=2.0, d=0.1, name=["Болезнь", "Disease"], min_stars=0, min_golds=0, index=0, rod=0,
                 s_coins=15, s_date=[1, 1, 2020],
                 z_outs=[1.45, 1.5, 1.3, 0.9, 0.6, 0.55, 0.5, 0.5, 0.9, 1.3, 1.35, 1.4],
                 transfer_coeff_const=1.0, c_points=1.0, im_term=6, s_im_level=0.0, pad=["O"] * 6, s_name="disease]",
                 min_gold=0):
        self.z = z
        self.d = d
        self.name = name
        self.small_name = s_name
        self.min_rep_stars = min_stars
        self.min_goldreserves = min_golds
        self.level = level
        self.index = index
        self.rod = rod
        self.start_coins = s_coins

        self.start_date = s_date
        self.z_out_seasonal = z_outs
        self.transfer_coeff_const = transfer_coeff_const
        self.c_s_points = c_points

        self.s_im_level = s_im_level
        self.immunity_term = im_term  # в месяцах

        self.padezhi = pad
        self.small_name = [self.padezhi[0], s_name]

        self.min_gold = min_gold


chuma_padezhi = ["бубонная чума", "бубонной чумы", "бубонной чуме", "бубонную чуму", "бубонной чумой", "бубонной чуме"]
ospa_padezhi = ["натуральная оспа", "натуральной оспы", "натуральной оспе", "натуральную оспу", "натуральной оспой",
                "натуральной оспе"]
grip_padezhi = ["свиной грипп", "свиного гриппа", "свиному гриппу", "свиной грипп", "свиным гриппом", "свином гриппе"]
covid_padezhi = ["Covid-19"] * 6
unknown_padezhi = ["неизвестная инфекция", "неизвестной инфекции", "неизвестной инфекции",
                   "неизвестную инфекцию", "неизвестной инфекцией", "неизвестной инфекции"]
monkey_padezhi = ["оспа обезьян", "оспы обезьян", "оспе обезьян", "оспу обезьян", "оспой обезьян", "оспе обезьян"]

covid_disease = Disease(z=2.5, d=0.03, im_term=6, s_im_level=0.01,
                        name=["Covid-19", "Covid-19"], s_name="covid-19",
                        level=3, index=0, rod=0, pad=covid_padezhi)

flu_disease = Disease(z=3.2, d=0.002, im_term=2, s_im_level=0.1,
                      name=["Свиной Грипп", "Swine influenza"], s_name="swine influenza",
                      level=5, index=1, rod=0,
                      s_coins=5, s_date=[1, 3, 2009], z_outs=[2.2, 2.4, 1.5, 1, 0.7, 0.5, 0.4, 0.4, 0.7, 1, 1.6, 2],
                      transfer_coeff_const=2, c_points=1, pad=grip_padezhi, min_gold=165)

chuma_disease = Disease(z=2.3, d=0.9, im_term=120, s_im_level=0.02,
                        name=["Бубонная чума", "Bubonic plague"], s_name="bubonic plague",
                        level=9, index=2, rod=1,
                        z_outs=[0.6, 0.6, 0.9, 1.1, 1.2, 1.35, 1.45, 1.45, 1.2, 1, 0.9, 0.7],
                        s_date=[1, now_month, now_year],
                        c_points=2.5, pad=chuma_padezhi, min_gold=470)

ospa_disease = Disease(level=6, z=2.8, d=0.3, im_term=1200, s_im_level=0.03,
                       name=["Натуральная оспа", "Smallpox"], s_name="smallpox",
                       min_stars=0, min_golds=0,
                       index=3, rod=1,
                       s_coins=20,
                       s_date=[1, now_month, now_year],
                       z_outs=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       transfer_coeff_const=.6,
                       c_points=2, pad=ospa_padezhi)

monkey_pox_disease = Disease(level=2, z=1.8, d=0.1, im_term=1200, s_im_level=0.4,
                             name=["Оспа обезьян", "Monkey pox"], s_name="monkey pox",
                             min_stars=0, min_golds=0,
                             index=5, rod=1,
                             s_coins=10,
                             s_date=[1, now_month, now_year],
                             z_outs=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             transfer_coeff_const=.6,
                             c_points=.7, pad=monkey_padezhi)

diseases_list = [covid_disease, flu_disease, chuma_disease, ospa_disease, monkey_pox_disease]


def control_unknown_disease():
    global diseases_list, unknown_disease
    for i in diseases_list:
        if i.index == 4:
            diseases_list.remove(i)
    unknown_disease = copy.deepcopy(random.choice(diseases_list))
    print(unknown_disease.name)
    unknown_disease.name = ["Неизвестная инфекция", "Unknown disease"]
    unknown_disease.small_name = ["неизвестная инфекция", "unknown disease"]
    unknown_disease.padezhi = unknown_padezhi
    unknown_disease.rod = 1
    unknown_disease.index = 4
    unknown_disease.level = 7
    unknown_disease.start_coins = 20
    unknown_disease.c_s_points = 1.6
    unknown_disease.start_date = [1, now_month, now_year]
    unknown_disease.min_gold = 0
    diseases_list.append(unknown_disease)


control_unknown_disease()
numbers_in_menu_ru = [covid_disease, monkey_pox_disease, flu_disease, ospa_disease, chuma_disease, unknown_disease]
numbers_in_menu_en = [covid_disease, monkey_pox_disease, flu_disease, ospa_disease, chuma_disease, unknown_disease]
numbers_in_menu = [numbers_in_menu_ru, numbers_in_menu_en]

'''
симптомы ковида:
повышение температуры; кашель; утомляемость; потеря обоняния и вкусовых ощущений.
симптомы свиного гриппа:
    Головная боль и боли в мышцах
    Поражение верхних дыхательных путей (сухой кашель, насморк, першение в горле, нехватку воздуха)
    Повышение температуры до 38-39°
    Сильная слабость
    Стремительное развитие болезни, быстрое ухудшение состояния

симптомы чумы:
увеличенные лимфатические узлы
цианоз
признаки сепсиса

симптомы оспы:
озноб, 
повышение температуры тела, 
сильными рвущие боли в пояснице, крестце и конечностях, 
сильная жажда, головокружение, головная боль, рвота

идеи для болезней и технологий к ним:
- "прокачка водоснабжения": z падает значительно. Только для бактериальных заболеваний. (для холеры). Действует только, когда температура больше 0 
- "осушение болот": для малярии. Тоже падает z.
* учёт того, что некоторые болезни только тропические.

* какая-то болезнь с очень большим коэффициентом переноса (из-за животных).

* лёгочная чума z=1.3, летальность 100%. Скорее болеют летом
* covid дельта 
* испанский грипп: смертность 10%. z = 2.0 (?, нигде не нашёл данных), опять же большая сезонность. уровень = 5.
* корь2 (когда вакцинирована только малая часть населения: 50%). z = 15. "мутировавшая обычная корь", вакцина стоит дешевле (например, 50 монет), а у части людей оказался иммунитет.
* холера в основном летом, смертность в 2010 составила 2-4%. Планируется брать 10%. Антибиотики есть. Очень заразна при антисанитарии.
* эбола (Эбола вирус): z = 1.5, d = 0.5, есть вакцина. ДРК, Уганда, Габон, ...
* сибирская язва: летальность 15-20% (если считать, что форма кожная). Болеет в основном крупный рогатый скот. В основном смертельно за несколько дней. 
* вирус Нипах: вызывает энцефалит или респираторные заболевания, передаётся через летучих мышей, нет лекарств или вакцин, высокая смерность.
----
'''
