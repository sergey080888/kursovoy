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
        # print((url_list, best_type_list))
        return (url_list, best_type_list)

    def json_file_make(self):
        file_name = []
        req = self.photo_get()["response"]["items"]
        for item in req:
            if str(item['likes']['count'])+'.jpg' not in file_name:
                file_name.append(str(item['likes']['count']) + '.jpg')
            else:
                file_name.append(str(item['likes']['count']) + '_' + str(item['date']) + '.jpg')

        json_file = [dict(zip(file_name, self.json_get()[1]))]

        with open('jfile.json', 'w') as f:
            json.dump(json_file, f)
        return json_file


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def folder(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.put(url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self):
        req_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'url': url, 'path': path}
        response = requests.post(req_url, headers=headers, params=params)
        return response.json()


if __name__ == '__main__':

    with open('tokenvk.txt', 'r') as file_object:
        access_token = file_object.read().strip()

    user_id = int(input('Введите id пользователя:'))
    vk = VK(access_token, user_id)
    pprint(vk.json_get())
    print(vk.json_file_make())

    with open('tokenyan.txt', 'r') as file_object:
        token = file_object.read().strip()
    
    ya = YaUploader(token)
    path = 1
    ya.folder(path)
    url = 'https%3A%2F%2Fsun2.43222.userapi.com%2Fimpf%2Fc210%2Fv210001%2F6%2F53_VwoACy4I.jpg%3Fsize%3D2560x1913%26quality%3D96%26sign%3Dc55f340348a35dd86542875a57ad8537%26c_uniq_tag%3DRvD_7O5cznGnLGO2duPrnqHQrL-0KVHqGZMBe4FtTqI%26type%3Dalbum>'

    # ya.upload_file_to_disk(url, path)
