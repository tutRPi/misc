from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from google.cloud import bigquery
from google.oauth2 import service_account


class RevenuePerCity(TemplateView):
    '''
    Generic FormView with our mixin to display user account page
    '''
    template_name = "metrics/revenue_per_city.html"

    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
    credentials = service_account.Credentials.from_service_account_file(settings.GOOGLE_APPLICATION_CREDENTIALS, scopes=SCOPES)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    def get_context_data(self, **kwargs):
        sql = """
            SELECT SUM(total_amount) AS revenue, pickup_city, pickup_country 
            FROM `schwarz-it-taxi.taxi.receipts` 
            WHERE tpep_pickup_datetime BETWEEN '2022-04-01' AND '2022-04-05'
            GROUP BY pickup_city, pickup_country
        """
        df = self.client.query(sql).to_dataframe()

        context = super().get_context_data(**kwargs)
        context['cities'] = df
        print(df)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
