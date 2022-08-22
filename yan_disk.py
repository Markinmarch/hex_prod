import requests
import VK_api

ya_token = input('Введите OAuth-токен: ')

class YaDisck:
    '''Метод загружает по ссылкам фотографии на Яндекс.Диск'''
    def __init__(self, ya_token, name, last_name, file_name):
        self.token = ya_token
        self.name = name
        self.last_name = last_name
        self.file_name = file_name
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
        what_to_upload = [i for i, x in VK_api.links]
        lst = list(zip(what_to_upload, self.file_name))
        for item in lst:
            where_to_upload = f'photo_from_vk/{self.name}_{self.last_name}'
            params = {'url': f'{item[0]}', 'path': f'{where_to_upload}/{item[1]}.jpeg', 'disable_redirects': 'false'}
            person_response = requests.post(url, headers= self.headers, params= params)
        if person_response.status_code == 202:
            return 'Успешно! Проверьте в Яндекс.Диске папку "photo_from_vk"'
        else:
            f'Ошибка! Код ошибки: {person_response.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'

YaDisck_info = YaDisck(ya_token,
                       VK_api.name_user,
                       VK_api.last_name_user,
                       VK_api.file_name)
ready_create_folde = YaDisck_info.create_folder()
ready_to_upload = YaDisck_info.uploader()