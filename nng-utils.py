# -*- coding: utf-8 -*-

# NNG UTILS 1.2 UNSTABLE

# Импорт библиотек
import vk_api
import requests
import urllib.request
import webbrowser
import datetime
import os
import re
from time import sleep
from sys import exit
from time import monotonic
from tempfile import gettempdir

# Подкрутки
DEBUG_MODE = True  # Откладочная информация. Поможет в случае возникновения бага.
tokenMode = False # Если отключить, то можно попасть в программу и без токена.
captchaTimer = 15  # Задержка после каптчи в секундах

# Данные для входа и авторизации в VK API | NOTE: Обязательно, получить можно по ссылке 'https://vk.cc/av5aLJ'.
# Скопировать из URL'а (access_token=xxxxx...) в переменную.
token = str("xxxxx")
if os.name == 'nt':
    ostype = str("windows")
elif os.name == 'mac':
    ostype = str("macos")
else:
    ostype = str("linux")

# URL группы | NOTE: Обязательно для работы с функциями: Бан, Выдача редактора, Мультибан, Редактирование настроек.
groupId = str("")

# Комментарий бана | NOTE: Обязательно для работы с функциями: Бан, Мультибан.
com = str("Блокировка после решения Администрации | По вопросам: https://vk.me/mralonas")

# URL сайта со списком на бан (raw .txt, ID через запятую) | NOTE: Обязательно для работы с функциями: Бан, Мультибан.
banurl = str("https://nng.alonas.ml/bnnd/rawline.txt")

# URL сайта со списком групп на бан (raw .txt, ID через запятую) (указывать вместе с основной группой) | NOTE: Обязательно для работы с функциями: Мультибан, Поиск по группам, Мультибанчек.
groupurl = str("https://nng.alonas.ml/lst/rawline.txt")

# Переменные с пользователем на поиск | user_id - для поиска 1 человека. user_ids - для поиска множества людей. NOTE: в usedr_ids указывать список, например: "344563175, 5423813428, 4234534325" | NOTE: Обязательно для работы с функцией: Поиск по группам.
user_id = str("")
user_ids = str("")

# Настройки для создания новой группы | https://vk.com/dev/groups.create | NOTE: Обязательно для работы с функциями:
# Создание группы
create_settings = {'title': ' ฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺ',
                   'description': 'Это сообщество не имеет никакого отношения к администрации ВКонтакте.\n\nПросьба ознакомиться с FAQ — https://nng.alonas.ml\n\nСпасибо.',
                   'type': 'group'}

# Настройки группы через метод Groups.Edit | https://vk.com/dev/groups.edit | NOTE: Обязательно для работы с функциями: Редактирование настроек группы
settings = {'group_id': id(groupId), 'title': ' ฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺฺ',
            'description': 'Это сообщество не имеет никакого отношения к администрации ВКонтакте.\n\nПросьба ознакомиться с FAQ — https://nng.alonas.ml\n\nСпасибо.',
            'website': 'https://vk.com/mralonas', 'screen_name': '0', 'messages': 0, 'access': 0, 'wall': 0,
            'topics': 0, 'photos': 0, 'video': 0, 'audio': 0, 'age_limits': 1, 'market': 0,
            'photo_url': 'https://nng.alonas.ml/img/lgo.png', 'cover_url': 'https://nng.alonas.ml/img/cvr.jpg'}

# Список screen_name для функции преобразования в ID | Необходимо указать количество пользователей и их screen_name либо ID, также можно указать ссылки, но тогда нужно выбрать преобразование из ссылок в меню | NOTE: Обязательно для работы с функцией: Преобразование в ID
# Пример записи: ids = {'count': 2, 'items': 'https://vk.com/screen_name,https://vk.com/screen_name2'} или {'count': 2, 'items': 'screen_name, screen_name2'}
ids = {'count': 1, 'items': 'screen_name'}

# URL сайта с приоритеным списком | NOTE: Обязательно для работы с функциями: Приоритетная выдача.
priority_list = str("")

# URL сайта с приоритеным списком | NOTE: Обязательно для работы с функциями: Неприоритетная выдача.
exception_list = str("")

if tokenMode:
    # Авторизация в VK API и начало сессии
    try:
        token = vk_api.VkApi(token=token)
        vk = token.get_api()
        name = vk.account.getProfileInfo()
        surname = name.get('last_name')
        userid = name.get('id')
        name = name.get('first_name')
    except Exception as Error:
        print(
            "Возможно Ваш access token недейстителен или перестал действовать, получите новый и впишите его в скрипт.\n")
        while True:
            sdf = str(input("Выйдите из программы и введите правильные данные!\n"))
            if sdf == "exit" or "q":
                exit()


# Функции
def color():
    if tokenMode:
        if ostype == "windows":
            os.system('cls')
            os.system('color a')
            print("\n[-- NNG UTILS --]\n\n1.2 Unstable | Авторизован в качестве", name, surname, "ID:", userid)
        else:
            os.system('clear')
            print("\n[-- NNG UTILS --]\n\n1.2 Unstable | Авторизован в качестве", name, surname, "ID:", userid)
    else:
        if ostype == "windows":
            os.system('cls')
            os.system('color a')
            print("\n[-- NNG UTILS --]\n\n1.2 Unstable | tokenMode выключен | Авторизация отключена")
        else:
            os.system('clear')
            print("\n[-- NNG UTILS --]\n\n1.2 Unstable | tokenMode выключен | Авторизация отключена")


def nIsDigit(object):
    if not object.isdigit():
        object = re.sub(r'\n', '', object)
        return object
    else:
        return object

def datacheckReturn(user):
    url = 'https://vk.com/foaf.php?id=' + str(user)
    test = requests.get(url).text
    with open("data.xml", 'w') as f:
        f.write(str(test))
    tree = ET.parse('data.xml')
    root = tree.getroot()

def datacheck(api, user):
    pass

def groupcheck(api, user, users):
    a=0
    for i in users:
        if i == user:
            if DEBUG_MODE==True:
                print('[GroupCheck]: found ',i,' in list. count =',a,'\n')
            a+=1
    if a>5:
        return False
    else:
        return True

