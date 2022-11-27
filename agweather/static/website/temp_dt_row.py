from datetime import datetime, timedelta


class DatetimeRow():    # Класс формирует строку дат для массива прогноза
    def __init__(self, forec_len_days):

        begin_date = beging_forec_date()  # Начальная дата
        # Суточный период прогнозов = 6 часов
        step = timedelta(hours=6)
        self.__datetime_row = [
            begin_date + i*step for i in range(0, forec_len_days*4)]  # Строка дат
        # self.__datetime_row = [i.strftime("%d.%m %H:%M") for i in self.__datetime_row]

    def get_row(self):
        return self.__datetime_row


def beging_forec_date():  # Вычисляет дату начала прогноза. Шаг 6 часов: 3:00, 9:00, 15:00, 21:00
    dt = datetime.now()  # Сейчас местное время
    dt = dt.replace(minute=0, second=0, microsecond=0)
    bhour = (((dt.hour-3)//6+1)*6+3)
    if bhour == 27:
        dt = dt.replace(hour=3)
        dt = dt + timedelta(days=1)
    else:
        dt = dt.replace(hour=bhour)
    return dt

if __name__ == '__main__':
    print(datetime.now())
    print(beging_forec_date())

    r = DatetimeRow(7).get_row()
    print(r)
