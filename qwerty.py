import requests
import datetime
import json

class VK_API:
    '''Класс, для определения требуемых параметров'''
    def __init__(self, user_id,
                 access_token,
                 version = 5.131,
                 album = 'profile',
                 extended = True,
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
    # функция, которая берёт фотографии со страницы
    def get_params(self):
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
        get_list_date = []
        for item in res.values():
            for inside_params in item['items']:
                date = datetime.datetime.fromtimestamp(int(inside_params['date']))
                get_list_date.append(date.strftime('%Y-%m-%d'))
        get_list_likes = []
        for item in res.values():
            for inside_params in item['items']:
                get_list_likes.append(str(inside_params['likes']['count']))
        lst = ['_'.join(i) for i in zip(get_list_likes, get_list_date)]
        return lst  
 
    # вне зависимости от размера фотографий, количества* и прочих параметров, эта функция всегда
    # будет выводить ссылки на самые большие фотографии и размеры иже         
    def get_photo_url_type_size(res):
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
    
    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        response = requests.get(url, params = {'access_token': self.token,
                                               'user_id': self.id,
                                               'v': self.version})
        return response.json().get('response') 
    
# вводим свой токен и id пользователя страницы
access_token = 'vk1.a.EDgakxBbcab3YsfNh1PCTGD5nXvM1O5zGqH8FC5oLH8SkAc1o54qXZczueHJQdNHScD80HO5vMPCsgP0IoAlUN5hb5N6STIGHwhhxrd86nMJXgPN5KgF5V-HSTTuUDa9Oel5vw4tScZBSkYw7lVbD15Ul1Gq996M4AXe_NZ8PZ8ABbsAtKi-zt5OY2K8IuAr'
user_id = 501244677


res_VK_data = VK_API(user_id, access_token)
res_VK = res_VK_data.get_params()
links = VK_API.get_photo_url_type_size(res_VK)
date = VK_API.get_photo_likes_date(res_VK)
user = VK_API(user_id, access_token)
# print(date, links)
user_data = user.users_info()[0]
# print(user_data.get('first_name'))

class json_file:
    '''Метод для формирования информации по файлу'''
    
    def __init__(self, likes_and_date, url_and_type_size):
        # указываем два параметра: количество лайков c датой, ссылки и типоразмер
        self.file_name = likes_and_date
        self.url_type = url_and_type_size

    def get_name_file(self):
        ready_lst = []
        size_lst = [size for url, size in self.url_type]
        lst = [[x, y] for x, y in (list(zip(self.file_name, size_lst)))]
        for item in lst:
            json_dict = {'file_name': item[0],
                         'size': item[1]}
            ready_lst.append(json_dict)
        return ready_lst
 
    def get_link(self):
        link_list = []
        for url in self.url_type:
            params = {'url': url[0]}   
            link_list.append(params)
        return link_list

res_json_data = json_file(date, links)
res_json_name = res_json_data.get_name_file()
res_json_link = res_json_data.get_link()
file_JSON = json.dumps(res_json_name)
# print(res_json_name)
# print(res_json_link)
# print(file_JSON)




class YaDisck:

    def __init__(self, ya_token, user_id, name, last_name, file_name):
        self.token = ya_token
        self.id = user_id
        self.name = name
        self.last_name = last_name
        self.file_name = file_name
    
    def create_folder(self):
        # запрос для создания папки на Я.Диске для фотографий
        create_url = 'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fphoto_from_vk'
        # запрос для создания папки по имени и фамилии профиля
        create_folder_profile_url = f'https://cloud-api.yandex.net/v1/disk/resources?path=%3A%2Fphoto_from_vk%3A%2F{self.name}_{self.last_name}'
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'OAuth {self.token}'}
        response_create_url = requests.put(create_url, headers=headers)
        response_create_url.raise_for_status()
        return response_create_url.status_code

        # raise_for_status(response_create_url)
        # if response_create_url.status_code == 201:
        #     response_create_folder_profile_url = requests.put(create_folder_profile_url, headers=headers).json()
        #     response.raise_for_status(response_create_folder_profile_url)
        #     if response_create_folder_profile_url.status_code == 201:
        #         return 'Успешно!'
        #     else:
        #         return f'Ошибка! Код ошибки: {response_create_folder_profile_url}'
        # elif response_create_url.status_code == 409:
        #     response_create_folder_profile_url = requests.put(create_folder_profile_url, headers=headers).json()
        #     response.raise_for_status(response_create_folder_profile_url)
        #     if response_create_folder_profile_url.status_code == 201:
        #         return 'Успешно!'
        #     else:
        #         return f'Ошибка! Код ошибки: {response_create_folder_profile_url.status_code}'
        # else:
        #     return f'Ошибка! Код ошибки: {response_create_url.status_code}'
        
    # def uploader(self, path):
    #     upload_url = ''
            
             
            
        
        

ya_token = 'AQAAAAA6JGSpAADLW9-3KotoUvEhl8HN9VNgOg'
name_user = user_data.get('first_name')

last_name_user = user_data.get('last_name')
YaDisck_info = YaDisck(ya_token,
                       user_id,
                       name_user,
                       last_name_user,
                       file_name = date)
print(YaDisck_info.create_folder())

# redress = YaDisck_info.create_folder()
# print(YaDisck.create_folder(redress))