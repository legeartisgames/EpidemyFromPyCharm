import time

import achieve_pannel
import ads_mob
import common_data
import common_var
import country_choicer

import country_variants

import disease_choicer
import diseases

import draw_for_epidemy
import end_of_step
import e_settings
import game_modes
import game_modes_choicer
import gold_transaction
import graph_maker
import init_of_tech
import lang_checkbox
import icon_func
import info_layouts
import interact_rules
import music_module
import regions_menu
import sizes

import spec_func
import special_achievs
import start_menu
import tech_info
import tech_sm
import widget_of_common_par

# next 2 lines - for windows packaging
import os
import sys
from kivy.resources import resource_add_path, resource_find

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scatter import ScatterPlane

t = time.time()


def escape_delay(dt):
    common_data.escape_ind = 0


def starting_new_game():
    common_data.continue_game = False
    if widget_of_common_par.opened_ask_pannel_is is not None:
        widget_of_common_par.opened_ask_pannel_is.close_ask_pannel(instance=5)

    del common_data.my_game

    common_data.is_game_running = "gaming"

    dis_right = 0
    for i in range(len(diseases.diseases_list)):
        if common_var.Current_dis == diseases.diseases_list[i].name[common_var.lang]:
            dis_right = i
            break

    mod_right = 0
    for i in range(len(game_modes.modes_list)):
        if common_var.Current_mode == game_modes.modes_list[i].name[common_var.lang]:
            mod_right = i
            break
    print("mod ", mod_right)

    i_right = 0
    for i in range(len(country_variants.Country_lands)):
        if common_var.Current_country == country_variants.Country_lands[i].name[common_var.lang]:
            i_right = i
            break

    print(diseases.diseases_list[dis_right].name)

    common_data.my_game = common_data.Game_Exemplar(country=country_variants.Country_lands[i_right],
                                                    disease=diseases.diseases_list[dis_right],
                                                    mode=game_modes.modes_list[mod_right])

    common_data.My_Country = country_variants.Country_lands[i_right]

    if mod_right == 4:  # когда критическое число штрафных очков в 5 раз больше
        common_data.my_game.game_pars.crit_straph_b *= 5

    if i_right == 0:  # if Australia
        common_data.my_game.parameters_of_tech[5][2][1][0] = 1 - (
                1 - common_data.my_game.parameters_of_tech[5][2][1][0]) * 3 / 2
        # z_out in reduce of communication is better
        common_data.my_game.parameters_of_tech[12][2][0] = 1 - (
                1 - common_data.my_game.parameters_of_tech[12][2][0]) * 3 / 4
        # distant is not very effective

    elif i_right == 1:  # if Argentina
        common_data.my_game.prices_of_tech[7][1] += 1  # жёсткий карантин дешевле вводить
        common_data.my_game.parameters_of_tech[7][2][0] = 1 - (
                1 - common_data.my_game.parameters_of_tech[7][2][0]) / 1.05
        # эффективность карантина ниже than normally

        common_data.my_game.parameters_of_tech[17][2][0][0] -= 1  # в аргентине не так беспокоятся при повышении налогов

    elif i_right == 2:  # if Brazil
        common_data.my_game.parameters_of_tech[6][2][1][0] *= 1.4  # it is harder to isolate all of them
        common_data.my_game.parameters_of_tech[7][2][0] = 1 / 8  # hard carantin not very effective
        common_data.my_game.prices_of_tech[7] = [tech_info.prices_of_tech[7][0] + 5, tech_info.prices_of_tech[7][1] + 2]
        # but it is cheaper

    elif i_right == 3:  # if India
        common_data.my_game.parameters_of_tech[7][2][0] = 1 / 9  # hard carantin isn't so effective
        common_data.my_game.prices_of_tech[7] = [tech_info.prices_of_tech[7][0], tech_info.prices_of_tech[7][1] + 2]
        # but it is much cheaper to make it

        common_data.my_game.parameters_of_tech[6][2][0][0] *= 10
        # isolation is more "effective" by quantity of isolated people
        common_data.my_game.parameters_of_tech[6][2][1][0] *= 1.5  # but it is harder to isolate all of them

        common_data.my_game.parameters_of_tech[10][2][0][0] *= 2  # больше производят вакцин за такт
        common_data.my_game.parameters_of_tech[10][2][2][0] -= 1  # вакцины дешевле штамповать

    elif i_right == 5:  # if China
        common_data.my_game.prices_of_tech[0][0] += 3  # investments in production in China are cheaper

        common_data.my_game.parameters_of_tech[6][2][0][0] *= 3
        # isolation is more "effective" by quantity of isolated people
        common_data.my_game.parameters_of_tech[6][2][1][0] *= 1.2
        # but it is harder to isolate all of them

        common_data.my_game.parameters_of_tech[10][2][0][0] *= 2  # больше производят вакцин за такт
        common_data.my_game.parameters_of_tech[10][2][2][0] -= 1  # вакцины дешевле штамповать

    elif i_right == 6:  # if Mexico
        common_data.my_game.parameters_of_tech[5][2][0][0] *= 5  # не так хорошо перекрывается сообщение
        common_data.my_game.parameters_of_tech[5][2][1][0] = \
            1 - (1 - common_data.my_game.parameters_of_tech[5][2][1][0]) / 1.7
        common_data.my_game.parameters_of_tech[5][3][0] += 1  # но и доход слабее падает

        common_data.my_game.parameters_of_tech[7][2][0] = 0.2  # hard quarantine isn't so effective
        common_data.my_game.prices_of_tech[7] = [tech_info.prices_of_tech[7][0], tech_info.prices_of_tech[7][1] + 1]
        # but it is cheaper

    elif i_right == 7:  # if Russia

        common_data.my_game.parameters_of_tech[5][2][0][0] *= 5  # не так хорошо перекрывается сообщение
        common_data.my_game.parameters_of_tech[5][2][1][0] = \
            1 - (1 - common_data.my_game.parameters_of_tech[5][2][1][0]) * 0.8
        common_data.my_game.parameters_of_tech[5][3][0] += 1  # но и доход слабее падает

        common_data.my_game.prices_of_tech[7] = [tech_info.prices_of_tech[7][0] + 5, tech_info.prices_of_tech[7][1] + 1]
        # карантин дешевле и придумать, и внедрить
        common_data.my_game.parameters_of_tech[7][2][0] = 1 / 10
        # жёсткий карантин в России не даёт такого сильного эффекта, как в других странах

        common_data.my_game.parameters_of_tech[0][3][0] = common_data.my_game.parameters_of_tech[0][3][0] + 2
        # инвестиции в производство у России более эффективны, чем у других стран
        common_data.my_game.prices_of_tech[0][0] -= 7  # но и дороже стоят

        common_data.my_game.prices_of_tech[2][0] -= 1  # инвестиции в исследования России дороже стоят
        common_data.my_game.prices_of_tech[1][0] -= 1  # investments в больницы в России дороже стоят

    elif i_right == 8:  # if USA

        common_data.my_game.prices_of_tech[1][0] -= 5  # ивестиции в больницы в USA дороже стоят
        common_data.my_game.parameters_of_tech[1][2][0][0] \
            = 1 - (1 - common_data.my_game.parameters_of_tech[1][2][0][0]) / 2
        # investments in hospital don't reduce z_in effective
        common_data.my_game.prices_of_tech[2][0] += 1  # investments in research are cheaper
        common_data.my_game.parameters_of_tech[3][2][1][0] *= 2
        # американцы болезненней реагируют на введение масочного режима

        common_data.my_game.parameters_of_tech[6][2][1][0] *= 2.5  # it is harder to isolate all of them
        common_data.my_game.prices_of_tech[9][0] += 2  # science communication is cheaper
        common_data.my_game.prices_of_tech[15][0] = int(common_data.my_game.prices_of_tech[15][0] / 1.4)
        # emission is cheaper
        common_data.my_game.parameters_of_tech[15][2][2][0] = 0
        # если денег напечатать чуть-чуть, то американцы не возмутятся

    elif i_right == 10:  # if Japan
        common_data.my_game.prices_of_tech[0][0] += 2  # investitions in production in Japan are cheaper
        common_data.my_game.prices_of_tech[2][0] += 1  # investitions in research in Japan are cheaper

        common_data.my_game.parameters_of_tech[5][3][0] += 2  # в Японии вполне автономно всё
        common_data.my_game.parameters_of_tech[5][2][1][0] = 1 - (
                1 - common_data.my_game.parameters_of_tech[5][2][1][0]) / 2
        # но и поэтому эффект более слабый от ограничения сообщения

        common_data.my_game.prices_of_tech[22][1] += 2  # автоматизация даётся проще

    elif i_right == 11:  # Turkey
        common_data.my_game.parameters_of_tech[4][3][0] -= 1  # туристический бизнес слаб без самолётов
        common_data.my_game.parameters_of_tech[5][3][0] += 1  # в Турции вполне автономно всё
        common_data.my_game.parameters_of_tech[6][2][1][0] *= 1.5  # it is harder to isolate all of them
    elif i_right == 12:  # Germany
        common_data.my_game.prices_of_tech[3][0] = int(1.5 * common_data.my_game.prices_of_tech[3][0])
        # респираторы дороже масок
        common_data.my_game.parameters_of_tech[3][2][0][0] = \
            1 - (1 - common_data.my_game.parameters_of_tech[3][2][0][0]) * 1.5
        # респираторы эффективней масок
        common_data.my_game.parameters_of_tech[3][2][1][0] = 1
        # респираторы протестов почти не вызывают
    if dis_right == 1:  # flu
        common_data.my_game.prices_of_tech[11][0] *= 1.25  # cure is more expensive
        common_data.my_game.prices_of_tech[11][0] = round(common_data.my_game.prices_of_tech[11][0])

    elif dis_right == 2:  # plague
        common_data.my_game.prices_of_tech[11][0] /= 1.25  # cure is cheaper
        common_data.my_game.prices_of_tech[11][0] = round(common_data.my_game.prices_of_tech[11][0])
        common_data.my_game.prices_of_tech[10][0] /= 1.1  # vaccine is cheaper
        common_data.my_game.prices_of_tech[10][0] = round(common_data.my_game.prices_of_tech[10][0])

    elif dis_right == 3:  # smallpox
        common_data.my_game.prices_of_tech[11][0] *= 1.5  # cure is more expensive
        common_data.my_game.prices_of_tech[11][0] = round(common_data.my_game.prices_of_tech[11][0])

    common_data.pre_final_layout.clear_widgets()

    try:
        del common_data.my_game_frontend
    except AttributeError:
        pass
    common_data.final_layout.clear_widgets()

    common_data.my_game_frontend = common_data.Game_Frontend()
    left_panel_key_bind()

    common_data.pre_final_layout.add_widget(common_data.stencil_s2)

    common_data.final_layout.add_widget(common_data.pre_final_layout)

    common_data.s2.canvas.clear()
    common_data.s2.clear_widgets()
    common_data.stencil_s2.remove_widget(common_data.s2)
    del common_data.s2

    common_data.s2 = ScatterPlane(do_rotation=False, scale_min=.37, scale_max=2.5, scale=.5,
                                  do_collide_after_children=True, on_touch_down=draw_for_epidemy.on_scatter_touch_down,
                                  on_touch_move=draw_for_epidemy.on_scatter_move)
    sizes.start_s2_pos_x = common_data.s2.pos[0]
    common_data.s2.pos = (common_data.s2.pos[0] +
                          sizes.Width_of_screen * common_data.my_game_frontend.left_pannel.table.size_hint_x, 0)
    sizes.normal_s2_pos_x = common_data.s2.pos[0]
    common_data.Country2 = draw_for_epidemy.Widget_Hex2()
    common_data.s2.add_widget(common_data.Country2)
    common_data.stencil_s2.add_widget(common_data.s2, canvas='before')
    common_data.page2_1.scroll_y = 1

    e_settings.nast.label_current_country_is.text_source = common_data.my_game.My_Country.name
    e_settings.nast.label_current_country_is.text = common_data.my_game.My_Country.name[common_var.lang]

    e_settings.nast.label_current_disease_is.text_source = common_data.my_game.My_disease.name
    e_settings.nast.label_current_disease_is.text = common_data.my_game.My_disease.name[common_var.lang]

    e_settings.nast.label_current_mode_is.text_source = common_data.my_game.My_mode.name
    e_settings.nast.label_current_mode_is.text = common_data.my_game.My_mode.name[common_var.lang]

    e_settings.nast.lab_can_get_stars.text = icon_func.add_star_icon(
        string=str(common_data.my_game.My_Country.stars + common_data.my_game.My_disease.level - 2),
        size=e_settings.nast.lab_can_get_stars.font_size)

    init_of_tech.init_all_techs()
    common_data.my_stats.possible_of_continue_game = True
    common_data.my_stats.save_to_file()
    common_data.my_game.save_to_file()
    common_var.is_game_running = "gaming"
    end_of_step.day_event = None

    if common_data.my_game.My_mode.index in {1, 2, 3}:
        print("fast mode")
        end_of_step.day_event = Clock.schedule_interval(end_of_step.mode_time_callback,
                                                        common_data.my_game.My_mode.step_time / 30)

    if common_data.my_game.My_disease.index == 4:  # random scenario
        common_data.to_str_dis_par(obj="z_out")
        common_data.to_str_dis_par(obj="d_out")
        common_data.to_str_dis_par(obj="transfer_c")


