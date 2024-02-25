NUM_OF_COUNTRIES = 13


class Land:
    def __init__(self, index, Cart_of_country, Number_of_regions, Capital_index, dens, pop, income_of_c, size, dy,
                 la_z_ins, stars, level, name,
                 min_reputation_status, min_coins_status, fluct_z_out, ups_by_y, real_size_of_hex, color_of_name,
                 hemisphere, coef_perenos,
                 crit_b, prepositional_case, names_of_provinces):
        self.index = index
        self.number_of_regions = Number_of_regions
        self.cart_of_country = Cart_of_country
        self.names_of_provinces = names_of_provinces
        self.capital_index = Capital_index
        self.dencity_of_people = dens
        self.population = tuple(pop)
        self.full_population = 0
        for i in range(len(pop)):
            self.full_population += pop[i]
        self.income = income_of_c
        self.sizes = size
        self.dy = dy
        self.z_ins = la_z_ins
        self.fluct_z_out = fluct_z_out
        self.stars = stars
        self.level = level
        self.name = name
        self.prepositional_case = prepositional_case
        self.min_rep_stars = min_reputation_status
        self.min_goldreserves = min_coins_status
        self.ups_by_y = ups_by_y
        self.real_size_of_hex = real_size_of_hex
        self.color_of_name = color_of_name
        self.hemisphere = hemisphere
        self.ind_perenos = coef_perenos
        self.crit_b = crit_b


number_of_regions_in_Argentina = 9
Argentina_cart = [0] * number_of_regions_in_Argentina
Argentina_cart[0] = [0, 0]
Argentina_cart[1] = [0, 1]
Argentina_cart[2] = [1, 0]
Argentina_cart[3] = [1, 1]
Argentina_cart[4] = [1, 2]
Argentina_cart[5] = [2, 1]
Argentina_cart[6] = [2, 2]
Argentina_cart[7] = [2, 3]
Argentina_cart[8] = [3, 3]
capital_of_Argentina = 5
Argentina_names = [["Гран Чако", "Gran Chaco"],  # locale (district of plain with low population)
                   ["Анды", "Andes"],  # locale
                   ["Кордова", "Córdoba"],  # city/province
                   ["Сан-Хуан", "San Juan"],  # city/province
                   ["Мендоса", "Mendoza"],  # province/city
                   ["Буэнос-Айрес", "Buenos Aires"],  # city/province
                   ["Рио-Негро", "Rio Negro"],  # river/province
                   ["Санта Крус", "Santa Cruz"],  # province
                   ["Огненная земля", "Tierra del Fuego"]]  # locale/province

number_of_regions_in_Australia = 12
Australia_cart = [0] * number_of_regions_in_Australia
Australia_cart[0] = [0, 0]
Australia_cart[1] = [0, 1]
Australia_cart[2] = [1, -1]
Australia_cart[3] = [1, 0]
Australia_cart[4] = [2, -1]
Australia_cart[5] = [2, 0]
Australia_cart[6] = [2, 1]
Australia_cart[7] = [3, -1]
Australia_cart[8] = [3, 0]
Australia_cart[9] = [3, 1]
Australia_cart[10] = [4, 0]
Australia_cart[11] = [4, 1]
capital_of_Australia = 11

Australia_names = [["Запад", "Western part"],  # province (real name is Западная Австралия/Western Australia)
                   ["Перт", "Perth"],  # city
                   ["Карламилии", "Karlamilyi Park"],  # locale (National park)
                   ["Виктория", "Victoria Desert"],  # locale (Great Desert)
                   ["Север", "Northern part"],  # province (Northern territory)
                   ["Алис-Спрингс", "Alice Springs"],  # city
                   ["Юг", "South"],  # province (South Australia)
                   ["Стаатен Ривер", "Staaten river"],  # locale (river)
                   ["Квинсленд", "Queensland"],  # province
                   ["Мельбурн", "Melbourne"],  # city
                   ["Брисбен", "Brisbane"],  # city
                   ["Сидней", "Sydney"]]  # city

number_of_regions_in_Brazilia = 11
Brazilia_cart = [0] * number_of_regions_in_Brazilia
Brazilia_cart[0] = [0, 0]
Brazilia_cart[1] = [0, 1]
Brazilia_cart[2] = [1, -1]
Brazilia_cart[3] = [1, 0]
Brazilia_cart[4] = [1, 1]
Brazilia_cart[5] = [2, 0]
Brazilia_cart[6] = [2, 1]
Brazilia_cart[7] = [2, 2]
Brazilia_cart[8] = [2, 3]
Brazilia_cart[9] = [3, 0]
Brazilia_cart[10] = [3, 1]
capital_of_Brazilia = 10

Brazil_names = [["Амазонас", "Amazonas"],  # province (in Brazil it is called state)
                ["Рондония", "Rondonia"],  # province
                ["Мараньян", "Maranhão"],  # province
                ["Пара", "Pará"],  # province
                ["Мату-Гросу", "Mato Grosso"],
                ["Форталеза", "Fortaleza"],  # city
                ["Минас Жерайс", "Minas Gerais"],  # province
                ["Сан Паулу", "São Paulo"],  # city
                ["Парана", "Paraná"],  # river and province
                ["Сальвадор", "Salvador"],  # city
                ["Рио-де-Жанейро", "Rio de Janeiro"]]  # city

