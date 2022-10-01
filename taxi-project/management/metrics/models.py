from django.db import models


class DateRange(models.Model):
    start_date = models.DateField(default='2022-04-01')
    end_date = models.DateField(default='2022-04-15')
