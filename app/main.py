from fastapi import FastAPI
from app.api import routes_query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(routes_query.router, prefix="/query", tags=["Query"])
origins = [
    "http://localhost:3000",  # React or web frontend
    "http://127.0.0.1:3000",
    # Add more if needed
    "https://yourfrontend.com"  # production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # OR ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],              # Allows all HTTP methods: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Allows all headers
)
