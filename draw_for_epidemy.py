import common_data as cd
import frases
import icon_func
import regions_menu
import sizes
import spec_func
import textures
import uix_classes

from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.label import Label

# система кодировки такая: первая координата по горизонатли,
# вторая по вертикали (причём 1;0 ниже чем 0;0) Начинаем слева сверху
# Приведённая схема верна для России

# start_point_y = 6 #чтобы координаты для y меньше нуля также были бы определены

coords_of_hexes = []
coords_of_centers = []


class CountryWidget(Widget):
    def __init__(self, **kwargs):
        super(CountryWidget, self).__init__(**kwargs)
        global side, height, x_start, y_start
        side = min(1.87 * (1 - .28) * sizes.width_res * (1 - 0.07 * cd.stats.sizes_ruler_on) / (
            cd.mg.My_Country.sizes[0]),
                   1.87 * sizes.height_res * (1 - 0.09 * cd.stats.sizes_ruler_on) / (
                           cd.mg.My_Country.sizes[1] * 1.732))
        height = side * 1.732

        with self.canvas:
            Color(0.5, 0.5, 0.5, 0.3)
            Color(0.6, 0.8, 0.5, 1)

            sizes.SIZE_OF_TEXT_FOR_LABEL = round(height * 0.16 / 50 * 17.5)
            dx = ((1 - .28) * sizes.width_res * 2 - cd.mg.My_Country.sizes[
                0] * side) / 2  # .28 is size_hint of left table, *1.8 is because of s2 scale

        x_start = side * 0.05 + 0.05 * cd.stats.sizes_ruler_on * sizes.width_res + dx
        y_start = (
                          1.9 - 0.09 * cd.stats.sizes_ruler_on) * sizes.height_res - cd.mg.My_Country.dy * height
        draw_country(x_start, y_start, side, height)


def define_hex_of_point(x, y):
    global coords_of_centers, side, height
    optim_hex = 0
    min_dist2 = (x - coords_of_centers[0][0]) ** 2 + (y - coords_of_centers[0][1]) ** 2
    for i in range(1, cd.mg.My_Country.number_of_regions):
        dist = (x - coords_of_centers[i][0]) ** 2 + (y - coords_of_centers[i][1]) ** 2

        if dist < min_dist2:
            optim_hex = i
            min_dist2 = dist
    xc = coords_of_centers[optim_hex][0]
    yc = coords_of_centers[optim_hex][1]
    is_hit = True
    # дальше идёт проверка на то, что точка лежит внутри гекса
    # левая нижняя прямая
    x1 = xc - side
    y1 = yc
    x2 = xc - side / 2
    y2 = yc - height / 2
    y_theor = (x - x1) * (y2 - y1) / (x2 - x1) + y1
    if y < y_theor:
        is_hit = False

    # левая верхняя прямая
    x1 = xc - side
    y1 = yc
    x2 = xc - side / 2
    y2 = yc + height / 2
    y_theor = (x - x1) * (y2 - y1) / (x2 - x1) + y1
    if y > y_theor:
        is_hit = False

    if y > yc + height / 2:
        is_hit = False
    # правая верхняя прямая
    x1 = xc + side
    y1 = yc
    x2 = xc + side / 2
    y2 = yc + height / 2
    y_theor = (x - x1) * (y2 - y1) / (x2 - x1) + y1
    if y > y_theor:
        is_hit = False
    # правая нижняя прямая
    x1 = xc + side
    y1 = yc
    x2 = xc + side / 2
    y2 = yc - height / 2
    y_theor = (x - x1) * (y2 - y1) / (x2 - x1) + y1
    if y < y_theor:
        is_hit = False
    if y < yc - height / 2:
        is_hit = False
    return optim_hex, is_hit


