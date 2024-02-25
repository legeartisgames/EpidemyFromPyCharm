import achieve_pannel
import common_data as cd
import common_var
import draw_for_epidemy
import gold_transaction
import icon_func
# import info_layouts
import init_of_tech
import interact_rules
import lang_checkbox
import music_module
import textures
import sizes
import uix_classes
import widget_of_common_par

from kivy.clock import Clock
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from custom_kivy.my_scrollview import ScrollView
from kivy.uix.slider import Slider


class AdditionalMenu(GridLayout):
    def __init__(self, type_of_nast="game_setts", **kwargs):
        super(AdditionalMenu, self).__init__(**kwargs)
        self.need_stars_box = BoxLayout()
        self.need_coins_box = BoxLayout()
        self.create(type_of_nast)
        self.type_of_nast = type_of_nast

    def create(self, type_of_nast="game_setts"):
        self.cols = 2
        self.spacing = (sizes.width_res / 250, sizes.height_res / 250)
        if type_of_nast == "game_setts":
            self.add_widget(uix_classes.Button_with_image(on_press=increase_money,
                                                          size_hint_y=None, height=sizes.height_res / 5,
                                                          font_size=sizes.NAST_SIZE, halign='center',
                                                          text_source=["Пополнить казну", "Get money"]))

        self.add_widget(uix_classes.Button_with_image(text_source=["Панель достижений", "Achievement bar"],
                                                      on_press=achieve_pannel.achieve_p.open_layout,
                                                      size_hint_y=None, height=sizes.height_res / 5,
                                                      font_size=sizes.NAST_SIZE, halign='center'))

        self.add_widget(uix_classes.Button_with_image(text_source=["Правила игры", "Game guide"],
                                                      on_press=interact_rules.rp.open_self,
                                                      size_hint_y=None, height=sizes.height_res / 5,
                                                      font_size=sizes.NAST_SIZE))
        if type_of_nast == "game_setts":
            self.add_widget(uix_classes.Button_with_image(text_source=['Назад к игре', "Back to the game"],
                                                          on_press=self.close_setts,
                                                          size_hint_y=None, height=sizes.height_res / 5,
                                                          font_size=sizes.NAST_SIZE, halign='center'))

            self.add_widget(uix_classes.Label_with_tr(text_source=["Текущая страна", "Current country"],
                                                      size_hint=[1, None], height=sizes.height_res / 5,
                                                      font_size=sizes.NAST_SIZE, halign='center'))

            self.current_country_label = uix_classes.Label_with_tr(text_source=cd.mg.My_Country.name,
                                                                   size_hint=[1, .3], font_size=sizes.NAST_SIZE,
                                                                   color="56b344")
            self.add_widget(self.current_country_label)

            self.add_widget(uix_classes.Label_with_tr(text_source=["Текущая инфекция", "Current infection"],
                                                      size_hint=[1, None], height=sizes.height_res / 5,
                                                      font_size=sizes.NAST_SIZE, halign='center'))

            self.label_current_disease_is = uix_classes.Label_with_tr(text_source=cd.mg.My_disease.name,
                                                                      size_hint=[1, .3],
                                                                      font_size=sizes.NAST_SIZE, color=[1, 0, 0, 1])
            self.add_widget(self.label_current_disease_is)

            self.add_widget(uix_classes.Label_with_tr(text_source=["Текущий режим", "Current mode"],
                                                      size_hint=[1, None], height=sizes.height_res / 5,
                                                      font_size=sizes.NAST_SIZE, halign='center'))

            self.label_current_mode_is = uix_classes.Label_with_tr(text_source=cd.mg.My_mode.name,
                                                                   size_hint=[1, .3],
                                                                   font_size=sizes.NAST_SIZE, color="2065ab")
            self.add_widget(self.label_current_mode_is)

        self.add_widget(uix_classes.Label_with_tr(text_source=["Музыка", "Music"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.music_switch = music_module.My_switch(size_hint=[1, .2])
        self.add_widget(self.music_switch)

        self.music_slider = Slider(min=0, max=1, size_hint=[1, .2], value=0.7, sensitivity="all", value_track=True,
                                   value_track_color=[70 / 256, 89 / 256, 94 / 256, 1], value_track_width="4.5dp")
        self.add_widget(uix_classes.Label_with_tr(text_source=["Громкость музыки", "Music volume"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.music_slider.bind(value=self.set_volume)

        self.add_widget(self.music_slider)

        if type_of_nast == "game_setts":
            self.add_widget(uix_classes.Label_with_tr(text_source=["Линейка на карте страны", "Ruler on country map"],
                                                      size_hint=[1, None], height=sizes.height_res / 5,
                                                      font_size=sizes.NAST_SIZE, halign='center'))
            self.switch_real_sizes = music_module.Switch(size_hint=[1, .2], active=cd.stats.sizes_ruler_on)
            self.add_widget(self.switch_real_sizes)

            self.switch_real_sizes.bind(active=draw_redraw_real_country_sizes)

            self.add_widget(uix_classes.Label_with_tr(
                text_source=["Отображение\nнедоступных методов", "Show yet unlocked\nmethods"],
                size_hint=[1, None], height=sizes.height_res / 5,
                font_size=sizes.NAST_SIZE, halign='center'))
            self.show_unlocked_methods_switch = music_module.Switch(size_hint=[1, .2],
                                                                    active=cd.stats.are_shown_unlocked_methods)
            self.add_widget(self.show_unlocked_methods_switch)

            self.show_unlocked_methods_switch.bind(active=operate_unlocked_methods)

        self.add_widget(uix_classes.Label_with_tr(text_source=["Процент побед", "Victory percent"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.lab_percent_of_v = Label(text=cd.victory_percent_str[common_var.lang],
                                      size_hint=[1, None], height=sizes.height_res / 5,
                                      font_size=sizes.NAST_SIZE)
        self.add_widget(self.lab_percent_of_v)

        self.add_widget(uix_classes.Label_with_tr(text_source=["Число сыгранных партий", "Completed games"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.num_games_label = Label(text=str(cd.stats.number_of_games),
                                     size_hint=[1, None], height=sizes.height_res / 5,
                                     font_size=sizes.NAST_SIZE)
        self.add_widget(self.num_games_label)

        self.add_widget(uix_classes.Label_with_tr(text_source=["Дней в игре", "Days with gaming"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.add_widget(uix_classes.Label(text=str(len(cd.stats.days_of_activity)),
                                          size_hint=[1, None], height=sizes.height_res / 5,
                                          font_size=sizes.NAST_SIZE, halign='center'))

        self.add_widget(uix_classes.Label_with_tr(text_source=["Звёзды репутации", "Reputation stars"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.num_stars_label = \
            Label(text=icon_func.add_star_icon(string=str(cd.stats.stars), size=sizes.NAST_SIZE),
                  size_hint=[1, None], height=sizes.height_res / 5,
                  font_size=sizes.NAST_SIZE, markup=True)
        self.add_widget(self.num_stars_label)

        self.add_widget(uix_classes.Label_with_tr(text_source=["Статус репутации", "Reputation Status"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.stars_status_label = uix_classes.Label_with_tr(
            text_source=common_var.stars_statuses[cd.stats.level_stars],
            size_hint=[1, None], height=sizes.height_res / 5,
            font_size=sizes.NAST_SIZE, halign='center')
        self.add_widget(self.stars_status_label)

        self.add_widget(
            uix_classes.Label_with_tr(text_source=["До следующего\nстатуса репутации", "For next reputation status"],
                                      size_hint=[1, None], height=sizes.height_res / 5,
                                      font_size=sizes.NAST_SIZE, halign='center'))

        self.lab_need_for_s = Label(text=icon_func.add_star_icon(string=str(common_var.need_s), size=sizes.NAST_SIZE),
                                    size_hint=[1, None], height=sizes.height_res / 5,
                                    font_size=sizes.NAST_SIZE, markup=True)

        self.lab_need_for_s.font_size = sizes.NAST_SIZE
        self.need_stars_box.clear_widgets()
        self.add_widget(self.need_stars_box)
        self.lab_need_for_s.size_hint_x = .35
        self.need_stars_box.add_widget(self.lab_need_for_s)

        self.stars_progress_bar = ProgressBar(value=cd.stats.stars,
                                              max=cd.stats.stars + common_var.need_s,
                                              size_hint_x=.57)
        self.need_stars_box.add_widget(self.stars_progress_bar)
        self.stars_progress_bar.value = cd.stats.stars

        if type_of_nast == "game_setts":
            self.add_widget(uix_classes.Label_with_tr(text_source=["Звёзды за победу в партии", "Stars for winning"],
                                                      size_hint=[1, None], height=sizes.height_res / 5,
                                                      font_size=sizes.NAST_SIZE))

            self.lab_can_get_stars = Label(text=icon_func.add_star_icon(
                string=str(cd.mg.My_Country.stars + cd.mg.My_disease.level - 2),
                size=sizes.NAST_SIZE),
                size_hint=[1, None], height=sizes.height_res / 5,
                font_size=sizes.NAST_SIZE, markup=True)
            self.add_widget(self.lab_can_get_stars)

        self.add_widget(uix_classes.Label_with_tr(text_source=["Золотовалютные\nрезервы", "Gold Exchange\nReserves"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.str_of_reserves = Label(text=icon_func.add_money_icon(string=str(cd.stats.goldreserves),
                                                                   size=sizes.NAST_SIZE),
                                     size_hint=[1, .3], markup=True, font_size=sizes.NAST_SIZE)

        self.add_widget(self.str_of_reserves)

        self.add_widget(uix_classes.Label_with_tr(text_source=["Статус Благосостояния", "Wealth status"],
                                                  size_hint=[1, None], height=sizes.height_res / 5,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.lab_status_of_rich = uix_classes.Label_with_tr(
            text_source=common_var.statuses_coins[cd.stats.level_coins],
            size_hint=[1, None], height=sizes.height_res / 5,
            font_size=sizes.NAST_SIZE, halign='center')
        self.add_widget(self.lab_status_of_rich)

        self.add_widget(
            uix_classes.Label_with_tr(text_source=["До следующего\nстатуса благосостояния", "For next wealth status"],
                                      size_hint=[1, None], height=sizes.height_res / 5,
                                      font_size=sizes.NAST_SIZE, halign='center'))

        self.lab_need_coins_for_next_status = Label(text=icon_func.add_money_icon(string=str(common_var.need_c),
                                                                                  size=sizes.NAST_SIZE),
                                                    size_hint=[.35, None], height=sizes.height_res / 5,
                                                    font_size=sizes.NAST_SIZE, markup=True)
        self.need_coins_box.clear_widgets()
        self.need_coins_box.add_widget(self.lab_need_coins_for_next_status)
        self.add_widget(self.need_coins_box)

        self.coins_progress_bar = ProgressBar(value=int(cd.stats.goldreserves),
                                              max=cd.stats.goldreserves + common_var.need_c,
                                              size_hint_x=.57)
        self.coins_progress_bar.value = int(cd.stats.goldreserves)
        self.need_coins_box.add_widget(self.coins_progress_bar)
        self.add_widget(uix_classes.Label_with_tr(text_source=["Текущий язык", "Language"],
                                                  size_hint=[1, None], height=sizes.height_res / 3,
                                                  font_size=sizes.NAST_SIZE, halign='center'))

        self.lang_checkbox = lang_checkbox.LanguageCheckbox()
        self.add_widget(self.lang_checkbox)

        if type_of_nast == "game_setts":
            self.add_widget(uix_classes.Button_with_image(text_source=["Карту по центру", "Center country map"],
                                                          on_press=redraw,
                                                          size_hint=[1, None], height=sizes.height_res / 6,
                                                          font_size=sizes.NAST_SIZE, halign='center'))

        if type_of_nast == "common_stats":
            self.add_widget(uix_classes.Button_with_image(text_source=["Закрыть статистику", "Close stats"],
                                                          on_press=self.close_setts,
                                                          size_hint_y=None, height=sizes.height_res / 6,
                                                          font_size=sizes.NAST_SIZE, halign='center'))

        self.add_widget(uix_classes.Button_with_image(text_source=["Выйти из игры", "Exit the app"],
                                                      on_press=do_you_want_to_exit,
                                                      size_hint_y=None, height=sizes.height_res / 6,
                                                      font_size=sizes.NAST_SIZE, halign='center'))

    def update_stats_after_end_of_the_game(self):
        self.num_games_label.text = str(cd.stats.number_of_games)

        self.lab_percent_of_v.text = cd.victory_percent_str[common_var.lang]
        self.lab_percent_of_v.text_source = cd.victory_percent_str

        self.str_of_reserves.text = icon_func.add_money_icon(string=str(cd.stats.goldreserves),
                                                             size=self.str_of_reserves.font_size)

        self.lab_need_coins_for_next_status.text = icon_func.add_money_icon(string=str(common_var.need_c),
                                                                            size=self.lab_need_coins_for_next_status.font_size)
        self.coins_progress_bar.value = int(cd.stats.goldreserves)
        self.coins_progress_bar.max = cd.stats.goldreserves + common_var.need_c

        self.lab_status_of_rich.text_cource = common_var.statuses_coins[cd.stats.level_coins]
        self.lab_status_of_rich.text = common_var.statuses_coins[cd.stats.level_coins][common_var.lang]

        self.stars_progress_bar.value = int(cd.stats.stars)
        self.stars_progress_bar.max = cd.stats.stars + common_var.need_s

        self.lab_need_for_s.text = icon_func.add_star_icon(string=str(common_var.need_s),
                                                           size=self.lab_need_for_s.font_size)

        self.stars_status_label.text_source = common_var.stars_statuses[cd.stats.level_stars]
        self.stars_status_label.text = common_var.stars_statuses[cd.stats.level_stars][common_var.lang]
        self.num_stars_label.text = icon_func.add_star_icon(string=str(cd.stats.stars),
                                                            size=self.num_stars_label.font_size)

    def close_setts(self, instance):
        cd.final_layout.remove_widget(self.parent)
        for i in self.outer_folders:
            cd.final_layout.add_widget(i)

    def set_volume(self, value, instance):
        cd.stats.volume_of_music = self.music_slider.value
        music_module.sound.volume = self.music_slider.value

    def open_setts(self, instance):
        self.outer_folders = []
        for i in cd.final_layout.children:
            self.outer_folders.append(i)
        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(self.parent)

        for i in range(common_var.NUM_OF_LANGS):
            self.lang_checkbox.check_boxes_for_lang[i].active = False
        self.lang_checkbox.check_boxes_for_lang[common_var.lang].active = True
        self.music_slider.value = cd.stats.volume_of_music


def do_you_want_to_exit(instance):
    ask_exit_menu = widget_of_common_par.AskPanel()
    if common_var.is_game_running == "gaming":
        if common_var.lang == 0:
            ask_exit_menu.open_ask_panel(
                messages=["Вы хотите выйти из приложения?\n", "Если вы это сделаете,\n то эта партия сохранится."],
                texture=textures.texture_questions, color_texture=(1, 1, 1, .6))
        if common_var.lang == 1:
            ask_exit_menu.open_ask_panel(
                messages=["Do you want to exit the app?\n", "Everything is OK, this game will be saved"],
                texture=textures.texture_questions, color_texture=(1, 1, 1, .6))

        btn_yes = Button(text=(["Выйти из\nприложения", "Exit\nthe app"][common_var.lang]),
                         size_hint=(.3 * ask_exit_menu.size_zone[0] / sizes.width_res,
                                    .17 * ask_exit_menu.size_zone[1] / sizes.height_res),
                         pos=(
                             ask_exit_menu.left_edge_pos[0] +
                             ask_exit_menu.size_zone[
                                 0] * 0.6,
                             ask_exit_menu.left_edge_pos[1] +
                             ask_exit_menu.size_zone[
                                 1] * 0.25),
                         font_size=sizes.ASK_SIZE, on_press=finish_all,
                         background_color=[1, 0, 0, 1], halign='center')

        ask_exit_menu.add_widget(btn_yes)

        btn_no = Button(text=(["Вернуться\nв игру", "Back to\nthe game"][common_var.lang]),
                        size_hint=(.3 * ask_exit_menu.size_zone[0] / sizes.width_res,
                                   .17 * ask_exit_menu.size_zone[1] / sizes.height_res),
                        pos=(
                            ask_exit_menu.left_edge_pos[0] +
                            ask_exit_menu.size_zone[
                                0] * 0.1,
                            ask_exit_menu.left_edge_pos[1] +
                            ask_exit_menu.size_zone[
                                1] * 0.25),
                        font_size=sizes.ASK_SIZE, on_press=ask_exit_menu.close_ask_panel,
                        background_color=[0, 1, 0, 1], halign='center')
        ask_exit_menu.add_widget(btn_no)
        ask_exit_menu.remove_widget(ask_exit_menu.btn_ask_close)
    else:
        finish_all(instance=5)


def draw_redraw_real_country_sizes(instance, value):
    cd.s2.scale = .43
    cd.s2.pos = (
        sizes.start_s2_pos_x * 2 + sizes.width_res * cd.frontend.lp.table.size_hint_x,
        sizes.height_res / 20)
    print("draw real sizes")
    draw_for_epidemy.redraw_undraw_real_sizes()
    cd.stats.save_to_file()


def finish_all(instance):
    cd.mg.was_playing_before = True
    cd.stats.save_to_file()
    widget_of_common_par.info_message(
        ["До встречи в новой игре!", "Goodbye for next game!"][common_var.lang], 'good', t=1.5)
    Clock.schedule_once(cd.close_game, 0.7)


def increase_money(instance):
    gold_transaction.create_gold_menu()


def operate_unlocked_methods(instance, value):
    cd.stats.are_shown_unlocked_methods = not cd.stats.are_shown_unlocked_methods
    cd.stats.save_to_file()
    for j in range(common_var.QUANT_OF_TECH):
        i = common_var.tech_order[j]
        init_of_tech.init_tech_card(i)


def redraw(instance):
    cd.s2.scale = .5
    cd.s2.pos = (
        sizes.start_s2_pos_x + sizes.width_res * cd.frontend.lp.table.size_hint_x, 0)
    mes = ["Карта страны в центральном положении", "Country map is centered"]
    widget_of_common_par.info_message(mes[common_var.lang], 'good', 3)


# common seets are for game
common_nast = ScrollView(pos=(sizes.width_res * 0.08, sizes.height_res * 0.05), size_hint=(.84, .9), do_scroll_x=False,
                         bar_color=[.35, .35, .25, 1], bar_width=15, scroll_type=['bars', 'content'])
nast = AdditionalMenu(size_hint=(.9, None), pos=(sizes.width_res * 0.9, sizes.height_res * 0.1))
nast.bind(minimum_height=nast.setter('height'))
common_nast.add_widget(nast)
