# from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
# from kivy.uix.button import Button
import common_data as cd
import common_var
import sizes
import web_goer

titles_ru = ['Вступительное слово', 'Общие для страны параметры эпидемии', "Устройство региона-гекса", "Базовые кнопки",
             "Пример карт методов", "Применение метода к региону: часть 1", "Применение метода к региону: часть 2",
             "Вакцина и Вакцинация: пошаговое руководство к методу", "Как начать игру"]
titles_en = ['Introduction', 'Country-wide epidemic parameters', "Stucture of region-hex", "Basic buttons",
             "Example method cards", "Applying the method to region: part 1", "Applying the method to region: part 2",
             "Vaccine and Vaccination: step-by-step guide to the method", "How to start the game"]

sources = ['empty', '01_common_ill.jpg', '02_hex.jpg', '03_buttons.jpg', '04_methods.jpg', '05_multichoice.jpg',
           '06_choose.jpg', '07_vaccine.jpg', 'empty']
sources_en = ['empty', 'en/01_common_ill_en.jpg', 'en/02_hex_en.jpg', 'en/03_buttons_en.jpg', 'en/04_methods_en.jpg',
              'en/05_multichoice_en.jpg', 'en/06_choose_en.jpg', 'en/07_vaccine_en.jpg', 'empty']


class InfoCarousel(Carousel):
    def __init__(self, **kwargs):
        super(InfoCarousel, self).__init__(**kwargs)
        self.direction = 'right'
        self.min_move = 0.06
        self.create()
        self.bind(on_touch_up=self.on_up)

    def create(self):

        for i in range(9):
            src_ru = 'demo_images/' + sources[i]
            src_en = 'demo_images/' + sources_en[i]

            if common_var.lang == 0:
                titles = titles_ru
                src = src_ru
            else:
                titles = titles_en
                src = src_en
            lab_title = Label(text=titles[i], size_hint_y=.08, font_size=sizes.width_res / 45)
            if 0 < i < 8:
                image = AsyncImage(source=src, allow_stretch=True, size_hint_y=.92)
            elif i == 0:
                rules_strings = ['', '']

                file_ru = open('manual_texts/ru/first_i_carousel_ru.txt', 'r', encoding='utf8')
                f = file_ru.readlines()
                for j in range(len(f)):
                    rules_strings[0] += (str(f[j]))
                file_ru.close()

                file_en = open('manual_texts/en/first_i_carousel_en.txt', 'r', encoding='utf8')
                f = file_en.readlines()
                for j in range(len(f)):
                    rules_strings[1] += (str(f[j]))
                file_en.close()

                image = Label(text=rules_strings[common_var.lang],
                              font_size=sizes.width_res / 45, markup=True, size_hint_y=.92)

            else:
                rules_strings = ['', '']

                file_ru = open('manual_texts/ru/last_i_carousel_ru.txt', 'r', encoding='utf8')
                f = file_ru.readlines()
                for j in range(len(f)):
                    rules_strings[0] += (str(f[j]))
                file_ru.close()

                file_en = open('manual_texts/en/last_i_carousel_en.txt', 'r', encoding='utf8')
                f = file_en.readlines()
                for j in range(len(f)):
                    rules_strings[1] += (str(f[j]))
                file_en.close()

                image = Label(text=rules_strings[common_var.lang],
                              font_size=sizes.width_res / 50, markup=True, size_hint_y=.92)
                image.bind(on_ref_press=lambda *args: web_goer.go_to_link(*args))

            bl = BoxLayout(orientation='vertical', padding=sizes.width_res / 50, spacing=sizes.width_res / 100)

            bl.add_widget(lab_title)
            bl.add_widget(image)
            self.add_widget(bl)

    def open(self, instance):
        self.outer_folders = []
        for i in cd.final_layout.children:
            self.outer_folders.append(i)
        cd.final_layout.clear_widgets()
        cd.final_layout.add_widget(self)

    def close(self, instance):
        cd.final_layout.remove_widget(self)
        for i in self.outer_folders:
            cd.final_layout.add_widget(i)

    def delete(self):
        for i in self.children:
            del i
        del self

    def on_up(self, instance, touch):
        if touch.is_double_tap:
            if touch.pos[0] > sizes.width_res / 2:
                if self.index == 8:
                    self.close(instance=0)
                    self.delete()
                self.index += 1
            else:
                if self.index > 0:
                    self.index -= 1
