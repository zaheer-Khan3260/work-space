from dotenv import load_dotenv # type: ignore
from app.db import database
from app.auth.models import authModel
from fastapi import FastAPI, status # type: ignore
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
authModel.Base.metadata.create_all(bind=database.engine)

auth = FastAPI()


auth.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@auth.get("/", status_code=status.HTTP_201_CREATED)
def healthCheck():
    return {"Message": "Database is connected. You are good to go"}





from app.auth.controllers.credential import router as auth_router # type: ignore



auth.include_router(auth_router)