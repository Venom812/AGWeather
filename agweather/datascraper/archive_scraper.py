"""Module scrapes data from archive source."""
from datetime import datetime
from json import load
import requests
from bs4 import BeautifulSoup
from .forecasts_scraper import month_rusname_to_number


def scrap_archive(path_to_config_file):
    """Run scarping archive data process."""
    # Reading configuration file
    with open(path_to_config_file, 'r', encoding='UTF-8') as file:
        datascraper_config = load(file)
    source_config = datascraper_config["archive_source"]

    try:

        data = source_config['data']
        data['ArchDate'] = datetime.now().strftime("%d.%m.%Y")
        req = requests.post(source_config['url'],
                            cookies=source_config['cookies'],
                            headers=source_config['headers'],
                            proxies=datascraper_config['proxies'],
                            data=data, timeout=10)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        # Parsing archive table data
        arch_tab = soup.find('table', id='archiveTable').find_all('tr')[1:]

        # Parsing source datetimerow
        source_datetime_row = [trow.find('td', class_='cl_dt')
                               for trow in arch_tab]
        source_datetime_row = [
            trow.get_text() if trow else None for trow in source_datetime_row]
        year_list = [(trow[:4] if trow.find('г.') == 4 else None) if trow
                     else None for trow in source_datetime_row]
        month_day_list = [trow.split('г.')[-1].split(',')[0].split('\xa0')
                          if trow else None for trow in source_datetime_row]
        month_day_list = [str(month_rusname_to_number(trow[1])).zfill(
            2) + '-' + trow[0].zfill(2) if trow else
            None for trow in month_day_list]
        for i, year in enumerate(year_list):
            year_list[i] = year_list[i-1] if not year_list[i] else year
        for i, mday in enumerate(month_day_list):
            month_day_list[i] = month_day_list[i - 1] \
                if not month_day_list[i] else mday

        # Parsing time_list, t_row, p_row, w_row
        time_list, t_row, p_row, w_row = [], [], [], []
        for trow in arch_tab:
            time_list.append(trow.find_all('td')[-29].get_text())
            t_row.append(float(trow.find_all('td')[-28].div.get_text()))
            p_row.append(float(trow.find_all('td')[-27].div.get_text()))
            w_row.append(trow.find_all('td')[-22])

        source_datetime_row = \
            [f"{year_list[i]}-{month_day_list[i]}T{time_list[i]}:00:00"
             for i in range(0, len(source_datetime_row))]
        w_row = [int(w.div.get_text().strip().split(' ')[0][1:])
                 if w.div else 0 for w in w_row]

        # Reversing data before saving
        w_row = w_row[::-1]
        t_row = t_row[::-1]
        p_row = p_row[::-1]
        source_datetime_row = source_datetime_row[::-1]

        # Prepearing database record
        archive_database_record = (source_datetime_row, (t_row, p_row, w_row))
        # print(archive_database_record)
        return archive_database_record

    except AttributeError:
        return


if __name__ == '__main__':
    pass
