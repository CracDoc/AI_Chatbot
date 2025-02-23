# from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Word(Base):
#     __tablename__ = 'words'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     word = Column(String(255), unique=True, nullable=False)
#     definition = Column(Text, nullable=False)
#     synonyms = Column(JSON, default=[])  # Replacing ARRAY with JSON
#     antonyms = Column(JSON, default=[])  # Replacing ARRAY with JSON
#     added_by = Column(String(100))
#     created_at = Column(DateTime, default=func.now())  # Using DateTime for timestamps
