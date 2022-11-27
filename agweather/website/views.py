from django.http import HttpResponse
from django.shortcuts import render, redirect
from datascraper.forecasts_scraper import weather_parameters, forecast_sources_urls, forecast_sources_names
from datascraper.models import ForecastsRecord, ArchiveRecord
from datetime import datetime


def forecast(request):
    # return HttpResponse("FORECAST")

    if request.method == 'GET':
        weather_parameter = weather_parameters[0]
        forecast_length = 7  # длина прогноза по умолчанию дней

    elif request.method == 'POST':
        weather_parameter = request.POST.get('weather-parameter')
        forecast_length = request.POST.get('forecast-length')

    forecast_length = 7 if forecast_length == '' else int(forecast_length)
    
    if forecast_length > 14:
        forecast_length = 14
    elif forecast_length < 1:
        forecast_length = 1

    forecasts = ForecastsRecord.objects.latest('rec_date').rec_data
    weather_parameter_index = weather_parameters.index(weather_parameter)
    forecast_length_steps = forecast_length*4
    tooltip_titles = [datetime.fromisoformat(i).strftime(
        "%d.%m %H:%M") for i in forecasts[0][:forecast_length_steps]]  # Всплывающие ярлыки
    tooltip_titles = insert_steps(tooltip_titles, '')
    weekday_rus = {0: 'ПН', 1: 'ВТ', 2: 'СР',
                   3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}
    labels = [weekday_rus[datetime.fromisoformat(i).weekday()] if datetime.fromisoformat(
        i).hour == 9 else '' for i in forecasts[0][:forecast_length_steps]]  # Ярлыки оси Х для графика
    labels = insert_steps(labels, '')
    
    for index in range(len(labels)):
        if tooltip_titles[index][-5:] == '21:00':
            labels[index+1] = " "
        elif tooltip_titles[index][-5:] == '09:00':
            labels[index+1] = labels[index]
            labels[index] = ""

    datasets = []
    for forecast in forecasts[1]:
        datasets.append({
            'label': forecast[0][0],
            # [i+50 for i in forecast[2] if i != 'none'],
            'data': insert_steps(forecast[1][weather_parameter_index][:forecast_length_steps], 'none'),
            'borderColor': forecast[0][1],
            'backgroundColor': forecast[0][1],
        })

    chartjs_data = {
        'labels': labels,
        'datasets': datasets,
    }
    
    last_database_refresh = ForecastsRecord.objects.latest('rec_date').rec_date.strftime("Дата обновления:  %d.%m.%Y %H:%M UTC")
    # return HttpResponse(last_database_refresh)

    scales_list = ((-5, 5), (755, 765), (0, 10))
    chartjs_options = {'suggestedMin': scales_list[weather_parameter_index][0],
                       'suggestedMax': scales_list[weather_parameter_index][1],
                       'tooltip_titles': tooltip_titles,
                       'last_database_refresh': last_database_refresh,
                       }

    context = {
        'weather_parameters': weather_parameters,
        'weather_parameter': weather_parameter,
        'forecast_length': forecast_length,
        'chartjs_data': chartjs_data,
        'chartjs_options': chartjs_options,
        'forecast_sources': zip(forecast_sources_names, forecast_sources_urls),
    }

    return render(request=request, template_name='forecast.html', context=context)


def archive(request):
    # return HttpResponse("ARCHIVE")

    if request.method == 'GET':
        weather_parameter = weather_parameters[0]
        forecast_length = 7  # длина прогноза по умолчанию

    elif request.method == 'POST':
        weather_parameter = request.POST.get('weather-parameter')
        forecast_length = int(request.POST.get('forecast-length'))

    context = {
        'weather_parameters': weather_parameters,
        'weather_parameter': weather_parameter,
        'forecast_length': forecast_length,
        # 'chartjs_data': chartjs_data,
        # 'chartjs_options': chartjs_options,
        'forecast_sources': zip(forecast_sources_names, forecast_sources_urls),
    }

    return render(request=request, template_name='archive.html', context=context)


def insert_steps(list, symbol):
    list_new = []
    for item in list:
        list_new.append(item)
        list_new.append(symbol)
    return list_new


def feedback(request):
    return HttpResponse("FEEDBACK")

    context = {'forecast_sources': zip(
        forecast_sources_names, forecast_sources_urls), }

    return render(request=request, template_name='feedback.html', context=context)


def about(request):
    return HttpResponse("ABOUT")

    context = {'forecast_sources': zip(
        forecast_sources_names, forecast_sources_urls), }

    return render(request=request, template_name='about.html', context=context)
