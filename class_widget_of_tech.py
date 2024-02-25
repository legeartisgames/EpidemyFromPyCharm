import common_data as cd
import common_func
import common_var

import frases
import icon_func
import sizes
import spec_func
import tech_info
import text_for_tech_generator
import tech_sm
import uix_classes
import widget_of_common_par

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class SpecialLabel(uix_classes.WrappedLabel, Widget):
    def __init__(self, method_id, **kwargs):
        super(SpecialLabel, self).__init__(**kwargs)
        self.method_id = method_id
        self.update_text()
        common_var.list_of_btns.append(self)

    def update_text(self, do_generate=False):
        if do_generate:
            text_for_tech_generator.generate_texts_for_tech()
        self.text_source = [text_for_tech_generator.texts_of_tech[self.method_id][0],
                            text_for_tech_generator.texts_of_tech[self.method_id][1]]
        self.text_source = [
            icon_func.letter_to_icons_increasing_size(size=tech_name_font_size, coef=1.6, string=self.text_source[0]),
            icon_func.letter_to_icons_increasing_size(size=tech_name_font_size, coef=1.6, string=self.text_source[1])]

        self.text = self.text_source[common_var.lang]


tech_name_font_size = round(21 / 45 * 0.013 * sizes.width_res * common_var.tech_cols_num)
tech_btn_font_size = round(13 / 45 * 0.013 * sizes.width_res * common_var.tech_cols_num)