number_of_regions_in_Canada = 13
Canada_cart = [0] * number_of_regions_in_Canada
Canada_cart[0] = [0, 0]
Canada_cart[1] = [0, 1]
Canada_cart[2] = [1, -1]
Canada_cart[3] = [1, 0]
Canada_cart[4] = [2, -1]
Canada_cart[5] = [2, 0]
Canada_cart[6] = [2, 1]
Canada_cart[7] = [3, -1]
Canada_cart[8] = [3, 0]
Canada_cart[9] = [3, 1]
Canada_cart[10] = [4, -1]
Canada_cart[11] = [4, 1]
Canada_cart[12] = [5, 0]
capital_of_Canada = 9

Canada_names = [["Юкон", "Yukon"],  # territory/river
                ["Бр. Колумбия", "British Columbia"],  # province
                ["Северо-Запад", "North-West"],  # Северо-Западные территории
                ["Альберта", "Alberta"],  # province
                ["о-ва Виктории", "Victoria Islands"],  # locale, in Nunavut and in North-West
                ["Невольничье оз.", "Great Slave Lake"],  # locale, in North-West
                ["Манитоба", "Manitoba"],  # province
                ["Нунавут", "Nunavut"],  # province (part of it)
                ["Квебек", "Quebec"],  # city/province
                ["Оттава", "Ottawa"],  # capital
                ["Земля Баффина", "Baffin Island"],  # locale (island), in Nunavut, остров Баффинова земля
                ["Лабрадор", "Labrador"],  # peninsula, province Newfoundland and Labrador
                ["Ньюфаундленд", "Newfoundland"],  # island, province Newfoundland and Labrador
                ]

number_of_regions_in_China = 12
China_cart = [0] * number_of_regions_in_China
China_cart[0] = [0, 0]
China_cart[1] = [0, 1]
China_cart[2] = [1, 0]
China_cart[3] = [1, 1]
China_cart[4] = [2, -1]
China_cart[5] = [2, 0]
China_cart[6] = [2, 1]
China_cart[7] = [2, 2]
China_cart[8] = [3, -1]
China_cart[9] = [3, 0]
China_cart[10] = [3, 1]
China_cart[11] = [4, 1]
capital_of_China = 9

China_names = [["Китайская Обл.", "Chinese Region"]] * number_of_regions_in_China

number_of_regions_in_Germany = 7
Germany_cart = [0] * number_of_regions_in_Germany
Germany_cart = [[0, 0], [0, 2], [1, -1], [1, 0], [1, 1], [2, 0], [2, 2]]
Germany_names = [["Немецкая Обл.", "German Region"]] * number_of_regions_in_Germany

number_of_regions_in_India = 10
India_cart = [0] * number_of_regions_in_India
India_cart[0] = [0, 0]
India_cart[1] = [0, 1]
India_cart[2] = [1, -1]
India_cart[3] = [1, 0]
India_cart[4] = [1, 1]
India_cart[5] = [1, 2]
India_cart[6] = [1, 3]
India_cart[7] = [2, 1]
India_cart[8] = [2, 2]
India_cart[9] = [3, 0]
capital_of_India = 3
India_names = [["Индийская Обл.", "Indian Region"]] * number_of_regions_in_India

number_of_regions_in_Mexica = 7
Mexica_cart = [0] * number_of_regions_in_Mexica
Mexica_cart[0] = [0, 0]
Mexica_cart[1] = [0, 1]
Mexica_cart[2] = [1, 0]
Mexica_cart[3] = [1, 1]
Mexica_cart[4] = [1, 2]
Mexica_cart[5] = [2, 3]
Mexica_cart[6] = [3, 2]
capital_of_Mexica = 4

Mexico_names = [["Мексиканская Обл.", "Mexican Region"]] * number_of_regions_in_Mexica

number_of_regions_in_Russia = 21
Russia_cart = [0] * number_of_regions_in_Russia
Russia_cart[0] = [0, 0]
Russia_cart[1] = [0, 2]
Russia_cart[2] = [1, 0]
Russia_cart[3] = [1, 1]
Russia_cart[4] = [2, 0]
Russia_cart[5] = [2, 1]
Russia_cart[6] = [2, 2]
Russia_cart[7] = [3, 0]
Russia_cart[8] = [3, 1]
Russia_cart[9] = [3, 2]
Russia_cart[10] = [4, 0]
Russia_cart[11] = [4, 1]
Russia_cart[12] = [4, 2]
Russia_cart[13] = [4, 3]
Russia_cart[14] = [5, 0]
Russia_cart[15] = [5, 1]
Russia_cart[16] = [6, 0]
Russia_cart[17] = [6, 1]
Russia_cart[18] = [6, 2]
Russia_cart[19] = [7, 0]
Russia_cart[20] = [8, 1]
capital_of_Russia = 5

