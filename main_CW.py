from os import path
import requests
import datetime
import json

print('Программа для импорта фотографий из Вконтаке на Я.Диск')
print('Перейдите по ссылке https://yandex.ru/dev/disk/poligon/ и сгенерируйте свой Яндекс-токен (при необходимости создайте аккаунт на Яндексе)')
# Вводим данные, согдасно ТЗ
ya_token = input('Введите OAuth-токен: ')
user_id = int(input('Введите id-номер страницы профиля: '))


class VK_API:
    '''Класс, для определения требуемых параметров'''
    def __init__(self, user_id,
                 access_token,
                 version = 5.131,
                 album = 'profile',
                 extended = False,
                 rev = True,
                 count = 5):
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
                                               'user_id': self.id,
                                               'v': self.version,
                                               'album_id': self.album,
                                               'extended': self.extended,
                                               'rev': self.rev,
                                               'count': self.count
                                               })
        return response.json()
    
    def get_photo_likes_date(res):
        # Формируем название фотографий по количеству лайков и дате фотографии
        get_list_date = []
        for item in res.values():
            for inside_params in item['items']:
                date = datetime.datetime.fromtimestamp(int(inside_params['date']))
                get_list_date.append(date.strftime('%d-%m-%Y'))
        get_list_likes = []
        for item in res.values():
            for inside_params in item['items']:
                get_list_likes.append(str(inside_params['likes']['count']))
        lst = ['_'.join(i) for i in zip(get_list_likes, get_list_date)]
        return lst  

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
                    date_dict.update({date : [max(dict_for_info, key=dict_for_info.get), type_size]})
        return [i for i in date_dict.values()]
    
    # достаём информацию о профиле
    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        response = requests.get(url, params = {'access_token': self.token,
                                               'user_id': self.id,
                                               'v': self.version})
        return response.json().get('response')
    
# вводим токен приложения. пользователь вводит номер id профиля Вконтакте
access_token = 'vk1.a.EDgakxBbcab3YsfNh1PCTGD5nXvM1O5zGqH8FC5oLH8SkAc1o54qXZczueHJQdNHScD80HO5vMPCsgP0IoAlUN5hb5N6STIGHwhhxrd86nMJXgPN5KgF5V-HSTTuUDa9Oel5vw4tScZBSkYw7lVbD15Ul1Gq996M4AXe_NZ8PZ8ABbsAtKi-zt5OY2K8IuAr'

res_VK_data = VK_API(user_id, access_token)
res_VK = res_VK_data.get_params()
links = VK_API.get_photo_url_type_size(res_VK)
date = VK_API.get_photo_likes_date(res_VK)
user_data = res_VK_data.users_info()[0]
name_user = user_data.get('first_name')
last_name_user = user_data.get('last_name')


def get_create_json(date, links):
    # соединяем в единый список количество лайков по дате и типоразмер
    ready_lst = []
    size_lst = [size for url, size in links]
    lst = [[x, y] for x, y in (list(zip(date, size_lst)))]
    for item in lst:
        json_dict = {'file_name': item[0],
                     'size': item[1]}
        ready_lst.append(json_dict)
    with open(rf'JSON/{name_user}_{last_name_user}.json', 'w') as write_file:
        return json.dump(ready_lst, write_file)

json_file = get_create_json(date, links)


class YaDisck:
    '''Метод загружает по ссылкам фотографии на Яндекс.Диск'''
    def __init__(self, ya_token, user_id, name, last_name, file_name):
        self.token = ya_token
        self.id = user_id
        self.name = name
        self.last_name = last_name
        date = file_name
        self.headers = {'Content-Type': 'application/json',
                   'Authorization': f'OAuth {self.token}'}
    
    def create_folder(self):
        # Создание общей папки на Яндекс.Диске для загрузки фотографий из вк,
        # затем, в этой папке создаём именованные папки под каждый профиль
        print('Создаём папки на Яндекс.Диске...')
        # запрос для создания папки на Я.Диске для фотографий
        create_url = 'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fphoto_from_vk'
        # запрос для создания папки по имени и фамилии профиля
        create_folder_profile_url = f'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fphoto_from_vk%2F{self.name}_{self.last_name}'
        response_create_url = requests.put(create_url, headers=self.headers)
        if response_create_url.status_code == 201:
            response_create_folder_profile_url = requests.put(create_folder_profile_url, headers=self.headers)
            if response_create_folder_profile_url.status_code == 201:
                return 'Успешно!'
            else:
                return f'Ошибка! Код ошибки: {response_create_folder_profile_url.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'
        elif response_create_url.status_code == 409:
            response_create_folder_profile_url = requests.put(create_folder_profile_url, headers=self.headers)
            if response_create_folder_profile_url.status_code == 201:
                return 'Успешно!'
            elif response_create_folder_profile_url.status_code == 409:
                return 'Папка уже существует.'
            else:
                return f'Ошибка! Код ошибки: {response_create_folder_profile_url.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'
        else:
            return f'Ошибка! Код ошибки: {response_create_url.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'
        
    def uploader(self):
        # Загружаем фотографии в папку
        print('Скачиваем фотографии с профиля и загружаем на Яндекс.Диск')
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        what_to_upload = [i for i, x in links]
        lst = list(zip(what_to_upload, date))
        for item in lst:
            where_to_upload = f'photo_from_vk/{self.name}_{self.last_name}'
            params = {'url': f'{item[0]}', 'path': f'{where_to_upload}/{item[1]}.jpeg', 'disable_redirects': 'false'}
            person_response = requests.post(url, headers= self.headers, params= params)
        if person_response.status_code == 202:
            return 'Успешно! Проверьте в Яндекс.Диске папку "photo_from_vk"'
        else:
            f'Ошибка! Код ошибки: {person_response.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'

name_user = user_data.get('first_name')
last_name_user = user_data.get('last_name')

if __name__ == '__main__':
    YaDisck_info = YaDisck(ya_token,
                            user_id,
                            name_user,
                            last_name_user,
                            file_name = date)
    print(YaDisck_info.create_folder())
    print(YaDisck_info.uploader())
    
# запустить в консоли: pip freeze > requirements.txt