import json
import os
import dateutil.parser

import pika

from app import crud
from app.db.session import SessionLocal
from app.schemas.receipt import ReceiptForBigQuery
from app.schemas.weather_data import WeatherData
from app.services.weather.visualcrossing_weather_api import VisualcrossingWeatherApi
from app.services.bigquery_service import bq

# TODO clean this mess...
# TODO use classes, dependency injection, etc

db = SessionLocal()
weather_api = VisualcrossingWeatherApi(os.getenv("VISUALCROSSING_API_KEY"))
queue_name = os.getenv("RABBITMQ_NEW_RECEIPT_ROUTING_KEY")
parameters = pika.URLParameters(os.getenv("RABBITMQ_URL"))

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)

        location = "{}, {}, {}, {}".format(data["pickup_location"]["city"], data["pickup_location"]["borough"],
                                           data["pickup_location"]["zone"], data["pickup_location"]["country"])
        location = location.replace("/", "-")

        date_time = dateutil.parser.parse(data["tpep_pickup_datetime"])

        weather_data = crud.weather_data.get_by_location(db=db, location=location, date_time=date_time)
        if not weather_data:
            # api call returns data for every hour. cache all, to reduce future api calls
            weather_data_create_array = weather_api.get_weather_data(location, date_time)
            for idx, weather_data_create in enumerate(weather_data_create_array):
                weather_data_existing = crud.weather_data.get_by_location(db=db, location=location, date_time=weather_data_create.datetime)
                if not weather_data_existing:
                    weather_data_create.country = data["pickup_location"]["country"]
                    weather_data_create.city = data["pickup_location"]["city"]
                    weather_data_tmp = crud.weather_data.create(db=db, obj_in=weather_data_create)
                    # our weather_data element is at position 0
                    if idx == 0:
                        weather_data = weather_data_tmp

        # enrich data and send to bigquery
        receipt_out = ReceiptForBigQuery(**dict({
            "best_route_distance": None,  # TODO use gcp directions api
            "pickup_city": data["pickup_location"]["city"],
            "pickup_country": data["pickup_location"]["country"],
            "pickup_latitude": weather_data.latitude,
            "pickup_longitude": weather_data.longitude,
            "dropoff_latitude": None,  # TODO: get latitude, longitude also for dropoff
            "dropoff_longitude": None,
            "weather_description": weather_data.description
        }, **data, **WeatherData.from_orm(weather_data).dict()))

        print("Send to bigquery")
        bq.insert_row(receipt_out.dict())

        # acknowledge
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(e)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