Russia_names = [["Русская Обл.", "Russian Province"]] * number_of_regions_in_Russia

number_of_regions_in_Turkey = 10
Turkey_cart = [0] * number_of_regions_in_Turkey
Turkey_cart = [[0, 0], [0, 1], [1, -1], [1, 0], [2, 0], [2, 1], [3, -1], [3, 0], [4, 0], [4, 1]]

Turkey_names = [["Турецкая обл", "Turkey Region"]] * number_of_regions_in_Turkey

number_of_regions_in_USA = 13
USA_cart = [0] * number_of_regions_in_USA
USA_cart[0] = [0, 0]
USA_cart[1] = [1, -1]
USA_cart[2] = [2, 1]
USA_cart[3] = [2, 2]
USA_cart[4] = [3, 0]
USA_cart[5] = [3, 1]
USA_cart[6] = [3, 2]
USA_cart[7] = [4, 1]
USA_cart[8] = [4, 2]
USA_cart[9] = [5, 0]
USA_cart[10] = [5, 1]
USA_cart[11] = [5, 2]
USA_cart[12] = [6, 1]
capital_of_USA = 10

USA_names = [["США обл.", "US Region"]] * number_of_regions_in_USA

Universal_cart = [0] * 7
Universal_cart[0] = [0, 0]
Universal_cart[1] = [0, 1]
Universal_cart[2] = [1, -1]
Universal_cart[3] = [1, 0]
Universal_cart[4] = [1, 1]
Universal_cart[5] = [2, 0]
Universal_cart[6] = [2, 1]
Universal_names = [["Универсальная обл.", "Universal Region"]] * 7

Japan_cart = [0] * 7
Japan_cart[0] = [0, 0]
Japan_cart[1] = [1, -1]
Japan_cart[2] = [1, -2]
Japan_cart[3] = [2, -4]
Japan_cart[4] = [2, -3]
Japan_cart[5] = [2, -2]
Japan_cart[6] = [2, -1]
Japan_names = [["Японская обл.", "Japanese Region"]] * 7

Argentina_dencity_of_population = [0] * 21
Argentina_dencity_of_population[0] = 7
Argentina_dencity_of_population[1] = 8
Argentina_dencity_of_population[2] = 18
Argentina_dencity_of_population[3] = 10
Argentina_dencity_of_population[4] = 15
Argentina_dencity_of_population[5] = 36
Argentina_dencity_of_population[6] = 25
Argentina_dencity_of_population[7] = 20
Argentina_dencity_of_population[8] = 5
Argentina_square = 2.8 * 1000000
Argentina_population = [0] * 21

counter = 0
for i in range(9):
    Argentina_population[i] = round(Argentina_dencity_of_population[i] * Argentina_square / 9 / 1000) * 1000
    counter += Argentina_population[i]

Australia_dencity_of_population = [0] * 21
Australia_dencity_of_population[0] = 2.8
Australia_dencity_of_population[1] = 3.2
Australia_dencity_of_population[2] = 4.2
Australia_dencity_of_population[3] = 0.1
Australia_dencity_of_population[4] = 4
Australia_dencity_of_population[5] = 0.13
Australia_dencity_of_population[6] = 3
Australia_dencity_of_population[7] = 5
Australia_dencity_of_population[8] = 0.11
Australia_dencity_of_population[9] = 4.7
Australia_dencity_of_population[10] = 5.9
Australia_dencity_of_population[11] = 6.2
Australia_square = 7.7 * 1000000
Australia_population = [0] * 21
counter = 0
for i in range(12):
    Australia_population[i] = round(Australia_dencity_of_population[i] * Australia_square / 12 / 1000) * 1000
    counter += Australia_population[i]

Brazilia_dencity_of_population = [0] * 21
Brazilia_dencity_of_population[0] = 1.1
Brazilia_dencity_of_population[1] = 2.4
Brazilia_dencity_of_population[2] = 2.1
Brazilia_dencity_of_population[3] = 1.3
Brazilia_dencity_of_population[4] = 3
Brazilia_dencity_of_population[5] = 10
Brazilia_dencity_of_population[6] = 15
Brazilia_dencity_of_population[7] = 50
Brazilia_dencity_of_population[8] = 30
Brazilia_dencity_of_population[9] = 60
Brazilia_dencity_of_population[10] = 100
Brazilia_square = 8.5 * 1000000

Brazilia_population = [0] * 21
counter = 0
for i in range(12):
    Brazilia_population[i] = round(Brazilia_dencity_of_population[i] * Brazilia_square / 11 / 1000) * 1000
    counter += Brazilia_population[i]