def clear():
    if ostype == "windows":
        os.system('cls')
    else:
        os.system('clear')


def banCheck(api, user, banned):
    output = []
    for i in range(len(user)):
        for b in range(len(banned)):
            if str(user[i]) == str(banned[b]):
                output.append(user[i])
    if output:
        return output
    else:
        return False


def getAllMembers(api, groups):
    try:
        a = [0] * len(groups)
        for i in range(len(groups)):
            if DEBUG_MODE:
                print('Group https://vk.com/club{}'.format(groups[i]))
            answer = api.groups.getMembers(group_id=id(groups[i]), sort='time_asc')
            if answer.get('count') > 1000:
                if answer.get('count') > 2000:
                    if answer.get('count') > 3000:
                        return 0
                    else:
                        answer2 = api.groups.getMembers(group_id=id(groups[i]), sort='time_asc', offset='1000')
                        answer3 = api.groups.getMembers(group_id=id(groups[i]), sort='time_asc', offset='2000')
                        a[i] = answer.get('items') + answer2.get('items') + answer3.get('items')
                else:
                    answer2 = api.groups.getMembers(group_id=id(groups[i]), sort='time_asc', offset='1000')
                    a[i] = answer.get('items') + answer2.get('items')
            else:
                a[i] = answer.get('items')
        return a

    except vk_api.exceptions.AccountBlocked as Error:
        if DEBUG_MODE:
            print(Error)
        pass
    except vk_api.exceptions.ApiError as Error:
        if DEBUG_MODE:
            print(Error)
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if DEBUG_MODE:
            print(Error)
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)


def timer():
    print("Таймер запущен!")
    current_time = monotonic()
    return current_time


def menu():
    color()
    print(
        "\n\n1.Бан\n\n2.Выдача редактора [UNSTABLE]\n\n3.Мультибан\n\n4.Разбан\n\n5.Создание "
        "сообщества\n\n6.Настройка сообщества\n\n7.Преобразование screen_name пользователей в ID\n\n8.Поиск по "
        "группам\n\n9.Снять все права\n\n10.Банчек\n\n11.Мультибанчек\n\n")
    choose = str(input(">"))
    if choose == "1":
        color()
        choose = str(input(
            "Выбрана операция: Бан\n\n1.Выполнить\n\n2.Выполнить с режимом 'без каптчи'\n\n3.Выполнить с режимом "
            "исключения без каптчи.\n\n4.Выйти\n\n\n>"))
        choose = "1" + choose
        if choose == "11":
            color()
            return choose
        elif choose == "12":
            color()
            return choose
        elif choose == "13":
            color()
            return choose
        else:
            menu()
    elif choose == "2":
        color()
        choose = "2" + str(input(
            "Выбрана опцерация: Выдача редактора.\n\n\n1.Выполнить\n\n2.Выполнить с приоритетным "
            "списком\n\n3.Выполнить с исключением\n\n4.Выполнить с групчеком и банчеком [UNSTABLE]\n\n5.Выйти\n\n\n>"))
        if choose == "21" or choose == "22" or choose == "23" or choose == "24":
            return choose
        else:
            menu()
    elif choose == "3":
        color()
        choose = "3" + str(
            input("Выбрана операция: Мультибан\n\n1.Выполнить\n\n2.Выполнить с режимом 'без каптчи'\n\n3.Выйти\n\n>"))
        if choose == "31" or choose == "32":
            color()
            return choose
        else:
            menu()
    elif choose == "4":
        color()
        choose = "4" + str(input(
            "Выбрана операция: Разбан всех участников в группе\n\n1.Выполнить\n\n2.Выполнить с режимом 'без "
            "каптчи'\n\n3.Разбанить пользователя во всех группах\n\n4.Выйти\n\n\n>"))
        if choose == "41" or choose == "42" or choose == "43":
            return choose
        else:
            menu()
    elif choose == "5":
        color()
        choose = "5" + str(input("Выбрана операция: Создание сообщества \n\n1.Выполнить\n\n2.Выйти\n\n\n>"))
        if choose == "51":
            return choose
        else:
            menu()
    elif choose == "6":
        choose = "6" + str(input("Выбрана операция: Настрокйка сообщества \n\n1.Выполнить\n\n2.Выйти\n\n\n>"))
        color()
        return choose
        if choose == "61":
            return choose
        else:
            menu()
    elif choose == "7":
        color()
        choose = "7" + str(input(
            "Выбрана операция: Преобразоване screen_name в ID \n\n1.Выполнить, вернуть ссылки\n\n2.Выполнить, "
            "вернуть ID\n\n3.Выполнить, принять ссылки и вернуть ссылки\n\n4.Выйти\n\n\n>"))
        if choose == "71" or choose == "72" or choose == "73":
            return choose
        else:
            menu()
    elif choose == "8":
        color()
        choose = "8" + str(input(
            "Выбрана операция: Поиск по группам.\n\n1.Выполнить поиск человека в группе\n\n2.Выполнить поиск людей в "
            "группе\n\n3.Вполнить поиск человека в группах\n\n4.Выйти\n\n>"))
        if choose == "81" or choose == "82" or choose == "83":
            return choose
        else:
            menu()
    elif choose == "9":
        color()
        choose = "9" + str(input(
            "\n\n\nВыбрана операция: Снятие всех прав.\n\n1.Выполнить\n\n2.Выполнить, снять права у заблокированных "
            "или удаленных страниц\n\n3.Снять права у пользователя во всех группах\n\n4.Выйти\n\n\n>"))
        if choose == "91" or choose == "92" or choose == "93":
            return choose
        else:
            menu()

    elif choose == "10":
        color()
        choose = "10" + str(input(
            "Выбрана операция: Банчек\n\n1.Выполнить\n\n2.Выполнить, снять права у пользователей и заблокировать их ["
            "BETA]\n\n3.Выйти\n\n\n>"))
        if choose == "101" or choose == "102":
            return choose
        else:
            menu()

    elif choose == "11":
        color()
        choose = "11" + str(input(
            "Выбрана операция: Мультибанчек\n\n1.Выполнить\n\n2.Выполнить, снять права у пользователей и "
            "заблокировать их\n\n3.Выйти\n\n\n>"))
        if choose == "111" or choose == "112":
            return choose
        else:
            menu()

    elif choose == "q" or choose == "quit" or choose == "" or choose == " " or choose == "\n":
        exit()

    else:
        fail()
        menu()

