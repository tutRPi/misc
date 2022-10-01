from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from google.cloud import bigquery
from google.oauth2 import service_account

from .forms import DateRangeForm
from .models import DateRange

import json


class RevenuePerCity(LoginRequiredMixin, FormView):
    '''
    Generic FormView with our mixin to display user account page
    '''
    template_name = "metrics/revenue_per_city.html"
    model = DateRange
    form_class = DateRangeForm

    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
    credentials = service_account.Credentials.from_service_account_file(settings.GOOGLE_APPLICATION_CREDENTIALS,
                                                                        scopes=SCOPES)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

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
            df = self.client.query(sql).to_dataframe()

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
