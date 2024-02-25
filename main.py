import time

import achieve_pannel
import ads_mob
import common_data as cd
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

from kivy.resources import resource_add_path  # , resource_find

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scatter import ScatterPlane


def escape_delay(dt):
    cd.escape_ind = 0


def starting_new_game():
    cd.continue_game = False
    if widget_of_common_par.opened_ask_panel is not None:
        widget_of_common_par.opened_ask_panel.close_ask_panel(instance=5)

    del cd.mg

    cd.is_game_running = "gaming"

    disease_ind = 0
    for i in range(len(diseases.diseases_list)):
        if common_var.Current_dis == diseases.diseases_list[i].name[common_var.lang]:
            disease_ind = i
            break

    mode_ind = 0
    for i in range(len(game_modes.modes_list)):
        if common_var.Current_mode == game_modes.modes_list[i].name[common_var.lang]:
            mode_ind = i
            break

    country_ind = 0
    for i in range(len(country_variants.Country_lands)):
        if common_var.Current_country == country_variants.Country_lands[i].name[common_var.lang]:
            country_ind = i
            break

    print(diseases.diseases_list[disease_ind].name)

    cd.mg = cd.GameBackend(country=country_variants.Country_lands[country_ind],
                                                  disease=diseases.diseases_list[disease_ind],
                                                  mode=game_modes.modes_list[mode_ind])

    cd.My_Country = country_variants.Country_lands[country_ind]

    if mode_ind == 4:  # когда критическое число штрафных очков в 5 раз больше
        cd.mg.pars.crit_penalty_points *= 5

    if country_ind == 0:  # if Australia
        cd.mg.parameters_of_tech[5][2][1][0] = 1 - (
                1 - cd.mg.parameters_of_tech[5][2][1][0]) * 3 / 2
        # z_out in reduce of communication is better
        cd.mg.parameters_of_tech[12][2][0] = 1 - (
                1 - cd.mg.parameters_of_tech[12][2][0]) * 3 / 4
        # distant is not very effective

    elif country_ind == 1:  # if Argentina
        cd.mg.prices_of_tech[7][1] += 1  # жёсткий карантин дешевле вводить
        cd.mg.parameters_of_tech[7][2][0] = 1 - (
                1 - cd.mg.parameters_of_tech[7][2][0]) / 1.05
        # эффективность карантина ниже than normally

        cd.mg.parameters_of_tech[17][2][0][0] -= 1  # в аргентине не так беспокоятся при повышении налогов

    elif country_ind == 2:  # if Brazil
        cd.mg.parameters_of_tech[6][2][1][0] *= 1.4  # it is harder to isolate all of them
        cd.mg.parameters_of_tech[7][2][0] = 1 / 8  # hard carantin not very effective
        cd.mg.prices_of_tech[7] = [tech_info.prices_of_tech[7][0] + 5, tech_info.prices_of_tech[7][1] + 2]
        # but it is cheaper

    elif country_ind == 3:  # if India
        cd.mg.parameters_of_tech[7][2][0] = 1 / 9  # hard carantin isn't so effective
        cd.mg.prices_of_tech[7] = [tech_info.prices_of_tech[7][0], tech_info.prices_of_tech[7][1] + 2]
        # but it is much cheaper to make it

        cd.mg.parameters_of_tech[6][2][0][0] *= 10
        # isolation is more "effective" by quantity of isolated people
        cd.mg.parameters_of_tech[6][2][1][0] *= 1.5  # but it is harder to isolate all of them

        cd.mg.parameters_of_tech[10][2][0][0] *= 2  # больше производят вакцин за такт
        cd.mg.parameters_of_tech[10][2][2][0] -= 1  # вакцины дешевле штамповать

    elif country_ind == 5:  # if China
        cd.mg.prices_of_tech[0][0] += 3  # investments in production in China are cheaper

        cd.mg.parameters_of_tech[6][2][0][0] *= 3
        # isolation is more "effective" by quantity of isolated people
        cd.mg.parameters_of_tech[6][2][1][0] *= 1.2
        # but it is harder to isolate all of them

        cd.mg.parameters_of_tech[10][2][0][0] *= 2  # больше производят вакцин за такт
        cd.mg.parameters_of_tech[10][2][2][0] -= 1  # вакцины дешевле штамповать

    elif country_ind == 6:  # if Mexico
        cd.mg.parameters_of_tech[5][2][0][0] *= 5  # не так хорошо перекрывается сообщение
        cd.mg.parameters_of_tech[5][2][1][0] = \
            1 - (1 - cd.mg.parameters_of_tech[5][2][1][0]) / 1.7
        cd.mg.parameters_of_tech[5][3][0] += 1  # но и доход слабее падает

        cd.mg.parameters_of_tech[7][2][0] = 0.2  # hard quarantine isn't so effective
        cd.mg.prices_of_tech[7] = [tech_info.prices_of_tech[7][0], tech_info.prices_of_tech[7][1] + 1]
        # but it is cheaper

    elif country_ind == 7:  # if Russia

        cd.mg.parameters_of_tech[5][2][0][0] *= 5  # не так хорошо перекрывается сообщение
        cd.mg.parameters_of_tech[5][2][1][0] = \
            1 - (1 - cd.mg.parameters_of_tech[5][2][1][0]) * 0.8
        cd.mg.parameters_of_tech[5][3][0] += 1  # но и доход слабее падает

        cd.mg.prices_of_tech[7] = [tech_info.prices_of_tech[7][0] + 5, tech_info.prices_of_tech[7][1] + 1]
        # карантин дешевле и придумать, и внедрить
        cd.mg.parameters_of_tech[7][2][0] = 1 / 10
        # жёсткий карантин в России не даёт такого сильного эффекта, как в других странах

        cd.mg.parameters_of_tech[0][3][0] = cd.mg.parameters_of_tech[0][3][0] + 2
        # инвестиции в производство у России более эффективны, чем у других стран
        cd.mg.prices_of_tech[0][0] -= 7  # но и дороже стоят

        cd.mg.prices_of_tech[2][0] -= 1  # инвестиции в исследования России дороже стоят
        cd.mg.prices_of_tech[1][0] -= 1  # investments в больницы в России дороже стоят

    elif country_ind == 8:  # if USA

        cd.mg.prices_of_tech[1][0] -= 5  # ивестиции в больницы в USA дороже стоят
        cd.mg.parameters_of_tech[1][2][0][0] \
            = 1 - (1 - cd.mg.parameters_of_tech[1][2][0][0]) / 2
        # investments in hospital don't reduce z_in effective
        cd.mg.prices_of_tech[2][0] += 1  # investments in research are cheaper
        cd.mg.parameters_of_tech[3][2][1][0] *= 2
        # американцы болезненней реагируют на введение масочного режима

        cd.mg.parameters_of_tech[6][2][1][0] *= 2.5  # it is harder to isolate all of them
        cd.mg.prices_of_tech[9][0] += 2  # science communication is cheaper
        cd.mg.prices_of_tech[15][0] = int(cd.mg.prices_of_tech[15][0] / 1.4)
        # emission is cheaper
        cd.mg.parameters_of_tech[15][2][2][0] = 0
        # если денег напечатать чуть-чуть, то американцы не возмутятся

    elif country_ind == 10:  # if Japan
        cd.mg.prices_of_tech[0][0] += 2  # investitions in production in Japan are cheaper
        cd.mg.prices_of_tech[2][0] += 1  # investitions in research in Japan are cheaper

        cd.mg.parameters_of_tech[5][3][0] += 2  # в Японии вполне автономно всё
        cd.mg.parameters_of_tech[5][2][1][0] = 1 - (
                1 - cd.mg.parameters_of_tech[5][2][1][0]) / 2
        # но и поэтому эффект более слабый от ограничения сообщения

        cd.mg.prices_of_tech[22][1] += 2  # автоматизация даётся проще

    elif country_ind == 11:  # Turkey
        cd.mg.parameters_of_tech[4][3][0] -= 1  # туристический бизнес слаб без самолётов
        cd.mg.parameters_of_tech[5][3][0] += 1  # в Турции вполне автономно всё
        cd.mg.parameters_of_tech[6][2][1][0] *= 1.5  # it is harder to isolate all of them
    elif country_ind == 12:  # Germany
        cd.mg.prices_of_tech[3][0] = int(1.5 * cd.mg.prices_of_tech[3][0])
        # респираторы дороже масок
        cd.mg.parameters_of_tech[3][2][0][0] = \
            1 - (1 - cd.mg.parameters_of_tech[3][2][0][0]) * 1.5
        # респираторы эффективней масок
        cd.mg.parameters_of_tech[3][2][1][0] = 1
        # респираторы протестов почти не вызывают
    if disease_ind == 1:  # flu
        cd.mg.prices_of_tech[11][0] *= 1.25  # cure is more expensive
        cd.mg.prices_of_tech[11][0] = round(cd.mg.prices_of_tech[11][0])

    elif disease_ind == 2:  # plague
        cd.mg.prices_of_tech[11][0] /= 1.25  # cure is cheaper
        cd.mg.prices_of_tech[11][0] = round(cd.mg.prices_of_tech[11][0])
        cd.mg.prices_of_tech[10][0] /= 1.1  # vaccine is cheaper
        cd.mg.prices_of_tech[10][0] = round(cd.mg.prices_of_tech[10][0])

    elif disease_ind == 3:  # smallpox
        cd.mg.prices_of_tech[11][0] *= 1.5  # cure is more expensive
        cd.mg.prices_of_tech[11][0] = round(cd.mg.prices_of_tech[11][0])

    cd.pre_final_layout.clear_widgets()

    try:
        del cd.frontend
    except AttributeError:
        pass
    cd.final_layout.clear_widgets()

    cd.frontend = cd.GameFrontend()
    left_panel_key_bind()

    cd.pre_final_layout.add_widget(cd.stencil_s2)

    cd.final_layout.add_widget(cd.pre_final_layout)

    cd.s2.canvas.clear()
    cd.s2.clear_widgets()
    cd.stencil_s2.remove_widget(cd.s2)
    del cd.s2

    cd.s2 = ScatterPlane(do_rotation=False, scale_min=.37, scale_max=2.5, scale=.5,
                                  do_collide_after_children=True, on_touch_down=draw_for_epidemy.on_scatter_touch_down,
                                  on_touch_move=draw_for_epidemy.on_scatter_move)
    sizes.start_s2_pos_x = cd.s2.pos[0]
    cd.s2.pos = (cd.s2.pos[0] +
                          sizes.width_res * cd.frontend.lp.table.size_hint_x, 0)
    sizes.normal_s2_pos_x = cd.s2.pos[0]
    cd.Country2 = draw_for_epidemy.CountryWidget()
    cd.s2.add_widget(cd.Country2)
    cd.stencil_s2.add_widget(cd.s2, canvas='before')
    cd.page2_1.scroll_y = 1

    e_settings.nast.current_country_label.text_source = cd.mg.My_Country.name
    e_settings.nast.current_country_label.text = cd.mg.My_Country.name[common_var.lang]

    e_settings.nast.label_current_disease_is.text_source = cd.mg.My_disease.name
    e_settings.nast.label_current_disease_is.text = cd.mg.My_disease.name[common_var.lang]

    e_settings.nast.label_current_mode_is.text_source = cd.mg.My_mode.name
    e_settings.nast.label_current_mode_is.text = cd.mg.My_mode.name[common_var.lang]

    e_settings.nast.lab_can_get_stars.text = icon_func.add_star_icon(
        string=str(cd.mg.My_Country.stars + cd.mg.My_disease.level - 2),
        size=e_settings.nast.lab_can_get_stars.font_size)

    init_of_tech.init_all_techs()
    cd.stats.possible_of_continue_game = True
    cd.stats.save_to_file()
    cd.mg.save_to_file()
    common_var.is_game_running = "gaming"
    end_of_step.auto_end_step_clock = None

    if cd.mg.My_mode.index in {1, 2, 3}:
        print("Mode with time limit per step")
        end_of_step.auto_end_step_clock = Clock.schedule_interval(end_of_step.mode_time_callback,
                                                                  cd.mg.My_mode.step_time / 30)

    if cd.mg.My_disease.index == 4:  # random scenario
        cd.to_str_dis_par(obj="z_out")
        cd.to_str_dis_par(obj="d_out")
        cd.to_str_dis_par(obj="transfer_c")


