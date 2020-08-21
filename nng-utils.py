# Импорт библиотек
import vk_api
import urllib.request
import webbrowser
import os
from time import sleep
from sys import exit

# Данные для входа и авторизации в VK API
token=str("")

# URL группы
groupId = str("")

# Комментарий бана
com=str("Блокировка после решения Администрации | По вопросам: https://vk.me/mralonas")

# URL сайта со списком на бан (raw .txt, ID через запятую)
banurl = str("https://nng.alonas.ml/bnnd/rawline.txt")

# Авторизация в VK API и начало сессии
try:
    token = vk_api.VkApi(token = token)
    vk = token.get_api()
    name=vk.account.getProfileInfo()
    surname=name.get('last_name')
    userid=name.get('id')
    name=name.get('first_name')
except:
    print("Возможно Ваш access token недейстителен или перестал действовать, получите новый и впишите его в скрипт.\n")
    while True:
        sdf=str(input("Выйдите из программы и введите правильные данные!\n"))
        if sdf=="exit" or "q":
            exit()

if os.name=='nt':
    ostype=str("windows")
elif os.name=='mac':
    ostype=str("macos")
else:
    ostype=str("linux")

# Функции
def color():
    if ostype=="windows":
        os.system('cls')
        print("\n[-- NNG UTLIS --]\n\nStable версия | Авторизован в качестве",name,surname,"ID:",userid)
    else:
        os.system('clear')
        print("\n[-- NNG UTLIS --]\n\nStable версия | Авторизован в качестве",name,surname,"ID:",userid)

def clear():
    if ostype=="windows":
        os.system('cls')
    else:
        os.system('clear')

def menu():
    color()
    print("\n\nМеню\n\n1.Бан\n\n2.Выдача редактора\n\n\n")
    choose = str(input(">"))
    if choose == "1":
        color()
        choose = str(input("Выбрана операция: Бан\n\n1.Выполнить\n\n2.Выйти\n\n\n>"))
        choose = "1" + choose
        if choose == "11":
            color()
            return choose
        else:
            menu()
    elif choose == "2":
        color()
        choose = "2" + str(input("Выбрана опцерация: Выдача редактора.\n\n\n1.Выполнить\n\n2.Выйти\n\n\n>"))
        if choose == "21":
            return choose
        else:
            menu()
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

# Меню
choose = menu()

#Локальные переменные для обработки
a=0
log=[]
flog=[]

# При выборе бана с каптчой
if choose == "11":
    # Импорт текста из URL (текст должен быть отформатирован в одну строчку и через запятую)
    s = urllib.request.urlopen(banurl).read().decode()

    # Создание массива из текста s.
    banned = s.split(',')
    banned = list(banned)
            
    # Считаем количество элементов в массиве "banned"
    count=len(banned)
    print("Количество пользователей:",count,sep='')
            
    # Бан через цикл с иключениями ошибок
    n=0
    while n!=count:
        try:
            result = vk.groups.ban(group_id=id(groupId),owner_id=int(banned[n]),reason=0,comment=com, comment_visible=1)
            if result == 1:
                print("Забанили: https://vk.com/id",banned[n],sep='')
                log.append(banned[n])
            else:
                "Что-то пошло не так."
            n+=1
        except vk_api.exceptions.AccountBlocked as Error:
            print(Error,"\nНе удалось забанить: ",banned[n],sep='')
            a+=1
            flog.append(banned[n])
            pass
        except vk_api.exceptions.ApiError as Error:
            print(Error,"\nНе удалось забанить: ",banned[n],sep='')
            a+=1
            flog.append(banned[n])
            n+=1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            print(Error,"\nНе удалось забанить: ",banned[n],sep='')
            a+=1
            flog.append(banned[n])
            n+=1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
    print("Завершено!")
    # Логи
    if a>=1:
        print("Не удалось забанить следующих ID:\n",flog,"\nКоличество аккаунтов: ",a, sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n",log,"\nКоличество аккаунтов: ",len(log),sep='')

# При выборе выдачи редактора всем участникам сообщества
elif choose=="21":
    # Запрос всех пользователей
    banneda = vk.groups.getMembers(group_id=id(groupId),sort = "time_asc")
    count = banneda.get('count')
    banned = banneda.get('items')
    managers = vk.groups.getMembers(group_id=id(groupId),sort = "time_asc", filter="managers")
    countu = managers.get('count')
    admins = [0] * countu
    for i in range(countu):
        admins[i] = managers.get('items')[i].get('id')
    print(admins)
    print("Администраторы:",*admins)
    banned = [i for i in banned if i not in admins]
    countu = len(banned)
    # Выввод общей информации
    print("Участники сообщества (без учёта администрации) :\n",banned,"\n\nКоличество участников:",countu)
    # Выдача редактора с циклом и учётом ошибок
    n=0
    log=[]
    while n!=countu:
        try:
            result = vk.groups.editManager(group_id=id(groupId), user_id=int(banned[n]),role='editor')
            if result==1:
                print("Выдали: https://vk.com/id",banned[n],sep='')
                log.append(banned[n])
            else:
                print("Ошибка.")
            n+=1
        except vk_api.exceptions.AccountBlocked as Error:
            print(Error,"\nНе удалось выдать редактора https://vk.com/id",banned[n], sep='')
            a+=1
            flog.append(banned[n])
            n+=1
            pass
        except vk_api.exceptions.ApiError as Error:
            print(Error,"\nНе удалось выдать редактора https://vk.com/id",banned[n], sep='')
            a+=1
            flog.append(banned[n])
            n+=1
            pass
        except vk_api.exceptions.ApiHttpError as Error:
            print(Error,"\nНе удалось выдать редактора https://vk.com/id",banned[n], sep='')
            a+=1
            flog.append(banned[n])
            n+=1
            pass
        except vk_api.exceptions.Captcha as captcha:
            captcha_handler(captcha)
            print("Выдали: https://vk.com/id",banned[n],sep='')
            n+=1
    print("Завершено!\n")
    if a>=1:
        print("Не удалось выдать редактора следующим аккаунтам:\n",*flog,"\nКоличество аккаунтов: ",len(flog), sep='')
    sdf = str(input("\nВывести логи операции?\n\n1.Да\n2.Нет\n\n>"))
    if sdf == "1":
        print("Логи операции:\n",log,"\nКоличество аккаунтов: ",len(log),sep='')