def scatter_touch_multichoice(self, touch):
    xs = cd.s2.pos[0]
    ys = cd.s2.pos[1]

    x = (touch.pos[0] - xs) / cd.s2.scale
    y = (touch.pos[1] - ys) / cd.s2.scale

    optim_hex, is_hit = define_hex_of_point(x, y)
    if not is_hit:
        return

    if cd.mg.multichoice_list[optim_hex] == 0:
        cd.frontend.hexes_chosen[optim_hex].show_circle()
        cd.mg.list_of_chosen.append(optim_hex)
        cd.mg.multichoice_list[optim_hex] = 1
    else:
        cd.frontend.hexes_chosen[optim_hex].hide_circle()
        cd.mg.list_of_chosen.remove(optim_hex)
        cd.mg.multichoice_list[optim_hex] = 0


def on_scatter_move(self, touch):
    if self.collide_point(*touch.pos):
        global active_zone
        x = self.pos[0]
        y = self.pos[1]

        if x < (sizes.normal_s2_pos_x - active_zone[1][0] * self.scale):
            # print("надо тащить вправо")
            self.pos = (sizes.normal_s2_pos_x - active_zone[1][0] * self.scale, self.pos[1])
        if x > (sizes.width_res - active_zone[0][0] * self.scale):
            # print("надо тащить влево")
            self.pos = (sizes.width_res - active_zone[0][0] * self.scale, self.pos[1])

        if y < (-active_zone[1][1] * self.scale):
            # print("надо тащить вниз")
            self.pos = (self.pos[0], -active_zone[1][1] * self.scale)
        if y > (sizes.height_res - active_zone[0][1] * self.scale):
            # print("надо тащить вверх")
            self.pos = (self.pos[0], sizes.height_res - active_zone[0][1] * self.scale)


def on_scatter_touch_down(self, touch):
    if self.collide_point(*touch.pos):
        if cd.mg.multichoice_ind == 1:
            scatter_touch_multichoice(self, touch)
        if touch.is_double_tap:
            xs = cd.s2.pos[0]
            ys = cd.s2.pos[1]

            x = (touch.pos[0] - xs) / cd.s2.scale
            y = (touch.pos[1] - ys) / cd.s2.scale

            optim_hex, is_hit = define_hex_of_point(x, y)

            print(optim_hex, is_hit)
            if not is_hit:
                return

            cd.mg.is_chosen_only_one = optim_hex
            for i in range(cd.mg.n):
                cd.frontend.hexes_chosen[i].hide_circle()
            cd.frontend.hexes_chosen[optim_hex].show_circle()
            cd.mg.list_of_chosen = [optim_hex]
            cd.mg.multichoice_list = [0] * 21
            cd.mg.multichoice_list[optim_hex] = 1

            regions_menu.region_menu()
            cd.frontend.hexes_chosen[optim_hex].hide_circle()
            cd.mg.list_of_chosen = []
            cd.mg.multichoice_list = [0] * 21
            return True


