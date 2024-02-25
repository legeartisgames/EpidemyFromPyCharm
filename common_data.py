# -*- coding: utf-8 -*-

import copy
import datetime
import math
import pickle
import random

import frases  # for some phrases for buttons, labels etc.
import sizes
import spec_func
import icon_func

import common_var
import country_variants
import diseases
import game_modes
import tech_info
import uix_classes

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatter import ScatterPlane
from custom_kivy.my_scrollview import ScrollView


def props(cls):
    return [i for i in cls.__dict__.keys() if i[:1] != '_']


class GameStatsAndSettings:
    def __init__(self, **kwargs):
        super(GameStatsAndSettings, self).__init__(**kwargs)
        self.set_pars_to_basic()

    def set_pars_to_basic(self):
        self.goldreserves = 25
        self.lang = 1
        import locale
        try:
            print("Locale. Default language and coding:", locale.getdefaultlocale())
            if locale.getdefaultlocale()[0] == 'ru':
                self.lang = 0
        except:
            print("locale.getdefaultlocale failed, setting English...")

        self.is_language_set = 0
        self.number_of_games = 0
        self.victory_percent = 1  # not in percent but in part of 1
        self.stars = 0
        self.cols_on_page_of_tech = 3
        self.possible_of_continue_game = False
        self.level_stars = 0
        self.level_coins = 1

        self.is_music_playing = True
        self.volume_of_music = 0.7

        self.sizes_ruler_on = True
        self.are_shown_unlocked_methods = True

        self.results_by_countries = [0] * 1000
        self.results_by_diseases = [0] * 300
        for i in range(len(self.results_by_countries)):
            self.results_by_countries[i] = list()
        for i in range(len(self.results_by_diseases)):
            self.results_by_diseases[i] = list()
        self.days_of_activity = list(list())

    def set_pars_from_file(self, f_stats):
        for i in properties_stats:
            if hasattr(f_stats, i):
                setattr(self, i, getattr(f_stats, i))

    def save_to_file(self):
        with open('../game_stats.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        print("game statistics is saved")


stats = GameStatsAndSettings()
properties_stats = props(GameStatsAndSettings())
try:
    with open('../game_stats.pkl', 'rb') as file_stats:
        loaded_stats = pickle.load(file_stats)
        stats.set_pars_from_file(f_stats=loaded_stats)  # to-do: copy constructor is better
        del loaded_stats

except FileNotFoundError:
    print("[Warning] No stats file, creating new empty")
    stats = GameStatsAndSettings()
    stats.save_to_file()
except AttributeError:
    stats = GameStatsAndSettings()
    stats.save_to_file()
    print("[Warning] Attribute error in stats file")

continue_game = False
common_var.previous_lang = int(stats.lang)

common_var.lang = int(stats.lang)  # Russian; 1 if English
common_var.tech_cols_num = stats.cols_on_page_of_tech

today_date = (datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
first_run_in_this_day = False
if today_date not in stats.days_of_activity:
    stats.days_of_activity.append(today_date)
    first_run_in_this_day = True


escape_ind = 0

page2 = GridLayout(cols=stats.cols_on_page_of_tech, size_hint_y=None) # techno page
page2.bind(minimum_height=page2.setter('height'))

page2_1 = ScrollView(size_hint=(.8, None), height=sizes.height_res, pos_hint={'center_x': .5, 'center_y': .5},
                     do_scroll_x=False, bar_color=[.35, .35, .25, 1], bar_width=10,
                     scroll_type=['bars', 'content'], bar_margin=sizes.width_res * 0.005)
page2_1.add_widget(page2)

pre_final_layout = BoxLayout(size=(sizes.width_res, sizes.height_res))
final_layout = FloatLayout()

pre_final_layout.size = (sizes.width_res, sizes.height_res)
pre_final_layout.pos = (0, 0)

victory_percent_str = [str(round(stats.victory_percent * 100, 1)) + "%",
                    str(round(stats.victory_percent * 100, 1)) + "%"]


def close_game(dt):
    App.get_running_app().stop()


common_var.need_s = spec_func.status_finder('stars', stats.stars)[1]
common_var.need_c = spec_func.status_finder('coins', stats.goldreserves)[1]


class EmptyClass:
    pass


stencil_s2 = uix_classes.StencilBox(size_hint=(None, None), size=(4000, sizes.height_res),
                                    pos_hint={'center_x': .5, 'center_y': .5}, size_hint_x=.8)
s2 = ScatterPlane(do_rotation=False, scale_min=.37, scale_max=2.5, scale=.5, size_hint=(None, None),
                  width=sizes.width_res * 3, height=sizes.height_res * 3)
stencil_s2.add_widget(s2)


def to_str_dis_par(obj=""):
    global mg
    if obj == "z_out":
        if mg.My_disease.index == 4:
            frontend.pars.labels.str_for_z_out.text = ["?", "?"][common_var.lang]
        else:
            frontend.pars.labels.str_for_z_out.text = str(round(mg.pars.z_out, 3))
    if obj == "d_out":
        if mg.My_disease.index == 4:
            frontend.pars.labels.str_for_d_out.text = ["?", "?"][common_var.lang]
        else:
            frontend.pars.labels.str_for_d_out.text = str(round(mg.pars.d_out, 5))
    if obj == "transfer_c":
        if mg.My_disease.index == 4:
            frontend.pars.labels.str_of_coef_of_perenos.text = ["?", "?"][common_var.lang]
        else:
            frontend.pars.labels.str_of_coef_of_perenos.text = str(
                round(mg.pars.spread_coeff, 4))


class GameBackend:
    My_Country = country_variants.USA_land
    My_land = My_Country.cart_of_country
    My_population = list(My_Country.population)

    n = 21

    pars = EmptyClass()

    setattr(pars, 'coins', 15)  # казна в стране
    setattr(pars, 'income', My_Country.income)

    setattr(pars, 'z_out', 2.0)
    setattr(pars, 'd_out', 0.1)

    pars.z_ins = [1] * common_var.n_max  # массив с числами z_in в каждом регионе
    pars.z_ins_dop = [1] * common_var.n_max
    # массив с дополонительными коэффициентами для z_in (например, жёсткий карантин)

    pars.d_ins = [1] * common_var.n_max  # массив с числами d_in
    pars.d_ins_dop = [1] * common_var.n_max

    pars.ill_nums = [50] * common_var.n_max  # массив с числом болеющих в каждом регионе
    pars.dead_nums = [0] * common_var.n_max  # массив с числом мерших в каждом регионе
    pars.spread_coeff = 0.1
    # такая часть болеющих в данном регионе появляется в каждом регионе-соседе дополнительно

    pars.reg_quarantine = [False] * common_var.n_max
    # информация о введённом жестком карантине в регионах: 0 означает, что карантина нет, а 1 - что есть

    pars.step_num = 1  # номер хода
    pars.date = [1, 1, 2020]
    pars.penalty_points = 0
    pars.victory_points = 0

    def __init__(self, disease=diseases.covid_disease, country=country_variants.USA_land, mode=game_modes.normal_mode,
                 **kwargs):
        super(GameBackend, self).__init__(**kwargs)

        self.My_Country = country
        self.My_disease = disease
        self.My_mode = mode
        self.set_game_pars_to_basic()

        self.counter_of_buys = [0] * common_var.QUANT_OF_TECH
        # а здесь хранится информация о числе покупок по каждой технологии, сделанных игроком
        # (первый элемент - для освоения, второй - для применения)
        for i in range(len(self.counter_of_buys)):
            self.counter_of_buys[i] = [0, 0]
        self.quant_of_buys = copy.deepcopy(tech_info.quant_of_buys)
        self.n = self.My_Country.number_of_regions
        self.set_situations()
        self.init_country_part()
        self.is_activated = [False] * common_var.QUANT_OF_TECH
        self.techs_avail_bool = [None] * common_var.QUANT_OF_TECH
        self.str_of_probably_activating_tech = ["Пока нет методов\nдля региона", "No methods\nfor region yet"]
        self.index_of_capital = self.My_Country.capital_index
        self.multichoice_ind = -1
        self.multichoice_list = [0] * 21
        self.list_of_chosen = []
        self.is_chosen_only_one = 'not exists'  # number of hex which was chosen alone
        common_var.is_open_tech = 0
        self.was_purchased_in_this_month = [False] * common_var.QUANT_OF_TECH
        # были ли в этом месяце инвестиции в исследования
        self.opened_by_research = []  # что открыли через исследования
        self.result_of_research = 'no research'
        self.hexes_chosen = [0] * common_var.n_max
        self.was_playing_before = False

        self.list_of_tech_tr = [["Пока нет методов\nдля региона", "No methods\nfor region yet"]]

        self.quant_of_tech = common_var.QUANT_OF_TECH  # суммарное число технологий (+ инвестиций)

        self.coef_skidka_na_tech = 1  # коэффициент для skidki

        self.prices_of_tech = copy.deepcopy(list(tech_info.prices_of_tech))
        self.parameters_of_tech = copy.deepcopy(list(tech_info.parameters_of_tech))

        self.archive_quant_of_ill = []  # архивируется в конце хода
        self.archive_quant_of_ill_sum = []  # архивируется в конце хода

        self.archive_quant_of_dead = []  # архивируется в конце хода
        self.archive_quant_of_dead_sum = []  # архивируется в конце хода

        self.archive_recovered = []  # архивируется в конце хода
        self.archive_recovered_sum = []
        self.archive_z_in_out = []  # архивируется в начале хода

        self.archive_new_dead = []
        # число мёртвых в конце этого хода - число мёртвых в конце предыдущего хода
        self.archive_new_dead_sum = []
        self.archive_new_recovered = []
        # число выздоровевших в конце этого хода - число выздоровевших в конце предыдущего хода
        self.archive_new_recovered_sum = []
        self.archive_new_ill = []  # число больных /30 (число дней) - приблизительно сколько заболевает за день
        self.archive_new_ill_sum = []

        self.archive_proc_immunated = []  # число иммунитетных/население
        self.archive_proc_immunated_sum = []

        self.archive_penalty_points_sum = []

        self.archive_previous_game_pars_after_step(beginning=True)

        self.version_id = common_var.VERSION_ID

    def archive_game_pars_before_step(self):
        self.archive_penalty_points_sum.append(self.pars.penalty_points)

        for_arch_z = [0] * len(self.pars.z_ins)
        for i in range(len(self.pars.z_ins)):
            for_arch_z[i] = round(self.pars.z_out * self.pars.z_ins[i] * self.pars.z_ins_dop[i], 4)
        self.archive_z_in_out.append(copy.deepcopy(for_arch_z))

    def archive_previous_game_pars_after_step(self, beginning=False):

        self.archive_quant_of_ill.append(copy.deepcopy(self.pars.ill_nums))
        self.archive_quant_of_ill_sum.append(sum(self.pars.ill_nums))

        if not beginning:
            new_ill = [0] * self.n
            ind = len(self.archive_quant_of_ill)
            for i in range(self.n):
                new_ill[i] = (self.pars.ill_nums[i]) / 30.5
            self.archive_new_ill.append(copy.deepcopy(new_ill))
            self.archive_new_ill_sum.append(sum(new_ill))

        self.archive_quant_of_dead.append(copy.deepcopy(self.pars.dead_nums))
        self.archive_quant_of_dead_sum.append(sum(self.pars.dead_nums))

        if not beginning:
            self.archive_recovered.append(copy.deepcopy(self.pars.recovered))
            self.archive_recovered_sum.append(sum(self.pars.recovered))

            new_dead = [0] * self.n
            ind = len(self.archive_quant_of_dead)
            for i in range(self.n):
                new_dead[i] = (self.archive_quant_of_dead[ind - 1][i] - self.archive_quant_of_dead[ind - 2][i]) / 30.5

            self.archive_new_dead.append(copy.deepcopy(new_dead))
            self.archive_new_dead_sum.append(sum(new_dead))

            new_recovered = [0] * self.n
            ind = len(self.archive_recovered)
            for i in range(self.n):
                new_recovered[i] = (self.archive_recovered[ind - 1][i] - self.archive_recovered[ind - 2][i]) / 30.5
            self.archive_new_recovered.append(copy.deepcopy(new_recovered))
            self.archive_new_recovered_sum.append(sum(new_recovered))

        proc_im = [0] * self.n
        for i in range(self.n):
            proc_im[i] = self.pars.immunated[i] / self.My_population[i] * 100

        self.archive_proc_immunated.append(copy.deepcopy(proc_im))

        proc_im_sum = sum(self.pars.immunated) / sum(self.My_population) * 100
        self.archive_proc_immunated_sum.append(proc_im_sum)

    def init_country_part(self):
        global continue_game
        if not continue_game:
            self.My_land = self.My_Country.cart_of_country

            self.My_population = list(self.My_Country.population)

            self.index_of_capital = self.My_Country.capital_index
            self.pars.spread_coeff *= self.My_Country.ind_perenos * self.My_disease.transfer_coeff_const
            self.pars.crit_penalty_points = int(self.My_Country.crit_b * self.My_disease.c_s_points)
            self.n = self.My_Country.number_of_regions

            for i in range(self.n):
                self.pars.immunated[i] = round(self.My_disease.s_im_level * self.My_Country.population[i])

            for i in range(self.My_Country.number_of_regions):
                x = round(self.My_Country.population[
                              i] * self.My_Country.number_of_regions / self.My_Country.full_population * 70 * random.gauss(
                    1, .4))
                if x < 20:
                    x = 0
                self.pars.ill_nums[i] = x

            self.pars.ill_nums[self.index_of_capital] *= 5

            self.pars.income = self.My_Country.income

            for i in range(self.n):
                self.pars.z_ins[i] = self.My_Country.z_ins[i]
                self.pars.z_ins_dop[i] = (self.My_population[i] - self.pars.immunated[i]) / (
                        self.My_population[i] + 0.001)

            for i in range(self.n):
                self.situation_in_hexes[i][0] = self.pars.z_ins[i] * self.pars.z_out / 2.5

                self.situation_in_hexes[i][1] = math.sqrt(
                    self.pars.ill_nums[i] / self.My_Country.population[i] * 10)

                self.situation_in_hexes[i][2] = math.sqrt(math.sqrt(self.pars.d_ins[i] * self.pars.d_out))

                self.situation_in_hexes[i][3] = math.sqrt(
                    self.pars.dead_nums[i] / self.My_Country.population[i] * 50)

            start_point_y = 6
            self.Existing_of_hexes = [0] * 20
            # двумерный массив с ячейками из 2 частей - первая указывает,
            # присутствует ли гекс с данными координатами в данной стране,
            # а вторая - если присутствует, то какой у него номер
            for i in range(20):
                self.Existing_of_hexes[i] = [0] * 20
                for j in range(20):
                    self.Existing_of_hexes[i][j] = tuple([0, 0])

            for i in range(0, self.n):
                self.Existing_of_hexes[self.My_land[i][0]][self.My_land[i][1] + start_point_y] = tuple([1, i])

        if continue_game:
            self.list_of_tech_tr = []
            for i in range(common_var.QUANT_OF_TECH):
                if self.counter_of_buys[i][0] > 0 and tech_info.possible_of_paying_to_action[i] == True:
                    if i != 10:
                        self.list_of_tech_tr.append(tech_info.names_of_tech[i])
                    else:
                        self.list_of_tech_tr.append(["Вакцинация", "Vaccination"])
            if len(self.list_of_tech_tr) == 0:
                self.list_of_tech_tr = [["Пока нет методов\nдля региона", "No methods\nfor region yet"]]
        common_var.n = self.n

    def save_to_file(self):
        with open('game_exemplar_data.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        with open('game_game_pars.pkl', 'wb') as output:
            pickle.dump(self.pars, output, pickle.HIGHEST_PROTOCOL)

    def set_game_pars_to_basic(self):
        self.pars = EmptyClass()
        self.pars.date = copy.deepcopy(self.My_disease.start_date)

        self.pars.coins = self.My_disease.start_coins  # казна в стране
        self.pars.income = self.My_Country.income
        eff_month = (self.pars.date[1] - 1 + 6 * (self.My_Country.hemisphere - 1)) % 12

        self.pars.z_out = round(
            self.My_disease.z * (1 + (self.My_disease.z_out_seasonal[eff_month] - 1) * self.My_Country.fluct_z_out), 4)
        self.pars.d_out = self.My_disease.d

        # model2 self.pars.quant_of_ill2 = [0]*self.n #массив, где храним распределение больных по дням. Считаем,
        # что все болеют одинаковое время, по окончании которого некоторые умирают model2 for i in range(self.n):
        # model2 self.pars.quant_of_ill2[i] = [0]*self.My_disease.length_of_illness model2 self.pars.table_of_ill = [
        # 0]*self.n #массив, где храним суммарное число больных в регионах (одна ячейка - один регион)
        self.n = self.My_Country.number_of_regions
        self.pars.z_ins = [1] * self.n  # массив с числами z_in в каждом регионе
        self.pars.z_ins_dop = [1] * self.n
        # массив с дополонительными коэффициентами для z_in (например, жёсткий карантин)

        self.pars.d_ins = [1] * self.n  # массив с числами d_in
        self.pars.d_ins_dop = [1] * self.n

        self.pars.ill_nums = [50] * self.n  # массив с числом болеющих в каждом регионе

        self.pars.dead_nums = [0] * self.n  # массив с числом мерших в каждом регионе
        self.pars.recovered = [0] * self.n
        # модель очень проста - выздоровело = больные_в прошлом_месяце*(1-смертность)
        self.pars.immunated = [0] * self.n  # immunated - число людей с иммунитетом к болезни
        self.pars.spread_coeff = 0.1
        # такая часть болеющих в жанно регионе появляется в каждом регионе-соседе дополнительно

        self.pars.reg_quarantine = [False] * self.n
        # информация о введённом жестком карантине в регионах
        self.pars.reg_stats_distortion = [False] * self.n  # информация о скручивании статистики в регионе
        self.pars.reg_automatisated = [False] * self.n  # для технологии "автоматизация"
        self.pars.step_num = 1  # номер хода

        self.pars.earned_straph_b = 0  # например, за денежную эмиссию, не пропадает в конце хода
        self.pars.penalty_points = 0
        self.pars.crit_penalty_points = 25
        self.pars.lim_penalty_increase = 100000000

        self.pars.victory_points = 0
        self.pars.earned_win_b = 0
        self.pars.crit_victory_points = 5

        self.pars.labels = EmptyClass()
        self.pars.labels.array_of_z_in = ["1"] * self.n  # массив с полями ввода для z_in в каждом регионе
        self.pars.labels.array_of_d_in = [1] * self.n  # массив с полями ввода для d_in

        self.pars.labels.array_of_ill = ["f"] * self.n  # массив с полями ввода для болеющих в каждом регионе
        self.pars.labels.array_of_dead = ["f"] * self.n  # массив с полями ввода для умерших в каждом регионе

        self.prices_of_tech = copy.deepcopy(list(tech_info.prices_of_tech))
        self.parameters_of_tech = copy.deepcopy(list(tech_info.parameters_of_tech))
        self.list_of_tech_tr = [["Пока нет методов\nдля региона", "No methods\nfor region yet"]]
        self.is_activated = ['None'] * common_var.QUANT_OF_TECH

        self.actions_end_step = []

    def calculate_table_of_ill(self):  # model2
        for i in range(self.n):
            self.pars.table_of_ill[i] = 0
            for k in range(self.My_disease.length_of_illness):
                self.pars.table_of_ill[i] += self.pars.quant_of_ill2[i][k]

    def set_situations(self):
        self.situation_in_hexes = [0] * 21
        # массив с ситуацией эпидемии в гексе если 0, то всё отлично, если 1, то всё ужасно рассчитываем по критерию
        self.region_straphs = [0] * 21
        for i in range(21):
            self.situation_in_hexes[i] = [0] * 4  # z_in, больные, d_in, умершие
            self.region_straphs[i] = [0] * 4  # z_in, больные, d_in, умершие

    def update_situations(self, i):
        global s2
        self.situation_in_hexes[i][0] = self.pars.z_ins[i] * self.pars.z_out * self.pars.z_ins_dop[
            i] / 2.5
        with s2.canvas:
            frontend.circles_situation_in_hexes[i][0].update_color()

        self.situation_in_hexes[i][1] = math.sqrt(self.pars.ill_nums[i] / self.My_Country.population[i] * 20)
        with s2.canvas:
            frontend.circles_situation_in_hexes[i][1].update_color()

        self.situation_in_hexes[i][2] = math.sqrt(
            math.sqrt(self.pars.d_ins[i] * self.pars.d_out * self.pars.d_ins_dop[i]))
        with s2.canvas:
            frontend.circles_situation_in_hexes[i][2].update_color()

        self.situation_in_hexes[i][3] = math.sqrt(self.pars.dead_nums[i] / self.My_Country.population[i] * 100)
        with s2.canvas:
            frontend.circles_situation_in_hexes[i][3].update_color()

    def delete_game_ex(self):
        del self


mg = GameBackend()


class GameFrontend:
    pars = EmptyClass()
    pars.labels = EmptyClass()
    lp = EmptyClass()
    lp.btns = EmptyClass()
    wid = ["a"] * common_var.QUANT_OF_TECH

    def __init__(self, **kwargs):
        super(GameFrontend, self).__init__(**kwargs)
        self.init_of_game_pars_labels()
        self.init_of_left_panel()
        self.init_situation_circles()
        self.init_cart_country_pars()

    def init_cart_country_pars(self):
        self.carta_labels = EmptyClass()
        self.carta_labels.z_in_label = [0] * 21
        self.carta_labels.ill_label = [0] * 21
        self.carta_labels.d_in_label = [0] * 21
        self.carta_labels.dead_label = [0] * 21

    def init_situation_circles(self):
        self.circles_situation_in_hexes = [0] * common_var.n_max
        # массив с ситуацией эпидемии в гексе если 0, то всё отлично, если 1, то всё ужасно рассчитываем по критерию

        for i in range(common_var.n_max):
            self.circles_situation_in_hexes[i] = [0] * 4  # z_in, больные, d_in, умершие

        self.hexes_chosen = [0] * common_var.n_max

    def init_of_game_pars_labels(self):
        global mg
        self.pars = EmptyClass()
        self.pars.labels = EmptyClass()
        self.pars.labels.str_of_naselenie = [0] * 21  # бывшее str_of_naselenie

        self.pars.labels.array_of_z_in = ['none'] * common_var.n_max
        # массив с полями ввода для z_in в каждом регионе
        self.pars.labels.array_of_d_in = ['none'] * common_var.n_max
        # массив с полями ввода для d_in

        self.pars.labels.array_of_ill = ['none'] * common_var.n_max
        # массив с полями ввода для болеющих в каждом регионе
        self.pars.labels.array_of_dead = ['none'] * common_var.n_max
        # массив с полями ввода для умерших в каждом регионе

        # для отдельных гексов
        self.change_points_labs = ['0'] * common_var.n_max
        self.autom_labs = ['0'] * common_var.n_max
        # конец
        self.pars.labels.str_for_d_out = uix_classes.Label_touch(size=(50, 30), size_hint=[.42, .2],
                                                                 font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                 text=str(round(mg.pars.d_out, 3)))

        self.pars.labels.str_for_z_out = uix_classes.Label_touch(size=(50, 30), size_hint=[.42, .2],
                                                                 font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                 text=str(round(mg.pars.z_out,
                                                                                3)))  # поле ввода для z_out

        self.pars.labels.cash_label = Label(size=(50, 30), size_hint=[.42, .2],
                                            text=icon_func.add_money_icon(string=str(mg.pars.coins),
                                                                          size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                          coef=2),
                                            font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                            markup=True)  # поле ввода для числа монет
        self.pars.labels.str_of_income = Label(size=(50, 30), size_hint=[.42, .2],
                                               text=icon_func.add_money_icon(string=str(mg.pars.income),
                                                                             size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                             coef=2),
                                               font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                               markup=True)  # поле ввода для дохода страны
        self.pars.labels.str_of_coef_of_perenos = Label(size=(50, 30), size_hint_x=.42,
                                                        font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                        text=str(round(mg.pars.spread_coeff,
                                                                       3)))  # поле ввода для коэффициента переноса
        self.pars.labels.str_of_straph = uix_classes.Label_touch(size=(50, 30), size_hint=[.42, .2], text=str(
            mg.pars.penalty_points) + '/[color=ff0000][b]' + str(mg.pars.crit_penalty_points) + '[/color][/b]',
                                                                 font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                 markup=True)
        self.pars.labels.str_of_straph.color = [1, 1, 1, 1]
        self.pars.labels.str_of_straph.bold = False

        if mg.pars.penalty_points >= 5:
            self.pars.labels.str_of_straph.color = [1, .5, .2, 1]
            self.pars.labels.str_of_straph.bold = True

        if mg.pars.penalty_points >= 10:
            self.pars.labels.str_of_straph.color = [1, 0, 0, 1]

        self.pars.labels.str_of_win = Label(size=(50, 30), size_hint=[.42, .2],
                                            text=str(mg.pars.victory_points) + '/[color=00ff00][b]' + str(
                                                mg.pars.crit_victory_points) + '[/color][/b]',
                                            font_size=sizes.TEXT_SIZE_TABLE_NUMBERS, markup=True)

        self.pars.labels.str_of_date = Label(text=spec_func.generate_str_date(mg.pars.date),
                                             size_hint_x=.42, font_size=round(sizes.TEXT_SIZE_TABLE_NUMBERS * .9))

    def init_of_left_panel(self):

        self.lp = EmptyClass()
        self.lp.btns = EmptyClass()

        self.lp.table = GridLayout(cols=1, size_hint=[.28, 1], spacing=(0, sizes.height_res / 250))

        self.lp.btns.btn_fin_step = uix_classes.Button_with_image(
            # on_press = App.get_running_app().Make_step, binding see in another place
            text_source=frases.str_end_step, size_hint_y=.1,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, padding=(0, sizes.height_res / 50))
        self.lp.table.add_widget(self.lp.btns.btn_fin_step)

        self.lp.btns.btn_open_pannel_of_tech = uix_classes.ToggleButton_with_image(
            text_source=frases.str_panel_of_tech, size_hint_y=.1,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, padding=(0, sizes.height_res / 50))
        self.lp.table.add_widget(self.lp.btns.btn_open_pannel_of_tech)

        self.tech_panel_mode = "panel"

        self.lp.multichoice_layout = BoxLayout(size_hint_y=.1, spacing=sizes.width_res / 330)
        self.lp.multichoice_layout.btn_activate = uix_classes.ToggleButton_with_image(
            text_source=["Множественный\nвыбор", "Multiselect"], size_hint_x=.7,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign='center')
        if mg.multichoice_ind == -1:
            self.lp.multichoice_layout.btn_activate.state = 'normal'
        else:
            self.lp.multichoice_layout.btn_activate.state = 'down'
        self.lp.multichoice_layout.add_widget(self.lp.multichoice_layout.btn_activate)

        self.lp.multichoice_layout.btn_do_it = \
            uix_classes.Button_with_image(text_source=["Ввод", "Enter"],
                                          size_hint_x=.3,
                                          # on_press = App.get_running_app().run_asking,
                                          font_size=sizes.TEXT_SIZE_OF_COMMON_PAR)
        self.lp.multichoice_layout.add_widget(self.lp.multichoice_layout.btn_do_it)

        self.lp.table.add_widget(self.lp.multichoice_layout)

        self.lp.par_table = uix_classes.CustomGridLayout(size_hint_y=.6)
        self.lp.table.add_widget(self.lp.par_table)
        tcp_halign = 'left'
        self.lp.par_table.add_widgets(
            uix_classes.Label_with_tr(text_source=["Штрафные очки", "Penalty points"], size_hint=[1, .2],
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign=tcp_halign))

        self.lp.par_table.add_widgets(self.pars.labels.str_of_straph)

        self.lp.par_table.add_widgets(
            uix_classes.Label_with_tr(text_source=["Победные очки", "Victory points"], size_hint=[1, .2],
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign=tcp_halign))

        self.lp.par_table.add_widgets(self.pars.labels.str_of_win)

        self.lp.par_table.add_widgets(Label(
            text=icon_func.letter_to_icons_increasing_size(coef=2, string="z_out", size=sizes.TEXT_SIZE_OF_COMMON_PAR),
            size_hint=[1, .2], halign=tcp_halign,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, markup=True))

        self.lp.par_table.add_widgets(self.pars.labels.str_for_z_out)

        self.lp.par_table.add_widgets(obj=Label(
            text=icon_func.letter_to_icons_increasing_size(coef=2, string="d_out", size=sizes.TEXT_SIZE_OF_COMMON_PAR),
            size_hint=[1, .2], halign=tcp_halign,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, markup=True))

        self.lp.par_table.add_widgets(obj=self.pars.labels.str_for_d_out)

        self.lp.par_table.add_widgets(
            uix_classes.Label_with_tr(text_source=["Перенос", "Spread coeff"], size_hint_x=1,
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign=tcp_halign))
        self.lp.par_table.add_widgets(self.pars.labels.str_of_coef_of_perenos)

        self.lp.par_table.add_widgets(
            uix_classes.Label_with_tr(text_source=frases.str_money, size_hint=[1, .2], halign=tcp_halign,
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR))
        self.lp.par_table.add_widgets(self.pars.labels.cash_label)

        self.lp.par_table.add_widgets(
            uix_classes.Label_with_tr(text_source=["Доход", "Income"], size_hint=[1, .2],
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR,
                                      halign=tcp_halign))
        self.lp.par_table.add_widgets(self.pars.labels.str_of_income)

        self.lp.par_table.add_widgets(uix_classes.Label_with_tr(text_source=["Дата", "Date"],
                                                                font_size=sizes.TEXT_SIZE_OF_COMMON_PAR,
                                                                size_hint_x=.6, halign=tcp_halign))

        self.lp.par_table.add_widgets(self.pars.labels.str_of_date)
        self.lp.btns.settings_button = uix_classes.Button_with_image(
            text_source=["Дополнительное", "Additional"], size_hint_y=.1,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR)  # settings_button

        self.lp.table.add_widget(self.lp.btns.settings_button)

        pre_final_layout.add_widget(self.lp.table)


frontend = None