def does_user_want_to_start_a_game(instance):
    cd.pre_final_layout.clear_widgets()
    cd.page2.clear_widgets()
    starting_new_game()


class EpidemicApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rewards = RewardsHandler(self)

    def on_stop(self):
        if not common_var.WAS_STOP:
            print("You were gaming: " + str(time.time() - time_run) + " s")
            if common_var.is_game_running == "gaming":
                cd.mg.save_to_file()
            common_var.WAS_STOP = True
        return True

    def on_pause(self):
        if cd.stats.is_music_playing:
            music_module.sound.pause()
        return True

    def on_resume(self):
        if cd.stats.is_music_playing:
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

        if cd.stats.is_language_set != 1:
            check = lang_checkbox.StartLangChooseLayout()
            cd.final_layout.add_widget(check)
        else:
            cd.final_layout.add_widget(start_menu.Main_menu)

        start_menu.Main_menu.filling()

        self.outer_folders = []
        for i in cd.final_layout.children:
            self.outer_folders.append(i)

        EpidemicApp.day_award()

        return cd.final_layout

    def continue_saved_game(self, instance):

        cd.continue_game = True
        common_var.is_game_running = "gaming"
        file_game = open('game_exemplar_data.pkl', 'rb')

        cd.mg = cd.pickle.load(file_game)
        file_game.close()

        file_game = open('game_game_pars.pkl', 'rb')

        cd.mg.pars = cd.pickle.load(file_game)
        file_game.close()

        if widget_of_common_par.opened_ask_panel is not None:
            widget_of_common_par.opened_ask_panel.close_ask_panel(instance=5)

        cd.pre_final_layout.clear_widgets()

        cd.frontend = cd.GameFrontend()
        left_panel_key_bind()

        cd.pre_final_layout.add_widget(cd.stencil_s2)

        cd.final_layout.clear_widgets()

        cd.final_layout.add_widget(cd.pre_final_layout)

        cd.s2.clear_widgets()
        cd.stencil_s2.remove_widget(cd.s2)
        cd.s2.canvas.clear()
        cd.s2 = ScatterPlane(do_rotation=False, scale_min=.37, scale_max=2.5, scale=.5,
                                      on_touch_down=draw_for_epidemy.on_scatter_touch_down,
                                      on_touch_move=draw_for_epidemy.on_scatter_move)
        sizes.start_s2_pos_x = cd.s2.pos[0]
        cd.s2.pos = (cd.s2.pos[0] +
                              sizes.width_res * cd.frontend.lp.table.size_hint_x, 0)
        sizes.normal_s2_pos_x = cd.s2.pos[0]
        e_settings.nast.current_country_label.text_source = cd.mg.My_Country.name
        e_settings.nast.current_country_label.text = cd.mg.My_Country.name[common_var.lang]
        e_settings.nast.lab_can_get_stars.text = \
            icon_func.add_star_icon(string=str(cd.mg.My_Country.stars),
                                    size=e_settings.nast.lab_can_get_stars.font_size)
        e_settings.nast.label_current_disease_is.text_source = cd.mg.My_disease.name
        e_settings.nast.label_current_disease_is.text = cd.mg.My_disease.name[common_var.lang]

        e_settings.nast.label_current_mode_is.text_source = cd.mg.My_mode.name
        e_settings.nast.label_current_mode_is.text = cd.mg.My_mode.name[common_var.lang]

        cd.Country2 = draw_for_epidemy.CountryWidget()
        for i in range(cd.mg.My_Country.number_of_regions):
            if cd.mg.pars.reg_quarantine[i]:
                draw_for_epidemy.draw_reg_isolation(draw_for_epidemy.coords_of_hexes[i][0],
                                                draw_for_epidemy.coords_of_hexes[i][1],
                                                draw_for_epidemy.side, draw_for_epidemy.height, draw=True)

        cd.s2.add_widget(cd.Country2)
        cd.stencil_s2.add_widget(cd.s2, canvas='before')

        init_of_tech.init_all_techs()

        if cd.mg.My_mode.index in {1, 2, 3}:
            end_of_step.auto_end_step_clock = Clock.schedule_interval(end_of_step.mode_time_callback,
                                                                      cd.mg.My_mode.step_time / 30)

        if cd.mg.My_disease.index == 4:  # unknown disease
            cd.to_str_dis_par(obj="z_out")
            cd.to_str_dis_par(obj="d_out")
            cd.to_str_dis_par(obj="transfer_c")
            print(cd.mg.My_disease.padezhi)

    @staticmethod
    def choosing_mode(instance):
        widget_of_common_par.Mode_var = game_modes_choicer.Mode_choiser_layout()
        widget_of_common_par.Mode_var.open_layout(instance=0)
        widget_of_common_par.Mode_var.btn_confirm.bind(on_press=does_user_want_to_start_a_game)

    @staticmethod
    def choosing_country(instance):
        widget_of_common_par.Country_var = country_choicer.Country_choiser_layout()
        widget_of_common_par.Country_var.open_layout(instance=0)
        widget_of_common_par.Country_var.btn_remake_country.bind(on_press=EpidemicApp.choosing_mode)

    @staticmethod
    def choosing_disease(instance=None):
        common_var.is_game_running = "preparing for game"
        widget_of_common_par.Dis_var = disease_choicer.DiseaseMenu()
        widget_of_common_par.Dis_var.open_layout(instance=None)
        widget_of_common_par.Dis_var.btn_confirm.bind(on_press=EpidemicApp.choosing_country)

    def close_game_space(self, instance):
        cd.final_layout.clear_widgets()

        for i in self.outer_folders:
            cd.final_layout.add_widget(i)

        common_var.is_game_running = "in_main_menu"
        print("returned to main menu")

        if not start_menu.Main_menu.covid_image.is_animating:
            start_menu.Main_menu.covid_image.is_animating = True
            start_menu.Main_menu.covid_image.generate_rotating_transition(instance=0, animation=0)
            start_menu.Main_menu.covid_image.generate_horizontal_moving(instance=0, animation=0)
            start_menu.Main_menu.covid_image.generate_vertical_moving(instance=0, animation=0)

    def end_of_game(self, first_text=""):
        if cd.mg.My_disease.index == 4:
            diseases.control_unknown_disease()
        common_var.is_game_running = "after_game"
        were_goldreserves = cd.stats.goldreserves
        were_stars = cd.stats.stars
        award_coins = None
        award_stars = None
        comments = None
        if common_var.is_victory == 1:
            award_stars = cd.mg.My_Country.stars + cd.mg.My_disease.level - 2
            award_coins = int(award_stars * 7)
            comments = ['красавчик', 'я такого не ожидала', 'молодец', 'так держать',
                        'очень круто', 'не зазнавайся', 'можно было бы и круче выступить']
            cd.stats.results_by_countries[cd.mg.My_Country.index].append(1)
            cd.stats.results_by_diseases[cd.mg.My_disease.index].append(1)
        if common_var.is_victory == 0:
            award_stars = min(cd.mg.My_Country.stars +
                              cd.mg.My_disease.level - 2 - 1,
                              round(cd.mg.pars.step_num / 15
                                    + cd.mg.My_disease.level / 5, 1))
            award_stars = round(award_stars, 1)
            award_coins = cd.math.ceil(award_stars * 3)
            comments = ['позор какой', 'Вы продулись', 'не распускай нюни',
                        'в следующий раз будет лучше', 'попробуй ещё раз',
                        'плоховато', 'не отчаивайся']
            cd.stats.results_by_countries[cd.mg.My_Country.index].append(0)
            cd.stats.results_by_diseases[cd.mg.My_disease.index].append(0)
        award_stars = round(award_stars * cd.mg.My_mode.coef_award, 1)
        award_coins = round(award_coins * cd.mg.My_mode.coef_award, 1)
        speech = cd.random.choice(comments)
        print(speech)
        '''
        if cd.random.randint(0, 4) == 0:
            try:
                sizes.plyer.tts.speak(speech)
            except:
                print("no voice")'''

        cd.stats.possible_of_continue_game = False

        cd.stats.number_of_games += 1

        cd.stats.victory_percent = (common_var.is_victory + (cd.stats.number_of_games - 1)
                                               * cd.stats.victory_percent) / \
                                              cd.stats.number_of_games
        cd.victory_percent_str = [str(round(cd.stats.victory_percent * 100, 1)) + "%",
                               str(round(cd.stats.victory_percent * 100, 1)) + "%"]

        cd.stats.goldreserves = int(cd.stats.goldreserves + award_coins)
        cd.stats.stars = round(cd.stats.stars + award_stars, 1)

        stars_level_promotion = False
        wealth_level_promotion = False

        prev_stars_level = cd.stats.level_stars
        cd.stats.level_stars = spec_func.status_finder(typ='stars', value=cd.stats.stars)[0]

        if cd.stats.level_stars > prev_stars_level:
            stars_level_promotion = True
            print("Stars level promotion!")

        prev_coins_level = cd.stats.level_coins
        cd.stats.level_coins = \
            spec_func.status_finder(typ='coins', value=cd.stats.goldreserves)[0]
        if cd.stats.level_coins > prev_coins_level:
            wealth_level_promotion = True
            print("Wealth level promotion!")

        cd.stats.save_to_file()

        awards_are_str = ["Вы заработали за эту партию:\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
            size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(size=sizes.WIN_SIZE) + "\n",
                               "Your awards:\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
                                   size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(
                                   size=sizes.WIN_SIZE) + "\n"]
        if award_stars == 0 and award_coins == 0:
            awards_are_str = ["", ""]

        if common_var.is_victory == 0:
            mes = ["К сожалению, Вы проиграли.\n" + awards_are_str[
                common_var.lang] + "\n" + "Нам кажется, что в следующий \nраз у Вас всё получится :)\n",
                   "You lose:(\n\n" + awards_are_str[
                       common_var.lang] + "\n" + "Try again! We guess you'll win next game :)\n"]
            widget_of_common_par.inform_about_end(mes[common_var.lang], 'bad', status_s_rising=stars_level_promotion,
                                                  status_c_rising=wealth_level_promotion)

        elif common_var.is_victory == 1:
            mes = ["Ура!!! Вы победили!\n\n" + awards_are_str[common_var.lang],
                   "You have won!!!\n\n" + awards_are_str[common_var.lang]]

            widget_of_common_par.inform_about_end(mes[common_var.lang], 'good', status_s_rising=stars_level_promotion,
                                                  status_c_rising=wealth_level_promotion)

        common_var.need_c = spec_func.status_finder('coins', cd.stats.goldreserves)[1]
        common_var.need_s = spec_func.status_finder('stars', cd.stats.stars)[1]

        e_settings.nast.update_stats_after_end_of_the_game()
        start_menu.Main_menu.stats_pannel_in.update_stats_after_end_of_the_game()

        cd.mg.delete_game_ex()

        new_countries = list()
        for i in range(len(country_variants.Country_lands)):
            if were_goldreserves < country_variants.Country_lands[i].min_goldreserves <= \
                    cd.stats.goldreserves:
                print(country_variants.Country_lands[i].name)
                new_countries.append(i)

        for i in range(len(country_variants.Country_lands)):
            if were_stars < country_variants.Country_lands[i].min_rep_stars <= cd.stats.stars:
                print(country_variants.Country_lands[i].name)
                new_countries.append(i)

        new_techs = list()
        for i in range(common_var.QUANT_OF_TECH):
            if were_goldreserves < tech_info.min_goldreserves_for_tech[i] <= cd.stats.goldreserves:
                new_techs.append(i)
                print(tech_info.names_of_tech[i])

        for i in range(common_var.QUANT_OF_TECH):
            if were_stars < tech_info.min_stars_for_tech[i] <= cd.stats.stars:
                new_techs.append(i)
                print(tech_info.names_of_tech[i])
        new_diseases = list()
        for i in range(len(diseases.diseases_list)):
            if were_goldreserves < diseases.diseases_list[i].min_gold <= cd.stats.goldreserves:
                new_diseases.append(i)

        try:  # to-do: rewrite without try
            del special_achievs.win_panel
        except:
            print("Win panel was deleted earlier")
        spec_achieves = []
        if first_text != "":
            spec_achieves.append(["first_text", first_text])
        if cd.random.randint(0, 4) == 1:
            spec_achieves.append(["link_vk_page", "https://vk.com/epidemy_inception"])

        history_of_games = cd.stats.results_by_countries[cd.mg.My_Country.index]
        if sum(history_of_games) == 1 and history_of_games[len(history_of_games) - 1] == 1:
            spec_achieves.append(
                ["victory_by_new_country", cd.mg.My_Country.name, cd.mg.My_Country.index])

            history_of_games = cd.stats.results_by_diseases[cd.mg.My_disease.index]
        if sum(history_of_games) == 1 and history_of_games[len(history_of_games) - 1] == 1:
            spec_achieves.append(
                ["victory_by_new_disease", cd.mg.My_disease.name, cd.mg.My_disease.rod])

        if new_techs != list():
            spec_achieves.append(["new_techs", new_techs])

        if new_countries != list():
            spec_achieves.append(["new_countries", new_countries])
        if new_diseases != list():
            spec_achieves.append(["new_disease", new_diseases])

        if stars_level_promotion:
            spec_achieves.append(["rep_status", cd.stats.level_stars])
        if wealth_level_promotion:
            spec_achieves.append(["gold_status", cd.stats.level_coins])

        if cd.random.randint(0, 10) == 1:
            app_store_link = "https://play.google.com/store/apps/details?id=com.legeartisgames.epidemy"
            if sizes.platform == "android":
                app_store_link = "market://details?id=com.legeartisgames.epidemy"

            spec_achieves.append(["rate_app", app_store_link])

        if len(spec_achieves) != 0:
            special_achievs.win_panel = special_achievs.SpecAchievPanel(achieves=spec_achieves)
            special_achievs.win_panel.open_panel(instance=5)

        common_var.is_victory = "none"

        if tech_sm.tech_viewer is not None:  # избавляемся от листания
            tech_sm.tech_viewer.close_self(instance=3)

    @staticmethod
    def day_award():
        if cd.first_run_in_this_day and len(cd.stats.days_of_activity) > 1:
            were_goldreserves = cd.stats.goldreserves
            were_stars = cd.stats.stars
            award_stars = 15
            award_coins = 25

            cd.stats.goldreserves = int(cd.stats.goldreserves + award_coins)
            cd.stats.stars = round(cd.stats.stars + award_stars, 1)

            stars_level_promotion = False
            wealth_level_promotion = False

            x = cd.stats.level_stars
            cd.stats.level_stars = spec_func.status_finder(typ='stars', value=cd.stats.stars)[0]

            if cd.stats.level_stars > x:
                stars_level_promotion = True
                print("stars_level_promotion")

            x = cd.stats.level_coins
            cd.stats.level_coins = \
                spec_func.status_finder(typ='coins', value=cd.stats.goldreserves)[0]
            if cd.stats.level_coins > x:
                wealth_level_promotion = True
                print("wealth_level_promotion")

            cd.stats.save_to_file()

            awards_are_str = [
                "Новый день - новая награда:\n\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
                    size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(
                    size=sizes.WIN_SIZE) + "\n\n",
                "New day - new reward:\n\n" + "+ " + str(award_stars) + icon_func.get_star_icon(
                    size=sizes.WIN_SIZE) + "\n" + "+ " + str(award_coins) + icon_func.get_coin_icon(
                    size=sizes.WIN_SIZE) + "\n\n"]

            common_var.need_c = spec_func.status_finder('coins', cd.stats.goldreserves)[1]
            common_var.need_s = spec_func.status_finder('stars', cd.stats.stars)[1]

            start_menu.Main_menu.stats_pannel_in.update_stats_after_end_of_the_game()

            cd.mg.delete_game_ex()
            new_countries = list()
            for i in range(len(country_variants.Country_lands)):
                if were_goldreserves < country_variants.Country_lands[i].min_goldreserves \
                        <= cd.stats.goldreserves:
                    print(country_variants.Country_lands[i].name)
                    new_countries.append(i)

            for i in range(len(country_variants.Country_lands)):
                if were_stars < country_variants.Country_lands[i].min_rep_stars <= cd.stats.stars:
                    print(country_variants.Country_lands[i].name)
                    new_countries.append(i)

            new_techs = list()
            for i in range(common_var.QUANT_OF_TECH):
                if were_goldreserves < tech_info.min_goldreserves_for_tech[i] <= cd.stats.goldreserves:
                    new_techs.append(i)
                    print(tech_info.names_of_tech[i])

            new_diseases = list()
            for i in range(len(diseases.diseases_list)):
                if were_goldreserves < diseases.diseases_list[i].min_gold <= cd.stats.goldreserves:
                    new_diseases.append(i)

            for i in range(common_var.QUANT_OF_TECH):
                if were_stars < tech_info.min_stars_for_tech[i] <= cd.stats.stars:
                    new_techs.append(i)
                    print(tech_info.names_of_tech[i])

            try:  # to-do: rewrite it
                del special_achievs.win_panel
            except:
                print("Win pannel was deleted earlier")

            spec_achieves = list()
            spec_achieves.append(["first_text", awards_are_str[common_var.lang]])

            if new_techs != list():
                spec_achieves.append(["new_techs", new_techs])

            if new_countries != list():
                spec_achieves.append(["new_countries", new_countries])

            if new_diseases != list():
                spec_achieves.append(["new_disease", new_diseases])

            if stars_level_promotion:
                spec_achieves.append(["rep_status", cd.stats.level_stars])
            if wealth_level_promotion:
                spec_achieves.append(["gold_status", cd.stats.level_coins])

            if cd.random.randint(0, 10) == 1:
                app_store_link = "https://play.google.com/store/apps/details?id=com.legeartisgames.epidemy"
                if sizes.platform == "android":
                    app_store_link = "market://details?id=com.legeartisgames.epidemy"

                spec_achieves.append(["rate_app", app_store_link])

            last_text = cd.random.choice([["Продолжайте спасать мир!", "Keep going!"], ["", ""],
                                                   ["Удачи в партиях!", "Good luck!"],
                                                   ["Эпидемия ждёт вас!", "Epidemy is waiting for you!",
                                                    "Рады видеть вас снова!", "Glad to see you again!"]])
            spec_achieves.append(["first_text", last_text[common_var.lang]])

            if len(spec_achieves) != 0:
                special_achievs.win_panel = special_achievs.SpecAchievPanel(achieves=spec_achieves,
                                                                                         color="green")
                special_achievs.win_panel.open_panel(instance=5)

            e_settings.nast.update_stats_after_end_of_the_game()

    @staticmethod
    def start_new_game_right_now(instance=None):
        common_var.is_game_running = "preparing for game"
        widget_of_common_par.Dis_var = disease_choicer.DiseaseMenu()
        widget_of_common_par.Dis_var.open_layout()
        widget_of_common_par.Dis_var.btn_confirm.bind(on_press=EpidemicApp.choosing_disease)

    @staticmethod
    def open_panel(instance):  # for tech panel
        if common_var.is_open_tech == 0:
            cd.pre_final_layout.remove_widget(cd.stencil_s2)

            cd.pre_final_layout.add_widget(cd.page2_1)
            common_var.is_open_tech = 1
            cd.frontend.lp.btns.btn_open_pannel_of_tech.state = 'down'

        elif common_var.is_open_tech == 1:
            cd.pre_final_layout.remove_widget(cd.page2_1)
            cd.pre_final_layout.add_widget(cd.stencil_s2)

            common_var.is_open_tech = 0
            cd.frontend.lp.btns.btn_open_pannel_of_tech.state = 'normal'

    def load_rewarded_video(self):
        self.ads.load_rewarded_ad(ads_mob.GOLD_REWARDED_ID)

    def post_build_init(self, *args):
        win = e_settings.Window
        win.bind(on_keyboard=self.my_key_handler)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:
            if widget_of_common_par.notifier.notifier_box.is_active:
                widget_of_common_par.notifier.notifier_box.clear_and_delete(dt=0)

            for i in cd.final_layout.children:
                if i.__class__.__name__ == "InfoCarousel":
                    i.close(instance=0)
                    i.delete()
                    return 5

            if interact_rules.rp in cd.final_layout.children:
                if interact_rules.rp.num == 1:  # contents
                    interact_rules.rp.close_self(instance=5)
                else:
                    interact_rules.rp.open_page(index=1, instance=0)
                return 5

            if graph_maker.current_graph in cd.final_layout.children:
                graph_maker.current_graph.close(instance=0)
                return 5

            if start_menu.Main_menu.stats_pannel in cd.final_layout.children:
                start_menu.Main_menu.stats_pannel.children[0].close_setts(instance=1)
                return 5

            for i in {info_layouts.country_info_pannel, info_layouts.diseases_info_pannel,
                      info_layouts.modes_info_pannel}:
                if i in cd.final_layout.children:
                    i.close_manual(instance=0)
                    return 5

            if achieve_pannel.achieve_p in cd.final_layout.children:
                achieve_pannel.achieve_p.close_layout(instance=0)
                return 5
            try:  # to-do: rewrite it
                if special_achievs.win_panel in cd.final_layout.children:
                    special_achievs.win_panel.close_panel(instance=0)
                    return 5
            except:
                print("No win pannel when you pressed esc button")

            if e_settings.common_nast in cd.final_layout.children:
                e_settings.nast.close_setts(instance=1)
                return 5
            if tech_sm.tech_viewer in cd.page2_1.children:
                tech_sm.tech_viewer.close_self(instance=0)
                return 5

            if common_var.is_open_tech == 1:
                self.open_panel(instance=5)
                return 5

            if common_var.is_game_running == "preparing for game":
                cd.final_layout.children[0].close_layout(instance=5)
                return 5

            if widget_of_common_par.opened_ask_panel is not None:
                widget_of_common_par.opened_ask_panel.close_ask_panel(instance=5)
                return 5

            if common_var.is_game_running == "gaming":
                e_settings.do_you_want_to_exit(instance=0)
                return 5

            if (common_var.is_game_running in {"in_main_menu", "after_game"}) and cd.escape_ind == 1:
                e_settings.finish_all(instance=2)
                return 5

            cd.escape_ind = 1

            mes = ['Нажмите ещё раз "назад" для выхода из приложения', "Tap back again to exit the app"]
            widget_of_common_par.info_message(mes[common_var.lang], 'good', 2)
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
    cd.frontend.pars.labels.str_for_z_out.bind(
        on_press=lambda x: graph_maker.make_graph(typ='new_ill', for_country=True))
    cd.frontend.pars.labels.str_for_d_out.bind(
        on_press=lambda x: graph_maker.make_graph(typ='new_dead', for_country=True))

    cd.frontend.pars.labels.str_of_straph.bind(
        on_press=lambda x: graph_maker.make_graph(typ='pen_points', for_country=True))

    cd.frontend.lp.btns.btn_fin_step.bind(on_press=end_of_step.Step_Make)
    cd.frontend.lp.btns.btn_open_pannel_of_tech.bind(
        on_press=EpidemicApp.open_panel)
    cd.frontend.lp.multichoice_layout.btn_activate.bind(on_press=multichoice_on_off)
    cd.frontend.lp.multichoice_layout.btn_do_it.bind(on_press=choose_technology_to_hex)
    cd.frontend.lp.btns.settings_button.bind(on_press=e_settings.nast.open_setts)


def choose_technology_to_hex(instance):
    if len(cd.mg.list_of_chosen) > 0:
        regions_menu.region_menu()


def multichoice_on_off(instance):
    if cd.mg.multichoice_ind == 1:
        for i in range(cd.mg.n):
            if cd.mg.multichoice_list[i] == 1:
                cd.frontend.hexes_chosen[i].hide_circle()
        cd.mg.multichoice_list = [0] * 21
        cd.mg.list_of_chosen = []
    cd.mg.multichoice_ind *= (-1)


if __name__ == '__main__':
    time_run = time.time()
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    EpidemicApp().run()