def draw_hex(x, y, side, height, i):
    with cd.s2.canvas:
        Color(0.6, 0.8, 0.5, 1)
        points = (
            x, y, x - side / 2, y + height / 2, x, y + height, x + side, y + height, x + 3 / 2 * side, y + height / 2,
            x + side, y)
        # 22 к 15 соотношение размеров области карты страны
        if (cd.mg.My_Country.sizes[0] / cd.mg.My_Country.sizes[
            1] / 1.732 > 1.47):  # тогда нормируем на ширину страны
            coef_of_width = 8 / cd.mg.My_Country.sizes[0]
        else:
            coef_of_width = 3.5 / cd.mg.My_Country.sizes[1]

        Line(points=tuple(points), close=True,
             width=sizes.height_res / 120 * coef_of_width, joint='round')

        color_of_ti_r = (1, 1, 1, 1)
        color_of_text_input = (.07, .1, .1, 1)
        delta_y = side * 0.19
        delta_x = side * 0.06

        cd.frontend.carta_labels.z_in_label[i] = HexParLabel(text=icon_func.letters_to_icons("z_in"),
                                                                        size=(side / 3, height * 0.16), pos=(
                x - delta_x, y + height * 0.8 - delta_y), font_size=sizes.SIZE_OF_TEXT_FOR_LABEL * 2.5,
                                                                        index=i, color_r=(0.5, 0.3, 0.5, 0.3),
                                                                        parent='s2', markup=True,
                                                                        typ="z_in")

        cd.frontend.pars.labels.array_of_z_in[i] = HexParLabel(
            size=(side * 0.5 + delta_x, height * 0.16), pos=(x + side / 3 - delta_x * 0.75, y + height * 0.8 - delta_y),
            font_size=sizes.SIZE_OF_TEXT_FOR_LABEL,
            text=str(round(cd.mg.pars.z_ins[i] * cd.mg.pars.z_ins_dop[i], 3)),
            parent='s2',
            index=i, color_r=color_of_ti_r,
            color=(color_of_text_input[0], color_of_text_input[1], color_of_text_input[2], color_of_text_input[3]),
            typ="z_in")
        if abs(cd.mg.pars.z_ins_dop[i] - (
                cd.mg.My_population[i] - cd.mg.pars.immunated[i]) / (
                       cd.mg.My_population[i] + 1)) > 0.01:
            cd.frontend.pars.labels.array_of_z_in[i].color = [1, 0, 0, 1]

        cd.frontend.carta_labels.ill_label[i] = HexParLabel(text=icon_func.letters_to_icons("Ill"),
                                                                       parent='s2',
                                                                       size=(side / 3, height * 0.16), pos=(
                x - delta_x, y + height * 0.63 - delta_y), font_size=sizes.SIZE_OF_TEXT_FOR_LABEL * 2.5,
                                                                       index=i, color_r=(0.3, 0.3, 0.5, 0.3),
                                                                       markup=True,
                                                                       typ="ill")

        cd.frontend.pars.labels.array_of_ill[i] = HexParLabel(parent='s2', size=(
            side * 0.5 + delta_x, height * 0.16), pos=(x + side / 3 - delta_x * 0.75, y + height * 0.63 - delta_y),
                                                                              font_size=sizes.SIZE_OF_TEXT_FOR_LABEL,
                                                                              text=spec_func.tri_sep(
                                                                                  cd.mg.pars.ill_nums[
                                                                                      i]),
                                                                              index=i, color_r=color_of_ti_r,
                                                                              color=(color_of_text_input[0],
                                                                                     color_of_text_input[1],
                                                                                     color_of_text_input[2],
                                                                                     color_of_text_input[3]),
                                                                              typ="ill")

        if cd.mg.pars.reg_stats_distortion[i]:
            draw_reg_distortion(draw=True, reg_id=i)

        if cd.mg.pars.reg_automatisated[i]:
            draw_automation(draw=True, reg_id=i)

        cd.frontend.carta_labels.d_in_label[i] = HexParLabel(parent='s2',
                                                                        text=icon_func.letters_to_icons("d_in"),
                                                                        size=(side / 3, height * 0.16), pos=(
                x - delta_x, y + height * 0.46 - delta_y),
                                                                        font_size=sizes.SIZE_OF_TEXT_FOR_LABEL * 2.5,
                                                                        index=i, color_r=(0.8, 0.3, 0.5, 0.3),
                                                                        markup=True,
                                                                        typ="d_in")

        cd.frontend.pars.labels.array_of_d_in[i] = HexParLabel(parent='s2', size=(
            side * 0.5 + delta_x, height * 0.16),
                                                                               pos=(
                                                                                   x + side / 3 - delta_x * 0.75,
                                                                                   y + height * 0.46 - delta_y),
                                                                               font_size=sizes.SIZE_OF_TEXT_FOR_LABEL,
                                                                               text=str(
                                                                                   cd.mg.pars.d_ins[
                                                                                       i] *
                                                                                   cd.mg.pars.d_ins_dop[
                                                                                       i]),
                                                                               index=i, color_r=color_of_ti_r,
                                                                               color=(color_of_text_input[0],
                                                                                      color_of_text_input[1],
                                                                                      color_of_text_input[2],
                                                                                      color_of_text_input[3]),
                                                                               typ="d_in")

        if cd.mg.pars.d_ins_dop[i] != 1:
            cd.frontend.pars.labels.array_of_d_in[i].color = [1, 0, 0, 1]

        cd.frontend.carta_labels.dead_label[i] = HexParLabel(parent='s2',
                                                                        text=icon_func.letters_to_icons("Dead"),
                                                                        size=(side / 3, height * 0.16), pos=(
                x - delta_x, y + height * 0.29 - delta_y),
                                                                        font_size=sizes.SIZE_OF_TEXT_FOR_LABEL * 2.5,
                                                                        index=i, color_r=(1, 0.2, 0, 0.25),
                                                                        markup=True,
                                                                        typ="dead")
        cd.frontend.pars.labels.array_of_dead[i] = HexParLabel(parent='s2', size=(
            side * 0.5 + delta_x, height * 0.16), pos=(x + side / 3 - delta_x * 0.75, y + height * 0.29 - delta_y),
                                                                               font_size=sizes.SIZE_OF_TEXT_FOR_LABEL,
                                                                               text=spec_func.tri_sep(
                                                                                   cd.mg.pars.dead_nums[
                                                                                       i]),
                                                                               index=i, color_r=color_of_ti_r,
                                                                               color=(color_of_text_input[0],
                                                                                      color_of_text_input[1],
                                                                                      color_of_text_input[2],
                                                                                      color_of_text_input[3]),
                                                                               typ="dead")

        cd.s2.add_widget(cd.frontend.pars.labels.array_of_z_in[i])
        cd.s2.add_widget(cd.frontend.carta_labels.z_in_label[i])

        cd.s2.add_widget(cd.frontend.carta_labels.ill_label[i])
        cd.s2.add_widget(cd.frontend.pars.labels.array_of_ill[i])

        cd.s2.add_widget(cd.frontend.carta_labels.d_in_label[i])
        cd.s2.add_widget(cd.frontend.pars.labels.array_of_d_in[i])

        cd.s2.add_widget(cd.frontend.carta_labels.dead_label[i])
        cd.s2.add_widget(cd.frontend.pars.labels.array_of_dead[i])

        cd.frontend.hexes_chosen[i] = MultichoiceCircle((x + side * 0.9, y + height * 0.1),
                                                                   side / 30, i, parent='s2')

    cd.frontend.circles_situation_in_hexes[i][0] = CircleWidget(
        pos=(x + side * 0.95 + delta_x, y + height * 0.87 - delta_y), radius=side / 20, ind=i, ty=0, parent='s2')
    cd.frontend.circles_situation_in_hexes[i][1] = CircleWidget(
        pos=(x + side * 0.95 + delta_x, y + height * 0.70 - delta_y), radius=side / 20, ind=i, ty=1, parent='s2')
    cd.frontend.circles_situation_in_hexes[i][2] = CircleWidget(
        pos=(x + side * 0.95 + delta_x, y + height * 0.53 - delta_y), radius=side / 20, ind=i, ty=2, parent='s2')
    cd.frontend.circles_situation_in_hexes[i][3] = CircleWidget(
        pos=(x + side * 0.95 + delta_x, y + height * 0.36 - delta_y), radius=side / 20, ind=i, ty=3, parent='s2')
    cd.s2.add_widget(cd.frontend.circles_situation_in_hexes[i][0])
    cd.s2.add_widget(cd.frontend.circles_situation_in_hexes[i][1])
    cd.s2.add_widget(cd.frontend.circles_situation_in_hexes[i][2])
    cd.s2.add_widget(cd.frontend.circles_situation_in_hexes[i][3])
    with cd.s2.canvas:
        Color(0.3, 1, 1, 1)

    if i == cd.mg.index_of_capital:
        cd.frontend.carta_labels.capital_label = uix_classes.Label_with_tr(
            text_source=frases.str_capital, size=(side * 0.7, height / 4), pos=(x, y - side * 0.1),
            font_size=int(14 / 11 * sizes.SIZE_OF_TEXT_FOR_LABEL), bold=True)

    # cd.frontend.carta_labels.region = uix_classes.Label_with_tr(text_source = ["Регион",
    # "Region"], size = (side/3, height/7), pos = (x+side*0.3, y+height*0.85), font_size = round(
    # sizes.SIZE_OF_TEXT_FOR_LABEL)*1.2)
    name_font_size = round(sizes.SIZE_OF_TEXT_FOR_LABEL) * 1.2
    add_for_name = 0.3
    if len(cd.mg.My_Country.names_of_provinces[i][cd.common_var.lang]) >= 10:
        add_for_name = 0.28
        name_font_size -= 1
    if len(cd.mg.My_Country.names_of_provinces[i][cd.common_var.lang]) >= 12:
        add_for_name = 0.25
        name_font_size -= 1
    if len(cd.mg.My_Country.names_of_provinces[i][cd.common_var.lang]) >= 15:
        add_for_name = 0.24
    cd.frontend.carta_labels.region = uix_classes.Label_with_tr(
        text_source=cd.mg.My_Country.names_of_provinces[i], size=(side / 3, height / 7),
        pos=(x + side * add_for_name, y + height * 0.85),
        font_size=name_font_size)

    cd.s2.add_widget(cd.frontend.carta_labels.region)
    add_for_hash = 0.735
    if i < 10:
        add_for_hash = 0.75
    cd.frontend.carta_labels.number_of_region = Label(text="#" + str(i), size=(side / 3, height / 7),
                                                               pos=(x + side * add_for_hash, y + height * 0.85),
                                                               font_size=name_font_size)
    cd.s2.add_widget(cd.frontend.carta_labels.number_of_region)

    cd.frontend.pars.labels.str_of_naselenie[i] = Label(
        text=spec_func.tri_sep(cd.mg.My_population[i]), size=(side / 3, height / 7),
        pos=(x + side * 0.2, y + height * 0.05), font_size=sizes.SIZE_OF_TEXT_FOR_LABEL)

    if i == cd.mg.index_of_capital:
        cd.s2.add_widget(cd.frontend.carta_labels.capital_label)