def does_user_want_to_start_a_game(instance):
    common_data.pre_final_layout.clear_widgets()
    common_data.page2.clear_widgets()

    starting_new_game()


class EpidemyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rewards = RewardsHandler(self)

    def on_stop(self):
        if not common_var.WAS_STOP:
            print("You were gaming: " + str(time.time() - time_run) + " s")
            if common_var.is_game_running == "gaming":
                common_data.my_game.save_to_file()
            common_var.WAS_STOP = True
        return True

    def on_pause(self):
        if common_data.my_stats.is_music_playing:
            music_module.sound.pause()
        return True

    def on_resume(self):
        if common_data.my_stats.is_music_playing:
            music_module.sound.play()
        if common_var.is_interstitial_working:
            self.ads.request_interstitial()
        return True

    def build(self):
        self.bind(on_start=self.post_build_init)

        self.ads = ads_mob.KivMob(ads_mob.APP_ID)  # put your Admob Id in case you want to put your own ads.
        self.ads.set_rewarded_ad_listener(self.rewards)
        self.ads.new_interstitial(ads_mob.INRERSTITIAL_ID)  # for an interstitial in the end of step
        self.load_rewarded_video()

        if common_data.my_stats.is_language_set != 1:
            check = lang_checkbox.Choose_language_start()
            common_data.final_layout.add_widget(check)
        else:
            common_data.final_layout.add_widget(start_menu.Main_menu)

        start_menu.Main_menu.filling()

        self.outer_folders = []
        for i in common_data.final_layout.children:
            self.outer_folders.append(i)

        print("Time_load = " + str(time.time() - t))

        self.day_award()

        return common_data.final_layout

    def continue_saved_game(self, instance):

        common_data.continue_game = True
        common_var.is_game_running = "gaming"
        file_game = open('game_exemplar_data.pkl', 'rb')

        common_data.my_game = common_data.pickle.load(file_game)
        file_game.close()

        file_game = open('game_game_pars.pkl', 'rb')

        common_data.my_game.game_pars = common_data.pickle.load(file_game)
        file_game.close()

        if widget_of_common_par.opened_ask_pannel_is is not None:
            widget_of_common_par.opened_ask_pannel_is.close_ask_pannel(instance=5)

        common_data.pre_final_layout.clear_widgets()

        common_data.my_game_frontend = common_data.Game_Frontend()
        left_pannel_key_bind()

        common_data.pre_final_layout.add_widget(common_data.stencil_s2)

        common_data.final_layout.clear_widgets()

        common_data.final_layout.add_widget(common_data.pre_final_layout)

        common_data.s2.clear_widgets()
        common_data.stencil_s2.remove_widget(common_data.s2)
        common_data.s2.canvas.clear()
        common_data.s2 = ScatterPlane(do_rotation=False, scale_min=.37, scale_max=2.5, scale=.5,
                                      on_touch_down=draw_for_epidemy.on_scatter_touch_down,
                                      on_touch_move=draw_for_epidemy.on_scatter_move)
        sizes.start_s2_pos_x = common_data.s2.pos[0]
        common_data.s2.pos = (common_data.s2.pos[0] +
                              sizes.Width_of_screen * common_data.my_game_frontend.left_pannel.table.size_hint_x, 0)
        sizes.normal_s2_pos_x = common_data.s2.pos[0]
        e_settings.nast.label_current_country_is.text_source = common_data.my_game.My_Country.name
        e_settings.nast.label_current_country_is.text = common_data.my_game.My_Country.name[common_var.lang]
        e_settings.nast.lab_can_get_stars.text = \
            icon_func.add_star_icon(string=str(common_data.my_game.My_Country.stars),
                                    size=e_settings.nast.lab_can_get_stars.font_size)
        e_settings.nast.label_current_disease_is.text_source = common_data.my_game.My_disease.name
        e_settings.nast.label_current_disease_is.text = common_data.my_game.My_disease.name[common_var.lang]

        e_settings.nast.label_current_mode_is.text_source = common_data.my_game.My_mode.name
        e_settings.nast.label_current_mode_is.text = common_data.my_game.My_mode.name[common_var.lang]

        common_data.Country2 = draw_for_epidemy.Widget_Hex2()
        for i in range(common_data.my_game.My_Country.number_of_regions):
            if common_data.my_game.game_pars.is_hard_carantin_in_current_region[i] == 0:
                draw_for_epidemy.draw_carantine(draw_for_epidemy.coords_of_hexes[i][0],
                                                draw_for_epidemy.coords_of_hexes[i][1],
                                                draw_for_epidemy.side, draw_for_epidemy.height, draw="draw")

        common_data.s2.add_widget(common_data.Country2)
        common_data.stencil_s2.add_widget(common_data.s2, canvas='before')

        init_of_tech.init_all_techs()

        if common_data.my_game.My_mode.index in {1, 2, 3}:
            end_of_step.day_event = Clock.schedule_interval(end_of_step.mode_time_callback,
                                                            common_data.my_game.My_mode.step_time / 30)

        if common_data.my_game.My_disease.index == 4:  # unknown disease
            common_data.to_str_dis_par(obj="z_out")
            common_data.to_str_dis_par(obj="d_out")
            common_data.to_str_dis_par(obj="transfer_c")
            print(common_data.my_game.My_disease.padezhi)

    def choosing_of_mode(self, instance):
        widget_of_common_par.Mode_var = game_modes_choicer.Mode_choiser_layout()
        widget_of_common_par.Mode_var.open_layout(instance=0)
        widget_of_common_par.Mode_var.btn_confirm.bind(on_press=does_user_want_to_start_a_game)

    def choosing_of_country(self, instance):

        widget_of_common_par.Country_var = country_choicer.Country_choiser_layout()
        widget_of_common_par.Country_var.open_layout(instance=0)
        widget_of_common_par.Country_var.btn_remake_country.bind(on_press=self.choosing_of_mode)

    def choosing_of_disease(self, instance):
        common_var.is_game_running = "preparing for game"
        widget_of_common_par.Dis_var = disease_choicer.Disease_choiser_layout()
        widget_of_common_par.Dis_var.open_layout(instance=0)
        widget_of_common_par.Dis_var.btn_confirm.bind(on_press=self.choosing_of_country)

    def close_game_space(self, instance):
        common_data.final_layout.clear_widgets()

        for i in self.outer_folders:
            common_data.final_layout.add_widget(i)

        common_var.is_game_running = "in_main_menu"
        print("returned to main menu")

        if not start_menu.Main_menu.covid_image.is_animating:
            start_menu.Main_menu.covid_image.is_animating = True
            start_menu.Main_menu.covid_image.generate_rotating_transition(instance=0, animation=0)
            start_menu.Main_menu.covid_image.generate_horizontal_moving(instance=0, animation=0)
            start_menu.Main_menu.covid_image.generate_vertical_moving(instance=0, animation=0)

    def end_of_game(self, first_text=""):
        if common_data.my_game.My_disease.index == 4:
            diseases.control_unknown_disease()
        common_var.is_game_running = "after_game"
        were_goldreserves = common_data.my_stats.goldreserves
        were_stars = common_data.my_stats.stars
        award_coins = None
        award_stars = None
        comments = None
        if common_var.is_victory == 1:
            award_stars = common_data.my_game.My_Country.stars + common_data.my_game.My_disease.level - 2
            award_coins = int(award_stars * 7)
            comments = ['красавчик', 'я такого не ожидала', 'молодец', 'так держать',
                        'очень круто', 'не зазнавайся', 'можно было бы и круче выступить']
            common_data.my_stats.results_by_countries[common_data.my_game.My_Country.index].append(1)
            common_data.my_stats.results_by_diseases[common_data.my_game.My_disease.index].append(1)
        if common_var.is_victory == 0:
            award_stars = min(common_data.my_game.My_Country.stars +
                              common_data.my_game.My_disease.level - 2 - 1,
                              round(common_data.my_game.game_pars.numer_step / 15
                                    + common_data.my_game.My_disease.level / 5, 1))
            award_stars = round(award_stars, 1)
            award_coins = common_data.math.ceil(award_stars * 3)
            comments = ['позор какой', 'Вы продулись', 'не распускай нюни',
                        'в следующий раз будет лучше', 'попробуй ещё раз',
                        'плоховато', 'не отчаивайся']
            common_data.my_stats.results_by_countries[common_data.my_game.My_Country.index].append(0)
            common_data.my_stats.results_by_diseases[common_data.my_game.My_disease.index].append(0)
        award_stars = round(award_stars * common_data.my_game.My_mode.coef_award, 1)
        award_coins = round(award_coins * common_data.my_game.My_mode.coef_award, 1)
        speech = common_data.random.choice(comments)
        print(speech)
        '''
        if common_data.random.randint(0, 4) == 0:
            try:
                sizes.plyer.tts.speak(speech)
            except:
                print("no voice")'''

        common_data.my_stats.possible_of_continue_game = False

        common_data.my_stats.number_of_games += 1

        common_data.my_stats.per_of_victory = (common_var.is_victory + (common_data.my_stats.number_of_games - 1)
                                               * common_data.my_stats.per_of_victory) / \
                                              common_data.my_stats.number_of_games
        common_data.str_percent_of_v = [str(round(common_data.my_stats.per_of_victory * 100, 1)) + "%",
                                        str(round(common_data.my_stats.per_of_victory * 100, 1)) + "%"]

        common_data.my_stats.goldreserves = int(common_data.my_stats.goldreserves + award_coins)
        common_data.my_stats.stars = round(common_data.my_stats.stars + award_stars, 1)

        s_rising = False
        c_rising = False

        x = common_data.my_stats.level_stars
        common_data.my_stats.level_stars = spec_func.status_finder(typ='stars', value=common_data.my_stats.stars)[0]

        if common_data.my_stats.level_stars > x:
            s_rising = True
            print("s_rising")

        x = common_data.my_stats.level_coins
        common_data.my_stats.level_coins = \
            spec_func.status_finder(typ='coins', value=common_data.my_stats.goldreserves)[0]
        if common_data.my_stats.level_coins > x:
            c_rising = True
            print("c_rising")

        common_data.my_stats.save_to_file()

        str_your_awards_are = ["Вы заработали за эту партию:\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
            size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(size=sizes.WIN_SIZE) + "\n",
                               "Your awards:\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
                                   size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(
                                   size=sizes.WIN_SIZE) + "\n"]
        if award_stars == 0 and award_coins == 0:
            str_your_awards_are = ["", ""]

        if common_var.is_victory == 0:
            mes = ["К сожалению, Вы проиграли.\n" + str_your_awards_are[
                common_var.lang] + "\n" + "Нам кажется, что в следующий \nраз у Вас всё получится :)\n",
                   "You lose:(\n\n" + str_your_awards_are[
                       common_var.lang] + "\n" + "Try again! We guess you'll win next game :)\n"]
            widget_of_common_par.inform_about_end(mes[common_var.lang], 'bad', status_s_rising=s_rising,
                                                  status_c_rising=c_rising)

        elif common_var.is_victory == 1:
            mes = ["Ура!!! Вы победили!\n\n" + str_your_awards_are[common_var.lang],
                   "You have won!!!\n\n" + str_your_awards_are[common_var.lang]]

            widget_of_common_par.inform_about_end(mes[common_var.lang], 'good', status_s_rising=s_rising,
                                                  status_c_rising=c_rising)

        common_var.need_c = spec_func.status_finder('coins', common_data.my_stats.goldreserves)[1]
        common_var.need_s = spec_func.status_finder('stars', common_data.my_stats.stars)[1]

        e_settings.nast.update_stats_after_end_of_the_game()
        start_menu.Main_menu.stats_pannel_in.update_stats_after_end_of_the_game()

        common_data.my_game.delete_game_ex()

        new_countries = list()
        for i in range(len(country_variants.Country_lands)):
            if were_goldreserves < country_variants.Country_lands[
                i].min_goldreserves <= common_data.my_stats.goldreserves:
                print(country_variants.Country_lands[i].name)
                new_countries.append(i)

        for i in range(len(country_variants.Country_lands)):
            if were_stars < country_variants.Country_lands[i].min_rep_stars <= common_data.my_stats.stars:
                print(country_variants.Country_lands[i].name)
                new_countries.append(i)

        new_techs = list()
        for i in range(common_var.QUANT_OF_TECH):
            if were_goldreserves < tech_info.min_goldreserves_for_tech[i] <= common_data.my_stats.goldreserves:
                new_techs.append(i)
                print(tech_info.names_of_tech[i])

        for i in range(common_var.QUANT_OF_TECH):
            if were_stars < tech_info.min_stars_for_tech[i] <= common_data.my_stats.stars:
                new_techs.append(i)
                print(tech_info.names_of_tech[i])
        new_diseases = list()
        for i in range(len(diseases.diseases_list)):
            if were_goldreserves < diseases.diseases_list[i].min_gold <= common_data.my_stats.goldreserves:
                new_diseases.append(i)

        try: # to-do: rewrite without try
            del special_achievs.win_pannel
        except:
            print("Win pannel was deleted earlier")
        spec_achieves = []
        if first_text != "":
            spec_achieves.append(["first_text", first_text])
        if common_data.random.randint(0, 4) == 1:
            spec_achieves.append(["link_vk_page", "https://vk.com/epidemy_inception"])

        history_of_games = common_data.my_stats.results_by_countries[common_data.my_game.My_Country.index]
        if sum(history_of_games) == 1 and history_of_games[len(history_of_games) - 1] == 1:
            spec_achieves.append(
                ["victory_by_new_country", common_data.my_game.My_Country.name, common_data.my_game.My_Country.index])

            history_of_games = common_data.my_stats.results_by_diseases[common_data.my_game.My_disease.index]
        if sum(history_of_games) == 1 and history_of_games[len(history_of_games) - 1] == 1:
            spec_achieves.append(
                ["victory_by_new_disease", common_data.my_game.My_disease.name, common_data.my_game.My_disease.rod])

        if new_techs != list():
            spec_achieves.append(["new_techs", new_techs])

        if new_countries != list():
            spec_achieves.append(["new_countries", new_countries])
        if new_diseases != list():
            spec_achieves.append(["new_disease", new_diseases])

        if s_rising:
            spec_achieves.append(["rep_status", common_data.my_stats.level_stars])
        if c_rising:
            spec_achieves.append(["gold_status", common_data.my_stats.level_coins])

        if common_data.random.randint(0, 10) == 1:
            app_store_link = "https://play.google.com/store/apps/details?id=com.legeartisgames.epidemy"
            if sizes.platform == "android":
                app_store_link = "market://details?id=com.legeartisgames.epidemy"

            spec_achieves.append(["rate_app", app_store_link])

        if len(spec_achieves) != 0:
            special_achievs.win_pannel = special_achievs.Special_Achievements_Pannel(achieves=spec_achieves)
            special_achievs.win_pannel.open_pannel(instance=5)

        common_var.is_victory = "none"

        if tech_sm.tech_viewer is not None:  # избавляемся от листания
            tech_sm.tech_viewer.close_self(instance=3)

    def day_award(self):
        if common_data.first_run_in_this_day and len(common_data.my_stats.days_of_activity) > 1:
            were_goldreserves = common_data.my_stats.goldreserves
            were_stars = common_data.my_stats.stars
            award_stars = 15
            award_coins = 25

            common_data.my_stats.goldreserves = int(common_data.my_stats.goldreserves + award_coins)
            common_data.my_stats.stars = round(common_data.my_stats.stars + award_stars, 1)

            s_rising = False
            c_rising = False

            x = common_data.my_stats.level_stars
            common_data.my_stats.level_stars = spec_func.status_finder(typ='stars', value=common_data.my_stats.stars)[0]

            if common_data.my_stats.level_stars > x:
                s_rising = True
                print("s_rising")

            x = common_data.my_stats.level_coins
            common_data.my_stats.level_coins = \
                spec_func.status_finder(typ='coins', value=common_data.my_stats.goldreserves)[0]
            if common_data.my_stats.level_coins > x:
                c_rising = True
                print("c_rising")

            common_data.my_stats.save_to_file()

            str_your_awards_are = [
                "Новый день - новая награда:\n\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
                    size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(
                    size=sizes.WIN_SIZE) + "\n\n",
                "New day - new reward:\n\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
                    size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(
                    size=sizes.WIN_SIZE) + "\n\n"]

            common_var.need_c = spec_func.status_finder('coins', common_data.my_stats.goldreserves)[1]
            common_var.need_s = spec_func.status_finder('stars', common_data.my_stats.stars)[1]

            start_menu.Main_menu.stats_pannel_in.update_stats_after_end_of_the_game()

            common_data.my_game.delete_game_ex()
            new_countries = list()
            for i in range(len(country_variants.Country_lands)):
                if were_goldreserves < country_variants.Country_lands[i].min_goldreserves \
                        <= common_data.my_stats.goldreserves:
                    print(country_variants.Country_lands[i].name)
                    new_countries.append(i)

            for i in range(len(country_variants.Country_lands)):
                if were_stars < country_variants.Country_lands[i].min_rep_stars <= common_data.my_stats.stars:
                    print(country_variants.Country_lands[i].name)
                    new_countries.append(i)

            new_techs = list()
            for i in range(common_var.QUANT_OF_TECH):
                if were_goldreserves < tech_info.min_goldreserves_for_tech[i] <= common_data.my_stats.goldreserves:
                    new_techs.append(i)
                    print(tech_info.names_of_tech[i])

            new_diseases = list()
            for i in range(len(diseases.diseases_list)):
                if were_goldreserves < diseases.diseases_list[i].min_gold <= common_data.my_stats.goldreserves:
                    new_diseases.append(i)

            for i in range(common_var.QUANT_OF_TECH):
                if were_stars < tech_info.min_stars_for_tech[i] <= common_data.my_stats.stars:
                    new_techs.append(i)
                    print(tech_info.names_of_tech[i])

            try:  # to-do: rewrite it
                del special_achievs.win_pannel
            except:
                print("Win pannel was deleted earlier")

            spec_achieves = list()
            spec_achieves.append(["first_text", str_your_awards_are[common_var.lang]])

            if new_techs != list():
                spec_achieves.append(["new_techs", new_techs])

            if new_countries != list():
                spec_achieves.append(["new_countries", new_countries])

            if new_diseases != list():
                spec_achieves.append(["new_disease", new_diseases])

            if s_rising:
                spec_achieves.append(["rep_status", common_data.my_stats.level_stars])
            if c_rising:
                spec_achieves.append(["gold_status", common_data.my_stats.level_coins])

            if common_data.random.randint(0, 10) == 1:
                app_store_link = "https://play.google.com/store/apps/details?id=com.legeartisgames.epidemy"
                if sizes.platform == "android":
                    app_store_link = "market://details?id=com.legeartisgames.epidemy"

                spec_achieves.append(["rate_app", app_store_link])

            last_text = common_data.random.choice([["Продолжайте спасать мир!", "Keep going!"], ["", ""],
                                                   ["Удачи в партиях!", "Good luck!"],
                                                   ["Эпидемия ждёт вас!", "Epidemy is waiting for you!",
                                                    "Рады видеть вас снова!", "Glad to see you again!"]])
            spec_achieves.append(["first_text", last_text[common_var.lang]])

            if len(spec_achieves) != 0:
                special_achievs.win_pannel = special_achievs.Special_Achievements_Pannel(achieves=spec_achieves,
                                                                                         color="green")
                special_achievs.win_pannel.open_pannel(instance=5)

            e_settings.nast.update_stats_after_end_of_the_game()

    def start_game(self, instance):
        common_var.is_game_running = "preparing for game"
        widget_of_common_par.Dis_var = disease_choicer.Disease_choiser_layout()
        widget_of_common_par.Dis_var.open_layout(instance=0)

        widget_of_common_par.Dis_var.btn_confirm.bind(on_press=self.choosing_of_country)

    def open_panel(self, instance):  # for tech panel

        if common_var.is_open_tech == 0:
            common_data.pre_final_layout.remove_widget(common_data.stencil_s2)

            common_data.pre_final_layout.add_widget(common_data.page2_1)
            common_var.is_open_tech = 1
            common_data.my_game_frontend.left_pannel.btns.btn_open_pannel_of_tech.state = 'down'

        elif common_var.is_open_tech == 1:
            common_data.pre_final_layout.remove_widget(common_data.page2_1)
            common_data.pre_final_layout.add_widget(common_data.stencil_s2)

            common_var.is_open_tech = 0
            common_data.my_game_frontend.left_pannel.btns.btn_open_pannel_of_tech.state = 'normal'

    def load_rewarded_video(self):
        self.ads.load_rewarded_ad(ads_mob.GOLD_REWARDED_ID)

    def post_build_init(self, *args):
        win = e_settings.Window
        win.bind(on_keyboard=self.my_key_handler)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:

            if widget_of_common_par.notifier.notifier_box.is_active:
                widget_of_common_par.notifier.notifier_box.clear_and_delete(dt=0)

            for i in common_data.final_layout.children:
                if i.__class__.__name__ == "InfoCarousel":
                    i.close(instance=0)
                    i.delete()
                    return 5

            if interact_rules.rp in common_data.final_layout.children:
                if interact_rules.rp.num == 1:  # contents
                    interact_rules.rp.close_self(instance=5)
                else:
                    interact_rules.rp.open_page(index=1, instance=0)
                return 5

            if graph_maker.current_graph in common_data.final_layout.children:
                graph_maker.current_graph.close(instance=0)
                return 5

            if start_menu.Main_menu.stats_pannel in common_data.final_layout.children:
                start_menu.Main_menu.stats_pannel.children[0].close_nast(instance=1)
                return 5

            for i in {info_layouts.country_info_pannel, info_layouts.diseases_info_pannel,
                      info_layouts.modes_info_pannel}:
                if i in common_data.final_layout.children:
                    i.close_manual(instance=0)
                    return 5

            if achieve_pannel.achieve_p in common_data.final_layout.children:
                achieve_pannel.achieve_p.close_layout(instance=0)
                return 5
            try:  # to-do: rewrite it
                if special_achievs.win_pannel in common_data.final_layout.children:
                    special_achievs.win_pannel.close_pannel(instance=0)
                    return 5
            except:
                print("No win pannel when you pressed esc button")

            if e_settings.common_nast in common_data.final_layout.children:
                e_settings.nast.close_nast(instance=1)
                return 5
            if tech_sm.tech_viewer in common_data.page2_1.children:
                tech_sm.tech_viewer.close_self(instance=0)
                return 5

            if common_var.is_open_tech == 1:
                self.open_panel(instance=5)
                return 5

            if common_var.is_game_running == "preparing for game":
                common_data.final_layout.children[0].close_layout(instance=5)
                return 5

            if widget_of_common_par.opened_ask_pannel_is is not None:
                widget_of_common_par.opened_ask_pannel_is.close_ask_pannel(instance=5)
                return 5

            if common_var.is_game_running == "gaming":
                e_settings.nast.do_you_want_to_exit(instance=0)
                return 5

            if (common_var.is_game_running in {"in_main_menu", "after_game"}) and common_data.escape_ind == 1:
                e_settings.nast.finish_all(instance=2)
                return 5

            common_data.escape_ind = 1

            mes = ['Нажмите ещё раз "назад" для выхода из приложения', "Tap back again to exit the app"]
            widget_of_common_par.inform_about_error(mes[common_var.lang], 'good', 2)
            Clock.schedule_once(escape_delay, 2)
            return True

        return False


