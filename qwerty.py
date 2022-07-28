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

# def main():

#     r = requests.get('https://api.vk.com/method/photos.get', params = {'user_id': 501244677, 'v': 5.131, 'access_token': 'vk1.a.EDgakxBbcab3YsfNh1PCTGD5nXvM1O5zGqH8FC5oLH8SkAc1o54qXZczueHJQdNHScD80HO5vMPCsgP0IoAlUN5hb5N6STIGHwhhxrd86nMJXgPN5KgF5V-HSTTuUDa9Oel5vw4tScZBSkYw7lVbD15Ul1Gq996M4AXe_NZ8PZ8ABbsAtKi-zt5OY2K8IuAr', 'album_id': 'profile', 'count': 2})
#     return r.json()

# if __name__ == '__main__':
    # print(main())