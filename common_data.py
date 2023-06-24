# -*- coding: utf-8 -*-

import copy
import math
import pickle
import random

import frases
import sizes
import spec_func
import icon_func

import common_var
import uix_classes


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
        self.per_of_victory = 1  # not in percent but in part of 1
        self.stars = 0
        self.cols_on_page_of_tech = 3
        self.possible_of_continue_game = False
        self.level_stars = 0
        self.level_coins = 1

        self.is_music_playing = True
        self.volume_of_music = 0.7

        self.is_shown_real_sizes_of_country = True
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


my_stats = GameStatsAndSettings()
properties_stats = props(GameStatsAndSettings())
try:
    file_stats = open('../game_stats.pkl', 'rb')
    my_stats2 = pickle.load(file_stats)
    file_stats.close()
    del file_stats
    my_stats.set_pars_from_file(f_stats=my_stats2)  # to-do: copy constructor is better
    del my_stats2

except FileNotFoundError:
    print("[Warning] No stats file, creating new empty")
    my_stats = GameStatsAndSettings()
    my_stats.save_to_file()
except AttributeError:
    my_stats = GameStatsAndSettings()
    my_stats.save_to_file()
    print("[Warning] Attribute error in stats file")

continue_game = False
common_var.previous_lang = int(my_stats.lang)

common_var.lang = int(my_stats.lang)  # Russian; 1 if English
common_var.K = 3 / int(my_stats.cols_on_page_of_tech)
num_of_cols_in_tech_panel = int(my_stats.cols_on_page_of_tech)

import datetime

