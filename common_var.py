WAS_STOP = False  # связано с багом в kivy, при котором on_stop вызывается 2 раза
IS_PREMIUM = False
VERSION_ID = 24

lang = 0
previous_lang = 0
list_of_btns = []  # for translate

NUM_OF_LANGS = 2

QUANT_OF_TECH = 32  # суммарное число технологий (+ инвестиций)
QUANT_OF_DIS = 3
tech_order = (0, 1, 28,  
              3, 4, 5, 
              6, 7, 8, 
              12, 13, 14,
              19, 20, 26,
              18, 21, 22,
              24, 25, 23,
              15, 16, 17,
              27, 30, 31,
              29, 10, 11, 
              2, 9)
is_game_running = "in_main_menu"
is_open_tech = 0
is_victory = "none"
tech_cols_num = 3  # K was 3/it

n = 21
n_max = 21
num_of_lands = 0

Current_country = None
Current_mode = None
Current_dis = None
statuses_coins = [["Индивидуальный\nпредприниматель (№1)", "Individual\nentrepreneur (#1)"], 
                  ["Владелец небольшой\n компании (№2)", "Small company owner  (#2)"], 
                  ["Бизнесмен (№3)", "Businessman (#3)"], ["Капиталист (№4)", "Capitalist (#4)"], 
                  ["Промышленник (№5)", "Industrialist (#5)"], ["Богач (№6)", "Rich (#6)"],
                  ["Монополист (№7)", "Monopolist (#7)"], ["Миллиардер (№8)", "Billionaire (#8)"],
                  ["Магнат (№9)", "Tycoon (№9)"], ["Олигарх (№10)", "Powerful (#10)"]]

thresh_hold_coins = [0, 10, 110, 200, 400, 725, 1200, 1800, 2500, 50000]

stars_statuses = [["Гость (№1)", "Guest  (#1)"],   ["Начинающий (№2)", "Beginner (#2)"], 
                  ["Дилетант (№3)", "Amateur (#3)"], ["Фанат (№4)", "Fan (#4)"], 
                  ["Кандидат (№5)", "Candidate (#5)"], ["Специалист (№6)", "Specialist (#6)"], 
                  ["Мастер (№7)", "Master (#7)"], ["Эксперт (№8)", "Expert (#8)"], 
                  ["Начальник (№9)", "Chief (#9)"], ["Министр (№10)", "Minister (#10)"],
                  ["Лидер (№11)", "Leader (#11)"], ["Вице-президент (№12)", "Vice president (#12)"],
                  ["Президент (№13)", "The president (#13)"], ["Мастер (№14)", "Master (#14)"]]

thresh_hold_stars = [0, 5, 40, 100, 180, 250, 350, 500, 700, 1000, 1200, 2500, 3500, 25000]
need_c = 0
need_s = 0

months_names = [["январь", "January"], ["февраль", "February"], ["март", "March"], ["апрель", "April"], 
                ["май", "May"], ["июнь", "June"], ["июль", "July"], ["август", "August"],
                ["сентябрь", "September"], ["октябрь", "October"], ["ноябрь", "November"], ["декабрь", "December"]]


