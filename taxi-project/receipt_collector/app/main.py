from fastapi import FastAPI
from app.api import receipt

app = FastAPI(title="Receipt API", openapi_url="/openapi.json")

app.include_router(receipt.router)

if __name__ == "__main__":
    # for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
