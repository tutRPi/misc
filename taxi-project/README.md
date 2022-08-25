
## Setup

- Start services: `docker-compose up`

### Receipt Collector
- `cd receipt_collector`
- optional: create virtual environment
- `pip install app/requirements.txt`
- `cp .env.example .env` and set your environment variables
- Run application via `uvicorn app.main:app`

### bla


## TODOs

-[ ] Auth (API Key or Bearer Token for Taxis, Admins)
-[ ] Replace SQLite with db



## Further Information

### Taxi Dataset
Source: https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Explanation: https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
