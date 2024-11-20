from __future__ import annotations
import nest_asyncio
nest_asyncio.apply()
from aws_lambda_powertools import Logger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum
from src.views import example

app = FastAPI(root_path="/v1", title="Application title")

app.openapi_url = '/openapi.json'

logger = Logger()

app.include_router(example.router)

app = CORSMiddleware(
    app=app,
    allow_origin_regex=r"^http.*",
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"],
)

handler = Mangum(app, api_gateway_base_path="/v1", lifespan="off")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=4000)