Canada_dencity_of_population = [0] * 21
Canada_dencity_of_population[0] = 0.32
Canada_dencity_of_population[1] = 0.4
Canada_dencity_of_population[2] = 0.2
Canada_dencity_of_population[3] = 3
Canada_dencity_of_population[4] = 0.13
Canada_dencity_of_population[5] = 0.29
Canada_dencity_of_population[6] = 11
Canada_dencity_of_population[7] = 0.11
Canada_dencity_of_population[8] = 1.5
Canada_dencity_of_population[9] = 15
Canada_dencity_of_population[10] = 0.23
Canada_dencity_of_population[11] = 18
Canada_dencity_of_population[12] = 12
Canada_square = 10 * 1000000

Canada_population = [0] * 21
counter = 0
for i in range(13):
    Canada_population[i] = round(Canada_dencity_of_population[i] * Canada_square / 13 / 1000) * 1000
    counter += Canada_population[i]

China_dencity_of_population = [0] * 21
China_dencity_of_population[0] = 23
China_dencity_of_population[1] = 21
China_dencity_of_population[2] = 25
China_dencity_of_population[3] = 30
China_dencity_of_population[4] = 70
China_dencity_of_population[5] = 60
China_dencity_of_population[6] = 160
China_dencity_of_population[7] = 80
China_dencity_of_population[8] = 100
China_dencity_of_population[9] = 650
China_dencity_of_population[10] = 300
China_dencity_of_population[11] = 146
China_square = 9.6 * 1000000

China_population = [0] * 21
counter = 0
for i in range(12):
    China_population[i] = round(China_dencity_of_population[i] * China_square / 12 / 1000) * 1000
    counter += China_population[i]

Germany_dencity_of_population = [0] * 21
Germany_dencity_of_population[0] = 450
Germany_dencity_of_population[1] = 280
Germany_dencity_of_population[2] = 200
Germany_dencity_of_population[3] = 170
Germany_dencity_of_population[4] = 140
Germany_dencity_of_population[5] = 250
Germany_dencity_of_population[6] = 150

Germany_square = 357 * 1000

Germany_population = [0] * 21
counter = 0
for i in range(7):
    Germany_population[i] = round(Germany_dencity_of_population[i] * Germany_square / 7 / 1000) * 1000
    counter += Germany_population[i]
print("Germany", counter)

India_dencity_of_population = [0] * 21
India_dencity_of_population[0] = 250
India_dencity_of_population[1] = 300
India_dencity_of_population[2] = 200
India_dencity_of_population[3] = 850
India_dencity_of_population[4] = 347
India_dencity_of_population[5] = 360
India_dencity_of_population[6] = 450
India_dencity_of_population[7] = 1278
India_dencity_of_population[8] = 400
India_dencity_of_population[9] = 500
India_square = 3.3 * 1000000

India_population = [0] * 21
counter = 0
for i in range(12):
    India_population[i] = round(India_dencity_of_population[i] * India_square / 10 / 1000) * 1000
    counter += India_population[i]

Mexica_dencity_of_population = [0] * 21
Mexica_dencity_of_population[0] = 20
Mexica_dencity_of_population[1] = 30
Mexica_dencity_of_population[2] = 22
Mexica_dencity_of_population[3] = 50
Mexica_dencity_of_population[4] = 200
Mexica_dencity_of_population[5] = 70
Mexica_dencity_of_population[6] = 60
Mexica_square = 2 * 1000000

Mexica_population = [0] * 21
counter = 0
for i in range(12):
    Mexica_population[i] = round(Mexica_dencity_of_population[i] * Mexica_square / 7 / 1000) * 1000
    counter += Mexica_population[i]

Russia_dencity_of_population = [0] * number_of_regions_in_Russia
Russia_dencity_of_population[0] = 12
Russia_dencity_of_population[1] = 22
Russia_dencity_of_population[2] = 15
Russia_dencity_of_population[3] = 15
Russia_dencity_of_population[4] = 8
Russia_dencity_of_population[5] = 35
Russia_dencity_of_population[6] = 25
Russia_dencity_of_population[7] = 5
Russia_dencity_of_population[8] = 14
Russia_dencity_of_population[9] = 12.7
Russia_dencity_of_population[10] = 0.11
Russia_dencity_of_population[11] = 1
Russia_dencity_of_population[12] = 5
Russia_dencity_of_population[13] = 9
Russia_dencity_of_population[14] = 0.12
Russia_dencity_of_population[15] = 0.3
Russia_dencity_of_population[16] = 0.05
Russia_dencity_of_population[17] = 0.14
Russia_dencity_of_population[18] = 0.13
Russia_dencity_of_population[19] = 0.12
Russia_dencity_of_population[20] = 0.11
Russia_square = 17.6 * 1000000

Russia_population = [0] * number_of_regions_in_Russia
counter = 0
for i in range(number_of_regions_in_Russia):
    Russia_population[i] = round(Russia_dencity_of_population[i] * Russia_square / 21 / 1000) * 1000
    counter += Russia_population[i]

Turkey_dencity_of_population = [0] * 21
Turkey_dencity_of_population[0] = 200
Turkey_dencity_of_population[1] = 220
Turkey_dencity_of_population[2] = 300
Turkey_dencity_of_population[3] = 70
Turkey_dencity_of_population[4] = 75
Turkey_dencity_of_population[5] = 100
Turkey_dencity_of_population[6] = 40
Turkey_dencity_of_population[7] = 35
Turkey_dencity_of_population[8] = 20
Turkey_dencity_of_population[9] = 40
Turkey_square = 785.6 * 1000

