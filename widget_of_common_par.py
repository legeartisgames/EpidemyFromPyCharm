import common_data as cd
import common_var
import icon_func
import notifier
import sizes
import textures

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

last_notify = 0


def info_message(message, typ, t):
    global last_notify
    if notifier.notifier_box.label.text == message or notifier.notifier_box2.label.text == message:
        return
    if last_notify == 1 and notifier.notifier_box in cd.final_layout.children:
        smooth_show = True
        if notifier.notifier_box2 in cd.final_layout.children:
            smooth_show = False
        notifier.notifier_box2.notify(text=message, tau=t, typ=typ, smooth_show=smooth_show)
        last_notify = 2
    else:
        smooth_show = True
        if notifier.notifier_box in cd.final_layout.children:
            smooth_show = False
        notifier.notifier_box.notify(text=message, tau=t, typ=typ, smooth_show=smooth_show)
        last_notify = 1


def change_input(delta, inp, max_v, instance, typ=None):
    inp.text = inp.text.replace(icon_func.add_money_icon_simple(""), "")
    if 0 <= round(float(inp.text)) + delta <= max_v:
        inp.text = str(round(float(inp.text) + delta))
    else:
        if round(float(inp.text)) + delta < 0:
            inp.text = '0'
        elif round(float(inp.text)) + delta > max_v:
            inp.text = str(max_v)
    if typ == "coin":
        inp.text = icon_func.add_money_icon_simple(inp.text)


rec_fin = 0
ind_rec_fin = 0
lab_fin = 0
exit_widget = FloatLayout()
btn_ask_res = 0


def inform_about_end(message, typ, status_c_rising=False, status_s_rising=False):
    global rec_fin, lab_fin, ind_rec_fin, exit_widget, btn_ask_res

    cd.final_layout.clear_widgets()
    cd.final_layout.add_widget(exit_widget, canvas="after")
    exit_widget.clear_widgets()
    exit_widget.canvas.clear()

    with exit_widget.canvas:
        add_for_label = ['', '']
        if status_c_rising:
            add_for_label[0] += "\nНовый статус благосостояния -  [color=00ffff]" + str(
                common_var.statuses_coins[cd.stats.level_coins][0]) + '[/color]\n'
            add_for_label[1] += "\nYour new wealth status is [color=00ffff]" + str(
                common_var.statuses_coins[cd.stats.level_coins][1]) + '[/color]\n'

        if status_s_rising:
            add_for_label[0] += "\nНовый статус репутации - [color=00ffff]" + str(
                common_var.stars_statuses[cd.stats.level_stars][0]) + "[/color]\n"
            add_for_label[1] += "\nYour new reputation status is [color=00ffff]" + str(
                common_var.stars_statuses[cd.stats.level_stars][1]) + "[/color]\n"

        if typ == 'bad':
            Color(1, 0, 0, 1)
            rec_texture = textures.error_texture
        if typ == 'good':
            Color(1, 1, 1, .7)
            add_for_label[0] += "\nПоздравляем!"
            add_for_label[1] += "\nCongratulations!"
            rec_texture = textures.texture_medals

        rec_fin = Rectangle(size=(sizes.width_res * 0.7, sizes.height_res * 0.9),
                            pos=(sizes.width_res * 0.15, sizes.height_res * 0.05),
                            texture=rec_texture, canvas='after')

        lab_fin = Label(text=message + add_for_label[common_var.lang], size=rec_fin.size,
                        pos=(rec_fin.pos[0], rec_fin.pos[1] + rec_fin.size[1] * 0.1),
                        font_size=sizes.WIN_SIZE, color=(1, 1, 1, 1),
                        bold=True, halign='center', valign='top', markup=True)

        exit_widget.add_widget(
            Button(text=["Сыграть ещё\nодну партию", "Play another\ngame"][common_var.lang], size_hint=(.20, .11),
                   pos=(rec_fin.pos[0] + rec_fin.size[0] * 0.65, rec_fin.pos[1] + rec_fin.size[1] * 0.07),
                   font_size=sizes.ASK_SIZE, halign='center',
                   on_press=type(App.get_running_app()).start_new_game_right_now))

        exit_widget.add_widget(
            Button(text=["Вeрнуться в\nглавное меню", "Return to main\nmenu"][common_var.lang], size_hint=(.20, .11),
                   pos=(rec_fin.pos[0] + rec_fin.size[0] * 0.06, rec_fin.pos[1] + rec_fin.size[1] * 0.07),
                   font_size=sizes.ASK_SIZE, halign='center', on_press=App.get_running_app().close_game_space))

        ind_rec_fin = 1


opened_ask_panel = None


class AskPanel(FloatLayout):
    def __init__(self, **kwargs):
        super(AskPanel, self).__init__(**kwargs)
        self.texture = None
        self.outer_folders = []
        self.prev_ask_panel = None

    def open_ask_panel(self, messages, texture=None, color_texture=(1, .6, .1, 1)):
        global opened_ask_panel
        self.texture = texture
        text_m = ''
        if len(messages) <= 2:
            size_tab = round(60 * sizes.height_res / 800)
        else:
            size_tab = round(40 * sizes.height_res / 800)

        for i in range(len(messages)):
            text_m = text_m + messages[i] + '[size=' + str(size_tab) + ']\n[/size]'

        self.outer_folders = []
        for i in cd.final_layout.children:
            self.outer_folders.append(i)

        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(self)
        with self.canvas:
            Color(1, .6, .1, 1)
            rec_ask = Rectangle(size=(sizes.width_res * 0.56, sizes.height_res * 0.7),
                                pos=(sizes.width_res * 0.22, sizes.height_res * 0.15),
                                texture=textures.texture_add_to_question)
            self.left_edge_pos = rec_ask.pos
            self.size_zone = rec_ask.size

            Color(color_texture[0], color_texture[1], color_texture[2], color_texture[3])
            self.active_zone = Rectangle(size=rec_ask.size, pos=rec_ask.pos, texture=self.texture)

            self.label_text = Label(text="[b]" + text_m, size=rec_ask.size,
                                    pos=(rec_ask.pos[0], rec_ask.pos[1] + rec_ask.size[1] * 0.22),
                                    font_size=round(1.1 * sizes.ASK_SIZE), color=[1, 1, 1, 1],
                                    markup=True, halign='center')

        self.btn_ask_close = Button(text=["Закрыть окно", "Close window"][common_var.lang], size_hint=(.15, .10),
                                    pos=(
                                        rec_ask.pos[0] + rec_ask.size[0] * 0.7,
                                        rec_ask.pos[1] + rec_ask.size[1] * 0.03),
                                    font_size=sizes.ASK_SIZE, on_press=self.close_ask_panel)

        self.add_widget(self.btn_ask_close)
        self.prev_ask_panel = opened_ask_panel
        opened_ask_panel = self

    def close_ask_panel(self, instance):
        global opened_ask_panel
        if opened_ask_panel is not None:
            cd.final_layout.clear_widgets()
            cd.final_layout.canvas.clear()

            opened_ask_panel = self.prev_ask_panel
            print("Opened ask panel is", opened_ask_panel)
            for i in self.outer_folders:
                cd.final_layout.add_widget(i)
            for i in range(len(self.children)):
                del self.children[0]
            self.canvas.clear()
            del self
