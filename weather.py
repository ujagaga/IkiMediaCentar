#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Script to display weather data. Uses www.weatherbit.io.
Dependencies: pip3 install requests
City ID can be acquired from city.list.json.gz at: http://bulk.openweathermap.org/sample/city.list.json.gz
'''

import requests
import json


API_KEY = "6b15e16bb3dc4ba1b063d0836d56ce44"
API_URL = "http://api.weatherbit.io/v2.0/current"
CITY_ID = '789518'      # Kikinda
# CITY_ID = '3194360'   # Novi Sad
# CITY_ID = '783814'    # Zrenjanin
# CITY_ID = '792680'    # Beograd
ASCII_ICON_DAY = {
    '200': '\u2633', '201': '\u2633', '202': '\u2633', '230': '\u2633', '231': '\u2633', '232': '\u2633',
    '233': '\u2633', '300': '\u1F328', '301': '\u1F328', '302': '\u1F328', '500': '\u1F327', '501': '\u1F327',
    '502': '\u1F327', '511': '\u1F327', '520': '\u1F327', '521': '\u1F327', '522': '\u1F327', '600': '\u1F328',
    '601': '\u1F328', '602': '\u1F328', '610': '\u1F328', '611': '\u1F328', '612': '\u1F328', '621': '\u1F328',
    '622': '\u1F328', '623': '\u1F328', '700': '\u2601', '711': '\u2601', '721': '\u2601', '731': '\u2601',
    '741': '\u2601', '751': '\u2601', '800': '\u263C', '801': '\u263C', '802': '\u26C5', '803': '\u1F324',
    '804': '\u1F324', '900': '\u2614'
}

ASCII_ICON_NIGHT = {
    '200': '\u2633', '201': '\u2633', '202': '\u2633', '230': '\u2633', '231': '\u2633', '232': '\u2633',
    '233': '\u2633', '300': '\u1F328', '301': '\u1F328', '302': '\u1F328', '500': '\u1F327', '501': '\u1F327',
    '502': '\u1F327', '511': '\u1F327', '520': '\u1F327', '521': '\u1F327', '522': '\u1F327', '600': '\u1F328',
    '601': '\u1F328', '602': '\u1F328', '610': '\u1F328', '611': '\u1F328', '612': '\u1F328', '621': '\u1F328',
    '622': '\u1F328', '623': '\u1F328', '700': '\u2601', '711': '\u2601', '721': '\u2601', '731': '\u2601',
    '741': '\u2601', '751': '\u2601', '800': '\u263D', '801': '\u263D', '802': '\u26C5', '803': '\u1F324',
    '804': '\u1F324', '900': '\u2614'
}


def query_server():
    url_params = {'key': API_KEY, 'city_id': CITY_ID}
    r = requests.get(API_URL, params=url_params)
    json_ret_val = json.loads(r.text)

    return json_ret_val


def output_to_display(text):
    file = open('/tmp/display', 'w')
    file.write(text)
    file.close()


if __name__ == '__main__':
    response = query_server()
    data = response['data'][0]
    temp = data['temp']
    weather = data['weather']
    description = weather['description']
    weather_code = '{}'.format(weather['code'])
    weather_icon = weather['icon']

    if weather_icon.endswith('n'):
        icon = ASCII_ICON_NIGHT[weather_code]
    else:
        icon = ASCII_ICON_DAY[weather_code]

    msg = '{}{}C {} {}'.format(temp, u'\N{DEGREE SIGN}', description, icon)

    output_to_display(msg)
