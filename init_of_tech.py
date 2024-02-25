import class_widget_of_tech
import common_data as cd
import common_var
import tech_sm
import textures
import sizes

from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label

tech_widgets_height = sizes.width_res / common_var.tech_cols_num


def init_tech_card(tech_ind, changing_content=False):
    try:
        cd.frontend.wid[tech_ind].method_id
        # if not initiated they are dummies, but they exist
    except AttributeError:
        already_exists = False
    else:
        already_exists = True

    if not already_exists:
        cd.frontend.wid[tech_ind] = class_widget_of_tech.TechnoWidget(method_id=tech_ind,
                                                                      size_hint_y=None,
                                                                      height=tech_widgets_height)
    else:
        if changing_content:
            cd.frontend.wid[tech_ind].reinit()

    if changing_content or not already_exists:

        with cd.frontend.wid[tech_ind].canvas.before:
            if cd.mg.techs_avail_bool[tech_ind]:
                Color(.56, .58, .13, .9)
                cd.frontend.wid[tech_ind].rect_wid = \
                    Rectangle(size=cd.frontend.wid[tech_ind].size,
                              pos=cd.frontend.wid[tech_ind].pos,
                              texture=textures.texture_of_tech)
                cd.frontend.wid[tech_ind].bind(
                    size=cd.frontend.wid[tech_ind].update_rect,
                    pos=cd.frontend.wid[tech_ind].update_rect)

                Color(1, 1, 1, .4)
                if tech_ind == 27:  # тёмный задний фон у убеждения
                    Color(1, 1, 1, .5)
                cd.frontend.wid[tech_ind].rect_wid_card = Rectangle(
                    size=cd.frontend.wid[tech_ind].size,
                    pos=cd.frontend.wid[tech_ind].pos,
                    texture=textures.textures_of_tech[tech_ind])
            else:  # then show locked

                Color(.56, .58, .13, .8)
                cd.frontend.wid[tech_ind].rect_wid = \
                    Rectangle(size=cd.frontend.wid[tech_ind].size,
                              pos=cd.frontend.wid[tech_ind].pos,
                              texture=textures.texture_of_tech)
                cd.frontend.wid[tech_ind].bind(
                    size=cd.frontend.wid[tech_ind].update_rect,
                    pos=cd.frontend.wid[tech_ind].update_rect)
                Color(1, 1, 1, .6)
                cd.frontend.wid[tech_ind].rect_wid_card = Rectangle(
                    size=cd.frontend.wid[tech_ind].size,
                    pos=cd.frontend.wid[tech_ind].pos,
                    texture=textures.texture_locked)

        cd.frontend.wid[tech_ind].bind(size=cd.frontend.wid[tech_ind].update_rect,
                                       pos=cd.frontend.wid[tech_ind].update_rect)

    if tech_ind != 2 and tech_ind != 9:  # old versions of science communication and investments are deprecated
        if cd.frontend.tech_panel_mode == "panel":
            if cd.frontend.wid[tech_ind].parent is None:
                if cd.stats.are_shown_unlocked_methods or cd.mg.techs_avail_bool[tech_ind]:
                    # wid[tech_ind] can be existing for a long while but not unlocked, but now is unlocked by lawmaking
                    cd.page2.add_widget(cd.frontend.wid[tech_ind])

            else:
                if (not cd.stats.are_shown_unlocked_methods) \
                        and (not cd.mg.techs_avail_bool[tech_ind]):
                    cd.page2.remove_widget(cd.frontend.wid[tech_ind])

        if cd.frontend.tech_panel_mode == "viewer":
            if cd.frontend.wid[tech_ind].parent is None:
                if (cd.stats.are_shown_unlocked_methods
                    and cd.mg.techs_avail_bool[tech_ind] != 'no in mode lack of methods') \
                        or cd.mg.techs_avail_bool[tech_ind]:
                    tech_sm.tech_viewer.add_screen_to_sm(tech_ind)
                    tech_sm.tech_viewer.add_element_to_screen(tech_ind)
            else:
                if (not cd.stats.are_shown_unlocked_methods) \
                        and (not cd.mg.techs_avail_bool[tech_ind]):
                    tech_sm.tech_viewer.remove_screen(tech_ind)


def init_all_techs():
    cd.page2.clear_widgets()
    for i in range(cd.stats.cols_on_page_of_tech):  # empty space in the top of method panel
        cd.page2.add_widget(Label(size_hint_y=None, height=sizes.height_res / 20))

    for j in range(common_var.QUANT_OF_TECH):
        tech_ind = common_var.tech_order[j]
        init_tech_card(tech_ind, changing_content=True)
    if cd.mg.My_Country.index == 12:  # respirators for Germany
        cd.frontend.wid[3].rect_wid_card.texture = textures.texture_respirator
