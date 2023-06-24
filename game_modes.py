class Game_mode():
    def __init__(self, name = ["Имя мода", "Mode Name"], index=None, min_rep_stars=0, min_golds=0, level=0, step_time = "unlim",
                 coef_award = 1):
        self.name = name
        self.index  = index
        self.min_rep_stars = min_rep_stars
        self.min_goldreserves = min_golds 
        self.level = level
        self.step_time = step_time
        self.coef_award = coef_award

normal_mode = Game_mode(index = 0, name = ["Обычный", "Common"], level = 3)
mode_30s = Game_mode(index = 1, name = ["25 секунд на ход", "25 seconds for 1 turn"], level = 5, step_time = 25, coef_award = 2) 
mode_60s = Game_mode(index = 2, name = ["40 секунд на ход", "40 seconds for 1 turn"], level = 4, step_time = 40, coef_award = 1.25) 
mode_20s = Game_mode(index = 3, name = ["15 секунд на ход", "15 seconds for 1 turn"], level = 8, step_time = 15, coef_award = 3) 
mode_x5penpoints = Game_mode(index = 4, name = ["Лимит штрафа x5", "Penalty limit x5"], level = 1, coef_award=0.2)
mode_laws = Game_mode(index=5, name=["Методы с нуля","Lack of methods"], level=6, coef_award=2.5)
mode_good_capital = Game_mode(index=6, name=["Довольная столица","Contented capital"], level=4, coef_award = 1.5)

numbers_in_menu_ru = [normal_mode, mode_60s, mode_30s, mode_20s, mode_x5penpoints, mode_laws, mode_good_capital]
numbers_in_menu_en = [normal_mode, mode_60s, mode_30s, mode_20s, mode_x5penpoints, mode_laws, mode_good_capital]
numbers_in_menu = [numbers_in_menu_ru, numbers_in_menu_en]

modes_list = [normal_mode, mode_30s, mode_60s, mode_20s, mode_x5penpoints, mode_laws, mode_good_capital]

'''
режим "довольная столица": если набрано более 2 штрафных баллов в столице, то проигрыш.
режим "динамика эпидемии": 
- если х ходов подряд число больных в стране растёт, то имеете х-1 штрафных очков за это (как только число больных перестаёт расти, штрафные очки сбрасываются)
- если х ходов подряд число больных в стране падает, то имеете х-4 победных балла за это (опять же может сброситься при росте)
чит: при режиме х5 штрафа можно наживаться через коррупцию и трансферты! (оставить его или нет?)
'''