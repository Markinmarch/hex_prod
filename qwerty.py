import requests

class VK_API:
    '''Класс, для определения требуемых параметров'''
    def __init__(self, user_id, access_token, version = 5.131, album = 'profile'):
        # id страницы пользователя
        self.id = user_id
        # токен АПИ
        self.token = access_token
        # версия АПИ ВК
        self.version = version
        # указание на фотографии аватарок ('profile') https://vk.com/dev/photos.get
        self.album = album
    # функция, которая берёт фотографии со страницы
    def get_photo(self):
        url = 'https://api.vk.com/method/photos.get'
        response = requests.get(url, params = {'access_token': self.token,
                                               'user_id': self.id,
                                               'v': self.version,
                                               'album_id': self.album})
        return response.json()

access_token = ''
user_id = 501244677

res_VK = VK_API(user_id, access_token)
print(res_VK.get_photo())