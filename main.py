import requests
import json
from pprint import pprint


class VK:

    def __init__(self, access_token_, user_id_, version='5.131'):
        self.token = access_token_
        self.id = user_id_
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def photo_get(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1, 'count': 1000}
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
        # pprint(url_list)

        file_name = []
        req = self.photo_get()["response"]["items"]  # [0]["sizes"][0]
        for item in req:
            if str(item['likes']['count'])+'.jpg' not in file_name:
                file_name.append(str(item['likes']['count']) + '.jpg')
            else:
                file_name.append(str(item['likes']['count']) + '_' + str(item['date']) + '.jpg')

        json_file = [dict(zip(file_name, best_type_list))]

        with open('jfile.json', 'w') as f:
            json.dump(json_file, f)
        return url_list


class YaUploader:
    def __init__(self, token: str):
        self.token = token

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
        return


    def upload_file_to_disk(self):

        url1 = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        url = 'https://sun9-63.userapi.com/c9591/u00001/136592355/w_62aef149.jpg'

        path = '/1/777'
        self._folder_('1')
        headers = self.get_headers()
        params = {'url': url,"path": path}
        response = requests.post(url1, headers=headers, params=params)

        return response




if __name__ == '__main__':

    with open('tokenvk.txt', 'r') as file_object:
        access_token = file_object.read().strip()

    user_id = int(input('Введите id пользователя:'))
    vk = VK(access_token, user_id)
    pprint(vk.json_get())

    with open('tokenyan.txt', 'r') as file_object:
        token = file_object.read().strip()
    
    ya = YaUploader(token)



    ya.upload_file_to_disk()

