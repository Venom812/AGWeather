import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import re
import json
import os

forecast_sources_names = ('РП5', 'Яндекс Погода',
                          'Meteoinfo.ru', 'Foreca.ru')
forecast_sources_urls = ("https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5",
                         "https://yandex.ru/pogoda/details/10-day-weather",
                         "https://meteoinfo.ru/forecasts",
                         # в конце добавлять дату в виде "20221116"
                         "https://www.foreca.ru/Russia/Saint_Petersburg?details=",
                         )
forecast_sources_colors = (
    '#1E90FF', '#FF0000', '#00FF00', '#fbff00')  # Цвета на графике
weather_parameters = (
    'Температура, °С', 'Давление, мм.рт.ст.', 'Скорость ветра, м/с')


def scarp_forecasts():  # Функция сбора данных с сайтов прогнозов погоды

    # forecasts_json_filename = datetime.now().replace(minute=0).strftime("forecasts_%d.%m_%H:%M")
    # folder_database_json = ("database_json/forecasts/")
    # if not os.path.exists(folder_database_json):
    #     os.mkdir(folder_database_json)
    # path_to_json_file = folder_database_json + "/" + forecasts_json_filename + ".json"

    # if os.path.isfile(path_to_json_file):
    #     with open(path_to_json_file) as file:
    #         json_data = json.load(file)
    #         file.close()
    #         json_data[0] = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in json_data[0]]
    #     return json_data


    # Ряд дат и времени с шагом 6 часов
    datetime_row = DatetimeRow(14).get_row() # Длина ряда 14 суток
    datetime_row_len = len(datetime_row)
    datetime_row_begin = datetime_row[0]
    
    forecasts_data_list = []
    
    scrap_source_succeed = False

    try: # Сайт прогноза РП5
        source_id = 0  
        source_name = forecast_sources_names[source_id]
        url = forecast_sources_urls[source_id]
        headers = {
            "Accept":  "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            # "Cookie":  "__utmz=66441069.1651364377.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); extreme_open=true; _ga=GA1.2.261921522.1651364377; tab_synop=1; tab_wug=1; tab_metar=1; full_table=1; ftab=t6; PHPSESSID=25e0f70662735d7dea1a83c4dd41e2e9; __utmc=66441069; i=4967|7285|7285|7285|7285; iru=4967|7285|7285|7285|7285; ru=Лодейное Поле|Санкт-Петербург|Санкт-Петербург|Санкт-Петербург|Санкт-Петербург; last_visited_page=http://rp5.ru/Погода_в_Санкт-Петербурге; lang=ru; __utma=66441069.261921522.1651364377.1668574755.1668580278.46; __utmt=1; __utmb=66441069.1.10.1668580278; cto_bundle=__utmz=66441069.1651364377.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); extreme_open=true; _ga=GA1.2.261921522.1651364377; tab_synop=1; tab_wug=1; tab_metar=1; full_table=1; ftab=t6; PHPSESSID=25e0f70662735d7dea1a83c4dd41e2e9; __utmc=66441069; __utma=66441069.261921522.1651364377.1668574755.1668580278.46; iru=4967|7285|7285|7285|7285; ru=Лодейное Поле|Санкт-Петербург|Санкт-Петербург|Санкт-Петербург|Санкт-Петербург; __utmb=66441069.3.10.1668580278; cto_bundle=ML561l91ekxEUXN6bE1MZDIyZCUyRjNNJTJGOHJRRk8lMkZiTTdreTB4TUswb2lmaEVkVnRsQlVwTHRQeSUyQmxoN21mcTJ3Z0R2bUNrcURVMTJDWHNiS1Z3WkhLOVZ3MGZjdUJhbWo5OEhxcHlISUtFVXNqRyUyRk5tSHFVajNqNk9CbHZzUHpmT2tjU3VXTmVVb0R1ZE9VUU1pZm4lMkYxSVdzUFElM0QlM0Q; lang=en; i=7285|7285; ien=7285|7285; en=Saint Petersburg|Saint Petersburg; last_visited_page=http://rp5.ru/Weather_in_Saint_Petersburg,_Russia",
            "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        }

        req = requests.get(url, headers=headers)
        src = req.text

        # with open("rp5.html", "w") as file:
        #     file.write(src)
        # return
        
        # with open("rp5.html") as file:
        #     src = file.read()
        # src = req.text

        soup = BeautifulSoup(src, "lxml")
        # Получаем данные из таблицы семидневного прогноза
        ftab = soup.find(id='ftab_6_content')
        # return

        # Извлекаем из источника начальную дату/вермя прогноза
        source_begin_datetime = ftab.b.get_text()  # ftab[0].find('td').get_text()
        source_begin_datetime = func_source_begin_datetime(
            month_rusname_to_number(source_begin_datetime),
            int(re.findall(r'\d+', source_begin_datetime)[0]),
            # int(ftab[1].find_all('td')[1].get_text())
            int(ftab.find(class_='underlineRow').next_sibling.next_sibling.get_text())
        )

        # добавки пустых значений вначале рядов или их обрезки для выравнивания в соотвествии рядом дат/времени datetime_row
        add_none, cut_exc = add_none_or_cut_exc(
            source_begin_datetime, datetime_row_begin)

        # Формируем ряд температур
        t_row = ftab.find_all(class_='toplineRow')[
            1:][cut_exc:][:datetime_row_len]
        t_row = [int(t.find(class_='t_0').get_text()) for t in t_row]
        t_row = add_none + t_row
        # print(t_row)

        # Формируем ряд давлений
        p_row = ftab.find_all(class_="p_0")[1:][cut_exc:][:datetime_row_len]
        p_row = [int(p.get_text()) for p in p_row]
        p_row = add_none + p_row
        # print(p_row)

        # Формируем ряд скоростей ветра
        w_row = ftab.find('a', class_="t_wind_velocity").parent.parent.find_all('td')
        w_row = [int(w.get_text().strip().split(' ')[0]) for w in w_row[1:]][cut_exc:][:len(t_row)]
        # print(w_row)

        # w_row = ftab.find_all(class_="wv_0")[1:][cut_exc:][:len(t_row)]
        # w_row = [int(w.get_text()) for w in w_row]
        w_row = add_none + w_row

        forecasts_data_list.append(((source_name, forecast_sources_colors[source_id]), (t_row, p_row, w_row)))
    except Exception:
        print(f"Failed scrap data on site {source_name}")

    try: # Сайт прогноза Яндекс Погода  
        source_id = 1  
        source_name = forecast_sources_names[source_id]
        url = forecast_sources_urls[source_id]

        source_name = forecast_sources_names[source_id]
        url = forecast_sources_urls[source_id]

        cookies = {
            'yandexuid': '6369593541650645601',
            'yuidss': '6369593541650645601',
            '_ym_uid': '1650645655385690765',
            'my': 'YwA=',
            'font_loaded': 'YSv1',
            'gdpr': '0',
            'amcuid': '3558357171651151328',
            'mda': '0',
            '_ym_d': '1667327762',
            'ymex': '1966005601.yrts.1650645601#1982746660.yrtsi.1667386660',
            'skid': '8561683441667921562',
            'uxs_uid': 'd9045580-644e-11ed-8f6a-438c9740570a',
            'i': 'squGayj7lbSNIwCFQQGUXkLB5aypG6L0r2yACW21lZwwZWMDjD45bXUDw3ZL+z2rSsaxOXMA9nzvfLZDB2WX2ZUnLpM=',
            'spravka': 'dD0xNjY4OTg1MTY0O2k9OTEuMTIyLjEwMy44MztEPTQzNEIzM0JGN0M0OTUyNDE4MzZCRjNCQUQ5NDE0MTkyNTJFNUIxOUU3OEFBOUQxNUM4N0Y2NDcwMEQzRjVGNkZDQjc4MUZEQzt1PTE2Njg5ODUxNjQ5Nzc5Nzc3NjU7aD05NDczMWE5NTYzNjM3YzA4MTE4M2ZiOTg0ODc0NDJhOQ==',
            'L': 'cncHQ10GQgxsBlR6eH9Sf3t+A29mbVdBJyMeKFcJNFYO.1669151070.15169.344711.46c0e96d1f5ad73f65f7ef3cbd2b7c1d',
            'yandex_login': 'skorodeev',
            'is_gdpr': '0',
            'is_gdpr_b': 'CIy8DhD4lgEoAg==',
            '_ym_isad': '2',
            'Session_id': '3:1669412327.5.1.1650956094897:YLBGsg:26.1.2:1|1130000058249596.4971645.2.2:4971645|127962874.18194976.2.2:18194976|3:10261701.377478.P3fgw6bQRYqKNHpQyqKX09IzBWU',
            'sessionid2': '3:1669412327.5.1.1650956094897:YLBGsg:26.1.2:1|1130000058249596.4971645.2.2:4971645|127962874.18194976.2.2:18194976|3:10261701.377478.fakesign0000000000000000000',
            'ys': 'wprid.1669428573495036-15543319323650144929-vla1-2676-vla-l7-balancer-8080-BAL-7381',
            'yabs-frequency': '/5/000K0000000O5e1Z/xeoL_g7CbMISIMFRhd4u2UHwHfL9vmo0YKvMy-K8Of19HqhciQJTEgL6U4akqBxZfCqGodsWII37UsuddFRYIA19GB0XWpg3uSH7e4aWc44EFE6kx6wWII3uVTxcUYFIGw198Bv73eOlnGbXe4cWQN-gTPHHJa2XIO01bUDqs4l_UKoWII3PS8ct5BEIJQ198DgIfCn34kfoe4aW7SvxfH5gytsWII1ZIlIyL2gUUA590080/',
            'yp': '1671953118.csc.1#1700810964.pgp.1_27821249#1669879764.mcv.2#1669879764.mcl.1xopkpp#1669879764.szm.1:1920x1080:1920x929#1700901884.p_sw.1669365883#1700902233.p_undefined.1669366232',
            '_ym_visorc': 'b',
            '_yasc': 'WPXhbA/iUo8GzcJ0dAkL1g/HCue92zsZPBsk1HnNgOtQfdidFA8vtA+0Vuw6NvNmAN+e8/sc1UM8LT2KqDxw1Gs=',
            'cycada': 'gyHhxlceFbSSDLvEHbwKZTj/GrbqKvz4H/4PMPQbAfQ=',
        }

        headers = {
            'authority': 'yandex.ru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'yandexuid=6369593541650645601; yuidss=6369593541650645601; _ym_uid=1650645655385690765; my=YwA=; font_loaded=YSv1; gdpr=0; amcuid=3558357171651151328; mda=0; _ym_d=1667327762; ymex=1966005601.yrts.1650645601#1982746660.yrtsi.1667386660; skid=8561683441667921562; uxs_uid=d9045580-644e-11ed-8f6a-438c9740570a; i=squGayj7lbSNIwCFQQGUXkLB5aypG6L0r2yACW21lZwwZWMDjD45bXUDw3ZL+z2rSsaxOXMA9nzvfLZDB2WX2ZUnLpM=; spravka=dD0xNjY4OTg1MTY0O2k9OTEuMTIyLjEwMy44MztEPTQzNEIzM0JGN0M0OTUyNDE4MzZCRjNCQUQ5NDE0MTkyNTJFNUIxOUU3OEFBOUQxNUM4N0Y2NDcwMEQzRjVGNkZDQjc4MUZEQzt1PTE2Njg5ODUxNjQ5Nzc5Nzc3NjU7aD05NDczMWE5NTYzNjM3YzA4MTE4M2ZiOTg0ODc0NDJhOQ==; L=cncHQ10GQgxsBlR6eH9Sf3t+A29mbVdBJyMeKFcJNFYO.1669151070.15169.344711.46c0e96d1f5ad73f65f7ef3cbd2b7c1d; yandex_login=skorodeev; is_gdpr=0; is_gdpr_b=CIy8DhD4lgEoAg==; _ym_isad=2; Session_id=3:1669412327.5.1.1650956094897:YLBGsg:26.1.2:1|1130000058249596.4971645.2.2:4971645|127962874.18194976.2.2:18194976|3:10261701.377478.P3fgw6bQRYqKNHpQyqKX09IzBWU; sessionid2=3:1669412327.5.1.1650956094897:YLBGsg:26.1.2:1|1130000058249596.4971645.2.2:4971645|127962874.18194976.2.2:18194976|3:10261701.377478.fakesign0000000000000000000; ys=wprid.1669428573495036-15543319323650144929-vla1-2676-vla-l7-balancer-8080-BAL-7381; yabs-frequency=/5/000K0000000O5e1Z/xeoL_g7CbMISIMFRhd4u2UHwHfL9vmo0YKvMy-K8Of19HqhciQJTEgL6U4akqBxZfCqGodsWII37UsuddFRYIA19GB0XWpg3uSH7e4aWc44EFE6kx6wWII3uVTxcUYFIGw198Bv73eOlnGbXe4cWQN-gTPHHJa2XIO01bUDqs4l_UKoWII3PS8ct5BEIJQ198DgIfCn34kfoe4aW7SvxfH5gytsWII1ZIlIyL2gUUA590080/; yp=1671953118.csc.1#1700810964.pgp.1_27821249#1669879764.mcv.2#1669879764.mcl.1xopkpp#1669879764.szm.1:1920x1080:1920x929#1700901884.p_sw.1669365883#1700902233.p_undefined.1669366232; _ym_visorc=b; _yasc=WPXhbA/iUo8GzcJ0dAkL1g/HCue92zsZPBsk1HnNgOtQfdidFA8vtA+0Vuw6NvNmAN+e8/sc1UM8LT2KqDxw1Gs=; cycada=gyHhxlceFbSSDLvEHbwKZTj/GrbqKvz4H/4PMPQbAfQ=',
            'device-memory': '8',
            'downlink': '4.9',
            'dpr': '1.25',
            'ect': '4g',
            'if-none-match': 'W/"2ffd0-BBYs+QJzmKfgF9qh85l4LsAZ0Kk"',
            'referer': 'https://yandex.ru/pogoda/saint-petersburg?via=reg&lat=59.938951&lon=30.315635',
            'rtt': '150',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'viewport-width': '764',
        }

        params = {
            'lat': '59.938951',
            'lon': '30.315635',
            'via': 'ms',
        }

        response = requests.get(url, params=params, cookies=cookies, headers=headers)
        src = response.text

        soup = BeautifulSoup(src, 'lxml')

        ftab = soup.find(
            class_=['forecast-details', 'i-bem', 'forecast-details_js_inited'])

        # Извлекаем из источника начальную дату/вермя прогноза
        source_begin_datetime = func_source_begin_datetime(
            month_rusname_to_number(
                ftab.find(class_='forecast-details__day-month').get_text()),
            int(ftab.find(class_='forecast-details__day-number').get_text()),
            9  # Утро
        )

        # добавки пустых значений вначале рядов или их обрезки для выравнивания в соотвествии рядом дат/времени datetime_row
        add_none, cut_exc = add_none_or_cut_exc(
            source_begin_datetime, datetime_row_begin)

        # Формируем ряд температур
        t_row = ftab.find_all(
            class_='weather-table__temp')[cut_exc:][:datetime_row_len]
        t_row = [t.get_text() for t in t_row]
        # Преобразование температуры вида "+6...+8" в среднее значение
        t_row = [t.replace(chr(8722), '-').split('…') for t in t_row]
        t_row = [[int(i) for i in t] for t in t_row]
        t_row = [int(sum(t)/len(t)) for t in t_row]
        t_row = add_none + t_row

        # Формируем ряд давлений
        p_row = ftab.find_all(
            class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[cut_exc:][:datetime_row_len]
        p_row = [int(p.get_text()) for p in p_row]
        p_row = add_none + p_row

        # Формируем ряд скоростей ветра
        w_row = ftab.find_all(class_="wind-speed")[cut_exc:][:datetime_row_len]
        w_row = [int(round(float(w.get_text().replace(',', '.')), 0))
                for w in w_row]
        w_row = add_none + w_row

        forecasts_data_list.append(((source_name, forecast_sources_colors[source_id]), (t_row, p_row, w_row)))
    except Exception:
        print(f"Failed scrap data on site {source_name}")

    try: # Сайт Meteoinfo.ru
        source_id = 2  
        source_name = forecast_sources_names[source_id]
        url = forecast_sources_urls[source_id]

        source_name = forecast_sources_names[source_id]
        url = forecast_sources_urls[source_id]
        headers = {
            "Accept":  "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie":  "66c548aa3ec10b30907b199d946947a3=acaabv5dqa640hjt4tri78ql72; tmr_lvid=4b60becf8aecbedfc54868a7108788c3; tmr_lvidTS=1663960116332; _ym_uid=1663960117360748641; _ym_d=1663960117; _ym_isad=2; stan=1468; lstan=1468; START_POGODA_P=1468; tmr_detect=0%7C1663967623293; tmr_reqNum=55",
            "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        }

        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        # Получаем данные из таблицы десятидневного прогноза
        ftab = soup.find(id='div_4_1')
        ftab = ftab.find(class_='hidden-desktop')
        # print(ftab)

        # Извлекаем из источника начальную дату/вермя прогноза
        source_begin_datetime = ftab.find('nobr')
        begin_hour = source_begin_datetime.parent.next_sibling.get_text()
        begin_hour = 15 if begin_hour.strip().lower() == 'день' else 3
        source_begin_datetime = source_begin_datetime.get_text()
        source_begin_datetime = func_source_begin_datetime(
            month_rusname_to_number(source_begin_datetime),
            int(re.findall(r'\d+', source_begin_datetime)[0]),
            begin_hour
        )
        # return source_begin_datetime

        # добавки пустых значений вначале рядов или их обрезки для выравнивания в соотвествии рядом дат/времени datetime_row
        add_none, cut_exc = add_none_or_cut_exc(
            source_begin_datetime, datetime_row_begin)
        add_none = add_none[:len(add_none)//2]
        cut_exc //= 2

        # Формируем ряд температур
        t_row = ftab.find_all(class_='fc_temp_short')[
            cut_exc:][:datetime_row_len]
        t_row = [[int(t.get_text().rstrip('°')), 'none'] for t in t_row]
        t_row = add_none + sum(t_row, [])

        # Формируем ряд скоростей ветра
        w_row = ftab.find_all('i')[cut_exc:][:datetime_row_len]
        p_row = w_row
        w_row = [[int(w.next_sibling.get_text()), 'none'] for w in w_row]
        w_row = add_none + sum(w_row, [])
        #list(map(lambda x: int(x.next_sibling.get_text()), w_row))

        # Формируем ряд давлений
        p_row = [[int(p.parent.next_sibling.get_text()), 'none'] for p in p_row]
        p_row = add_none + sum(p_row, [])

        forecasts_data_list.append(((source_name, forecast_sources_colors[source_id]), (t_row, p_row, w_row)))
    except Exception:
        print(f"Failed scrap data on site {source_name}")

    try:  # Сайт Foreca.ru  
        source_id = 3  
        source_name = forecast_sources_names[source_id]
        url = forecast_sources_urls[source_id]

        source_name = forecast_sources_names[source_id]
        url = forecast_sources_urls[source_id]

        cookies = {
            'nlv': 'Russia%2FSaint_Petersburg-FCA-cnU6MTAwNDk4ODE3',
            '_ga': 'GA1.1.699186197.1668585320',
            'cc2018': '0bacfd01-bd10-4b5f-a264-2596b77220cc',
            'st2': 'lang%3Dru%26units%3Dmetricmmhg%26tf%3D24h%26ml%3D%26u%3DTRRTQZUZYY0A',
            '_ga_V376KP84L7': 'GS1.1.1669435053.16.0.1669435053.0.0.0',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }

        t_row, p_row, w_row = [], [], []

        old_url_with_date = ''
        for date in datetime_row[:36]:
            url_with_date = url + str(date).replace('-', '')[:8]
            if url_with_date != old_url_with_date:
                old_url_with_date = url_with_date
                req = requests.get(url_with_date, cookies=cookies, headers=headers)
                # print(url_with_date)
                src = req.text
                soup = BeautifulSoup(src, "lxml")
                with open("foreca.html", "w") as file:
                    file.write(src)
            try:
                # print(str(date)[11:16])
                tag = soup.find('strong', string=str(date)[11:16]).parent.parent
                tag = tag.next_sibling.next_sibling
                temp = int(tag.get_text().strip().replace('°', ''))
                tag = tag.next_sibling.next_sibling
                wind = int(tag.get_text().strip().replace(' м/с', ''))
                tag = tag.next_sibling.next_sibling
                press = int(tag.get_text().strip().split(' ')[-3])
            
            except Exception:
                temp = press = wind = 'none'
            finally:
                t_row.append(temp)
                p_row.append(press)
                w_row.append(wind)

        forecasts_data_list.append(((source_name, forecast_sources_colors[source_id]), (t_row, p_row, w_row)))
    except Exception:
        print(f"Failed scrap data on site {source_name}")

    
    forecasts_database_record = (datetime_row, forecasts_data_list)
    

    # with open(f"{folder_database_json}/{forecasts_json_filename}.json", "w", encoding="utf-8") as file:
    #     json.dump(forecasts_database_record, file, indent=4, sort_keys=True, default=str) #ensure_ascii=False)

    # (дата_вермя_ось_Х, дата_вермя_вспл), ((имя источника, цвет),(тепература, давление, скорость ветра))
    return forecasts_database_record

# def read_forecasts_record_from_json_file(path_to_json_file):
#     with open(path_to_json_file) as file:
#         data = json.load(file)
#     print(data[0][])
#     return "fuck"

class DatetimeRow():    # Класс формирует строку дат для массива прогноза
    def __init__(self, forec_len_days):

        begin_date = self.begin_forec_date()  # Начальная дата
        # Суточный период прогнозов = 6 часов
        step = timedelta(hours=6)
        self.datetime_row = [
            begin_date + i*step for i in range(0, forec_len_days*4)]  # Строка дат

    def get_row(self):
        return self.datetime_row

    @staticmethod
    def begin_forec_date():  # Вычисляет дату начала прогноза. Шаг 6 часов: 3:00, 9:00, 15:00, 21:00
        dt = datetime.now()  # Сейчас местное время
        dt = dt.replace(minute=0, second=0, microsecond=0)
        bhour = (((dt.hour-3)//6+1)*6+3)
        if bhour == 27:
            dt = dt.replace(hour=3)
            dt = dt + timedelta(days=1)
        else:
            dt = dt.replace(hour=bhour)
        return dt

# Функция извлечения из источника начальной даты/вермемени прогноза
def func_source_begin_datetime(begin_month, begin_day, begin_hour):
    begin_year = datetime.now().year
    if datetime.now().month == 12 and begin_month == 1:  # Обработка перехода через новый год
        begin_year += 1
    return datetime(year=begin_year, month=begin_month, day=begin_day, hour=begin_hour)

# Функция перевода имени месяца (на русском) в его номер
def month_rusname_to_number(name):

    month_numbers = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'май': 5,
                     'июн': 6, 'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12}

    number = name.strip().lower().split(' ')[-1][:3]
    number = month_numbers[number]

    return number

# Функция добавки пустых значений вначале рядов или их обрезки для выравнивания в соотвествии рядом дат/времени datetime_row
def add_none_or_cut_exc(source_begin_datetime, datetime_row_begin):
    if source_begin_datetime == datetime_row_begin:
        add_none, cut_exc = 0, 0
    elif source_begin_datetime > datetime_row_begin:
        add_none, cut_exc = (source_begin_datetime -
                             datetime_row_begin)//timedelta(hours=6), 0
    else:
        add_none, cut_exc = 0, (datetime_row_begin -
                                source_begin_datetime)//timedelta(hours=6)
    add_none = ['none' for i in range(0, add_none)]
    return add_none, cut_exc


if __name__ == '__main__':

    # for i in scarp_forecasts(1):
    forecasts = scarp_forecasts()
    print(forecasts)
    # quit()

    # forecast_all = [forecast_scarp(id,14) for id in range(0, len(forecast_sources_names)-1)]

    # forecast_all_T = list(zip(*forecast_all)) #[list(i) for i in zip(*forecast_all)]
    # forecast_all_T[1] = forecast_all_T[1][0]