x = (datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
first_run_in_this_day = False
if x not in my_stats.days_of_activity:
    my_stats.days_of_activity.append(x)
    first_run_in_this_day = True

print(my_stats.days_of_activity)

import country_variants
import diseases
import game_modes

escape_ind = 0
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatter import ScatterPlane
from custom_kivy.my_scrollview import ScrollView

page2 = GridLayout(cols=int(3 / common_var.K),
                   size_hint_y=None)  # страница с описанием технологий и возможностью их приобретения
page2.bind(minimum_height=page2.setter('height'))

page2_1 = ScrollView(size_hint=(.8, None), height=sizes.Height_of_screen, pos_hint={'center_x': .5, 'center_y': .5},
                     do_scroll_x=False, bar_color=[.35, .35, .25, 1], bar_width=10,
                     scroll_type=['bars', 'content'], bar_margin=sizes.Width_of_screen * 0.005)
page2_1.add_widget(page2)

pre_final_layout = BoxLayout(size=(sizes.Width_of_screen, sizes.Height_of_screen))
final_layout = FloatLayout()

pre_final_layout.size = (sizes.Width_of_screen, sizes.Height_of_screen)
pre_final_layout.pos = (0, 0)

str_percent_of_v = [str(round(my_stats.per_of_victory * 100, 1)) + "%",
                    str(round(my_stats.per_of_victory * 100, 1)) + "%"]

import tech_info


def close_game(dt):
    App.get_running_app().stop()


common_var.need_s = spec_func.status_finder('stars', my_stats.stars)[1]
common_var.need_c = spec_func.status_finder('coins', my_stats.goldreserves)[1]


class Empty_Class():
    pass


stencil_s2 = uix_classes.StencilBox(size_hint=(None, None), size=(4000, sizes.Height_of_screen),
                                    pos_hint={'center_x': .5, 'center_y': .5}, size_hint_x=.8)
s2 = ScatterPlane(do_rotation=False, scale_min=.37, scale_max=2.5, scale=.5, size_hint=(None, None),
                  width=sizes.Width_of_screen * 3, height=sizes.Height_of_screen * 3)
stencil_s2.add_widget(s2)
s2.size_hint_x = None
s2.size_hint_y = None


def to_str_dis_par(obj=""):
    global my_game
    if obj == "z_out":
        if my_game.My_disease.index == 4:
            my_game_frontend.game_pars.labels.str_for_z_out.text = ["?", "?"][common_var.lang]
        else:
            my_game_frontend.game_pars.labels.str_for_z_out.text = str(round(my_game.game_pars.z_out, 3))
    if obj == "d_out":
        if my_game.My_disease.index == 4:
            my_game_frontend.game_pars.labels.str_for_d_out.text = ["?", "?"][common_var.lang]
        else:
            my_game_frontend.game_pars.labels.str_for_d_out.text = str(round(my_game.game_pars.d_out, 5))
    if obj == "transfer_c":
        if my_game.My_disease.index == 4:
            my_game_frontend.game_pars.labels.str_of_coef_of_perenos.text = ["?", "?"][common_var.lang]
        else:
            my_game_frontend.game_pars.labels.str_of_coef_of_perenos.text = str(
                round(my_game.game_pars.coef_of_perenos, 4))


class Game_Exemplar():
    My_Country = country_variants.USA_land
    My_land = My_Country.cart_of_country
    My_population = list(My_Country.population)

    n = 21

    game_pars = Empty_Class()

    setattr(game_pars, 'coins', 15)  # казна в стране
    setattr(game_pars, 'income', My_Country.income)

    setattr(game_pars, 'z_out', 2.0)
    setattr(game_pars, 'd_out', 0.1)

    game_pars.z_ins = [1] * common_var.n_max  # массив с числами z_in в каждом регионе
    game_pars.z_ins_dop = [
                              1] * common_var.n_max  # массив с дополонительными коэффициентами для z_in (например, жёсткий карантин)

    game_pars.d_ins = [1] * common_var.n_max  # массив с числами d_in
    game_pars.d_ins_dop = [1] * common_var.n_max

    game_pars.quant_of_ill = [50] * common_var.n_max  # массив с числом болеющих в каждом регионе
    game_pars.quant_of_dead = [0] * common_var.n_max  # массив с числом мерших в каждом регионе
    game_pars.coef_of_perenos = 0.1  # такая часть болеющих в данном регионе появляется в каждом регионе-соседе дополнительно

    game_pars.is_hard_carantin_in_current_region = [
                                                       1] * common_var.n_max  # информация о введённом жестком карантине в регионах :1 означает, что карантина нет, а 0 - что есть

    game_pars.numer_step = 1  # номер хода
    game_pars.date = [1, 1, 2020]
    game_pars.straph_b = 0
    game_pars.win_b = 0

    def __init__(self, disease=diseases.covid_disease, country=country_variants.USA_land, mode=game_modes.normal_mode,
                 **kwargs):
        super(Game_Exemplar, self).__init__(**kwargs)

        self.My_Country = country
        self.My_disease = disease
        self.My_mode = mode
        self.set_game_pars_to_basic()

        self.counter_of_buys = [
                                   0] * common_var.QUANT_OF_TECH  # а здесь хранится информация о числе покупок по каждой технологии, сделанных игроком (первый элемент - для освоения, второй - для применения)
        for i in range(len(self.counter_of_buys)):
            self.counter_of_buys[i] = [0, 0]
        self.quant_of_buys = copy.deepcopy(tech_info.quant_of_buys)
        self.n = self.My_Country.number_of_regions
        self.set_situations()
        self.init_country_part()
        self.is_activated = [False] * common_var.QUANT_OF_TECH
        self.is_tech_avaliable = [None] * common_var.QUANT_OF_TECH
        self.str_of_probably_activating_tech = ["Пока нет методов\nдля региона", "No methods\nfor region yet"]
        self.index_of_capital = self.My_Country.capital_index
        self.multichoice_ind = -1
        self.multichoice_list = [0] * 21
        self.list_of_chosen = []
        self.is_chosen_only_one = 'not exists'  # number of hex which was chosen alone
        common_var.is_open_tech = 0
        self.was_purchased_in_this_month = [
                                               False] * common_var.QUANT_OF_TECH  # были ли в этом месяце инвестиции в исследования
        self.opened_by_research = []  # что открыли через исследования
        self.result_of_research = 'no research'
        self.hexes_chosen = [0] * common_var.n_max
        self.was_playing_before = False

        self.list_of_tech_tr = [["Пока нет методов\nдля региона", "No methods\nfor region yet"]]

        self.quant_of_tech = common_var.QUANT_OF_TECH  # суммарное число технологий (+ инвестиций)

        self.coef_skidka_na_tech = 1  # коэффициент для skidki

        self.prices_of_tech = copy.deepcopy(list(tech_info.prices_of_tech))
        self.parameters_of_tech = copy.deepcopy(list(tech_info.parameters_of_tech))

        self.archieve_quant_of_ill = []  # архивируется в конце хода
        self.archieve_quant_of_ill_sum = []  # архивируется в конце хода

        self.archieve_quant_of_dead = []  # архивируется в конце хода
        self.archieve_quant_of_dead_sum = []  # архивируется в конце хода

        self.archieve_recovered = []  # архивируется в конце хода
        self.archieve_recovered_sum = []
        self.archieve_z_in_out = []  # архивируется в начале хода

        self.archieve_new_dead = []  # число мёртвых в конце этого хода - число мёртвых в конце предыдущего хода
        self.archieve_new_dead_sum = []
        self.archieve_new_recovered = []  # число выздоровевших в конце этого хода - число выздоровевших в конце предыдущего хода
        self.archieve_new_recovered_sum = []
        self.archieve_new_ill = []  # число больных /30 (число дней) - приблизительно сколько заболевает за день
        self.archieve_new_ill_sum = []

        self.archieve_proc_immunated = []  # число иммунитетных/население
        self.archieve_proc_immunated_sum = []

        self.archieve_penalty_points_sum = []

        self.archieve_previous_game_pars_after_step(beginning=True)

    def archieve_game_pars_before_step(self):
        self.archieve_penalty_points_sum.append(self.game_pars.straph_b)

        for_arch_z = [0] * len(self.game_pars.z_ins)
        for i in range(len(self.game_pars.z_ins)):
            for_arch_z[i] = round(self.game_pars.z_out * self.game_pars.z_ins[i] * self.game_pars.z_ins_dop[i], 4)
        self.archieve_z_in_out.append(copy.deepcopy(for_arch_z))

    def archieve_previous_game_pars_after_step(self, beginning=False):

        self.archieve_quant_of_ill.append(copy.deepcopy(self.game_pars.quant_of_ill))
        self.archieve_quant_of_ill_sum.append(sum(self.game_pars.quant_of_ill))

        if beginning == False:

            new_ill = [0] * self.n
            ind = len(self.archieve_quant_of_ill)
            for i in range(self.n):
                new_ill[i] = (self.game_pars.quant_of_ill[i]) / 30.5
            self.archieve_new_ill.append(copy.deepcopy(new_ill))
            self.archieve_new_ill_sum.append(sum(new_ill))

        self.archieve_quant_of_dead.append(copy.deepcopy(self.game_pars.quant_of_dead))
        self.archieve_quant_of_dead_sum.append(sum(self.game_pars.quant_of_dead))

        if beginning == False:
            self.archieve_recovered.append(copy.deepcopy(self.game_pars.recovered))
            self.archieve_recovered_sum.append(sum(self.game_pars.recovered))

        if beginning == False:

            new_dead = [0] * self.n
            ind = len(self.archieve_quant_of_dead)
            for i in range(self.n):
                new_dead[i] = (self.archieve_quant_of_dead[ind - 1][i] - self.archieve_quant_of_dead[ind - 2][i]) / 30.5

            self.archieve_new_dead.append(copy.deepcopy(new_dead))
            self.archieve_new_dead_sum.append(sum(new_dead))

        if beginning == False:

            new_recovered = [0] * self.n
            ind = len(self.archieve_recovered)
            for i in range(self.n):
                new_recovered[i] = (self.archieve_recovered[ind - 1][i] - self.archieve_recovered[ind - 2][i]) / 30.5
            self.archieve_new_recovered.append(copy.deepcopy(new_recovered))
            self.archieve_new_recovered_sum.append(sum(new_recovered))

        proc_im = [0] * self.n
        for i in range(self.n):
            proc_im[i] = self.game_pars.immunated[i] / self.My_population[i] * 100

        self.archieve_proc_immunated.append(copy.deepcopy(proc_im))

        proc_im_sum = sum(self.game_pars.immunated) / sum(self.My_population) * 100
        self.archieve_proc_immunated_sum.append(proc_im_sum)

    def init_country_part(self):

        global continue_game
        if continue_game == False:
            self.My_land = self.My_Country.cart_of_country

            self.My_population = list(self.My_Country.population)

            self.index_of_capital = self.My_Country.capital_index
            self.game_pars.coef_of_perenos *= self.My_Country.ind_perenos * self.My_disease.c_coef_perenos
            self.game_pars.crit_straph_b = int(self.My_Country.crit_b * self.My_disease.c_s_points)
            self.n = self.My_Country.number_of_regions

            for i in range(self.n):
                self.game_pars.immunated[i] = round(self.My_disease.s_im_level * self.My_Country.population[i])

            for i in range(self.My_Country.number_of_regions):
                x = round(self.My_Country.population[
                              i] * self.My_Country.number_of_regions / self.My_Country.full_population * 70 * random.gauss(
                    1, .4))
                if x < 20:
                    x = 0
                self.game_pars.quant_of_ill[i] = x

            self.game_pars.quant_of_ill[self.index_of_capital] *= 5

            self.game_pars.income = self.My_Country.income

            for i in range(self.n):
                self.game_pars.z_ins[i] = self.My_Country.z_ins[i]
                self.game_pars.z_ins_dop[i] = (self.My_population[i] - self.game_pars.immunated[i]) / (
                            self.My_population[i] + 0.001)

            for i in range(self.n):
                self.situation_in_hexes[i][0] = self.game_pars.z_ins[i] * self.game_pars.z_out / 2.5

                self.situation_in_hexes[i][1] = math.sqrt(
                    self.game_pars.quant_of_ill[i] / self.My_Country.population[i] * 10)

                self.situation_in_hexes[i][2] = math.sqrt(math.sqrt(self.game_pars.d_ins[i] * self.game_pars.d_out))

                self.situation_in_hexes[i][3] = math.sqrt(
                    self.game_pars.quant_of_dead[i] / self.My_Country.population[i] * 50)

            start_point_y = 6
            self.Existing_of_hexes = [
                                         0] * 20  # двумерный массив с ячейками из 2 частей - первая указывает, присутствует ли гекс с данными координатами в данной стране, а вторая - если присутствует, то какой у него номер
            for i in range(20):
                self.Existing_of_hexes[i] = [0] * 20
                for j in range(20):
                    self.Existing_of_hexes[i][j] = tuple([0, 0])

            for i in range(0, self.n):
                self.Existing_of_hexes[self.My_land[i][0]][self.My_land[i][1] + start_point_y] = tuple([1, i])

        if continue_game == True:
            self.list_of_tech_tr = []
            for i in range(common_var.QUANT_OF_TECH):
                if self.counter_of_buys[i][0] > 0 and tech_info.possible_of_paying_to_action[i] == True:
                    if i != 10:
                        self.list_of_tech_tr.append(tech_info.names_of_tech[i])
                    else:
                        self.list_of_tech_tr.append(["Вакцинация", "Vaccination"])
            if self.list_of_tech_tr == []:
                self.list_of_tech_tr = [["Пока нет методов\nдля региона", "No methods\nfor region yet"]]
        common_var.n = self.n

    def save_to_file(self):
        with open('game_exemplar_data.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        with open('game_game_pars.pkl', 'wb') as output:
            pickle.dump(self.game_pars, output, pickle.HIGHEST_PROTOCOL)

    def set_game_pars_to_basic(self):
        self.game_pars = Empty_Class()
        self.game_pars.date = copy.deepcopy(self.My_disease.start_date)

        self.game_pars.coins = self.My_disease.start_coins  # казна в стране
        self.game_pars.income = self.My_Country.income
        eff_month = (self.game_pars.date[1] - 1 + 6 * (self.My_Country.half_ball - 1)) % 12

        self.game_pars.z_out = round(
            self.My_disease.z * (1 + (self.My_disease.z_out_seasonal[eff_month] - 1) * self.My_Country.fluct_z_out), 4)
        self.game_pars.d_out = self.My_disease.d

        # model2 self.game_pars.quant_of_ill2 = [0]*self.n #массив, где храним распределение больных по дням. Считаем, что все болеют одинаковое время, по окончании которого некоторые умирают
        # model2 for i in range(self.n):
        # model2 self.game_pars.quant_of_ill2[i] = [0]*self.My_disease.length_of_illness
        # model2 self.game_pars.table_of_ill = [0]*self.n #массив, где храним суммарное число больных в регионах (одна ячейка - один регион)
        self.n = self.My_Country.number_of_regions
        self.game_pars.z_ins = [1] * self.n  # массив с числами z_in в каждом регионе
        self.game_pars.z_ins_dop = [
                                       1] * self.n  # массив с дополонительными коэффициентами для z_in (например, жёсткий карантин)

        self.game_pars.d_ins = [1] * self.n  # массив с числами d_in
        self.game_pars.d_ins_dop = [1] * self.n

        self.game_pars.quant_of_ill = [50] * self.n  # массив с числом болеющих в каждом регионе

        self.game_pars.quant_of_dead = [0] * self.n  # массив с числом мерших в каждом регионе
        self.game_pars.recovered = [
                                       0] * self.n  # модель очень проста - выздоровело = больные_в прошлом_месяце*(1-смертность)
        self.game_pars.immunated = [0] * self.n  # immunated - число людей с иммунитетом к болезни
        self.game_pars.coef_of_perenos = 0.1  # такая часть болеющих в жанно регионе появляется в каждом регионе-соседе дополнительно

        self.game_pars.is_hard_carantin_in_current_region = [
                                                                1] * self.n  # информация о введённом жестком карантине в регионах :1 означает, что карантина нет, а 0 - что есть
        self.game_pars.is_stats_right = [True] * self.n  # информация о скручивании статистики в регионе
        self.game_pars.is_automatisated = [False] * self.n  # для технологии "автоматизация"
        self.game_pars.numer_step = 1  # номер хода

        self.game_pars.earned_straph_b = 0  # например, за денежную эмиссию, не пропадает в конце хода
        self.game_pars.straph_b = 0
        self.game_pars.crit_straph_b = 25
        self.game_pars.lim_penalty_increase = 100000000

        self.game_pars.win_b = 0
        self.game_pars.earned_win_b = 0
        self.game_pars.crit_win_b = 5

        self.game_pars.labels = Empty_Class()
        self.game_pars.labels.array_of_z_in = ["1"] * self.n  # массив с полями ввода для z_in в каждом регионе
        self.game_pars.labels.array_of_d_in = [1] * self.n  # массив с полями ввода для d_in

        self.game_pars.labels.array_of_ill = ["f"] * self.n  # массив с полями ввода для болеющих в каждом регионе
        self.game_pars.labels.array_of_dead = ["f"] * self.n  # массив с полями ввода для умерших в каждом регионе

        self.prices_of_tech = copy.deepcopy(list(tech_info.prices_of_tech))
        self.parameters_of_tech = copy.deepcopy(list(tech_info.parameters_of_tech))
        self.list_of_tech_tr = [["Пока нет методов\nдля региона", "No methods\nfor region yet"]]
        self.is_activated = ['None'] * common_var.QUANT_OF_TECH

        self.actions_end_step = []

    def calculate_table_of_ill(self):  # model2
        for i in range(self.n):
            self.game_pars.table_of_ill[i] = 0
            for k in range(self.My_disease.length_of_illness):
                self.game_pars.table_of_ill[i] += self.game_pars.quant_of_ill2[i][k]

    def set_situations(self):
        self.situation_in_hexes = [
                                      0] * 21  # массив с ситуацией эпидемии в гексе если 0, то всё отлично, если 1, то всё ужасно рассчитываем по критерию
        self.region_straphs = [0] * 21
        for i in range(21):
            self.situation_in_hexes[i] = [0] * 4  # z_in, больные, d_in, умершие
            self.region_straphs[i] = [0] * 4  # z_in, больные, d_in, умершие

    def update_situations(self, i):
        global s2
        self.situation_in_hexes[i][0] = self.game_pars.z_ins[i] * self.game_pars.z_out * self.game_pars.z_ins_dop[
            i] / 2.5
        with s2.canvas:
            my_game_frontend.circles_situation_in_hexes[i][0].update_color()

        self.situation_in_hexes[i][1] = math.sqrt(self.game_pars.quant_of_ill[i] / self.My_Country.population[i] * 20)
        with s2.canvas:
            my_game_frontend.circles_situation_in_hexes[i][1].update_color()

        self.situation_in_hexes[i][2] = math.sqrt(
            math.sqrt(self.game_pars.d_ins[i] * self.game_pars.d_out * self.game_pars.d_ins_dop[i]))
        with s2.canvas:
            my_game_frontend.circles_situation_in_hexes[i][2].update_color()

        self.situation_in_hexes[i][3] = math.sqrt(self.game_pars.quant_of_dead[i] / self.My_Country.population[i] * 100)
        with s2.canvas:
            my_game_frontend.circles_situation_in_hexes[i][3].update_color()

    def delete_game_ex(self):
        del self


my_game = Game_Exemplar()


class Game_Frontend():
    game_pars = Empty_Class()
    game_pars.labels = Empty_Class()
    left_pannel = Empty_Class()
    left_pannel.btns = Empty_Class()
    wid = ["a"] * common_var.QUANT_OF_TECH

    def __init__(self, **kwargs):
        super(Game_Frontend, self).__init__(**kwargs)
        self.init_of_game_pars_labels()
        self.init_of_left_pannel()
        self.init_situation_circles()
        self.init_cart_country_pars()

    def init_cart_country_pars(self):
        self.carta_labels = Empty_Class()
        self.carta_labels.z_in_label = [0] * 21
        self.carta_labels.ill_label = [0] * 21
        self.carta_labels.d_in_label = [0] * 21
        self.carta_labels.dead_label = [0] * 21

    def init_situation_circles(self):
        self.circles_situation_in_hexes = [
                                              0] * common_var.n_max  # массив с ситуацией эпидемии в гексе если 0, то всё отлично, если 1, то всё ужасно рассчитываем по критерию

        for i in range(common_var.n_max):
            self.circles_situation_in_hexes[i] = [0] * 4  # z_in, больные, d_in, умершие

        self.hexes_chosen = [0] * common_var.n_max

    def init_of_game_pars_labels(self):
        global my_game
        self.game_pars = Empty_Class()
        self.game_pars.labels = Empty_Class()
        self.game_pars.labels.str_of_naselenie = [0] * 21  # бывшее str_of_naselenie

        self.game_pars.labels.array_of_z_in = [
                                                  'none'] * common_var.n_max  # массив с полями ввода для z_in в каждом регионе
        self.game_pars.labels.array_of_d_in = ['none'] * common_var.n_max  # массив с полями ввода для d_in

        self.game_pars.labels.array_of_ill = [
                                                 'none'] * common_var.n_max  # массив с полями ввода для болеющих в каждом регионе
        self.game_pars.labels.array_of_dead = [
                                                  'none'] * common_var.n_max  # массив с полями ввода для умерших в каждом регионе

        # для отдельных гексов
        self.change_points_labs = ['0'] * common_var.n_max
        self.autom_labs = ['0'] * common_var.n_max
        # конец
        self.game_pars.labels.str_for_d_out = uix_classes.Label_touch(size=(50, 30), size_hint=[.42, .2],
                                                                      font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                      text=str(round(my_game.game_pars.d_out, 3)))

        self.game_pars.labels.str_for_z_out = uix_classes.Label_touch(size=(50, 30), size_hint=[.42, .2],
                                                                      font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                      text=str(round(my_game.game_pars.z_out,
                                                                                     3)))  # поле ввода для z_out

        self.game_pars.labels.str_of_money = Label(size=(50, 30), size_hint=[.42, .2],
                                                   text=icon_func.add_money_icon(string=str(my_game.game_pars.coins),
                                                                                 size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                                 coef=2),
                                                   font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                   markup=True)  # поле ввода для числа монет
        self.game_pars.labels.str_of_income = Label(size=(50, 30), size_hint=[.42, .2],
                                                    text=icon_func.add_money_icon(string=str(my_game.game_pars.income),
                                                                                  size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                                  coef=2),
                                                    font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                    markup=True)  # поле ввода для дохода страны
        self.game_pars.labels.str_of_coef_of_perenos = Label(size=(50, 30), size_hint_x=.42,
                                                             font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                             text=str(round(my_game.game_pars.coef_of_perenos,
                                                                            3)))  # поле ввода для коэффициента переноса
        self.game_pars.labels.str_of_straph = uix_classes.Label_touch(size=(50, 30), size_hint=[.42, .2], text=str(
            my_game.game_pars.straph_b) + '/[color=ff0000][b]' + str(my_game.game_pars.crit_straph_b) + '[/color][/b]',
                                                                      font_size=sizes.TEXT_SIZE_TABLE_NUMBERS,
                                                                      markup=True)
        self.game_pars.labels.str_of_straph.color = [1, 1, 1, 1]
        self.game_pars.labels.str_of_straph.bold = False

        if my_game.game_pars.straph_b >= 5:
            self.game_pars.labels.str_of_straph.color = [1, .5, .2, 1]
            self.game_pars.labels.str_of_straph.bold = True

        if my_game.game_pars.straph_b >= 10:
            self.game_pars.labels.str_of_straph.color = [1, 0, 0, 1]

        self.game_pars.labels.str_of_win = Label(size=(50, 30), size_hint=[.42, .2],
                                                 text=str(my_game.game_pars.win_b) + '/[color=00ff00][b]' + str(
                                                     my_game.game_pars.crit_win_b) + '[/color][/b]',
                                                 font_size=sizes.TEXT_SIZE_TABLE_NUMBERS, markup=True)

        self.game_pars.labels.str_of_date = Label(text=spec_func.generate_str_date(my_game.game_pars.date),
                                                  size_hint_x=.42, font_size=round(sizes.TEXT_SIZE_TABLE_NUMBERS * .9))

    def init_of_left_pannel(self):

        self.left_pannel = Empty_Class()
        self.left_pannel.btns = Empty_Class()

        self.left_pannel.table = GridLayout(cols=1, size_hint=[.28, 1], spacing=(0, sizes.Height_of_screen / 250))

        self.left_pannel.btns.btn_fin_step = uix_classes.Button_with_image(
            # on_press = App.get_running_app().Make_step,
            text_source=frases.str_end_step, size_hint_y=.1,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, padding=(0, sizes.Height_of_screen / 50))
        self.left_pannel.table.add_widget(self.left_pannel.btns.btn_fin_step)

        self.left_pannel.btns.btn_open_pannel_of_tech = uix_classes.ToggleButton_with_image(
            text_source=frases.str_panel_of_tech, size_hint_y=.1,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, padding=(0, sizes.Height_of_screen / 50))
        self.left_pannel.table.add_widget(self.left_pannel.btns.btn_open_pannel_of_tech)

        self.mode_of_tech_panel = "panel"

        self.left_pannel.multichoise_layout = BoxLayout(size_hint_y=.1, spacing=sizes.Width_of_screen / 330)
        self.left_pannel.multichoise_layout.btn_activate = uix_classes.ToggleButton_with_image(
            text_source=["Множественный\nвыбор", "Multiselect"], size_hint_x=.7,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign='center')
        if my_game.multichoice_ind == -1:
            self.left_pannel.multichoise_layout.btn_activate.state = 'normal'
        else:
            self.left_pannel.multichoise_layout.btn_activate.state = 'down'
        self.left_pannel.multichoise_layout.add_widget(self.left_pannel.multichoise_layout.btn_activate)

        self.left_pannel.multichoise_layout.btn_do_it = uix_classes.Button_with_image(text_source=frases.str_e,
                                                                                      size_hint_x=.3,
                                                                                      # on_press = App.get_running_app().run_asking,
                                                                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR)
        self.left_pannel.multichoise_layout.add_widget(self.left_pannel.multichoise_layout.btn_do_it)

        self.left_pannel.table.add_widget(self.left_pannel.multichoise_layout)

        self.left_pannel.table_of_common_par = uix_classes.CustomGridLayout(size_hint_y=.6)
        self.left_pannel.table.add_widget(self.left_pannel.table_of_common_par)
        tcp_halign = 'left'
        self.left_pannel.table_of_common_par.add_widgets(
            uix_classes.Label_with_tr(text_source=frases.str_straph_points, size_hint=[1, .2],
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign=tcp_halign))

        self.left_pannel.table_of_common_par.add_widgets(self.game_pars.labels.str_of_straph)

        self.left_pannel.table_of_common_par.add_widgets(
            uix_classes.Label_with_tr(text_source=frases.str_win_points, size_hint=[1, .2],
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign=tcp_halign))

        self.left_pannel.table_of_common_par.add_widgets(self.game_pars.labels.str_of_win)

        self.left_pannel.table_of_common_par.add_widgets(Label(
            text=icon_func.letter_to_icons_increasing_size(coef=2, string="z_out", size=sizes.TEXT_SIZE_OF_COMMON_PAR),
            size_hint=[1, .2], halign=tcp_halign,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, markup=True))

        self.left_pannel.table_of_common_par.add_widgets(self.game_pars.labels.str_for_z_out)

        self.left_pannel.table_of_common_par.add_widgets(obj=Label(
            text=icon_func.letter_to_icons_increasing_size(coef=2, string="d_out", size=sizes.TEXT_SIZE_OF_COMMON_PAR),
            size_hint=[1, .2], halign=tcp_halign,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, markup=True))

        self.left_pannel.table_of_common_par.add_widgets(obj=self.game_pars.labels.str_for_d_out)

        self.left_pannel.table_of_common_par.add_widgets(
            uix_classes.Label_with_tr(text_source=["Перенос", "Transfer coeff"], size_hint_x=1,
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR, halign=tcp_halign))
        self.left_pannel.table_of_common_par.add_widgets(self.game_pars.labels.str_of_coef_of_perenos)

        self.left_pannel.table_of_common_par.add_widgets(uix_classes.Label_with_tr(text_source=frases.str_money,
                                                                                   size_hint=[1, .2], halign=tcp_halign,
                                                                                   font_size=sizes.TEXT_SIZE_OF_COMMON_PAR))
        self.left_pannel.table_of_common_par.add_widgets(self.game_pars.labels.str_of_money)

        self.left_pannel.table_of_common_par.add_widgets(
            uix_classes.Label_with_tr(text_source=["Доход", "Income"], size_hint=[1, .2],
                                      font_size=sizes.TEXT_SIZE_OF_COMMON_PAR,
                                      halign=tcp_halign))
        self.left_pannel.table_of_common_par.add_widgets(self.game_pars.labels.str_of_income)

        self.left_pannel.table_of_common_par.add_widgets(uix_classes.Label_with_tr(text_source=["Дата", "Date"],
                                                                                   font_size=sizes.TEXT_SIZE_OF_COMMON_PAR,
                                                                                   size_hint_x=.6, halign=tcp_halign))

        self.left_pannel.table_of_common_par.add_widgets(self.game_pars.labels.str_of_date)
        self.left_pannel.btns.settings_button = uix_classes.Button_with_image(
            text_source=["Дополнительное", "Additional"], size_hint_y=.1,
            font_size=sizes.TEXT_SIZE_OF_COMMON_PAR)  # settings_button

        self.left_pannel.table.add_widget(self.left_pannel.btns.settings_button)

        pre_final_layout.add_widget(self.left_pannel.table)
