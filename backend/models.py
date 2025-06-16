from sqlalchemy import Column, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
import os

Base = declarative_base()

class Title(Base):
    __tablename__ = 'title'
    id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    citation = Column(Text, nullable=False)

class ContentEmbedding(Base):
    __tablename__ = 'content_embedding'
    law_id = Column(Text, primary_key=True)
    embedding = Column(Vector(1536))

engine = create_engine(os.getenv('DATABASE_URL'))
session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)