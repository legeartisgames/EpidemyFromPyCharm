import math
import socket

import common_var


def status_finder(typ, value):
    # function returns [level of status, objects for next status]
    if typ == 'stars':
        for i in range(len(common_var.thresh_hold_stars) - 1):
            if value < common_var.thresh_hold_stars[i + 1]:
                return [i, round(common_var.thresh_hold_stars[i + 1] - value, 1)]

    if typ == 'coins':
        for i in range(len(common_var.thresh_hold_coins) - 1):
            if value < common_var.thresh_hold_coins[i + 1]:
                return [i, round(common_var.thresh_hold_coins[i + 1] - value, 1)]


def update_texts():
    for i in common_var.list_of_btns:
        i.text = i.text_source[common_var.lang]


def tri_sep(x):
    answer = ''
    u = 1
    while 10 ** (3 * u - 3) <= x:
        val = math.floor((x % (10 ** (3 * u))) / (10 ** (3 * u - 3)))
        f = str(val)
        if 10 ** (3 * u) <= x:
            if len(f) == 0:
                f = '000' + f
            if len(f) == 1:
                f = '00' + f
            if len(f) == 2:
                f = '0' + f

        if answer != '':
            answer = f + ' ' + answer
        else:
            answer = f
        u += 1
    if x == 0:
        answer = "0"
    return answer


def del_sep(x):
    answer = x.replace(' ', '')
    return answer


def to_rgba(string):
    h = string.strip()
    answer = list(int(h[i:i + 2], 16) / 256 for i in (0, 2, 4))
    answer.append(1)
    return answer


'''
def rp_pen_poins(val):
    if val % 10 == 1 and val != 11:
        return "штрафного балла"
    else:
        return "штрафных баллов"
'''


def fin_of_word(val, rod):
    if rod == 0:  # женский
        if val % 10 == 1 and val != 11:
            return "а"
        elif 1 < val % 10 < 5 and (val > 20 or val < 10):
            return "ы"
        else:
            return ""
    if rod == 1:  # мужской
        if 2 <= val % 10 <= 4 and (val < 10 or val > 10):
            return "а"
        else:
            return ""


def generate_str_date(date):
    if common_var.lang == 0:

        answer = ''
        if date[0] < 10:
            answer += '0'
        answer += str(date[0]) + '.'
        if date[1] < 10:
            answer += '0'
        answer += str(date[1]) + '.' + str(date[2])
    else:
        answer = str(date[2]) + '-' + '0' * (date[1] < 10) + str(date[1]) + '-' + '0' * (date[0] < 10) + str(date[0])

    return answer


def two_weeks_go(date):  # really uses as 1 month
    date_new = list(date)

    date_new[0] = 1
    if date[1] == 12:
        date_new[1] = 1
        date_new[2] += 1
    else:
        date_new[1] += 1
    return date_new


def month_back(date):
    date_new = list(date)

    date_new[0] = 1
    if date[1] == 1:
        date_new[1] = 12
        date_new[2] -= 1
    else:
        date_new[1] -= 1
    return date_new


def date_go(date, days=1):  # days < 31!
    # 0- days, 1-months, 2-years
    date_new = list(date)
    if date[1] in {4, 6, 9, 11}:
        if date[0] + days > 30:
            date_new[0] = date[0] + days - 30
            date_new[1] += 1
        else:
            date_new[0] += days
    elif date[1] in {1, 3, 5, 7, 8, 10, 12}:
        if date[0] + days > 31:
            date_new[0] = date[0] + days - 31
            if date[1] == 12:
                date_new[1] = 1
                date_new[2] += 1
            else:
                date_new[1] += 1
        else:
            date_new[0] += days
    elif date[1] == 2:
        if date[2] % 4 == 0:
            if date[0] + days > 29:
                date_new[0] = date[0] + days - 29
                date_new[1] += 1
            else:
                date_new[0] += days

        else:
            if date[0] + days > 28:
                date_new[0] = date[0] + days - 28
                date_new[1] += 1
            else:
                date_new[0] += days
    return date_new


def is_internet():
    try:
        sock = socket.create_connection(('8.8.8.8', 53), timeout=1.5)
        sock.close()
        ind = True
    except:
        print("No internet!\n")
        ind = False
    return ind