Turkey_population = [0] * 21
counter = 0
for i in range(13):
    Turkey_population[i] = round(Turkey_dencity_of_population[i] * Turkey_square / 10 / 1000) * 1000
    counter += Turkey_population[i]

USA_dencity_of_population = [0] * 21
USA_dencity_of_population[0] = 4
USA_dencity_of_population[1] = 3
USA_dencity_of_population[2] = 40
USA_dencity_of_population[3] = 60
USA_dencity_of_population[4] = 8
USA_dencity_of_population[5] = 15
USA_dencity_of_population[6] = 17
USA_dencity_of_population[7] = 8
USA_dencity_of_population[8] = 15
USA_dencity_of_population[9] = 40
USA_dencity_of_population[10] = 90
USA_dencity_of_population[11] = 70
USA_dencity_of_population[12] = 70
USA_square = 9.8 * 1000000

USA_population = [0] * 21
counter = 0
for i in range(13):
    USA_population[i] = round(USA_dencity_of_population[i] * USA_square / 13 / 1000) * 1000
    counter += USA_population[i]

Universal_population = [2000000, 2000000, 2000000, 10000000, 2000000, 2000000, 2000000]
Japan_dencity_of_population = [0] * 21
Japan_dencity_of_population[0] = 350
Japan_dencity_of_population[1] = 280
Japan_dencity_of_population[2] = 450
Japan_dencity_of_population[3] = 150
Japan_dencity_of_population[4] = 200
Japan_dencity_of_population[5] = 350
Japan_dencity_of_population[6] = 550
Japan_square = 378 * 10 ** 3
Japan_population = [0] * 21
counter = 0
for i in range(7):
    Japan_population[i] = round(Japan_dencity_of_population[i] * Japan_square / 7 / 1000) * 1000
    counter += Japan_population[i]

Argentina_z_ins = [0] * 21
Argentina_z_ins[0] = 1.2
Argentina_z_ins[1] = 1.2
Argentina_z_ins[2] = 1.9
Argentina_z_ins[3] = 1.1
Argentina_z_ins[4] = 1.3
Argentina_z_ins[5] = 3
Argentina_z_ins[6] = 2.2
Argentina_z_ins[7] = 1.2
Argentina_z_ins[8] = 0.9

Australia_z_ins = [0] * 21
Australia_z_ins[0] = 1
Australia_z_ins[1] = 1
Australia_z_ins[2] = 1
Australia_z_ins[3] = 0.8
Australia_z_ins[4] = 1
Australia_z_ins[5] = 0.8
Australia_z_ins[6] = 1
Australia_z_ins[7] = 1.5
Australia_z_ins[8] = 0.8
Australia_z_ins[9] = 1.3
Australia_z_ins[10] = 1.8
Australia_z_ins[11] = 1.8

Brazilia_z_ins = [0] * 21
Brazilia_z_ins[0] = 0.9
Brazilia_z_ins[1] = 1.1
Brazilia_z_ins[2] = 0.9
Brazilia_z_ins[3] = 1
Brazilia_z_ins[4] = 1
Brazilia_z_ins[5] = 1.3
Brazilia_z_ins[6] = 1.3
Brazilia_z_ins[7] = 2.1
Brazilia_z_ins[8] = 1.8
Brazilia_z_ins[9] = 2.3
Brazilia_z_ins[10] = 3.1

Canada_z_ins = [0] * 21
Canada_z_ins[0] = 0.8
Canada_z_ins[1] = 0.9
Canada_z_ins[2] = 0.8
Canada_z_ins[3] = 1
Canada_z_ins[4] = 0.7
Canada_z_ins[5] = 1
Canada_z_ins[6] = 1
Canada_z_ins[7] = 0.7
Canada_z_ins[8] = 1
Canada_z_ins[9] = 1.4
Canada_z_ins[10] = 0.8
Canada_z_ins[11] = 1.5
Canada_z_ins[12] = 1.3

China_z_ins = [0] * 21
China_z_ins[0] = 1
China_z_ins[1] = 1
China_z_ins[2] = 1.1
China_z_ins[3] = 1.1
China_z_ins[4] = 1.3
China_z_ins[5] = 1.3
China_z_ins[6] = 1.8
China_z_ins[7] = 1.3
China_z_ins[8] = 1.4
China_z_ins[9] = 3.3
China_z_ins[10] = 2.0
China_z_ins[11] = 1.8

Germany_z_ins = [0] * 21
Germany_z_ins[0] = 2
Germany_z_ins[1] = 1.6
Germany_z_ins[2] = 1.4
Germany_z_ins[3] = 1.3
Germany_z_ins[4] = 1.5
Germany_z_ins[5] = 1.8
Germany_z_ins[6] = 1.4

