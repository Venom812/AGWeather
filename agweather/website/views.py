from django.http import HttpResponse
from django.shortcuts import render, redirect
from datascraper.forecasts_scraper import weather_parameters, forecast_sources_urls, forecast_sources_names
from datascraper.models import ForecastsRecord, ArchiveRecord
from datetime import datetime
from django.http import HttpResponseRedirect
from .forms import FeedbackForm
from .models import Feedback
from django.utils import timezone


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

    def insert_steps(list, symbol):
        list_new = []
        for item in list:
            list_new.append(item)
            list_new.append(symbol)
        return list_new

    forecasts = ForecastsRecord.objects.latest('rec_date').rec_data
    weather_parameter_index = weather_parameters.index(weather_parameter)
    forecast_length_steps = forecast_length*4
    tooltip_titles = [datetime.fromisoformat(i).strftime(
        "%d.%m %H:%M") for i in forecasts[0][:forecast_length_steps]]  # Всплывающие ярлыки
    tooltip_titles = insert_steps(tooltip_titles, '')
    # weekday_rus = {0: 'ПН', 1: 'ВТ', 2: 'СР',
    #                3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}
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

    last_database_refresh = ForecastsRecord.objects.latest(
        'rec_date').rec_date.strftime("Дата обновления базы:  %d.%m.%Y %H:%M UTC")
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

    print(context)
    return render(request=request, template_name='forecast.html', context=context)


def archive(request):
    # return HttpResponse("ARCHIVE")

    if request.method == 'GET':
        weather_parameter = weather_parameters[0]
        archive_length = 14  # длина архива по умолчанию дней
        forecasts_foresight = 1

    elif request.method == 'POST':
        weather_parameter = request.POST.get('weather-parameter')
        archive_length = request.POST.get('archive-length')
        forecasts_foresight = request.POST.get('forecasts-foresight')

    archive_length = 14 if archive_length == '' else int(archive_length)
    if archive_length > 30:
        archive_length = 30
    elif archive_length < 1:
        archive_length = 1

    forecasts_foresight = 1 if forecasts_foresight == '' else int(
        forecasts_foresight)
    if forecasts_foresight > 10:
        forecasts_foresight = 10
    elif forecasts_foresight < 1:
        forecasts_foresight = 1

    archive = ArchiveRecord.objects.latest('rec_date').rec_data
    # archive = ArchiveRecord.objects.all().order_by('-rec_date')
    # archive = archive[2].rec_data
    # return HttpResponse(archive)

    weather_parameter_index = weather_parameters.index(weather_parameter)
    archive_length_steps = archive_length*8
    datetime_row = [datetime.fromisoformat(
        d) for d in archive[0][-archive_length_steps:]]
    tooltip_titles = [weekday_rus[i.weekday()] + i.strftime(" %d.%m %H:%M")
                      for i in datetime_row]  # Всплывающие ярлыки
    # return HttpResponse(tooltip_titles)

    labels = [i.strftime("%d.%m") if i.hour == 12 else ' ' if i.hour ==
              0 else '' for i in datetime_row]  # Ярлыки оси Х для графика

    datasets = [{
        'label': "Архив РП5",
        # [i+50 for i in forecast[2] if i != 'none'],
        'data': archive[1][weather_parameter_index][-archive_length_steps:],
        'borderColor': '#FFFFFF',
        # 'backgroundColor': '#FFFFFF',
        # 'borderDash': [10, 4],
        'borderWidth': 2,
        'pointStyle': 'circle',
        'pointRadius': 1,
        'pointHoverRadius': 3,
    },]

    # datasets = datasets.append(datasets)
    # del datasets[0]['data'][-1] #labels[-1]
    # print(len(labels), len(datasets[0]['data']))
    # print(labels)

    chartjs_data = {
        'labels': labels,
        'datasets': datasets,
    }
    print(chartjs_data)
    # print(datasets[0]['data'])

    last_database_refresh = ForecastsRecord.objects.latest(
        'rec_date').rec_date.strftime("Дата обновления базы:  %d.%m.%Y %H:%M UTC")
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
        'archive_length': archive_length,
        'forecasts_foresight': forecasts_foresight,
        'chartjs_data': chartjs_data,
        'chartjs_options': chartjs_options,
        'forecast_sources': zip(forecast_sources_names, forecast_sources_urls),
    }
    # print(context)
    return render(request=request, template_name='archive.html', context=context)


def insert_steps(list, symbol):
    list_new = []
    for item in list:
        list_new.append(item)
        list_new.append(symbol)
    return list_new


def feedback(request):
    # return HttpResponse("FEEDBACK")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            Feedback.objects.create(feedback_date=timezone.now(),
                                    feedbackers_name=form.cleaned_data['feedbackers_name'],
                                    feedbackers_email=form.cleaned_data['feedbackers_email'],
                                    feedback_message=form.cleaned_data['feedback_message'])
            # ...
            # redirect to a new URL:
            # return HttpResponse("FEEDBACK")
            return HttpResponseRedirect('/feedback_sent')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()

    context = {'forecast_sources': zip(
        forecast_sources_names, forecast_sources_urls), 'form': form}
    return render(request=request, template_name='feedback.html', context=context)


def feedback_sent(request):
    context = {'forecast_sources': zip(
        forecast_sources_names, forecast_sources_urls)}
    return render(request=request, template_name='feedback_sent.html', context=context)


def about(request):
    # return HttpResponse("ABOUT")

    context = {'forecast_sources': zip(
        forecast_sources_names, forecast_sources_urls), }

    return render(request=request, template_name='about.html', context=context)


weekday_rus = {0: 'ПН', 1: 'ВТ', 2: 'СР',
               3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}