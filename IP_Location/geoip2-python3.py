#!/usr/bin/env python3
import socket
import geoip2.database
import argparse
import json

# default утгаараа python.org авдаг optional --hostname гэсэн коммандын мөрийн аргумент авдаг болгоно
parser = argparse.ArgumentParser(description='Get IP Geolocation info')
parser.add_argument('--hostname', action="store", dest="hostname", default='python.org')
# Коммандын мөрөөс авсан аргументаа parse хийнэ
given_args = parser.parse_args()
# Уг утгаа hostname хувьсагчид хадгална
hostname = given_args.hostname
# Уг домайн нэрийн харгалзах IP хаягийг авна
ip_address = socket.gethostbyname(hostname)
print("IP address: {0}".format(ip_address))
# GeoLite2-City.mmdb гэсэн өгөгдлийн санг унших обьект үүсгэнэ
reader = geoip2.database.Reader('GeoLite2-City.mmdb')
# Уг IP хаягийн газарзүйн мэдээллийг авч хэвлэнэ
response = reader.city(ip_address)
if response is not None:
    print('Country: ', response.country)
    print('Continent: ', response.continent)
    print('Location: ', response.location)
