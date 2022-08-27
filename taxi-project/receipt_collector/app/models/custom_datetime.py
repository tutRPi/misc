import datetime

from sqlalchemy import TypeDecorator, DateTime


class CustomDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        return value