def redraw_undraw_real_sizes():
    if cd.stats.sizes_ruler_on:
        cd.stats.sizes_ruler_on = False
        cd.s2.canvas.remove_group("real_sizes")
        cd.s2.remove_widget(cd.frontend.hor_ruler_label)
        cd.s2.canvas.remove(cd.frontend.hor_ruler_label.canvas)
        cd.s2.remove_widget(cd.frontend.vert_ruler_label)
    else:
        cd.stats.sizes_ruler_on = True

        with cd.s2.canvas:
            Color(38 / 256, 112 / 256, 110 / 256, 1)
            cd.s2.canvas.add(cd.s2.hor_ruler_line)
            cd.s2.canvas.add(cd.s2.ver_ruler_line)
        cd.s2.add_widget(cd.frontend.hor_ruler_label)
        cd.s2.add_widget(cd.frontend.vert_ruler_label)


def draw_ruler_on_map(x, y, side, height):
    with cd.s2.canvas:
        Color(r=38 / 256, g=112 / 256, b=110 / 256, a=1, group="real_sizes")
        global active_zone
        active_zone = [0, 0]
        active_zone[0] = (x - side * 0.7 + side,
                          y - cd.mg.My_Country.ups_by_y * height + height - height *
                          cd.mg.My_Country.sizes[1] + side / 2)
        active_zone[1] = (x - side / 2 + side * cd.mg.My_Country.sizes[0] - side,
                          y - cd.mg.My_Country.ups_by_y * height + 1.2 * height - side)

        cd.s2.hor_ruler_line = Line(points=(x - side / 2,
                                                     y - cd.mg.My_Country.ups_by_y * height + 1.2 * height,
                                                     x - side / 2 + side * cd.mg.My_Country.sizes[0],
                                                     y - cd.mg.My_Country.ups_by_y * height + 1.2 * height),
                                             width=5 * sizes.height_res / 1000,
                                             group="real_sizes")
        # ups< 0; 1 height из-за того, что хотим нарисовать сверху гекса

        Color(38 / 256, 112 / 256, 110 / 256, 1)
        cd.s2.ver_ruler_line = Line(points=(x - side * 0.7,
                                                     y - cd.mg.My_Country.ups_by_y * height + height,
                                                     x - side * 0.7,
                                                     y - cd.mg.My_Country.ups_by_y * height + height - height *
                                                     cd.mg.My_Country.sizes[1]),
                                             width=5 * sizes.height_res / 1000,
                                             group="real_sizes")
        # ups< 0; 1 height из-за того, что хотим нарисовать сверху гекса

    cd.frontend.hor_ruler_label = Label(pos=(
        cd.s2.hor_ruler_line.points[0],
        cd.s2.hor_ruler_line.points[1] + height * 0.05),
        size=(side * cd.mg.My_Country.sizes[0],
              sizes.height_res / 20),
        text=str(round(cd.mg.My_Country.sizes[
                           0] * cd.mg.My_Country.real_size_of_hex / 100) * 100) + " km",
        font_size=sizes.TEXT_SIZE_OF_COMMON_PAR * 1.25)

    cd.frontend.vert_ruler_label = Label(
        size=(side * 1.1, height * cd.mg.My_Country.sizes[1]),
        text=str(100 * round(height / side * cd.mg.My_Country.sizes[
            1] * cd.mg.My_Country.real_size_of_hex / 100)) + " km",
        font_size=sizes.TEXT_SIZE_OF_COMMON_PAR * 1.25, halign='right')
    cd.frontend.vert_ruler_label.pos = (
        cd.s2.ver_ruler_line.points[0] - cd.frontend.vert_ruler_label.size[0],
        cd.s2.ver_ruler_line.points[1] - cd.frontend.vert_ruler_label.size[1])
    if cd.stats.sizes_ruler_on:
        cd.s2.add_widget(cd.frontend.hor_ruler_label)
        cd.s2.add_widget(cd.frontend.vert_ruler_label)
    else:
        cd.s2.canvas.remove_group("real_sizes")


