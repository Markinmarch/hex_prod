import requests

def main():

    response = requests.get('https://api.vk.com/method/photos.get', params = {'user_id': 501244677, 'v': 5.131, 'access_token': 'vk1.a.EDgakxBbcab3YsfNh1PCTGD5nXvM1O5zGqH8FC5oLH8SkAc1o54qXZczueHJQdNHScD80HO5vMPCsgP0IoAlUN5hb5N6STIGHwhhxrd86nMJXgPN5KgF5V-HSTTuUDa9Oel5vw4tScZBSkYw7lVbD15Ul1Gq996M4AXe_NZ8PZ8ABbsAtKi-zt5OY2K8IuAr', 'album_id': 'profile', 'count': 2})
    return response.json()

if __name__ == '__main__':
    print(main())