
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine 

load_dotenv()
postgresql_database_url = os.getenv("POSTGRESQL_DATABASE_URL")

engine = create_engine(postgresql_database_url,client_encoding="utf8",
 pool_recycle= 3600, pool_size=10, max_overflow=20, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
   