import requests


class IPtoGeo(object):
    def __init__(self, ip_address):
        # Тухайн IP хаягаас олж болох мэдээллийг хадгалах хувьсагчид
        self.latitude = ''
        self.longitude = ''
        self.country = ''
        self.city = ''
        self.time_zone = ''
        self.ip_address = ip_address
        self.get_location()

    def get_location(self):
        # HTTP GET request IP хаягийг параметр дамжуулан илгээж хариуг нь json format-аар авч байна
        json_request = requests.get('https://freegeoip.app/json/%s' % self.ip_address).json()
        # Уг ирсэн хариунд доорх түлхүүр байвал түүний утгийг классын атрибутуудад хадгална
        if 'country_name' in json_request.keys():
            self.country = json_request['country_name']
        if 'country_code' in json_request.keys():
            self.country_code = json_request['country_code']
        if 'time_zone' in json_request.keys():
            self.time_zone = json_request['time_zone']
        if 'city' in json_request.keys():
            self.city = json_request['city']
        if 'latitude' in json_request.keys():
            self.latitude = json_request['latitude']
        if 'longitude' in json_request.keys():
            self.longitude = json_request['longitude']


if __name__ == '__main__':
    # IPtoGeo классын обьект үүсгэж уг обьектыг dictionary хэлбэрээр хэвлэнэ
    ip = IPtoGeo('8.8.8.8')
    print(ip.__dict__)