def fail():
    print("\n\nОшибка ввода!\n")
    sleep(1)
    color()


def id(idg):
    group = vk.groups.getById(group_ids=idg)
    idg = group[0].get('id')
    return idg


def captcha_handler(captcha):
    webbrowser.open_new(captcha.get_url())
    key = input("Введите код каптчи: {0}: ".format(captcha.get_url())).strip()
    try:
        captcha.try_again(key)
    except vk_api.exceptions.Captcha as captcha:
        print("Неправильный ввод каптчи! Попробуйте снова.\n")
        captcha_handler(captcha)
        color()


def download(setting):
    response = requests.get(settings.get(setting))
    filename = settings.get(setting).split('/')[-1]
    if ostype == 'windows':
        file = open(str(gettempdir()) + '\\' + filename, "wb")
    else:
        file = open("/tmp/" + filename, "wb")
    file.write(response.content)
    file.close()


def cut(listt):
    answer = str(input("Обрезать количество участников на какое-то число (введите -1, чтобы не обрезать список): "))
    if answer == "-1":
        return listt
    else:
        try:
            count = int(answer)
        except ValueError:
            print("Введите, пожалуйста, число!\n")
            cut(listt)
        except IndexError:
            print("Введите, пожалуйста, число, которое будет меньше самого списка.")
            cut(listt)
    list1 = []
    for i in range(int(count)):
        list1.append(listt[i])
    return list1


def getAllPosts(api, group):
    answer = api.wall.get(owner_id=-id(group))
    listt = answer
    answer = answer.get('items')
    for i in range(int(listt.get('count'))):
        answer[i] = answer[i].get('id')
    return answer


def deletePosts(api, group, posts):
    try:
        for i in range(len(posts)):
            answer = api.wall.delete(owner_id=-id(group), post_id=posts[i])
            if DEBUG_MODE:
                print('Удалили пост', posts[i], 'из сообщества', id(group))
    except vk_api.exceptions.AccountBlocked as Error:
        if DEBUG_MODE:
            print(Error)
        pass
    except vk_api.exceptions.ApiError as Error:
        if DEBUG_MODE:
            print(Error)
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if DEBUG_MODE:
            print(Error)
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    return True


def isMember(users, group):
    try:
        answer = vk.groups.isMember(group_id=id(group), user_ids=users)
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    answer_isMember = [0] * len(answer)
    answer_ids = [0] * len(answer)
    for i in range(len(answer)):
        answer_isMember[i] = answer[i].get('member')
        answer_ids[i] = answer[i].get('user_id')
    if DEBUG_MODE:
        print(answer, "\n", answer_ids, "\n", answer_isMember, sep='')
    for i in range(len(answer)):
        if answer_isMember[i] == 1:
            pass
        else:
            del answer_ids[i]
    return answer_ids


# Меню
choose = menu()

# Локальные переменные для обработки
a = 0
log = []
flog = []
groups = urllib.request.urlopen(groupurl).read().decode().split(',')

