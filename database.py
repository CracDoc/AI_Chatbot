import sys
sys.path.append("E:\\Downloads\\Full Stack Projects\\Dictionary-chatbot\\venv\\Lib\\site-packages")


import pymysql
pymysql.install_as_MySQLdb()  # Ensure pymysql is recognized

from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/dictionary_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), unique=True, nullable=False)
    definition = Column(Text, nullable=False)
    synonyms = Column(Text, nullable=True)
    antonyms = Column(Text, nullable=True)
    added_by = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

# Create tables in the database if they do not exist
Base.metadata.create_all(bind=engine)