India_z_ins = [0] * 21
India_z_ins[0] = 2.1
India_z_ins[1] = 2.1
India_z_ins[2] = 2
India_z_ins[3] = 3
India_z_ins[4] = 2.3
India_z_ins[5] = 2.3
India_z_ins[6] = 2.6
India_z_ins[7] = 4
India_z_ins[8] = 2.4
India_z_ins[9] = 2.5

Mexica_z_ins = [0] * 21
Mexica_z_ins[0] = 1.2
Mexica_z_ins[1] = 1.3
Mexica_z_ins[2] = 1.2
Mexica_z_ins[3] = 1.3
Mexica_z_ins[4] = 3
Mexica_z_ins[5] = 1.5
Mexica_z_ins[6] = 1.4

Russia_z_ins = [0] * 21
Russia_z_ins[0] = 1.3
Russia_z_ins[1] = 1.5
Russia_z_ins[2] = 1.1
Russia_z_ins[3] = 1.6
Russia_z_ins[4] = 1
Russia_z_ins[5] = 2.5
Russia_z_ins[6] = 1.3
Russia_z_ins[7] = 1.1
Russia_z_ins[8] = 1
Russia_z_ins[9] = 1.1
Russia_z_ins[10] = 0.9
Russia_z_ins[11] = 0.9
Russia_z_ins[12] = 0.9
Russia_z_ins[13] = 1
Russia_z_ins[14] = 0.9
Russia_z_ins[15] = 1
Russia_z_ins[16] = 0.8
Russia_z_ins[17] = 1.3
Russia_z_ins[18] = 1
Russia_z_ins[19] = 1
Russia_z_ins[20] = 1

Turkey_z_ins = [0] * 21
Turkey_z_ins[0] = 1.2
Turkey_z_ins[1] = 1.2
Turkey_z_ins[2] = 2.5
Turkey_z_ins[3] = 1.2
Turkey_z_ins[4] = 1.4
Turkey_z_ins[5] = 1.1
Turkey_z_ins[6] = 1.2
Turkey_z_ins[7] = 1
Turkey_z_ins[8] = .9
Turkey_z_ins[9] = 1
Turkey_z_ins[10] = .9
Turkey_z_ins[11] = 1

USA_z_ins = [0] * 21
USA_z_ins[0] = 0.95
USA_z_ins[1] = 0.9
USA_z_ins[2] = 1.8
USA_z_ins[3] = 2.0
USA_z_ins[4] = 1
USA_z_ins[5] = 1
USA_z_ins[6] = 1.1
USA_z_ins[7] = 1
USA_z_ins[8] = 1
USA_z_ins[9] = 1.5
USA_z_ins[10] = 2.6
USA_z_ins[11] = 1.8
USA_z_ins[12] = 2.3

Japan_z_ins = [0] * 21
Japan_z_ins[0] = 1.9
Japan_z_ins[1] = 2.0
Japan_z_ins[2] = 2.8
Japan_z_ins[3] = 1.4
Japan_z_ins[4] = 1.8
Japan_z_ins[5] = 2.1
Japan_z_ins[6] = 3.2

Universal_z_ins = [1] * 7
Universal_z_ins[3] = 2

# widthes are in side, heights - in height of hex
Argentina_width = 7
Argentina_height = 4.5
Australia_width = 8
Brazilia_width = 6.5
Brazilia_height = 4.5
Australia_height = 3.5
Canada_width = 9.5
Canada_height = 3.5
China_width = 8
China_height = 4
India_width = 6
India_height = 5
Mexica_width = 6
Mexica_height = 4
Russia_width = 14
Russia_height = 4
USA_width = 11
USA_height = 4

Argentina_dy = 1
Australia_dy = 2
Brazilia_dy = 1.5
Canada_dy = 2
China_dy = 2
India_dy = 1.5
Mexica_dy = 1
Russia_dy = 1.5
USA_dy = 1.5

income_of_Argentina = 14
income_of_Australia = 13
income_of_Brazilia = 17
income_of_Canada = 15
income_of_China = 22
income_of_Germany = 19
income_of_India = 20
income_of_Mexica = 13
income_of_Russia = 22
income_of_Turkey = 17
income_of_USA = 24
income_of_Japan = 23

stars_of_Argentina = 7
stars_of_Australia = 5
stars_of_Brazil = 9
stars_of_Canada = 2
stars_of_China = 8
stars_of_India = 15
stars_of_Mexico = 7
stars_of_Russia = 12
stars_of_Turkey = 4
stars_of_USA = 5
stars_of_Japan = 6
stars_of_Germany = 4

levels = [4, 5, 6,
          9, 2, 5,
          4, 8, 4,
          1, 4, 4,
          3]
# австр, арг, браз, инд, кан, кит, мекс, рос, сша, уни, яп, турц, герм
crit_penalty_points = [25, 35, 35,
                       50, 20, 28,
                       30, 40, 23,
                       25, 28, 28,
                       23]
country_open_min_rep_status = [0] * 13
country_open_min_rep_status[2] = 63  # brazil
country_open_min_rep_status[3] = 148  # india
country_open_min_rep_status[10] = 26  # for japan