class TechnoWidget(FloatLayout):
    def __init__(self, method_id, **kwargs):
        super(TechnoWidget, self).__init__(**kwargs)
        self.real_init(method_id)

    def reinit(self):
        self.canvas.before.remove(self.rect_wid)
        self.canvas.before.remove(self.rect_wid_card)
        self.clear_widgets()
        self.real_init(self.method_id)

    def real_init(self, method_id):
        self.method_id = method_id
        i = self.method_id
        if cd.stats.goldreserves >= tech_info.min_goldreserves_for_tech[i] and \
                cd.stats.stars >= tech_info.min_stars_for_tech[i]:
            self.is_available = True
        else:
            self.is_available = False
        if cd.mg.My_mode.index == 5:  # режим "с нуля"
            if self.method_id in {10, 11, 26}:
                self.is_available = True
            else:
                self.is_available = 'no in mode lack of methods'

        if cd.mg.techs_avail_bool[self.method_id] is None:
            cd.mg.techs_avail_bool[self.method_id] = self.is_available
        else:
            self.is_available = cd.mg.techs_avail_bool[self.method_id]

        if self.method_id == 0:
            text_for_tech_generator.generate_texts_for_tech()

        self.rect_wid_card = None
        self.rect_wid = None

        self.pm_buttons = [None, None]
        self.str_of_input_for_tech = [''] * common_var.QUANT_OF_TECH
        # для активации технологии за монетки, первый элемент - вывеска,
        # второй - окно ввода, третий - кнопка применения эффекта
        for i in range(common_var.QUANT_OF_TECH):
            self.str_of_input_for_tech[i] = [0, 0, 0]
        tech_name = tech_info.names_of_tech[self.method_id]
        if cd.mg.My_Country.index == 12 and self.method_id == 3:  # if Germany
            tech_name = ["Респираторы", "Respirators"]
        tech_name_font_markup = ['[font=fonts/Tahoma.ttf]', '[font=fonts/MuseoSlab.ttf]']
        self.method_name_label = \
            uix_classes.WrappedLabel_with_tr(text_source=[
                '[b]' + '[size=' + str(tech_name_font_size) + ']' + tech_name_font_markup[common_var.lang] + tech_name[
                    0] + '[/font]' + '[/b]' + '\n' + '[/size]',
                '[b]' + '[size=' + str(tech_name_font_size) + ']' + tech_name_font_markup[common_var.lang] + tech_name[
                    1] + '[/font]' + '[/b]' + '\n' + '[/size]'],
                font_size=int(
                    1.2 * 0.013 * sizes.width_res * 3 / common_var.tech_cols_num),
                pos_hint={'center_x': .5, 'center_y': .87},
                valign='center', halign='center', size_hint_x=.75,
                markup=True, color=[1, 1, 1, 1])
        self.add_widget(self.method_name_label)

        font_size = int(1.2 * 0.013 * sizes.width_res * 3 / common_var.tech_cols_num)

        if not self.is_available:
            i = self.method_id
            tags_text = ['[i]Теги метода[/i]: ', '[i]Tags[/i]: ']
            for j in range(len(tech_info.tech_tags[i])):
                if j != 0:
                    tags_text[0] += ', '
                    tags_text[1] += ', '
                tags_text[0] += tech_info.tech_tags[i][j][0]
                tags_text[1] += tech_info.tech_tags[i][j][1]

            self.label_of_tags = uix_classes.WrappedLabel(size_hint=(.9, None),
                                                          font_size=font_size,
                                                          pos_hint={'center_x': .5, 'top': .55}, valign='top',
                                                          halign='center',
                                                          markup=True, color=[1, 1, 1, 1],
                                                          text=tags_text[common_var.lang])
            self.label_of_tags.text_source = tags_text

            common_var.list_of_btns.append(self.label_of_tags)
            self.add_widget(self.label_of_tags)

            resource_need = '?'
            quant_need = '?'
            if cd.stats.goldreserves < tech_info.min_goldreserves_for_tech[i]:
                resource_need = 'coins'
                quant_need = round(-cd.stats.goldreserves + tech_info.min_goldreserves_for_tech[i])
            if cd.stats.stars < tech_info.min_stars_for_tech[i]:
                resource_need = 'stars'
                quant_need = round(-cd.stats.stars + tech_info.min_stars_for_tech[i], 1)

            if quant_need != '?':
                text_s = ['[i]До получения[/i] ещё ' + str(quant_need) + ' ' + resource_need,
                          '[i]Need[/i] extra ' + str(quant_need) + ' ' + resource_need]

                text_s[0] = icon_func.letter_to_icons_increasing_size(size=sizes.width_res / 53, coef=1.6,
                                                                      string=text_s[0])
                text_s[1] = icon_func.letter_to_icons_increasing_size(size=sizes.width_res / 53, coef=1.6,
                                                                      string=text_s[1])

            else:
                text_s = ["В следующей партии этот метод будет разблокирован",
                          "This method will be unlocked in the next game"]
            self.label_need = uix_classes.WrappedLabel(size_hint=(.9, None),
                                                       font_size=font_size,
                                                       pos_hint={'center_x': .5, 'top': .85}, valign='top',
                                                       halign='center',
                                                       markup=True, color=[1, 1, 1, 1], text=text_s[common_var.lang])
            self.label_need.text_source = text_s

            if quant_need == '?':
                self.label_need.pos_hint = {'center_x': .5, 'top': .8}

            common_var.list_of_btns.append(self.label_need)
            self.add_widget(self.label_need)

            return

        self.label_of_tech = SpecialLabel(size_hint=(.9, None),
                                          font_size=font_size,
                                          pos_hint={'center_x': .5, 'top': .83}, valign='top', halign='center',
                                          markup=True, color=[1, 1, 1, 1],
                                          method_id=self.method_id)

        self.label_of_tech.outline_color = (1, 1, 0, 1)

        self.add_widget(self.label_of_tech)

        self.button_buy = uix_classes.Button_asfalt(
            text_source=frases.str_get_tech,
            size_hint=(.4, .12),
            pos_hint={'right': 0.95, 'top': 0.145},
            on_press=self.Multiply_on_parameter,
            font_size=tech_btn_font_size)

        if tech_info.type_of_get[self.method_id] == 1:
            self.button_buy.text = frases.str_research_tech[common_var.lang]
            self.button_buy.text_source = frases.str_research_tech
            self.button_buy.pos_hint = {'right': 0.98, 'top': 0.17}
            self.button_buy.size_hint = (.4, .15)

        if self.method_id in {0, 1, 2, 28, 31}:
            self.button_buy.text_source = frases.str_proinvest
            self.button_buy.text = self.button_buy.text_source[common_var.lang]
            if common_var.lang == 0:
                self.button_buy.size_hint = (.5, .15)
                self.button_buy.pos_hint = {'right': 0.98, 'top': 0.17}
            else:
                self.button_buy.size_hint = (.4, .12)
                self.button_buy.pos_hint = {'right': 0.96, 'top': 0.14}
            self.button_buy.halign = 'center'

        self.add_widget(self.button_buy)

        if tech_info.possible_of_activation[self.method_id] and \
                cd.mg.is_activated[self.method_id] is not True:

            self.button_of_activation = uix_classes.Button_asfalt(
                text_source=frases.str_activate_tech,
                size_hint=(.42, .15),
                pos_hint={'right': 0.44, 'top': 0.17},
                on_press=self.Activate_Deactivate,
                halign='center',
                font_size=tech_btn_font_size)

        elif tech_info.possible_of_activation[self.method_id] and cd.mg.is_activated[self.method_id]:
            self.button_of_activation = uix_classes.Button_asfalt(
                text_source=frases.str_deactivate_tech,
                size_hint=(.42, .15),
                pos_hint={'right': 0.44, 'top': 0.17},
                on_press=self.Activate_Deactivate,
                halign='center',
                font_size=tech_btn_font_size)

        if tech_info.quant_of_buys[self.method_id][0] != -1 \
                and cd.mg.counter_of_buys[self.method_id][0] >= 1:
            self.set_btn_to_researched()

        if ((tech_info.quant_of_buys[self.method_id][0] >
             cd.mg.counter_of_buys[self.method_id][0] or
             tech_info.quant_of_buys[self.method_id][0] <= -1) and
            cd.mg.counter_of_buys[self.method_id][0] > 0) \
                or cd.mg.counter_of_buys[self.method_id][1] > 0:
            self.set_done_x_times()

        if tech_info.possible_of_activation[self.method_id] == True and \
                cd.mg.counter_of_buys[self.method_id][0] > 0:
            self.add_widget(self.button_of_activation)

        self.spec_methods_button_preparing()

    def Activate_Deactivate(self, instance, do_notify=True):
        if cd.mg.is_activated[self.method_id]:
            par = cd.mg.parameters_of_tech[self.method_id]
            answer = ["0"] * 4
            answer[0] = par[0]
            answer[1] = par[1]
            if type(par[2][0]) == float or type(par[2][0]) == int:
                if par[2][1] == "*":
                    answer[2] = [1 / par[2][0], "*"]
                elif par[2][1] == "+":
                    answer[2] = [-par[2][0], "+"]
            else:
                answer[2] = []
                for i in range(len(par[2])):
                    if par[2][i][1] == "*":
                        answer[2].append([1 / par[2][i][0], "*"])
                    elif par[2][i][1] == "+":
                        answer[2].append([-par[2][i][0], "+"])
            answer[3] = [-par[3][0], "+"]
            common_func.Mult_on_par(answer, self.method_id, do_notify=do_notify)
            self.button_of_activation.text_source = frases.str_activate_tech
            cd.mg.is_activated[self.method_id] = False
            self.button_of_activation.text = frases.str_activate_tech[common_var.lang]

        else:
            common_func.Mult_on_par(cd.mg.parameters_of_tech[self.method_id],
                                    self.method_id, do_notify=do_notify)
            cd.mg.is_activated[self.method_id] = True
            self.button_of_activation.text_source = frases.str_deactivate_tech

            self.button_of_activation.text = frases.str_deactivate_tech[common_var.lang]

    def Multiply_on_parameter(self, instance, do_notify=True):
        global tech_btn_font_size

        if cd.mg.pars.coins + cd.mg.prices_of_tech[self.method_id][
            0] >= 0:  # if we have enough money
            was_counter_of_buys = cd.mg.counter_of_buys[self.method_id][0]

            cd.mg.counter_of_buys[self.method_id][0] += 1

            cd.mg.pars.coins += (cd.mg.prices_of_tech[self.method_id][0])
            cd.frontend.pars.labels.cash_label.text = icon_func.add_money_icon(
                string=str(cd.mg.pars.coins),
                size=cd.frontend.pars.labels.cash_label.font_size)

            if self.method_id == 4:  # delay of airlines
                cd.mg.parameters_of_tech[4][1] = cd.mg.index_of_capital

            if self.method_id == 9:  # science communication
                # update of skidka to vakzine and cure
                x = cd.mg.prices_of_tech[10][0]
                coef = cd.mg.parameters_of_tech[9][2][1][0]
                cd.mg.prices_of_tech[10][0] = round(cd.mg.prices_of_tech[10][0] * coef)

                x = cd.mg.prices_of_tech[11][0]
                cd.mg.prices_of_tech[11][0] = round(cd.mg.prices_of_tech[11][0] * coef)
                text_for_tech_generator.generate_texts_for_tech()
                cd.frontend.wid[10].label_of_tech.update_text()
                cd.frontend.wid[11].label_of_tech.update_text()

            if (self.method_id in {6, 7, 8, 10, 18, 21, 22, 24, 25}) and was_counter_of_buys == 0:

                if cd.mg.list_of_tech_tr[0][0] == "Пока нет методов\nдля региона":
                    del cd.mg.list_of_tech_tr[0]  # for spinner of technologies
                name = tech_info.names_of_tech[self.method_id]
                if self.method_id == 10:
                    name = ["Вакцинация", "Vaccination"]
                cd.mg.str_of_probably_activating_tech = name

                cd.mg.list_of_tech_tr.append(name)
                print("New region method was gotten")

            elif self.method_id in {15, 16, 17, 26}:  # coin emission or goscompany
                print("New economical tech was gotten")
            else:
                common_func.Mult_on_par(cd.mg.parameters_of_tech[self.method_id],
                                        self.method_id)

            if self.method_id == 2:  # для инвестиций в науку
                for i in range(common_var.QUANT_OF_TECH):
                    if tech_info.quant_of_buys[i][0] > 0 and cd.mg.counter_of_buys[i][0] < \
                            tech_info.quant_of_buys[i][0]:  # if did't buy, and it isn't investition
                        # we make skidka for tech

                        if i == 10 or i == 11:

                            cd.mg.prices_of_tech[i][0] += 5 * cd.mg.coef_skidka_na_tech
                        else:
                            cd.mg.prices_of_tech[i][0] += cd.mg.coef_skidka_na_tech
                        if cd.mg.prices_of_tech[i][
                            0] > 0:  # цена всегда меньше 0, т.к. число монет при покупке падает
                            cd.mg.prices_of_tech[i][0] = 0

                text_for_tech_generator.generate_texts_for_tech()

                for i in range(common_var.QUANT_OF_TECH):
                    cd.frontend.wid[i].label_of_tech.update_text()

            if tech_info.possible_of_activation[self.method_id]:  # if tech can be activated
                self.set_btn_activate()

            if self.method_id == 12:
                if cd.mg.pars.date[1] in {6, 7, 8}:  # if summer and researched distant
                    self.Activate_Deactivate(instance=3, do_notify=False)
                    cd.frontend.wid[12].label_summer = cd.uix_classes.Label_with_tr(
                        text_source=['Лето!', 'Summer'],
                        font_size=cd.frontend.wid[12].button_of_activation.font_size * 1.2,
                        pos_hint={'right': 0.44, 'top': 0.18},
                        size_hint=cd.frontend.wid[12].button_of_activation.size_hint,
                        color=[52 / 256, 235 / 256, 158 / 256, 1], bold=True)
                    cd.frontend.wid[12].add_widget(cd.frontend.wid[12].label_summer)

                    if cd.frontend.wid[12].button_of_activation in cd.frontend.wid[12].children:
                        cd.frontend.wid[12].remove_widget(cd.frontend.wid[12].button_of_activation)

            if tech_info.quant_of_buys[self.method_id][0] == \
                    cd.mg.counter_of_buys[self.method_id][0]:  # if tech is researched
                self.set_btn_to_researched()

            elif tech_info.quant_of_buys[self.method_id][0] > \
                    cd.mg.counter_of_buys[self.method_id][0] or \
                    tech_info.quant_of_buys[self.method_id][0] <= -1:

                self.set_done_x_times()

                if self.method_id == 0:
                    cd.mg.prices_of_tech[self.method_id][0] -= 5
                else:
                    cd.mg.prices_of_tech[self.method_id][0] -= 1

                self.label_of_tech.update_text(do_generate=True)
                if self.method_id == 1:  # for bolnitsy

                    cd.mg.parameters_of_tech[1][2][0][0] += (1 -
                                                             cd.mg.parameters_of_tech[1][2][
                                                                 0][0]) * 0.25
                    cd.mg.parameters_of_tech[1][2][1][0] += (1 -
                                                             cd.mg.parameters_of_tech[1][2][
                                                                 1][0]) * 0.25
                    text_for_tech_generator.generate_texts_for_tech()
                    cd.frontend.wid[1].label_of_tech.update_text()
        elif do_notify:
            widget_of_common_par.info_message(["У Вас не хватает денег\nна данное действие",
                                              "You haven't enough\nmoney for this action"][common_var.lang],
                                             'no money', 2)

    def make_paid_option(self, instance):
        ind = -1
        if self.method_id in {6, 7, 8, 10, 18, 21, 22, 24, 25}:
            ind = int(self.str_of_input_for_tech[1].text)
            cd.mg.parameters_of_tech[self.method_id][1] = ind

        if cd.mg.prices_of_tech[self.method_id][1] >= -1 or ind == -1:
            skidka = 0
        else:
            skidka = cd.mg.pars.reg_automatisated[ind] * \
                     cd.mg.parameters_of_tech[22][2][0]

        if cd.mg.pars.coins + skidka + \
                cd.mg.prices_of_tech[self.method_id][
                    1] >= 0:  # if we have enough money for paid option

            cd.mg.pars.coins += cd.mg.prices_of_tech[self.method_id][
                                    1] + skidka

            cd.frontend.pars.labels.cash_label.text = icon_func.add_money_icon(
                string=str(cd.mg.pars.coins),
                size=cd.frontend.pars.labels.cash_label.font_size)

            if self.method_id in {15, 16, 17, 26}:
                cd.mg.counter_of_buys[self.method_id][1] += 1
                self.set_done_x_times()
            common_func.Mult_on_par(cd.mg.parameters_of_tech[self.method_id],
                                    self.method_id)
        else:
            if common_var.lang == 0:
                widget_of_common_par.info_message("У Вас не хватает денег\nна данное действие", 'no money', 2)
            elif common_var.lang == 1:
                widget_of_common_par.info_message("You haven't enough\nmoney for this action", 'no money', 2)

    def set_done_x_times(self):
        str_done_ending = ' '
        times = cd.mg.counter_of_buys[self.method_id][
            tech_info.what_counting[self.method_id]]
        if 1 < times % 10 < 5 and times > 20:
            str_done_ending = 'а'
        elif 1 < times < 5:
            str_done_ending = 'а'
        max_d = ['', '']
        if cd.mg.quant_of_buys[self.method_id][1] != None:
            max_d = [' из ' + str(cd.mg.quant_of_buys[self.method_id][1]),
                     ' of ' + str(cd.mg.quant_of_buys[self.method_id][1])]

        mes = ['Уже применено\n' + str(times) + ' раз' + str_done_ending + max_d[0],
               'Already done\n' + str(times) + ' time' + 's' * (times > 1) + max_d[1]]

        if not hasattr(self, 'btn_already_done_x_times'):
            self.btn_already_done_x_times = uix_classes.WrappedLabel_with_tr(text_source=mes,
                                                                             size_hint=(.3, None),
                                                                             font_size=int(
                                                                                 0.011 * sizes.width_res * 3 / common_var.tech_cols_num),
                                                                             pos_hint={'center_x': .2, 'top': .15},
                                                                             valign='top', halign='center'
                                                                             )
            self.add_widget(self.btn_already_done_x_times)
            if self.method_id in {15, 16, 17, 26}:  # emission or govcompany
                self.remove_widget(self.button_buy)
        else:
            self.btn_already_done_x_times.text_source = mes
            self.btn_already_done_x_times.text = mes[common_var.lang]

        if cd.mg.quant_of_buys[self.method_id][1] is not None \
                and self.method_id in {16} \
                and cd.mg.quant_of_buys[self.method_id][1] <= \
                cd.mg.counter_of_buys[self.method_id][1]:
            self.remove_widget(self.button_make)
            self.button_make = uix_classes.WrappedLabel_with_tr(
                text_source=["Метод исчерпан", "Method is used"],
                size_hint=(.4, .13),
                pos_hint={'right': 0.98, 'top': 0.17},
                on_press=self.make_paid_option,
                font_size=tech_btn_font_size,
                color=[66 / 256, 245 / 256, 188 / 256, 1], bold=False)
            self.add_widget(self.button_make)

    def set_btn_activate(self):
        self.add_widget(self.button_of_activation)
        self.button_of_activation.text_source = frases.str_deactivate_tech
        self.button_of_activation.text = self.button_of_activation.text_source[common_var.lang]
        cd.mg.is_activated[self.method_id] = True

    def set_btn_to_researched(self):
        self.remove_widget(self.button_buy)
        if tech_info.type_of_get[self.method_id] == 1:
            button_buy_text_source = frases.str_researched
        if tech_info.type_of_get[self.method_id] == 2:
            button_buy_text_source = frases.str_gotten_tech

        self.button_buy = uix_classes.Label_with_tr(
            text_source=button_buy_text_source,
            size_hint=(.25, .1),
            pos_hint={'right': 0.9, 'top': 0.15},
            font_size=tech_btn_font_size
        )

        self.add_widget(self.button_buy)

        if self.method_id in {6, 7, 8, 10, 18, 21, 22, 24, 25}:  # if we can use tech for region
            self.button_buy.pos_hint = {'right': 0.9, 'top': 0.11}
            self.remove_widget(self.button_buy)
            level_of_btn_for_pay = 0.08

            self.str_of_input_for_tech[1] = TextInput(
                text="0",
                size_hint=(.115, .08),
                # height = sizes.height_res/23,
                pos_hint={'right': 0.458, 'center_y': level_of_btn_for_pay},
                readonly=True, halign="center",
                font_size=int(tech_btn_font_size * 1.3)
            )

            self.pm_buttons[0] = Button(
                text="-", font_size=tech_btn_font_size * 1.5,
                size_hint=(.12, .08), valign='center', halign='center', bold=True,
                pos_hint={'right': 0.35, 'center_y': level_of_btn_for_pay},
                on_press=lambda *args: widget_of_common_par.change_input(-1, self.str_of_input_for_tech[1],
                                                                         cd.mg.n - 1, *args)
            )

            self.pm_buttons[1] = Button(
                text="+", font_size=tech_btn_font_size * 1.5,
                size_hint=(.12, .08), valign='center', halign='center', bold=True,
                pos_hint={'right': 0.575, 'center_y': level_of_btn_for_pay},
                on_press=lambda *args: widget_of_common_par.change_input(+1, self.str_of_input_for_tech[1],
                                                                         cd.mg.n - 1, *args)
            )
            self.add_widget(self.pm_buttons[0])
            self.add_widget(self.pm_buttons[1])

            self.str_of_input_for_tech[0] = uix_classes.Label_with_tr(
                text_source=["Введите\nномер\nрегиона", "Enter\nregion\nindex"],
                size_hint=(.35, .15),
                pos_hint={'right': 0.30, 'center_y': level_of_btn_for_pay},
                font_size=tech_btn_font_size
            )

            enter_ts = ["Применить!", "Apply!"]
            enter_sh = [.35, .09]
            enter_ph = .95

            if self.method_id == 10:
                enter_ts = ["Вакцинировать!", "Vaccinise!"]
                enter_sh = [.393, .105]
                enter_ph = .98

            self.str_of_input_for_tech[2] = uix_classes.Button_asfalt(
                text_source=enter_ts,
                size_hint=enter_sh,
                pos_hint={'right': enter_ph, 'center_y': level_of_btn_for_pay},
                on_press=self.make_paid_option,
                font_size=tech_btn_font_size
            )

            self.add_widget(self.str_of_input_for_tech[0])
            self.add_widget(self.str_of_input_for_tech[1])
            self.add_widget(self.str_of_input_for_tech[2])

            if self.method_id == 10:
                self.btn_make_vaccine = uix_classes.Button_asfalt(
                    text_source=["Произвести дозы!", "Make doses!"],
                    size_hint=(.47, .105),
                    pos_hint={'center_x': 0.5, 'top': 0.28},
                    on_press=common_func.make_new_vac_dozes,
                    font_size=tech_btn_font_size
                )

                self.add_widget(self.btn_make_vaccine)

        if self.method_id in {15, 16, 17, 26}:  # coin emission or goscompany
            self.button_make = uix_classes.Button_asfalt(
                text_source=["Применить!", "Make!"],
                size_hint=(.4, .13),
                pos_hint={'right': 0.98, 'top': 0.17},
                on_press=self.make_paid_option,
                font_size=tech_btn_font_size)

            self.add_widget(self.button_make)
            self.button_buy.pos_hint = {'center_x': .2, 'top': .15}

    def on_touch_up(self, touch):  # can go to viewer mode
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                if hasattr(self, "button_buy"):
                    if self.button_buy.collide_point(touch.pos[0], touch.pos[1]):
                        return
                if hasattr(self, "str_of_input_for_tech"):
                    if hasattr(self.str_of_input_for_tech[2], "collide_point"):
                        if self.str_of_input_for_tech[2].collide_point(touch.pos[0], touch.pos[1]):
                            return
                        if self.pm_buttons[0].collide_point(touch.pos[0], touch.pos[1]):
                            return
                        if self.pm_buttons[1].collide_point(touch.pos[0], touch.pos[1]):
                            return
                if hasattr(self, "button_of_activation"):
                    if self.button_of_activation.collide_point(touch.pos[0], touch.pos[1]):
                        return
                if hasattr(self, "btn_make_vaccine"):
                    if self.btn_make_vaccine.collide_point(touch.pos[0], touch.pos[1]):
                        return
                if cd.frontend.tech_panel_mode == "panel":
                    tech_sm.TechViewer().open_self(ind_tech=self.method_id, instance=0)
                    return
                if cd.frontend.tech_panel_mode == "viewer":
                    tech_sm.tech_viewer.close_self(instance=5)

    def spec_methods_button_preparing(self):
        if self.method_id == 12 and cd.mg.counter_of_buys[12][0] > 0:  # if distant
            print("SUMMER")
            if cd.mg.pars.date[1] in {6, 7,
                                      8} and self.button_of_activation in self.children:
                # if summer and researched distant

                self.label_summer = cd.uix_classes.Label_with_tr(text_source=['Лето!', 'Summer'],
                                                                 font_size=self.button_of_activation.font_size * 1.2,
                                                                 pos_hint={'right': 0.44, 'top': 0.18},
                                                                 size_hint=self.button_of_activation.size_hint,
                                                                 color=[52 / 256, 235 / 256, 158 / 256, 1],
                                                                 bold=True)
                self.add_widget(self.label_summer)

                self.remove_widget(self.button_of_activation)

                if cd.mg.is_activated[12]:
                    self.Activate_Deactivate(instance=5)

                    cd.my_game_game.must_be_activated_distant = True
        if self.method_id == 28 and cd.mg.was_purchased_in_this_month[28] == True:
            self.label_using_now = cd.uix_classes.Label_with_tr(text_source=['Исследования\nуже ведутся!',
                                                                             'Researches\nare conducting!'],
                                                                font_size=self.button_buy.font_size,
                                                                pos_hint=self.button_buy.pos_hint,
                                                                size_hint=self.button_buy.size_hint,
                                                                color=[52 / 256, 235 / 256, 158 / 256, 1],
                                                                bold=True, halign='center')
            self.add_widget(self.label_using_now)

            self.remove_widget(self.button_buy)
        if self.method_id == 31 and cd.mg.was_purchased_in_this_month[31]:
            self.label_using_now = cd.uix_classes.Label_with_tr(text_source=['Оздоровление\nудалось!',
                                                                             'We are now\nhealthier!'],
                                                                font_size=self.button_buy.font_size,
                                                                pos_hint=self.button_buy.pos_hint,
                                                                size_hint=self.button_buy.size_hint,
                                                                color=[32 / 256, 187 / 256, 214 / 256, 1],
                                                                bold=True, halign='center')
            self.add_widget(self.label_using_now)

            self.remove_widget(self.button_buy)

    def update_rect(self, instance, value):
        self.rect_wid_card.pos = self.pos
        self.rect_wid_card.size = self.size
        self.rect_wid.pos = self.pos
        self.rect_wid.size = self.size