def draw_country(x, y, side, height):
    draw_ruler_on_map(x, y, side, height)  # we create it but not add to canvas if we are not asked
    global coords_of_hexes, coords_of_centers
    coords_of_hexes = [0] * cd.mg.My_Country.number_of_regions
    coords_of_centers = [0] * cd.mg.My_Country.number_of_regions
    with cd.s2.canvas:
        for i in range(cd.mg.n):
            coords_of_hexes[i] = [
                x + 3 / 2 * side * cd.mg.My_land[i][0] + cd.stats.sizes_ruler_on * 0.2 * side,
                y - (cd.mg.My_land[i][0] % 2) * height / 2 - cd.mg.My_land[i][
                    1] * height - cd.stats.sizes_ruler_on * 0.2 * side]
            draw_hex(coords_of_hexes[i][0], coords_of_hexes[i][1],
                     side, height, i)
            coords_of_centers[i] = [coords_of_hexes[i][0] + side / 2, coords_of_hexes[i][1] + height / 2]


class CircleWidget(Widget):
    def __init__(self, radius, ind, ty, parent='s2', **kwargs):
        super().__init__(**kwargs)

        self.index = ind
        self.ty = ty
        self.points = self.pos
        self.r = min(cd.mg.situation_in_hexes[self.index][self.ty], 1)
        self.g = 1 - min(cd.mg.situation_in_hexes[self.index][self.ty], 1)
        self.radius = radius

        self.l2 = None

        with self.canvas:
            Color(self.r, self.g, 0, 1)
            self.l = Line(circle=(self.points[0], self.points[1], self.radius), width=self.radius)
            if cd.mg.situation_in_hexes[self.index][self.ty] ** 2 >= 1 and (ty == 1 or ty == 3):
                Color(.5, 0, .8, 1)
                Line(circle=(self.points[0], self.points[1],
                             self.radius / 10 * cd.mg.situation_in_hexes[self.index][self.ty]),
                     width=self.radius / 10 * cd.mg.situation_in_hexes[self.index][self.ty])
        self.update_color()

    def update_color(self):
        self.canvas.remove(self.l)
        with self.canvas:
            Color(min(cd.mg.situation_in_hexes[self.index][self.ty], 1),
                  1 - min(cd.mg.situation_in_hexes[self.index][self.ty], 1), 0, 1)
            self.l = (Line(circle=(self.points[0], self.points[1], self.radius), width=self.radius))
            if self.l2 in self.canvas.children:
                self.canvas.remove(self.l2)

        if cd.mg.region_straphs[self.index][self.ty] >= 1 and self.ty in {1, 3}:
            if hasattr(self, "label_straph_b"):
                self.label_straph_b.text = str(cd.mg.region_straphs[self.index][self.ty])
                if self.label_straph_b not in self.children:
                    self.add_widget(self.label_straph_b)
                if (not cd.mg.pars.reg_stats_distortion[self.index]) \
                        and self.label_straph_b.color != (.5, 0, .8, 1):
                    self.label_straph_b.color = (.5, 0, .8, 1)
                elif cd.mg.pars.reg_stats_distortion[self.index]:
                    self.label_straph_b.color = (.2, 1, .2, 1)
            else:
                if not cd.mg.pars.reg_stats_distortion[self.index]:
                    color_straph = (.5, 0, .8, 1)
                else:
                    color_straph = (.2, 1, .2, 1)
                self.label_straph_b = Label(text=str(cd.mg.region_straphs[self.index][self.ty]),
                                            halign='left',
                                            pos=[self.pos[0] + self.radius * 1.7, self.pos[1] + self.radius * 1.9],
                                            size=(self.radius * 0.8, self.radius),
                                            font_size=15, color=color_straph)
                self.add_widget(self.label_straph_b)

            with self.canvas:
                Color(.5, 0, .8, 1)
                self.l2 = Line(circle=(self.points[0], self.points[1],
                                       min(self.radius / 8 * cd.mg.situation_in_hexes[self.index][
                                           self.ty], self.radius * 1.2)),
                               width=min(self.radius / 8 * cd.mg.situation_in_hexes[self.index][self.ty],
                                         self.radius * 1.2))

        elif self.ty == 1 or self.ty == 3:  # если надо удалять штрафную вывеску, т.к. штрафных баллов нет
            if hasattr(self, "label_straph_b"):
                if self.label_straph_b in self.children:
                    self.label_straph_b.canvas.clear()
                    del self.label_straph_b


