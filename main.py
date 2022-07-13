import requests
import json
import time
from tqdm import tqdm


with open('tokenvk.txt', 'r') as file_object:
    access_token = file_object.read().strip()
with open('tokenyan.txt', 'r') as f:
    token = f.read().strip()


class VK:

    def __init__(self, access_token_, version='5.131'):
        self.access_token_ = access_token_
        self.token = token
        self.id_1 = id_1
        self.version = version
        self.token = token
        self.params = {'access_token': self.access_token_, 'v': self.version}

    def photo_get(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id_1, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1, 'count': 1000}
        response = requests.get(url, params={**self.params, **params})

        return response.json()

    def json_get(self):
        best_type_list = []
        url_list = []
        req = self.photo_get()["response"]["items"]
        for item in req:
            dict_type = {'w': 10, 'z': 9, 'y': 8, 'r': 7, 'q': 6, 'p': 5, 'o': 4, 'x': 3, 'm': 2, 's': 1}
            best_url = None
            best_type = 0
            max_type = 0
            for size in item['sizes']:
                if dict_type[size["type"]] > max_type:
                    max_type = dict_type[size["type"]]
                    best_url = size['url']
                    best_type = size["type"]
            url_list.append(best_url)
            best_type_list.append(best_type)

        file_name = []
        req = self.photo_get()["response"]["items"]
        for item in req:
            if str(item['likes']['count'])+'.jpg' not in file_name:
                file_name.append(str(item['likes']['count']) + '.jpg')
            else:
                file_name.append(str(item['likes']['count']) + '_' + str(item['date']) + '.jpg')
        return url_list, file_name, best_type_list

    def make_json(self):
        json_file = [dict(zip(self.json_get()[1], self.json_get()[2]))]
        with open('jfile.json', 'w') as f:
            json.dump(json_file, f)
        print('Файл jfile.json - создан')
        return

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _folder_(self, folder_name):

        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder_name}
        response = requests.put(url, headers=headers, params=params)
        return response

    def upload_file_to_disk(self):
        self.make_json()
        url1 = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        if quantity <= len(self.json_get()[0]):
            self._folder_(id_1)
            print('Папка для копирования фото создана ')
            for i in tqdm(range(quantity)):
                time.sleep(1)
                url = self.json_get()[0][i]
                path = '/' + str(id_1) + '/' + self.json_get()[1][i]
                headers = self.get_headers()
                params = {'url': url, "path": path}
                requests.post(url1, headers=headers, params=params)
            print('Загрузка завершена')
            return
        else:
            print('Количество запрашиваемых фото для сохранения больше,чем есть в альбоме')


if __name__ == '__main__':
    id_1 = int(input('Введите id пользователя:'))
    quantity = int(input('Введите кол-во фото для скачивания:'))
    vk = VK(access_token)
    vk.upload_file_to_disk()
