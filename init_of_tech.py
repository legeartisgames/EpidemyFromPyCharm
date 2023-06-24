import class_widget_of_tech
import common_data
import common_var
# import tech_info
import tech_sm
import textures
import sizes

from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label

height_of_tech_widgets = sizes.Width_of_screen * 0.33 * common_var.K


def init_tech_card(tech_ind, changing_content=False):
    try:
        common_data.my_game_frontend.wid[tech_ind].index_of_current_tech
        # if not initiated they are dummies, but they exist
    except AttributeError:
        already_exists = False
    else:
        already_exists = True

    if not already_exists:
        common_data.my_game_frontend.wid[tech_ind] = class_widget_of_tech.Widget_of_tech(index_of_current_tech=tech_ind,
                                                                                         size_hint_y=None,
                                                                                         height=height_of_tech_widgets)
    else:
        if changing_content:
            common_data.my_game_frontend.wid[tech_ind].reinit()

    if changing_content or not already_exists:

        with common_data.my_game_frontend.wid[tech_ind].canvas.before:
            if common_data.my_game.is_tech_avaliable[tech_ind]:
                Color(.56, .58, .13, .9)
                common_data.my_game_frontend.wid[tech_ind].rect_wid = \
                    Rectangle(size=common_data.my_game_frontend.wid[tech_ind].size,
                              pos=common_data.my_game_frontend.wid[tech_ind].pos,
                              texture=textures.texture_of_tech)
                common_data.my_game_frontend.wid[tech_ind].bind(
                    size=common_data.my_game_frontend.wid[tech_ind].update_rect,
                    pos=common_data.my_game_frontend.wid[tech_ind].update_rect)

                Color(1, 1, 1, .4)
                if tech_ind == 27:  # тёмный задний фон у убеждения
                    Color(1, 1, 1, .5)
                common_data.my_game_frontend.wid[tech_ind].rect_wid_card = Rectangle(
                    size=common_data.my_game_frontend.wid[tech_ind].size,
                    pos=common_data.my_game_frontend.wid[tech_ind].pos,
                    texture=textures.textures_of_tech[tech_ind])
            else:  # then show locked

                Color(.56, .58, .13, .8)
                common_data.my_game_frontend.wid[tech_ind].rect_wid = \
                    Rectangle(size=common_data.my_game_frontend.wid[tech_ind].size,
                              pos=common_data.my_game_frontend.wid[tech_ind].pos,
                              texture=textures.texture_of_tech)
                common_data.my_game_frontend.wid[tech_ind].bind(
                    size=common_data.my_game_frontend.wid[tech_ind].update_rect,
                    pos=common_data.my_game_frontend.wid[tech_ind].update_rect)
                Color(1, 1, 1, .6)
                common_data.my_game_frontend.wid[tech_ind].rect_wid_card = Rectangle(
                    size=common_data.my_game_frontend.wid[tech_ind].size,
                    pos=common_data.my_game_frontend.wid[tech_ind].pos,
                    texture=textures.texture_locked)

        common_data.my_game_frontend.wid[tech_ind].bind(size=common_data.my_game_frontend.wid[tech_ind].update_rect,
                                                        pos=common_data.my_game_frontend.wid[tech_ind].update_rect)

    if tech_ind != 2 and tech_ind != 9:  # old versions of science communication and investments are deprecated
        if common_data.my_game_frontend.mode_of_tech_panel == "panel":
            if common_data.my_game_frontend.wid[tech_ind].parent is None:
                if common_data.my_stats.are_shown_unlocked_methods or common_data.my_game.is_tech_avaliable[tech_ind]:
                    # wid[tech_ind] can be existing for a long while but not unlocked, but now is unlocked by lawmaking
                    common_data.page2.add_widget(common_data.my_game_frontend.wid[tech_ind])

            else:
                if (not common_data.my_stats.are_shown_unlocked_methods) \
                        and (not common_data.my_game.is_tech_avaliable[tech_ind]):
                    common_data.page2.remove_widget(common_data.my_game_frontend.wid[tech_ind])

        if common_data.my_game_frontend.mode_of_tech_panel == "viewer":
            if common_data.my_game_frontend.wid[tech_ind].parent is None:
                if (common_data.my_stats.are_shown_unlocked_methods
                    and common_data.my_game.is_tech_avaliable[tech_ind] != 'no in mode lack of methods')\
                        or common_data.my_game.is_tech_avaliable[tech_ind]:
                    tech_sm.tech_viewer.add_screen_to_sm(tech_ind)
                    tech_sm.tech_viewer.add_element_to_screen(tech_ind)
            else:
                if (not common_data.my_stats.are_shown_unlocked_methods) \
                        and (not common_data.my_game.is_tech_avaliable[tech_ind]):
                    tech_sm.tech_viewer.remove_screen(tech_ind)


def init_all_techs():
    common_data.page2.clear_widgets()
    for i in range(common_data.num_of_cols_in_tech_panel):  # empty space in the top of method panel
        common_data.page2.add_widget(Label(size_hint_y=None, height=sizes.Height_of_screen / 20))

    for j in range(common_var.QUANT_OF_TECH):
        tech_ind = common_var.tech_order[j]
        init_tech_card(tech_ind, changing_content=True)
    if common_data.my_game.My_Country.index == 12:  # Germany&respirators
        common_data.my_game_frontend.wid[3].rect_wid_card.texture = textures.texture_respirator
