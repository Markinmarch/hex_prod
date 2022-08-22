import requests
import datetime
import configparser

    
print('Программа для импорта фотографий из Вконтаке на Я.Диск')
print('Перейдите по ссылке https://yandex.ru/dev/disk/poligon/ и сгенерируйте свой Яндекс-токен (при необходимости создайте аккаунт на Яндексе)')

config = configparser.ConfigParser()
config.read('token.ini')
access_token = config['VK_API']['access_token']
    
user_id = input('Введите id-номер или короткое имя (никнейм) страницы профиля: ')
photo_count = int(input('Введите количество скачиваемых фотографий со страницы профиля: '))

class VK_API:
    '''Класс, для определения требуемых параметров'''

    
    def __init__(self, user_id,
                 access_token,
                 count,
                 version = 5.131,
                 album = 'profile',
                 extended = False,
                 rev = True):
        # id страницы пользователя
        self.id = user_id
        # токен АПИ
        self.token = access_token
        # версия АПИ ВК
        self.version = version
        # вызов фотографий аватарок профиля ('profile')
        self.album = album
        # вызываем доп.информацию (для определения количества лайков) (True)
        self.extended = extended
        # вызов фото в хронологичном порядке (True)
        self.rev = rev
        # количество записей
        self.count = count

    def get_params(self):
    # функция, которая берёт json со страницы
        url = 'https://api.vk.com/method/photos.get'
        # вызываем и вводим параметры вызова
        response = requests.get(url, params = {'access_token': self.token,
                                               'user_ids': self.id,
                                               'v': self.version,
                                               'album_id': self.album,
                                               'extended': self.extended,
                                               'rev': self.rev,
                                               'count': self.count
                                               })
        return response.json()
    
    def file_name(res):
        # функция для присваивания имён фотографиям
        # создаём список из количества лайков под фотографиями
        get_list_likes = []
        for item in res.values():
            for inside_params in item['items']:
                get_list_likes.append(str(inside_params['likes']['count']))
        # создаём список из дат загрузки фотографий
        get_list_date = []
        for item in res.values():
            for inside_params in item['items']:
                date = datetime.datetime.fromtimestamp(int(inside_params['date']))
                get_list_date.append(date.strftime('%d-%m-%Y'))
        # условие: если количество лайков одиннаковое под фотографиями - то им добавляются даты загрузки
        if lst_likes := [i for i, x in enumerate(get_list_likes) if get_list_likes.count(x) > 1]:
            for indx in lst_likes:
                correct = get_list_likes[indx] + f'_{get_list_date[indx]}'
                get_list_likes[indx] = correct
            return get_list_likes
        # а если количество лайков разное - то именя фото будут состоять только из количества лайков
        else:
            return get_list_likes
    
    def get_photo_url_type_size(res):
        # Формируем список из ссылок и типоразмера фотографий
        date_dict = {}
        for item in res.values():
            for inside_params in item['items']:
                # создаём список для дальнейшего сравнения по размерам
                size_list = []
                # создаём список для адресов по аналогии списка размеров
                url_list = []
                # в дальнейшем привязываемся к дате фотографий по переменной date
                date = inside_params['date']
                for size in inside_params['sizes']:
                    value = size['height']
                    url = size['url']
                    type_size = size['type']
                    size_list.append(value)
                    url_list.append(url)
                    # необходимость создания словаря, чтобы по значению выводить наибольшее значение
                    dict_for_info = dict(zip(url_list, size_list))
                    # вот тут привязываемся по дате фотографий с указанием типоразмера
                    date_dict.update({date: [max(dict_for_info, key=dict_for_info.get), type_size]})
        return [i for i in date_dict.values()]
    
    # достаём информацию о профиле
    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        response = requests.get(url, params = {'access_token': self.token,
                                               'user_ids': self.id,
                                               'v': self.version})
        return response.json().get('response')

res_VK_data = VK_API(user_id, access_token, photo_count)
res_VK = res_VK_data.get_params()
links = VK_API.get_photo_url_type_size(res_VK)
user_data = res_VK_data.users_info()[0]
name_user = user_data.get('first_name')
last_name_user = user_data.get('last_name')
file_name = VK_API.file_name(res_VK)

# print(file_name)
# print(links)
# print(user_data)
# print(name_user)
# print(last_name_user)

