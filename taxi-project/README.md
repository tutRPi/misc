
## Setup

- Start services: `docker-compose up`

### Receipt Collector
- `cd receipt_collector`
- optional: create and activate virtual environment
- Run the following command 
```
pip install requirements.txt
python ./app/backend_pre_start.py
alembic upgrade head
```
- Run application via `uvicorn app.main:app`
- To add migration, run `alembic revision --autogenerate -m "description"`

### bla

- `cp .env.example .env` and set your environment variables

## TODOs

- [ ] Insert to queue, before storing in db (if load is high)
- [ ] Auth (API Key or Bearer Token for Taxis, Admins)
- [ ] Replace SQLite with db
- [ ] Use UUID's instead of int receipt id (depending on db)
- [ ] Wrap services in docker files
- [ ] (better) documentation (openapi)



## Further Information

### Taxi Dataset
Source: https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Explanation: https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
