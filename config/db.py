from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Nombre de connexions dans le pool
    max_overflow=10,  # Connexions supplémentaires autorisées
    pool_timeout=30,  # Timeout en secondes
    pool_recycle=1800,  # Recycle les connexions après 30 minutes
)

session = Session(bind=engine)