import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app.rabbitmq.consumer import channel


def main():
    # TODO cleanup: crate consumer classes with dependency injection
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