class MultichoiceCircle(Line):
    def __init__(self, poi, radius, ind, parent='s', **kwargs):
        super(MultichoiceCircle).__init__(**kwargs)

        self.widget_parent = 0

        if parent == 's2':
            self.widget_parent = cd.s2
        self.index = ind
        self.points = poi
        self.b = 1
        self.radius = radius

        Color(0, 0, 0, 1)
        self.l = Line(circle=(self.points[0], self.points[1], self.radius), width=self.radius)
        if cd.mg.multichoice_list[self.index] == 1:
            self.show_circle()

    def show_circle(self):
        self.widget_parent.canvas.remove(self.l)
        with self.widget_parent.canvas:
            Color(0, 1, 1, 1)
            self.l = (Line(circle=(self.points[0], self.points[1], self.radius), width=self.radius))

    def hide_circle(self):
        self.widget_parent.canvas.remove(self.l)
        with self.widget_parent.canvas:
            Color(0, 0, 0, 1)
            self.l = (Line(circle=(self.points[0], self.points[1], self.radius), width=self.radius))


class HexParLabel(Label):
    def __init__(self, index, color_r, typ, parent='s', type_of_icon="none", **kwargs):
        super(HexParLabel, self).__init__(**kwargs)
        self.index = index  # number_of_region
        self.category = typ  # z_in, d_in, ill, dead
        self.widget_parent = 0

        if parent == 's2':
            self.widget_parent = cd.s2
        with self.widget_parent.canvas:
            Color(color_r[0], color_r[1], color_r[2], color_r[3])
            Rectangle(pos=self.pos, size=self.size, texture=textures.tex_ramka)

        self.was_touch = False
        self.start_plotting_clock = None

    def do_make_graph(self, dt):
        vec = [cd.s2.pos[0] - self.down_s2_pos[0],
               cd.s2.pos[1] - self.down_s2_pos[1]]

        if vec[0] ** 2 + vec[1] ** 2 < 1000:
            self.go_to_graph()

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.was_touch == True:
            if self.start_plotting_clock is not None:
                self.start_plotting_clock.cancel()
            else:
                print("Plotting clock is None")
            self.was_touch = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.was_touch = True
            self.down_s2_pos = tuple(cd.s2.pos)
            if cd.mg.multichoice_ind == -1 or self.category != "z_in":
                self.start_plotting_clock = Clock.schedule_once(self.do_make_graph, timeout=1.5)
            return super(HexParLabel, self).on_touch_down(touch)

    def go_to_graph(self):
        cd.mg.is_chosen_only_one = self.index
        regions_menu.graph_maker.make_graph(typ=self.category)


