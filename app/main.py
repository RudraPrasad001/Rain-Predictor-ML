from fastapi import FastAPI
from app.api import routes_query

app = FastAPI()


app.include_router(routes_query.router, prefix="/query", tags=["Query"])