country_open_min_coins_status = [0] * 13
country_open_min_coins_status[11] = 37  # for Turkey
country_open_min_coins_status[5] = 550  # for China
country_open_min_coins_status[0] = 320  # for Australia

carts = [Australia_cart, Argentina_cart, Brazilia_cart, India_cart, Canada_cart, China_cart,
         Mexica_cart, Russia_cart, USA_cart, Universal_cart, Japan_cart, Turkey_cart, Germany_cart]

names_of_provinces = [Australia_names, Argentina_names, Brazil_names, India_names, Canada_names, China_names,
                      Mexico_names, Russia_names, USA_names, Universal_names, Japan_names, Turkey_names, Germany_names]

ups_by_y = [0] * 13  # массив самых верхних координат гексов на карте страны
for i in range(len(carts)):
    ups_by_y[i] = carts[i][0][1]
    for j in range(len(carts[i])):
        if ups_by_y[i] > carts[i][j][1] + (carts[i][j][0] % 2) / 2:
            ups_by_y[i] = carts[i][j][1] + (carts[i][j][0] % 2) / 2

number_of_regions = [number_of_regions_in_Australia, number_of_regions_in_Argentina, number_of_regions_in_Brazilia,
                     number_of_regions_in_India, number_of_regions_in_Canada, number_of_regions_in_China,
                     number_of_regions_in_Mexica, number_of_regions_in_Russia, number_of_regions_in_USA,
                     7, 7, 10,
                     7]

ind_capitals = [capital_of_Australia, capital_of_Argentina, capital_of_Brazilia, capital_of_India,
                capital_of_Canada, capital_of_China, capital_of_Mexica, capital_of_Russia, capital_of_USA, 3, 6, 2, 5]

dencity_of_population = [Australia_dencity_of_population, Argentina_dencity_of_population,
                         Brazilia_dencity_of_population, India_dencity_of_population,
                         Canada_dencity_of_population, China_dencity_of_population,
                         Mexica_dencity_of_population, Russia_dencity_of_population,
                         USA_dencity_of_population, [5] * 7, Japan_dencity_of_population,
                         Turkey_dencity_of_population, Germany_dencity_of_population]

population = [Australia_population, Argentina_population, Brazilia_population, India_population,
              Canada_population, China_population, Mexica_population,
              Russia_population, USA_population, Universal_population, Japan_population,
              Turkey_population, Germany_population]

incomes = [income_of_Australia, income_of_Argentina, income_of_Brazilia, income_of_India,
           income_of_Canada, income_of_China, income_of_Mexica, income_of_Russia, income_of_USA,
           15, income_of_Japan, income_of_Turkey, income_of_Germany]

widthes = [Australia_width, Argentina_width, Brazilia_width,
           India_width, Canada_width, China_width,
           Mexica_width, Russia_width, USA_width,
           5, 5, 8,
           5]

heightes = [Australia_height, Argentina_height, Brazilia_height, India_height, Canada_height,
            China_height, Mexica_height, Russia_height, USA_height, 3, 5, 2.5, 3.5]

real_widthes = [4200, 2300, 4300,
                2700, 6600, 5300,
                2500, 11700, 7600,
                1100, 1000, 1500,
                650]  # в тысячах километров

countries_z_ins = [Australia_z_ins, Argentina_z_ins, Brazilia_z_ins, India_z_ins,
                   Canada_z_ins, China_z_ins, Mexica_z_ins, Russia_z_ins, USA_z_ins,
                   Universal_z_ins, Japan_z_ins, Turkey_z_ins, Germany_z_ins]

country_coefs_base = [.8, 1.2, 1, 2,
                      .8, 1.2, 1.1,
                      .9, 2, 1,
                      .8, 1.1, 1,
                      1]  # coeff of perenos
country_dy = [Australia_dy, Argentina_dy, Brazilia_dy,
              India_dy, Canada_dy, China_dy,
              Mexica_dy, Russia_dy, USA_dy,
              1.5, 5, 1.5,
              1.5]
country_stars = [stars_of_Australia, stars_of_Argentina, stars_of_Brazil,
                 stars_of_India, stars_of_Canada, stars_of_China,
                 stars_of_Mexico, stars_of_Russia, stars_of_USA,
                 1, stars_of_Japan, stars_of_Turkey,
                 stars_of_Germany]
country_fluctuation_z_out = [0.5, 0.7, 0.6, 0.65,
                             1.2, 0.9, 0.6, 1.3,
                             1.1, 0, 1.05, 0.7,
                             1]  # чем больше, тем сильнее зависит от сезона коэффициент
colors_of_name = ["069719", "c6a729", "c66709",
                  "86b759", "7677ff", "f63069",
                  "66ef79", "e60719", "f69739",
                  "a6c329", "2637ff", "e1eb34",
                  "ad6e2f"]
hemispheres = [0, 0, 0,
               1, 1, 1,
               1, 1, 1,
               1, 1, 1,
               1]  # полушария

