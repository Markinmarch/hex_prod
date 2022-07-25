# проверка работы токена
import requests

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()


access_token = 'vk1.a.EDgakxBbcab3YsfNh1PCTGD5nXvM1O5zGqH8FC5oLH8SkAc1o54qXZczueHJQdNHScD80HO5vMPCsgP0IoAlUN5hb5N6STIGHwhhxrd86nMJXgPN5KgF5V-HSTTuUDa9Oel5vw4tScZBSkYw7lVbD15Ul1Gq996M4AXe_NZ8PZ8ABbsAtKi-zt5OY2K8IuAr'
user_id = '8225633'
vk = VK(access_token, user_id)
print(vk.users_info())
