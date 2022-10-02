from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from google.cloud import bigquery
from google.oauth2 import service_account

from .forms import DateRangeForm, CityDateRangeForm
from .models import DateRange, CityDateRange

import json

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
credentials = service_account.Credentials.from_service_account_file(settings.GOOGLE_APPLICATION_CREDENTIALS,
                                                                    scopes=SCOPES)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


def get_weekly_trip_lengths(start_date, end_date, city=None):
    sql = """
        SELECT pickup_city AS city, EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS weekday, 
        AVG(trip_distance) AS average_trip_length, SUM(trip_distance) AS sum_trip_length, COUNT(*) AS number_pf_trips
        FROM `schwarz-it-taxi.taxi.receipts` 
        WHERE tpep_pickup_datetime BETWEEN '{}' AND '{}'
    """.format(start_date.strftime('%Y-%m-%d'),
               end_date.strftime('%Y-%m-%d'))

    if city:
        sql += " AND pickup_city LIKE '%{}%'".format(city)

    sql += """
        GROUP BY weekday, city
        ORDER BY city, weekday 
    """
    print(sql)
    df = client.query(sql).to_dataframe()

    json_records = df.reset_index().to_json(orient='records')
    return json.loads(json_records)


def get_weather_trip_lengths(start_date, end_date, city=None):
    sql = """
        SELECT pickup_city AS city, weather_description,
        AVG(trip_distance) AS average_trip_length, SUM(trip_distance) AS sum_trip_length, COUNT(*) AS number_pf_trips
        FROM `schwarz-it-taxi.taxi.receipts` 
        WHERE tpep_pickup_datetime BETWEEN '{}' AND '{}'
    """.format(start_date.strftime('%Y-%m-%d'),
               end_date.strftime('%Y-%m-%d'))

    if city:
        sql += " AND pickup_city LIKE '%{}%'".format(city)

    sql += """
        GROUP BY city, weather_description
        ORDER BY city, weather_description 
    """
    df = client.query(sql).to_dataframe()

    json_records = df.reset_index().to_json(orient='records')
    return json.loads(json_records)


class RevenuePerCity(LoginRequiredMixin, FormView):
    template_name = "metrics/revenue_per_city.html"
    model = DateRange
    form_class = DateRangeForm

    def form_valid(self, form):
        # Render the template
        # get_context_data populates object in the context
        # or you also get it with the name you want if you define context_object_name in the class
        context = self.get_context_data(form=form)

        if form.is_valid():
            sql = """
                SELECT pickup_city AS city, pickup_country AS country, SUM(total_amount) AS revenue
                FROM `schwarz-it-taxi.taxi.receipts`
                WHERE tpep_pickup_datetime BETWEEN '{}' AND '{}'
                GROUP BY pickup_city, pickup_country
            """.format(form.cleaned_data['start_date'].strftime('%Y-%m-%d'),
                       form.cleaned_data['end_date'].strftime('%Y-%m-%d'))
            df = client.query(sql).to_dataframe()

            json_records = df.reset_index().to_json(orient='records')
            data = json.loads(json_records)

            context['data'] = data
            context['start_date'] = form.cleaned_data['start_date']
            context['end_date'] = form.cleaned_data['end_date']

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TripLength(LoginRequiredMixin, FormView):
    template_name = "metrics/trip_length.html"
    model = CityDateRange
    form_class = CityDateRangeForm

    def form_valid(self, form):
        # Render the template
        # get_context_data populates object in the context
        # or you also get it with the name you want if you define context_object_name in the class
        context = self.get_context_data(form=form)

        if form.is_valid():
            # aggregations on weekday, daily

            weekly_data = get_weekly_trip_lengths(form.cleaned_data['start_date'], form.cleaned_data['end_date'], form.cleaned_data['city'])
            weather_data = get_weather_trip_lengths(form.cleaned_data['start_date'], form.cleaned_data['end_date'], form.cleaned_data['city'])

            context['weekly_data'] = weekly_data
            context['weather_data'] = weather_data
            context['start_date'] = form.cleaned_data['start_date']
            context['end_date'] = form.cleaned_data['end_date']

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
