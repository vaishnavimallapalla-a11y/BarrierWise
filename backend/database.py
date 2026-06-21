import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./barrierwise.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    category = Column(String) # "skincare" or "haircare"
    price = Column(Float)
    budget_tier = Column(String) # "budget", "mid", "premium"
    skin_type = Column(String, nullable=True) # "oily", "dry", "sensitive", "combination"
    scalp_type = Column(String, nullable=True) # "oily", "dry"
    hair_porosity = Column(String, nullable=True) # "low", "medium", "high"
    key_ingredients = Column(Text)
    description = Column(Text)
    
    # New additions for Indian Market extension
    image_url = Column(String)
    rating = Column(Float)
    review_count = Column(Integer)
    featured_review_text = Column(Text)
    featured_review_name = Column(String)
    routine_step = Column(String)

class ProductPriceListing(Base):
    __tablename__ = "product_price_listings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    platform = Column(String) # Amazon, Flipkart, Nykaa, Myntra
    price = Column(Float)
    url = Column(String)

class HomeRemedy(Base):
    __tablename__ = "home_remedies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String) # "skincare" or "haircare"
    skin_type = Column(String, nullable=True)
    scalp_type = Column(String, nullable=True)
    hair_porosity = Column(String, nullable=True)
    ingredients_used = Column(Text)
    instructions = Column(Text)
    image_url = Column(String)

class QuizResponse(Base):
    __tablename__ = "quiz_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    category = Column(String)
    answers = Column(JSON)
    result_type = Column(String)
