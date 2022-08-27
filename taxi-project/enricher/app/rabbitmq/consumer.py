import json
import os
import dateutil.parser

import pika

from app import crud
from app.db.session import SessionLocal
from app.services.weather.visualcrossing_weather_api import VisualcrossingWeatherApi


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
    data = json.loads(body)

    location = "{}, {}, {}, {}".format(data["pickup_location"]["city"], data["pickup_location"]["borough"],
                                       data["pickup_location"]["zone"], data["pickup_location"]["country"])
    date_time = dateutil.parser.parse(data["tpep_pickup_datetime"])

    weather_data = crud.weather_data.get_by_location(db=db, location=location, date_time=date_time)
    if not weather_data:
        weather_data_create = weather_api.get_weather_data(location, date_time)
        weather_data = crud.weather_data.create(db=db, obj_in=weather_data_create)

    # now send to bigquery



channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
