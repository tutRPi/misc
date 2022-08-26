from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import receipt

app = FastAPI(title="Receipt API", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # TODO replace with origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(receipt.router)

if __name__ == "__main__":
    # for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
