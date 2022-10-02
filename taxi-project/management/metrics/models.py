from django.db import models


class DateRange(models.Model):
    start_date = models.DateField(default='2022-04-01')
    end_date = models.DateField(default='2022-04-15')


class CityDateRange(DateRange):
    city = models.CharField(max_length=32, default="New York")

