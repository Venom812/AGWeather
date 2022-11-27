from datetime import datetime, timedelta

d = datetime.now().replace(minute=0,second=0, microsecond=0).isoformat()

a = '7777'

print(a.zfill(1))

print(len(d))

x = [1,2,3,4,5,6,7]

y = x

print(y)

import requests

cookies = {
    '__utmz': '66441069.1651364377.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'extreme_open': 'true',
    '_ga': 'GA1.2.261921522.1651364377',
    'tab_wug': '1',
    'tab_metar': '1',
    'full_table': '1',
    'ien': '7285%7C7285%7C7285',
    'en': 'Saint%20Petersburg%7CSaint%20Petersburg%7CSaint%20Petersburg',
    'stat_parameter': '2',
    'tab_synop': '1',
    'PHPSESSID': '586d9cec3633265099ba0c94093a9653',
    '__utmc': '66441069',
    'format': 'xls',
    'f_enc': 'ansi',
    '__utma': '66441069.261921522.1651364377.1669524939.1669530892.69',
    'i': '55%7C44%7C172631%7C7285%7C7285',
    'iru': '55%7C44%7C172631%7C7285%7C7285',
    'ru': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%7C%D0%9F%D0%B5%D1%80%D0%B5%D0%B1%D1%80%D0%BE%D0%B4%D1%8C%D0%B5%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3',
    'last_visited_page': 'http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5',
    'ftab': '2',
    '__utmt': '1',
    '__utmb': '66441069.9.10.1669530892',
    'lang': 'ru',
    'cto_bundle': 'z1HsWV91ekxEUXN6bE1MZDIyZCUyRjNNJTJGOHJRT1N3YnVmeFBlNHZoY1diJTJCS3hZSmJjUk14NWphUjVFU25GTXBYREZYZFFBczhtbU5UJTJCd3NuY0hkOHZDY1BMcnIzRlJQTm1MSjRBMUZuRzVDT1pDcGRsOUQ3bWQyQktIQWs0VWV1R1BrJTJGdUs0SElPRWQ4NFdxR29wb0lUWVZsYm13JTNEJTNE',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '__utmz=66441069.1651364377.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); extreme_open=true; _ga=GA1.2.261921522.1651364377; tab_wug=1; tab_metar=1; full_table=1; ien=7285%7C7285%7C7285; en=Saint%20Petersburg%7CSaint%20Petersburg%7CSaint%20Petersburg; stat_parameter=2; tab_synop=1; PHPSESSID=586d9cec3633265099ba0c94093a9653; __utmc=66441069; format=xls; f_enc=ansi; __utma=66441069.261921522.1651364377.1669524939.1669530892.69; i=55%7C44%7C172631%7C7285%7C7285; iru=55%7C44%7C172631%7C7285%7C7285; ru=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%7C%D0%9F%D0%B5%D1%80%D0%B5%D0%B1%D1%80%D0%BE%D0%B4%D1%8C%D0%B5%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5; ftab=2; __utmt=1; __utmb=66441069.9.10.1669530892; lang=ru; cto_bundle=z1HsWV91ekxEUXN6bE1MZDIyZCUyRjNNJTJGOHJRT1N3YnVmeFBlNHZoY1diJTJCS3hZSmJjUk14NWphUjVFU25GTXBYREZYZFFBczhtbU5UJTJCd3NuY0hkOHZDY1BMcnIzRlJQTm1MSjRBMUZuRzVDT1pDcGRsOUQ3bWQyQktIQWs0VWV1R1BrJTJGdUs0SElPRWQ4NFdxR29wb0lUWVZsYm13JTNEJTNE',
    'Origin': 'https://rp5.ru',
    'Referer': 'https://rp5.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'ArchDate': '26.11.2022',
    'pe': '30',
    'lang': 'ru',
    'time_zone_add': '3',
}

response = requests.post('https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5', cookies=cookies, headers=headers, data=data)