class RewardsHandler(ads_mob.RewardedListenerInterface):  # to-do: check renaming everywhere to CamelCase
    def __init__(self, other):
        self.AppObj = other

    def on_rewarded_video_ad_started(self):
        App.get_running_app().ads.load_rewarded_video()

    def on_rewarded_video_ad_failed_to_load(self, error_code):
        print("Rewarded video failed to load")

    def on_rewarded(self, reward_name, reward_amount):
        gold_transaction.after_rewarded_ads(instance=5)

    def on_rewarded_video_ad_completed(self):
        self.on_rewarded("Points", 10)


def left_panel_key_bind(): # to-do: check that everywhere it was renamed from pannel to panel
    common_data.my_game_frontend.game_pars.labels.str_for_z_out.bind(
        on_press=lambda x: graph_maker.make_graph(typ='new_ill', for_country=True))
    common_data.my_game_frontend.game_pars.labels.str_for_d_out.bind(
        on_press=lambda x: graph_maker.make_graph(typ='new_dead', for_country=True))

    common_data.my_game_frontend.game_pars.labels.str_of_straph.bind(
        on_press=lambda x: graph_maker.make_graph(typ='pen_points', for_country=True))

    common_data.my_game_frontend.left_pannel.btns.btn_fin_step.bind(on_press=end_of_step.Step_Make)
    common_data.my_game_frontend.left_pannel.btns.btn_open_pannel_of_tech.bind(
        on_press=App.get_running_app().open_panel)
    common_data.my_game_frontend.left_pannel.multichoise_layout.btn_activate.bind(on_press=multichoice_on_off)
    common_data.my_game_frontend.left_pannel.multichoise_layout.btn_do_it.bind(on_press=choose_technology_to_hex)
    common_data.my_game_frontend.left_pannel.btns.settings_button.bind(on_press=e_settings.nast.open_nast)


def choose_technology_to_hex(instance):
    if len(common_data.my_game.list_of_chosen) > 0:
        regions_menu.region_menu()


def multichoice_on_off(instance):
    if common_data.my_game.multichoice_ind == 1:
        for i in range(common_data.my_game.n):
            if common_data.my_game.multichoice_list[i] == 1:
                common_data.my_game_frontend.hexes_chosen[i].hide_circle()
        common_data.my_game.multichoice_list = [0] * 21
        common_data.my_game.list_of_chosen = []
    common_data.my_game.multichoice_ind *= (-1)


if __name__ == '__main__':
    print("Time_load = " + str(time.time() - t))
    time_run = time.time()
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    EpidemyApp().run()