def draw_reg_isolation(x=0, y=0, side=100, height=100, draw=True):
    if draw:
        with cd.s2.canvas:
            points = (
                x, y, x - side / 2, y + height / 2, x, y + height, x + side, y + height, x + 3 / 2 * side,
                y + height / 2,
                x + side, y)

            center = [x + side / 2, y + height / 2]
            k = 0.93
            new_points = [0] * 12
            for j in range(len(points)):
                new_points[j] = center[j % 2] * (1 - k) + k * points[j]

            Color(1, 0.2, 0.5, 1, group="quarantine_group")
            Line(points=tuple(new_points), close=True, width=1,
                 dash_length=20, dash_offset=10, group="quarantine_group")
    else:
        cd.s2.canvas.remove_group("quarantine_group")


def draw_reg_distortion(draw=True, reg_id=0):
    global side
    global height
    global coords_of_hexes
    x = coords_of_hexes[reg_id][0]
    y = coords_of_hexes[reg_id][1]

    if draw:
        with cd.s2.canvas:
            Color(.5, 0, .8, .3, group="change_points")
            rec = Rectangle(size=(side / 6.5, side / 6.5),
                            pos=(x + side * 1.23 - side * 0.06 * 0.75, y + height * 0.585 - side * 0.19),
                            group="change_points")
            cd.frontend.change_points_labs[i] = Label(
                text=str(cd.mg.parameters_of_tech[21][2][0]),
                pos=rec.pos, size=rec.size, font_size=sizes.SIZE_OF_TEXT_FOR_LABEL * 1.45,
                color=(217 / 256, 172 / 256, 26 / 256), halign='center')
            cd.s2.add_widget(cd.frontend.change_points_labs[i])

    else:
        cd.s2.canvas.remove_group("change_points")
        cd.s2.remove_widget(cd.frontend.change_points_labs[i])
        cd.frontend.change_points_labs[reg_id].canvas.clear()


def draw_automation(draw=True, reg_id=0):
    global side
    global height
    global coords_of_hexes
    x = coords_of_hexes[reg_id][0]
    y = coords_of_hexes[reg_id][1]

    if draw:
        with cd.s2.canvas:
            Color(97 / 256, 93 / 256, 40 / 256, .3, group="autom")
            rec = Rectangle(size=(side / 6.5, side / 6.5),
                            pos=(x - side * 0.28 - side * 0.06 * 0.75, y + height * 0.585 - side * 0.19), group="autom")
            cd.frontend.autom_labs[i] = Label(text=str("A"), pos=rec.pos, size=rec.size,
                                                       font_size=sizes.SIZE_OF_TEXT_FOR_LABEL * 1.45,
                                                       color=(16 / 256, 185 / 256, 232 / 256), halign='center')
            cd.s2.add_widget(cd.frontend.autom_labs[reg_id])

    else:
        cd.s2.canvas.remove_group("autom")
        cd.s2.remove_widget(cd.frontend.autom_labs[reg_id])
        cd.frontend.autom_labs[reg_id].canvas.clear()