# При выборе бана с каптчой
if choose == "11":
    # Импорт текста из URL (текст должен быть отформатирован в одну строчку и через запятую)
    s = urllib.request.urlopen(banurl).read().decode()

    # Создание массива из текста s.
    banned = s.split(',')
    banned = list(banned)

    # Считаем количество элементов в массиве "banned"
    count = len(banned)
    print("Количество пользователей:", count, sep='')

    # Бан через цикл с иключениями ошибок
    n = 0
    while n != count:
        try:
            result = vk.groups.ban(group_id=id(groupId), owner_id=int(banned[n]), reason=0, comment=com,
                                   comment_visible=1)
            if result == 1:
                print("Забанили: https://vk.com/id", banned[n], sep='')
                log.append(banned[n])
            else:
                "Что-то пошло не так."
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён или заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
    print("Завершено!")
    # Логи
    if a >= 1:
        print("Не удалось забанить следующих ID:\n", flog, "\nКоличество аккаунтов: ", a, sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')

# При выборе бана без каптчи
elif choose == "12":
    # Импорт текста из URL (текст должен быть отформатирован в одну строчку и через запятую)
    s = urllib.request.urlopen(banurl).read().decode()

    # Создание массива из текста s.
    banned = s.split(',')
    banned = list(banned)

    # Считаем количество элементов в массиве "banned"
    count = len(banned)
    print("Количество пользователей: ", count, sep='')

    # Бан через цикл с иключениями ошибок
    n = 0
    while n != count:
        try:
            result = vk.groups.ban(group_id=id(groupId), owner_id=int(banned[n]), reason=0, comment=com,
                                   comment_visible=1)
            if result == 1:
                print("Забанили: https://vk.com/id", banned[n], sep='')
                log.append(banned[n])
            else:
                "Что-то пошло не так."
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён или заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            if DEBUG_MODE:
                print("Каптча. Ждем 15 секунд")
            sleep(15)
            pass
    print("Завершено!")
    # Логи
    if a >= 1:
        print("Не удалось забанить следующих ID:\n", flog, "\nКоличество аккаунтов: ", a, sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')

# При выборе выдачи редактора всем участникам сообщества
elif choose == "21":
    # Запрос всех пользователей
    banneda = vk.groups.getMembers(group_id=id(groupId), sort="time_asc")
    count = banneda.get('count')
    banned = banneda.get('items')
    managers = vk.groups.getMembers(group_id=id(groupId), sort="time_asc", filter="managers")
    countu = managers.get('count')
    admins = [0] * countu
    for i in range(countu):
        admins[i] = managers.get('items')[i].get('id')
    print(admins)
    print("Администраторы:", *admins)
    b = len(admins)
    bs = 0
    banned = [i for i in banned if i not in admins]
    banned = cut(banned)
    countu = len(banned)
    # Выввод общей информации
    print("Участники сообщества (без учёта администрации) :\n", banned, "\n\nКоличество участников:", countu)
    # Выдача редактора с циклом и учётом ошибок
    n = 0
    log = []
    while n != countu:
        try:
            result = vk.groups.editManager(group_id=id(groupId), user_id=int(banned[n]), role='editor')
            if result == 1:
                print("Выдали: https://vk.com/id", banned[n], sep='')
                log.append(banned[n])
            else:
                print("Ошибка.")
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            print("Выдали: https://vk.com/id", banned[n], sep='')
            n += 1
            sleep(captchaTimer)
    print("Завершено!\n")
    if a >= 1:
        print("Не удалось выдать редактора следующим аккаунтам:\n", *flog, "\nКоличество аккаунтов: ", len(flog),
              sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')
# При выборе выдачи редактора с приоритетом
elif choose == "22":
    # Запрос всех пользователей
    s = urllib.request.urlopen(priority_list).read().decode()
    priority_list = s.split(',')
    priority_list = isMember(users=priority_list, group=groupId)
    banneda = vk.groups.getMembers(group_id=id(groupId), sort="time_asc")
    count = banneda.get('count')
    banned = banneda.get('items')
    managers = vk.groups.getMembers(group_id=id(groupId), sort="time_asc", filter="managers")
    countu = managers.get('count')
    admins = [0] * countu
    for i in range(countu):
        admins[i] = managers.get('items')[i].get('id')
    bs = 0
    banned = [i for i in banned if i not in admins]
    banned = priority_list + banned
    banned = cut(banned)
    countu = len(banned)
    # Выввод общей информации
    if DEBUG_MODE:
        print("Приоритетный список: ", priority_list, "\n\nУчастники сообщества (без учёта администрации) :\n", banned,
              "\n\nКоличество участников:", countu)
    # Выдача редактора с циклом и учётом ошибок
    n = 0
    log = []
    while n != countu:
        try:
            result = vk.groups.editManager(group_id=id(groupId), user_id=int(banned[n]), role='editor')
            if result == 1:
                print("Выдали: https://vk.com/id", banned[n], sep='')
                log.append(banned[n])
            else:
                print("Ошибка.")
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            print("Выдали: https://vk.com/id", banned[n], sep='')
            n += 1
            sleep(captchaTimer)
    print("Завершено!\n")
    if a >= 1:
        print("Не удалось выдать редактора следующим аккаунтам:\n", flog, "\nКоличество аккаунтов: ", len(flog), sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')
# При выборе выдачи редактора с исключением
elif choose == "23":
    # Запрос всех пользователей
    s = urllib.request.urlopen(exception_list).read().decode()
    exception_list = s.split(',')
    exception_list = isMember(users=exception_list, group=groupId)
    banneda = vk.groups.getMembers(group_id=id(groupId), sort="time_asc")
    count = banneda.get('count')
    banned = banneda.get('items')
    managers = vk.groups.getMembers(group_id=id(groupId), sort="time_asc", filter="managers")
    countu = managers.get('count')
    admins = [0] * countu
    for i in range(countu):
        admins[i] = managers.get('items')[i].get('id')
    bs = 0
    banned = [i for i in banned if i not in admins]
    banned = cut(banned)
    # Выввод общей информации
    if DEBUG_MODE:
        print("Не приоритетный список: ", exception_list, "\n\nУчастники сообщества (без учёта администрации) :\n",
              banned, "\n\nКоличество участников:", countu)
    # Выдача редактора с циклом и учётом ошибок
    n = 0
    log = []
    while n != countu:
        try:
            result = vk.groups.editManager(group_id=id(groupId), user_id=int(banned[n]), role='editor')
            if result == 1:
                print("Выдали: https://vk.com/id", banned[n], sep='')
                log.append(banned[n])
            else:
                print("Ошибка.")
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось выдать редактора https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            print("Выдали: https://vk.com/id", banned[n], sep='')
            n += 1
            sleep(captchaTimer)
    print("Завершено!\n")
    if a >= 1:
        print("Не удалось выдать редактора следующим аккаунтам:\n", flog, "\nКоличество аккаунтов: ", a, sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')

# При выборе мультибана всех участников с капчтой
elif choose == "31":
    # Импорт текста из URL (текст должен быть отформатирован в одну строчку и через запятую)
    s = urllib.request.urlopen(banurl).read().decode()

    # Создание массива из текста s.
    banned = s.split(',')

    # Импорт текста из URL (текст должен быть отформатирован в одну строчку и через запятую)
    s = urllib.request.urlopen(groupurl).read().decode()

    groups = s.split(',')
    if DEBUG_MODE:
        print("Данные для откладки. Массив с забаненными:", banned, "\nМассив с группами:", groups,
              "\nКоличество участников на бан:", len(banned))
        sdf = str(input("Enter для продолжения..."))
        color()
    n = 0
    g = 0
    log = []
    for i in range(len(groups)):
        groups[i] = id(groups[i])
    # Бан через цикл с исключением ошибок
    t = timer()
    while True:
        try:
            result = vk.groups.ban(group_id=groups[g], owner_id=int(banned[n]), reason=0, comment=com,
                                   comment_visible=1)
            if result == 1:
                print("Забанили: https://vk.com/id", banned[n], " в группе: ", groups[g], sep='')
            if DEBUG_MODE:
                print("Переменная 'n' равна:", n)
            log.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nОткладочная информация: текущая группа под номером g = ", g, ": ", groups[g],
                      "\nТекущий забаненный с номером n = ", n, ": ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups):
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nОткладочная информация: текущая группа под номером g = ", g, ": ", groups[g],
                      "\nТекущий забаненный с номером n = ", n, ": ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nОткладочная информация: текущая группа под номером g = ", g, ": ", groups[g],
                      "\nТекущий забаненный с номером n = ", n, ": ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
    print("Завершено!\Таймер:", monotonic() - t)
    # Логи
    if a > 1:
        print("В ходе выполнения скрипта не удалось забанить следующие ID:\n", flog)
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')
# При выборе мультибана всех участников без каптчи
elif choose == "32":
    # Импорт текста из URL (текст должен быть отформатирован в одну строчку и через запятую)
    s = urllib.request.urlopen(banurl).read().decode()

    # Создание массива из текста s.
    banned = s.split(',')

    # Импорт текста из URL (текст должен быть отформатирован в одну строчку и через запятую)
    s = urllib.request.urlopen(groupurl).read().decode()

    groups = s.split(',')
    if DEBUG_MODE:
        print("Данные для откладки. Массив с забаненными:", banned, "\nМассив с группами:", groups,
              "\nКоличество участников на бан:", len(banned))
        sdf = str(input("Enter для продолжения..."))
        color()
    n = 0
    g = 0
    log = []
    for i in range(len(groups)):
        groups[i] = id(groups[i])
    # Бан через цикл с исключением ошибок
    t = timer()
    while True:
        try:
            result = vk.groups.ban(group_id=groups[g], owner_id=int(banned[n]), reason=0, comment=com,
                                   comment_visible=1)
            if result == 1:
                print("Забанили: https://vk.com/id", banned[n], " в группе: ", groups[g], sep='')
            if DEBUG_MODE:
                print("Переменная 'n' равна:", n)
            log.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nОткладочная информация: текущая группа под номером g = ", g, ": ", groups[g],
                      "\nТекущий забаненный с номером n = ", n, ": ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups):
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nОткладочная информация: текущая группа под номером g = ", g, ": ", groups[g],
                      "\nТекущий забаненный с номером n = ", n, ": ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nОткладочная информация: текущая группа под номером g = ", g, ": ", groups[g],
                      "\nТекущий забаненный с номером n = ", n, ": ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
            else:
                n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            if DEBUG_MODE:
                print("Каптча, ждем 15 секунд и заново.")
            sleep(15)
            if n >= len(banned) - 1:
                n = 0
                if g == len(groups) - 1:
                    print("Забанили всех участников в последней группе!")
                    break
                else:
                    print("Забанили всех участников в группе: ", groups[g], ", переходим к следущей.")
                    g += 1
    print("Завершено!\Таймер:", monotonic() - t)
    if a > 1:
        print("В ходе выполнения скрипта не удалось забанить следующие ID:\n", flog)
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')


# При выборе разбана с каптчой
elif choose == "41":
    count = vk.groups.getBanned(group_id=id(groupId), count=200)
    banned = [0] * count.get('count')
    if 200 < count.get('count') <= 400:
        coun = vk.groups.getBanned(group_id=id(groupId), count=200, offset=200)
    for i in range(count.get('count')):
        if i > 200:
            banned[i] = coun.get('items')[i].get('profile').get('id')
        banned[i] = count.get('items')[i].get('profile').get('id')
    count = count.get('count')
    n = 0
    # Разбан через цикл с иключениями ошибок
    while n != count:
        try:
            result = vk.groups.unban(group_id=id(groupId), owner_id=int(banned[n]))
            log.append(banned[n])
            if result == 1:
                print("Разбанили: https://vk.com/id", banned[n], sep='')
            else:
                "Что-то пошло не так."
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён или заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось разбанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            n += 1
    # Логи
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')
# При выборе разбана без каптчи
elif choose == "42":
    count = vk.groups.getBanned(group_id=id(groupId), count=200)
    banned = [0] * count.get('count')
    if 200 < count.get('count') <= 400:
        coun = vk.groups.getBanned(group_id=id(groupId), count=200, offset=200)
    for i in range(count.get('count')):
        if i > 200:
            banned[i] = coun.get('items')[i].get('profile').get('id')
        banned[i] = count.get('items')[i].get('profile').get('id')
    count = count.get('count')
    n = 0
    # Разбан через цикл с иключениями ошибок
    while n != count:
        try:
            result = vk.groups.unban(group_id=id(groupId), owner_id=int(banned[n]))
            if result == 1:
                print("Разбанили: https://vk.com/id", banned[n], sep='')
                log.append(banned[n])
            else:
                "Что-то пошло не так."
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён или заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось забанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось разбанить: ", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            if DEBUG_MODE:
                print("Каптча, ждем 15 секунд.")
            sleep(15)
    # Логи
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')
# При выборе разбана во всех группах
elif choose == "43":
    user = str(input('Пожалуйста, введите ID пользователя: '))
    while not user.isDigit():
        print('\n\n\nID пользователя содержит сторонние символы. Введите пожалуйста ID только цифрами\n')
        user = str(input('\n\n>'))
    groups = urllib.request.urlopen(groupurl).read().decode().split(',')
    for i in range(len(groups)):
        groups[i] = nIsDigit(groups[i])
    for group in groups:
        try:
            answer = vk.groups.unban(group_id=id(group), owner_id=user)
            if answer == 1 or answer == "1":
                print("Успешно разбанили пользователя https://vk.com/id{} в сообществе https://vk.com/club{}".format(
                    user), id(group))
        except vk_api.exceptions.AccountBlocked as Error:
            print(Error, "\nНе удалось разбанить https://vk.com/id{}".format(user))
            pass
        except vk_api.exceptions.ApiError as Error:
            print(Error, "\nНе удалось разбанить https://vk.com/id{}".format(user))
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            print(Error, "\nНе удалось разбанить https://vk.com/id{}".format(user))
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            print("Успешно разбанили пользователя https://vk.com/id{} в сообществе https://vk.com/club{}".format(user),
                  id(group))

# При выборе создания сообщества
elif choose == "51":
    print('\n\nСоздается группа, ожидайте...\n\n')
    try:
        answer = vk.groups.create(title=create_settings.get('title'), description=create_settings.get('description'),
                                  type=create_settings.get('type'))
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    print("\n\nУспешно завершено! Адрес вашей новой группы: https://vk.com/", answer.get('screen_name'),
          "\n\nЕсли вы дальше планируете взаимодействовать с новой группой через скрипт, то в значение groupId "
          "впишите screen_name вашего сообщества: 'public342...' или shortURL",
          sep='')
    url = "https://vk.com/" + str(answer.get('screen_name')) + str("?act=edit")
    webbrowser.open(url)
# При выборе настройки сообщества
elif choose == "61":
    print('\n\nУстанавливаются настройки группы, ожидайте...\n\n')
    try:
        upload = vk_api.VkUpload(vk=vk)
        download('photo_url')
        download('cover_url')
        if DEBUG_MODE == True:
            print('Посылаем запрос на аватар к VK API...')
            # print(settings.get('cover_url').split('/')[-1],'\n',settings.get('cover_url').split('/'),'\n',
            # settings.get('cover_url'), str(gettempdir()), str(gettempdir())+settings.get('cover_url').split('/')[-1])
        answer = upload.photo_profile(photo=str(gettempdir()) + '\\' + settings.get('photo_url').split('/')[-1],
                                      owner_id=-(id(groupId)), crop_x='-15', crop_y='-15')
        if DEBUG_MODE:
            print("Ответ VK API:", answer)
        print('Установили аватар сообщества. Приступаем к установке ковера...')
        if DEBUG_MODE:
            print('Посылаем запрос на ковер к VK API...')
        # if DEBUG_MODE==True:
        #    print()
        answer = upload.photo_cover(photo=str(gettempdir()) + '\\' + settings.get('cover_url').split('/')[-1],
                                    group_id=id(groupId))
        if DEBUG_MODE:
            print("Ответ VK API:", answer)
        posts = getAllPosts(vk, groupId)
        deletePosts(vk, groupId, posts)
        answer = vk.groups.edit(group_id=id(groupId), title=settings.get('title'), website=settings.get('website'),
                                description=settings.get('description'), screen_name=settings.get('screen_name'),
                                access=settings.get('access'), wall=settings.get('wall'), topics=settings.get('topics'),
                                photos=settings.get('photos'), video=settings.get('video'), audio=settings.get('audio'),
                                age_limits=settings.get('age_limits'), market=settings.get('market'),
                                public_category='1002', public_subcategory='3143')
        if DEBUG_MODE:
            print(answer)
        answer = vk.groups.setSettings(group_id=id(groupId), messages=settings.get('messages'))
        print('Настройки установлены.')
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    print("\n\nУспешно завершено!")

# При выборе преобразования screen_name в ссылки
elif choose == "71":
    try:
        answer = vk.users.get(user_ids=ids.get('items'))
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    for i in range(ids.get('count')):
        answer[i] = "https://vk.com/id" + str(answer[i].get('id'))
    print("Список ссылок:")
    for i in range(ids.get('count')):
        print(answer[i])
# При выборе преобразования screen_name в ID
elif choose == "72":
    try:
        answer = vk.users.get(user_ids=ids.get('items'))
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    for i in range(ids.get('count')):
        answer[i] = str(answer[i].get('id'))
    print("Список ID:")
    for i in range(ids.get('count')):
        print(answer[i])
# При выборе преобразования screen_name из ссылок в ссылки
elif choose == "73":
    count = ids.get('count')
    ids = ids.get('items').split(',')
    for i in range(count):
        ids[i] = ids[i][15:]
        if DEBUG_MODE:
            print(ids)
    try:
        answer = vk.users.get(user_ids=ids)
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    if DEBUG_MODE:
        print(answer)
    for i in range(count):
        answer[i] = "https://vk.com/id" + str(answer[i].get('id'))
    print("Список ссылок:")
    for i in range(count):
        print(answer[i])


# При выборе поиска человека по группе
elif choose == "81":
    try:
        answer = vk.groups.isMember(group_id=id(groupId), user_id=user_id)
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    if DEBUG_MODE:
        print(answer, "\n\n")
    if answer == 1:
        print("Пользователь есть в сообществе:", groupId)
    else:
        print("Пользователя нет в сообществе:", groupId)
# При выборе поиска людей по группе
elif choose == "82":
    try:
        answer = vk.groups.isMember(group_id=id(groupId), user_ids=user_ids)
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
    answer_isMember = [0] * len(answer)
    answer_ids = [0] * len(answer)
    for i in range(len(answer)):
        answer_isMember[i] = answer[i].get('member')
        answer_ids[i] = answer[i].get('user_id')
    if DEBUG_MODE:
        print(answer, "\n", answer_ids, "\n", answer_isMember, sep='')
    for i in range(len(answer)):
        if answer_isMember[i] == 1:
            print("Пользователь https://vk.com/id", answer_ids[i], " является участником сообщества ", groupId, sep='')
        else:
            print("Пользователь https://vk.com/id", answer_ids[i], " не является участником сообщества ", groupId,
                  sep='')
# При выборе поиска человека по группам
elif choose == "83":
    n = 0
    s = urllib.request.urlopen(groupurl).read().decode()
    groupId = s.split(',')
    try:
        while True:
            if n == len(groupId):
                break
            answer = vk.groups.isMember(group_id=id(groupId[n]), user_id=user_id)
            if DEBUG_MODE:
                print(answer, "\n\n")
            if answer == 1:
                print("Пользователь есть в сообществе:", groupId[n])
            else:
                print("Пользователя нет в сообществе:", groupId[n])
            n += 1
    except vk_api.exceptions.AccountBlocked as Error:
        if not DEBUG_MODE:
            print("Не удалось выполнить операцию, так как аккаунт заблокирован.")
        else:
            print(Error, "\nНе удалось выполнить операцию")
            n += 1
            pass
    except vk_api.exceptions.ApiError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        n += 1
        pass
    except vk_api.exceptions.ApiHttpError as Error:
        if not DEBUG_MODE:
            print("Ошибка на стороне сервера или API")
        else:
            print(Error, "\nНе удалось выполнить операцию")
        n += 1
        pass
    except vk_api.exceptions.Captcha as captcha:
        captcha_handler(captcha)
        if DEBUG_MODE:
            print(answer, "\n\n")
        if answer == 1:
            print("Пользователь есть в сообществе:", groupId[n])
        else:
            print("Пользователя нет в сообществе:", groupId[n])

# При выборе снятия прав
elif choose == "91":
    banned = vk.groups.getMembers(group_id=id(groupId), sort="time_asc", filter="managers")
    countu = banned.get('count')
    banned = banned.get('items')
    n = 0
    for i in range(countu):
        banned[i] = banned[i].get('id')
    while n != countu:
        try:
            result = vk.groups.editManager(group_id=id(groupId), user_id=int(banned[n]))
            if result == 1:
                print("Убрали: https://vk.com/id", banned[n], sep='')
                log.append(banned[n])
            else:
                print("Ошибка.")
            n += 1
        except vk_api.exceptions.AccountBlocked as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiError as Error:
            if not DEBUG_MODE:
                print("Аккаунт https://vk.com/id", banned[n], " удалён/заблокирован. Пропуск.", sep='')
            else:
                print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            if not DEBUG_MODE:
                print("Ошибка на стороне сервера или API. Пропуск аккаунта https://vk.com/id", banned[n], sep='')
            else:
                print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
            a += 1
            flog.append(banned[n])
            n += 1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            n += 1
    print("Завершено!\n")
    if a >= 1:
        print("Не удалось убрать роль следующим аккаунтам:\n", flog, "\nКоличество аккаунтов: ", a, sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n", log, "\nКоличество аккаунтов: ", len(log), sep='')
# При выборе снятия редактора у заблокированных или удаленных страниц
elif choose == "92":
    banned = vk.groups.getMembers(group_id=id(groupId), sort="time_asc", filter="managers").get('items')
    for i in range(len(banned)):
        banned[i] = banned[i].get('id')
    banned = vk.users.get(user_ids=banned)
    print(banned)
    if DEBUG_MODE:
        print(banned, len(banned))
    ids = status = [0] * len(banned)
    foredit = []
    names = []
    surnames = []
    no = True
    if DEBUG_MODE:
        print(banned)
        print("Начало цикла")
    for i in range(len(banned)):
        if DEBUG_MODE:
            print(i)
            print(banned[i])
        ids[i] = banned[i].get('id')
        if 'deactivated' in banned[i]:
            foredit.append(ids[i])
            no = False
            print("Нашли забаненного!")
            names.append(banned[i].get('first_name'))
            surnames.append(banned[i].get('last_name'))

    if not no:
        print("\n\nСписок удаленных страниц на бан:", foredit)
        webbrowser.open('https://vk.com/club' + str(id(groupId)) + '?act=users')
        print("\nБыстрые данные для копирования:")
        for i in range(len(names)):
            print("Пользователь #", i + 1, " - ", names[i], " ", surnames[i], sep='')
        print(
            "\n\nК сожалению API ВКонтакте не позволяет удалять/снимать с должностей забаненных пользователей, "
            "но это можно сделать с помощью веб-интерфейса.")
    else:
        print("Не найдены заблокированные пользователи среди администрации сообщества.")
# При выборе ...
elif choose == "93":
    user = str(input('Пожалуйста, введите ID пользователя: '))
    while not user.isDigit():
        print('\n\n\nID пользователя содержит сторонние символы. Введите пожалуйста ID только цифрами\n')
        user = str(input('\n\n>'))
    groups = urllib.request.urlopen(groupurl).read().decode().split(',')
    for i in range(len(groups)):
        groups[i] = nIsDigit(groups[i])
    for group in groups:
        try:
            answer = vk.groups.unban(group_id=id(group), owner_id=user)
            if answer == 1 or answer == "1":
                print(
                    "Успешно сняли права у пользователя https://vk.com/id{} в сообществе https://vk.com/club{}".format(
                        user), id(group))
        except vk_api.exceptions.AccountBlocked as Error:
            print(Error, "\nНе удалось снять права: https://vk.com/id{}".format(user))
            pass
        except vk_api.exceptions.ApiError as Error:
            print(Error, "\nНе удалось снять права: https://vk.com/id{}".format(user))
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            print(Error, "\nНе удалось снять права: https://vk.com/id{}".format(user))
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            print("Успешно сняли права у пользователя https://vk.com/id{} в сообществе https://vk.com/club{}".format(
                user), id(group))

# При выборе банчека
elif choose == "101":
    banlist = urllib.request.urlopen(banurl).read().decode().split(',')
    for i in range(len(banlist)):
        banlist[i] = nIsDigit(str(banlist[i]))

    if DEBUG_MODE:
        print('Список забаненных:', banlist)
    answer = vk.groups.getMembers(group_id=id(groupId), sort='time_asc', filter='managers')
    ids = []
    fail = []
    for i in range(answer.get('count')):
        ids.append(answer.get('items')[i].get('id'))
    fail = banCheck(vk, ids, banlist)
    if fail:
        print('Были найдены забаненные руководители в сообщесте https://vk.com/club{}\nID руководителей:{}'.format(
            id(group), *fail))
    else:
        print('Забаненных руководителей в сообществе найдено не было.')
# При выборе банчека со снятием прав
elif choose == "102":
    banlist = urllib.request.urlopen(banurl).read().decode().split(',')
    for i in range(len(banlist)):
        banlist[i] = nIsDigit(str(banlist[i]))
    if DEBUG_MODE:
        print('Список забаненных:', banlist)
    answer = vk.groups.getMembers(group_id=id(groupId), sort='time_asc', filter='managers')
    ids = []
    fail = []
    for i in range(answer.get('count')):
        ids.append(answer.get('items')[i].get('id'))
    fail = banCheck(vk, ids, banlist)
    if fail:
        print(
            'Были найдены забаненные руководители в сообщесте https://vk.com/club{}\nID руководителей:{}\n\nСнятие '
            'прав в процессе...'.format(
                id(group), *fail))
        n = 0
        flog = []
        log = []
        log2 = []
        for i in range(len(fail)):
            try:
                answer = vk.groups.editManager(group_id=id(groupId), user_id=fail[i])
                if answer == 1 or answer == '1':
                    log.append(fail[i])
                    print('Сняли права у https://vk.com/id{}'.format(fail[i]))
            except vk_api.exceptions.AccountBlocked as Error:
                print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
                flog.append(banned[n])
                n += 1
                pass
            except vk_api.exceptions.ApiError as Error:
                print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
                flog.append(banned[n])
                n += 1
                pass
            except vk_api.exceptions.ApiHttpError as Error:
                print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
                flog.append(banned[n])
                n += 1
                pass
            except vk_api.exceptions.Captcha as captcha:
                captcha_handler(captcha)
                print("Убрали роль у: https://vk.com/id", banned[n], sep='')
                n += 1
        if len(flog) >= 1:
            print("Не удалось снять права у следующих ID:\n", flog, "\nКоличество аккаунтов: ", len(flog), sep='')
        flog = []
        sdf = str(input('\nНажмите Enter для продолжения...'))
        color()
        print('\n\n\nСнятие прав завершено. Приступаем к блокировке.')
        for i in range(len(fail)):
            try:
                answer = vk.groups.ban(group_id=id(groupId), owner_id=fail[i], reason=0, comment=com, comment_visible=1)
                if answer == 1 or answer == '1':
                    log2.append(fail[i])
                    print('Забанили https://vk.com/id{}'.format(fail[i]))
            except vk_api.exceptions.AccountBlocked as Error:
                print(Error, "\nНе удалось забанить https://vk.com/id", banned[n], sep='')
                flog.append(banned[n])
                n += 1
                pass
            except vk_api.exceptions.ApiError as Error:
                print(Error, "\nНе удалось забанить https://vk.com/id", banned[n], sep='')
                flog.append(banned[n])
                n += 1
                pass
            except vk_api.exceptions.ApiHttpError as Error:
                print(Error, "\nНе удалось забанить https://vk.com/id", banned[n], sep='')
                flog.append(banned[n])
                n += 1
                pass
            except vk_api.exceptions.Captcha as captcha:
                captcha_handler(captcha)
                print("Забанили: https://vk.com/id", banned[n], sep='')
                n += 1
        if len(flog) >= 1:
            print("Не удалось забанить следующих ID:\n", flog, "\nКоличество аккаунтов: ", len(flog), sep='')
        sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
        if sdf == "1":
            print('Логи банчека:\n\nСняли права: {}\n\nЗабанили: {}'.format(log, log2))
    else:
        print('Забаненных руководителей в сообществе найдено не было.')

# При выборе мультибанчека
elif choose == "111":
    banlist = urllib.request.urlopen(banurl).read().decode().split(',')
    for i in range(len(banlist)):
        banlist[i] = nIsDigit(str(banlist[i]))
    if DEBUG_MODE:
        print('Список забаненных:', banlist)
    ids = []
    fail = []
    groups = urllib.request.urlopen(groupurl).read().decode().split(',')
    for group in groups:
        answer = vk.groups.getMembers(group_id=id(group), sort='time_asc', filter='managers')
        for i in range(answer.get('count')):
            ids.append(answer.get('items')[i].get('id'))
        fail = banCheck(vk, ids, banlist)
        if fail:
            print('Были найдены забаненные руководители в сообщесте https://vk.com/club{}\nID руководителей:{}'.format(
                id(group), *fail))
        else:
            print('Забаненных руководителей в сообществе https://vk.com/club{} найдено не было.'.format(id(group)))
# При выборе мультибанчека со снятием прав
elif choose == "112":
    print('\n\n\n')
    banlist = urllib.request.urlopen(banurl).read().decode().split(',')
    for i in range(len(banlist)):
        banlist[i] = nIsDigit(str(banlist[i]))
    ids = []
    fail = []
    groups = urllib.request.urlopen(groupurl).read().decode().split(',')
    for group in groups:
        answer = vk.groups.getMembers(group_id=id(group), sort='time_asc', filter='managers')
        for i in range(answer.get('count')):
            ids.append(answer.get('items')[i].get('id'))
        fail = banCheck(vk, ids, banlist)
        if fail:
            print(
                'Были найдены забаненные руководители в сообщесте https://vk.com/club{}\nID руководителей:{}\n\nСнятие прав в процессе...'.format(
                    id(group), *fail))
            n = 0
            flog = []
            log = []
            for i in range(len(fail)):
                try:
                    answer = vk.groups.editManager(group_id=id(group), user_id=fail[i])
                    if answer == 1 or answer == '1':
                        log.append(fail[i])
                        print('Сняли права у https://vk.com/id{} в группе https://vk.com/club{}'.format(fail[i], group))
                except vk_api.exceptions.AccountBlocked as Error:
                    print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
                    flog.append(banned[n])
                    n += 1
                    pass
                except vk_api.exceptions.ApiError as Error:
                    print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
                    flog.append(banned[n])
                    n += 1
                    pass
                except vk_api.exceptions.ApiHttpError as Error:
                    print(Error, "\nНе удалось убрать роль у https://vk.com/id", banned[n], sep='')
                    flog.append(banned[n])
                    n += 1
                    pass
                except vk_api.exceptions.Captcha as captcha:
                    captcha_handler(captcha)
                    print("Убрали роль у: https://vk.com/id", banned[n], sep='')
                    n += 1
            if len(flog) >= 1:
                print("Не удалось снять права у следующих ID:\n", flog, "\nКоличество аккаунтов: ", len(flog), sep='')
            print('\n\n\nСнятие прав завершено. Приступаем к блокировке.')
            for i in range(len(fail)):
                try:
                    answer = vk.groups.ban(group_id=id(group), owner_id=fail[i], reason=0, comment=com,
                                           comment_visible=1)
                    if answer == 1 or answer == '1':
                        log.append(fail[i])
                        print('Забанили https://vk.com/id{} в группе https://vk.com/club{}'.format(fail[i], group))
                except vk_api.exceptions.AccountBlocked as Error:
                    print(Error, "\nНе удалось забанить https://vk.com/id", banned[n], sep='')
                    flog.append(banned[n])
                    n += 1
                    pass
                except vk_api.exceptions.ApiError as Error:
                    print(Error, "\nНе удалось забанить https://vk.com/id", banned[n], sep='')
                    flog.append(banned[n])
                    n += 1
                    pass
                except vk_api.exceptions.ApiHttpError as Error:
                    print(Error, "\nНе удалось забанить https://vk.com/id", banned[n], sep='')
                    flog.append(banned[n])
                    n += 1
                    pass
                except vk_api.exceptions.Captcha as captcha:
                    captcha_handler(captcha)
                    print("Забанили: https://vk.com/id", banned[n], sep='')
                    n += 1
            if len(flog) >= 1:
                print("Не удалось забанить следующих ID:\n", flog, "\nКоличество аккаунтов: ", len(flog), sep='')
            print('\n\n\nЗавершено. Переходим к следущей группе')
        else:
            print('Забаненных руководителей в сообществе {} найдено не было.'.format(group))
