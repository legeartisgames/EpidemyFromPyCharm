import common_data as cd
import common_var
import interact_rules
import info_carousel
import spec_func
import start_menu
import sizes
import uix_classes

list_of_var = ("Русский", "English")

from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class LanguageCheckbox(GridLayout):

    def __init__(self, **kwargs):
        super(LanguageCheckbox, self).__init__(**kwargs)
        self.check_boxes_for_lang = [CheckBox(active=False)] * common_var.NUM_OF_LANGS
        self.check_boxes_for_lang[0].active = True
        # 2 columns in grid layout 
        self.cols = 2
        for i in range(0, len(list_of_var)):
            self.add_widget(Label(text=list_of_var[i], size_hint_x=.2, font_size=round(sizes.width_res / 60)))
            self.check_boxes_for_lang[i] = CheckBox()
            if i == common_var.lang:
                self.check_boxes_for_lang[i].active = True
            self.check_boxes_for_lang[i].group = "lang_group"
            self.check_boxes_for_lang[i].font_size = (sizes.width_res / 70)
            self.check_boxes_for_lang[i].size_hint_x = .2
            self.check_boxes_for_lang[i].bind(on_press=self.on_checkbox_press)
            self.add_widget(self.check_boxes_for_lang[i])

    def on_checkbox_press(self, instance):
        ind = 0
        for i in range(2):
            if self.check_boxes_for_lang[i].active:
                if i != common_var.lang:
                    common_var.previous_lang = common_var.lang
                    common_var.lang = i
                    cd.stats.lang = i
                    spec_func.update_texts()
                    interact_rules.rp = interact_rules.RulePage(typ='contents')

                ind = 1
        if ind == 0:  # смысл в том, что если checkbox в принципе везде не выбран, то ставим русский
            self.check_boxes_for_lang[0].active = True
            if common_var.lang != 0:
                common_var.previous_lang = common_var.lang
                common_var.lang = 0
                cd.stats.lang = 0
                spec_func.update_texts()
                interact_rules.rp = interact_rules.RulePage(typ='contents')


class StartLangChooseLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(StartLangChooseLayout, self).__init__(**kwargs)
        self.start_lang_checkbox = LanguageCheckbox(size_hint=[.6, .5], pos_hint={'center_x': .3, 'center_y': .5})
        self.add_widget(self.start_lang_checkbox)

        self.btn = uix_classes.Button_with_image(text_source=["Ввод", "Enter"], on_press=self.set_lang_and_start_gaming,
                                                 size_hint=[.3, .3], pos_hint={'center_x': .7, 'center_y': .5},
                                                 font_size=(sizes.width_res / 40))

        self.add_widget(self.btn)

    def set_lang_and_start_gaming(self, instance):
        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(start_menu.Main_menu)
        App.get_running_app().outer_folders = [start_menu.Main_menu]
        cd.stats.is_language_set = 1
        cd.stats.save_to_file()
        info_carousel.InfoCarousel().open(instance=5)
        del self
