import logging
import main_CW
import requests

response = requests.get(url='https://api.vk.com/method/users.get',
                        params = {'access_token': main_CW.access_token,
                                  'user_id': main_CW.user_id,
                                  'v': '5.131'})

class ContextFilter(logging.Filter):
    ''' Фильтр, который вводит контекстную информацию в журнал.'''

    USER = main_CW.name_user + ' ' + main_CW.last_name_user
    ID = main_CW.user_id

    def filter(self, record):

        record.ip = (ContextFilter.ID)
        record.user = (ContextFilter.USER)
        return True

if __name__ == '__main__':
    levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    logging.basicConfig(filename='activeApp.log',
                        level=logging.DEBUG,
                        format='%(asctime)-15s %(name)-5s %(levelname)-8s Id: %(ip)-15s User: %(user)-8s %(message)s',
                        encoding='utf-8',)

    links = logging.getLogger('Ссылки     ')
    authenticity = logging.getLogger('Подлинность')

    filt = ContextFilter()
    links.addFilter(filt)
    authenticity.addFilter(filt)
       
if len(main_CW.ya_token) == 39:
    links.info('Информация корректна')
    links.debug([i for i, q in main_CW.links])
else:
    links.error(f'Данные не верны. Проверьте формат переменных "ya_token" или "user_id"!')

if response.status_code == 200:
    authenticity.info('Информация доступна')
    authenticity.debug(response.json())
else:
    authenticity.error('Внимание! Ошибка доступа!', response.status_code)
    authenticity.critical(main_CW.__dict__)
 
print('Смотри логи в файле "activeApp.log"')