country_names = [["Австралия", "Australia"],
                 ["Аргентина", "Argentina"],
                 ["Бразилия", "Brazil"],
                 ["Индия", "India"],
                 ["Канада", "Canada"],
                 ["Китай", "China"],
                 ["Мексика", "Mexico"],
                 ["Россия", "Russia"],
                 ["США", "USA"],
                 ["Универсальная", "Universal"],
                 ["Япония", "Japan"],
                 ["Турция", "Turkey"],
                 ["Германия", "Germany"]
                 ]

flags_source = ["00_australia", "01_argentina", "02_brazil", "03_india", "04_canada",
                "05_china", "06_mexico", "07_russia", "08_usa", "09_usa", "10_japan",
                "11_turkey", "12_germany"]

pp_names = ["Австралии", "Аргентине", "Бразилии",
            "Индии", "Канаде", "Китае",
            "Мексике", "России", "США",
            "Универсальной", "Японии", "Турции",
            "Германии"]

Country_lands = [None] * 13
for i in range(13):
    Country_lands[i] = Land(index=i,
                            Cart_of_country=carts[i],
                            Number_of_regions=number_of_regions[i],
                            Capital_index=ind_capitals[i],
                            dens=dencity_of_population[i],
                            pop=population[i],
                            income_of_c=incomes[i],
                            size=(widthes[i], heightes[i]),
                            la_z_ins=countries_z_ins[i],
                            stars=country_stars[i],
                            level=levels[i],
                            name=country_names[i],
                            dy=country_dy[i],
                            min_reputation_status=country_open_min_rep_status[i],
                            min_coins_status=country_open_min_coins_status[i],
                            fluct_z_out=country_fluctuation_z_out[i],
                            ups_by_y=ups_by_y[i],
                            real_size_of_hex=real_widthes[i] / widthes[i],
                            color_of_name=colors_of_name[i],
                            hemisphere=hemispheres[i],
                            coef_perenos=country_coefs_base[i],
                            crit_b=crit_penalty_points[i],
                            prepositional_case=pp_names[i],
                            names_of_provinces=names_of_provinces[i])

Argentina_land = Country_lands[1]

Australia_land = Country_lands[0]

Brazilia_land = Country_lands[2]

Canada_land = Country_lands[4]

China_land = Country_lands[5]

India_land = Country_lands[3]

Mexica_land = Country_lands[6]

Russia_land = Country_lands[7]

USA_land = Country_lands[8]
# 9 - Universal, 10 - Japan, 11 - Germany


# indexes_of_lands: Австралия - 1, Аргентина - 2, Бразилия - 3, Индия - 4, Канада - 5, Китай - 6, Мексика - 7, Россия - 8, США - 9
numbers_in_menu_ru = [7] * 13
numbers_in_menu_ru[0] = Australia_land
numbers_in_menu_ru[1] = Argentina_land
numbers_in_menu_ru[2] = Brazilia_land
numbers_in_menu_ru[3] = Country_lands[12]  # Germany
numbers_in_menu_ru[4] = India_land
numbers_in_menu_ru[5] = Canada_land
numbers_in_menu_ru[6] = China_land
numbers_in_menu_ru[7] = Mexica_land
numbers_in_menu_ru[8] = Russia_land
numbers_in_menu_ru[9] = Country_lands[11]  # Turkey
numbers_in_menu_ru[10] = USA_land
numbers_in_menu_ru[11] = Country_lands[9]  # Universal
numbers_in_menu_ru[12] = Country_lands[10]  # Japan

numbers_in_menu_en = [8] * 13
numbers_in_menu_en[0] = Argentina_land
numbers_in_menu_en[1] = Australia_land
numbers_in_menu_en[2] = Brazilia_land
numbers_in_menu_en[3] = Canada_land
numbers_in_menu_en[4] = China_land
numbers_in_menu_en[5] = Country_lands[12]  # Germany
numbers_in_menu_en[6] = India_land
numbers_in_menu_en[7] = Country_lands[10]  # Japan
numbers_in_menu_en[8] = Mexica_land
numbers_in_menu_en[9] = Russia_land
numbers_in_menu_en[10] = Country_lands[11]  # Turkey
numbers_in_menu_en[11] = Country_lands[9]  # Universal
numbers_in_menu_en[12] = USA_land

numbers_in_menu = [numbers_in_menu_ru, numbers_in_menu_en]

'''
триплеты базовых для каждой из стран технологий при законотворческом режиме (там они доступны в панели технологий)
или при режиме (новая эпидемия). Там они уже исследованы.

австралия: отмена авиа, ограничение сообщения, повышение налогов
аргентина: 
бразилия:
индия:
канада: запрет авиаперевозок, 
китай: инвестиции в больницы, жёсткий карантин, инвестиции в производство 
мексика: 
россия: искажение данных, пропаганда, жёсткий карантин.
сша: денежная эмиссия, инвестиции в исследования, массовые тесты.
турция:
универсальная: изолировать
япония: маски и перчатки, инвестиции в исследования
'''
