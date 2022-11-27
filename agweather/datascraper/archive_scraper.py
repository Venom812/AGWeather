import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .forecasts_scraper import month_rusname_to_number

def scrap_archive():  # Функция сбора данных с сайтов прогнозов погоды

    # archive_datetime_row = ArchiveDatetimeRow(30).get_row() # Длина ряда 30 суток
    # end_archive_day = archive_datetime_row[-1][:10].split('-')[::-1]
    # end_archive_day = '.'.join(end_archive_day)

    cookies = {
        '__utmz': '66441069.1651364377.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'extreme_open': 'true',
        '_ga': 'GA1.2.261921522.1651364377',
        'tab_wug': '1',
        'tab_metar': '1',
        'full_table': '1',
        'ftab': 't6',
        'ien': '7285%7C7285%7C7285',
        'en': 'Saint%20Petersburg%7CSaint%20Petersburg%7CSaint%20Petersburg',
        'stat_parameter': '2',
        'tab_synop': '1',
        'PHPSESSID': '586d9cec3633265099ba0c94093a9653',
        'i': '7285%7C55%7C44%7C172631%7C7285',
        'iru': '7285%7C55%7C44%7C172631%7C7285',
        'ru': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%7C%D0%9D%D0%BE%D0%B2%D0%BE%D0%BF%D0%BE%D0%BB%D0%BE%D1%86%D0%BA%7C%D0%9F%D0%B5%D1%80%D0%B5%D0%B1%D1%80%D0%BE%D0%B4%D1%8C%D0%B5%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3',
        'last_visited_page': 'http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5',
        '__utma': '66441069.261921522.1651364377.1669439507.1669516649.67',
        '__utmc': '66441069',
        'format': 'xls',
        'f_enc': 'ansi',
        '__utmb': '66441069.3.10.1669516649',
        'lang': 'ru',
        'cto_bundle': 'lsNQD191ekxEUXN6bE1MZDIyZCUyRjNNJTJGOHJRRkxtTkcxcEgzelJhRTBIcjlDNHVJOGhRZCUyRmw4cWQ1Z0tXYVFnV1hmcUxsdDBtY1J1dSUyQnMybmFUNXZsTTNYJTJCdXNSMlUzWlpueiUyRkZEOSUyRnZLRGlOeXBvdE0za2xmcTNXcyUyQndpcVRDODVuMnpvd2slMkY1dlladEZtY3Vsb0F5RHRZMHclM0QlM0Q',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': '__utmz=66441069.1651364377.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); extreme_open=true; _ga=GA1.2.261921522.1651364377; tab_wug=1; tab_metar=1; full_table=1; ftab=t6; ien=7285%7C7285%7C7285; en=Saint%20Petersburg%7CSaint%20Petersburg%7CSaint%20Petersburg; stat_parameter=2; tab_synop=1; PHPSESSID=586d9cec3633265099ba0c94093a9653; i=7285%7C55%7C44%7C172631%7C7285; iru=7285%7C55%7C44%7C172631%7C7285; ru=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%7C%D0%9D%D0%BE%D0%B2%D0%BE%D0%BF%D0%BE%D0%BB%D0%BE%D1%86%D0%BA%7C%D0%9F%D0%B5%D1%80%D0%B5%D0%B1%D1%80%D0%BE%D0%B4%D1%8C%D0%B5%7C%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5; __utma=66441069.261921522.1651364377.1669439507.1669516649.67; __utmc=66441069; format=xls; f_enc=ansi; __utmb=66441069.3.10.1669516649; lang=ru; cto_bundle=lsNQD191ekxEUXN6bE1MZDIyZCUyRjNNJTJGOHJRRkxtTkcxcEgzelJhRTBIcjlDNHVJOGhRZCUyRmw4cWQ1Z0tXYVFnV1hmcUxsdDBtY1J1dSUyQnMybmFUNXZsTTNYJTJCdXNSMlUzWlpueiUyRkZEOSUyRnZLRGlOeXBvdE0za2xmcTNXcyUyQndpcVRDODVuMnpvd2slMkY1dlladEZtY3Vsb0F5RHRZMHclM0QlM0Q',
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
        'ArchDate': datetime.now().strftime("%d.%m.%Y"), 
        'pe': '30',
        'lang': 'ru',
        'time_zone_add': '3',
    }
    try:
        response = requests.post('https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5', cookies=cookies, headers=headers, data=data)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        arch_tab = soup.find('table', id='archiveTable').find_all('tr')[1:]
        source_datetime_row = [tr.find('td', class_='cl_dt') for tr in arch_tab]
        source_datetime_row = [tr.get_text() if tr else None for tr in source_datetime_row]
        year_list = [(tr[:4] if tr.find('г.') == 4 else None) if tr else None for tr in source_datetime_row]
        month_day_list = [tr.split('г.')[-1].split(',')[0].split('\xa0') if tr else None for tr in source_datetime_row]
        month_day_list = [str(month_rusname_to_number(tr[1])).zfill(2) + '-' + tr[0].zfill(2) if tr else None for tr in month_day_list]
        for i, year in enumerate(year_list):
            year_list[i] = year_list[i-1] if not year_list[i] else year
        for i, md in enumerate(month_day_list):
            month_day_list[i] = month_day_list[i-1] if not month_day_list[i] else md

        time_list, t_row, p_row, w_row = [], [], [], []
        for tr in arch_tab:
            time_list.append(tr.find_all('td')[-29].get_text())
            t_row.append(float(tr.find_all('td')[-28].div.get_text()))
            p_row.append(float(tr.find_all('td')[-27].div.get_text()))
            w_row.append(tr.find_all('td')[-22])

        w_row = [int(w.div.get_text().strip().split(' ')[0][1:]) if w.div else 0 for w in w_row]
        w_row = w_row[::-1]
        t_row = t_row[::-1]
        p_row = p_row[::-1]

        source_datetime_row = [f"{year_list[i]}-{month_day_list[i]}T{time_list[i]}:00:00" for i in range(0,len(source_datetime_row))]
        source_datetime_row = source_datetime_row[::-1]

        archive_database_record = (source_datetime_row , (t_row, p_row, w_row))
        # archive_database_record = list(zip(source_datetime_row, t_row, p_row, w_row))
        return archive_database_record

    except Exception:
        return

    

# class ArchiveDatetimeRow():    # Класс формирует строку дат для массива архива погоды
#     def __init__(self, archive_len_days):
#         # begin_archive_date = self.begin_archive_date(archive_len_days)  # Начальная дата
#         # Вычисляем дату начала архива. Шаг 3 часа: 0:00, 3:00 ...
#         begin_archive_date = datetime.now()  # Сейчас местное время
#         begin_archive_date = begin_archive_date.replace(minute=0, second=0, microsecond=0)
#         begin_hour = begin_archive_date.hour//3*3
#         begin_archive_date = begin_archive_date.replace(hour=begin_hour) - timedelta(archive_len_days)
#         # Период архива = 3 часа
#         step = timedelta(hours=3)
#         archive_len_steps = archive_len_days*8
#         self.archive_datetime_row  = [
#             begin_archive_date + i*step for i in range(0, archive_len_steps+1)]  # Ряд дат
#         self.archive_datetime_row = [i.isoformat() for i in self.archive_datetime_row]

#     def get_row(self):
#         return self.archive_datetime_row


if __name__ == '__main__':

    archive = scrap_archive()
    print(archive)