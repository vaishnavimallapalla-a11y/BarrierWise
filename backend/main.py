import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any

from database import engine, Base, SessionLocal, Product, HomeRemedy, QuizResponse, ProductPriceListing
from recommend import rank_products, IDEAL_SKINCARE_PROFILES, IDEAL_HAIRCARE_PROFILES

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS Middleware for local frontend and production origin
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QuizAnswers(BaseModel):
    session_id: str = "default_session"
    answers: Dict[str, Any]

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/products/{product_id}/prices")
def get_product_prices(product_id: int, db: Session = Depends(get_db)):
    listings = db.query(ProductPriceListing).filter(ProductPriceListing.product_id == product_id).all()
    return [
        {c.name: getattr(l, c.name) for c in l.__table__.columns} for l in listings
    ]

@app.post("/api/quiz/skincare")
def quiz_skincare(data: QuizAnswers, db: Session = Depends(get_db)):
    answers = data.answers
    
    scores = {"dry": 0, "oily": 0, "combination": 0, "sensitive": 0}
    
    # Q1
    q1 = answers.get("q1", "")
    if q1 == "A": scores["dry"] += 1
    elif q1 == "B": scores["combination"] += 1
    elif q1 == "C": scores["oily"] += 1
    elif q1 == "D": scores["sensitive"] += 1
    
    # Q2
    q2 = answers.get("q2", "")
    if q2 == "A": scores["dry"] += 1
    elif q2 == "B": scores["oily"] += 1
    elif q2 == "C": scores["combination"] += 1
    elif q2 == "D": scores["sensitive"] += 1
    
    # Q3
    q3 = answers.get("q3", "")
    if q3 == "A": scores["dry"] += 1
    elif q3 == "B": scores["oily"] += 1
    elif q3 == "C": scores["combination"] += 1
    elif q3 == "D": scores["sensitive"] += 1
    
    # Q4
    q4 = answers.get("q4", "")
    if q4 == "A": scores["dry"] += 1
    elif q4 == "B": scores["oily"] += 0.5; scores["combination"] += 0.5
    elif q4 == "C": scores["sensitive"] += 1
    elif q4 == "D": scores["combination"] += 1
    
    # Q5
    q5 = answers.get("q5", "")
    if q5 == "A": scores["dry"] += 1
    elif q5 == "B": scores["oily"] += 1
    elif q5 == "C": scores["combination"] += 1
    elif q5 == "D": scores["sensitive"] += 1
    
    max_score = max(scores.values())
    tied_types = [k for k, v in scores.items() if v == max_score]
    
    if "combination" in tied_types:
        result_type = "combination"
    else:
        result_type = tied_types[0]
        
    q_resp = QuizResponse(session_id=data.session_id, category="skincare", answers=answers, result_type=result_type)
    db.add(q_resp)
    db.commit()
    
    products = db.query(Product).filter(Product.category == "skincare", Product.skin_type == result_type).all()
    remedies = db.query(HomeRemedy).filter(HomeRemedy.category == "skincare", HomeRemedy.skin_type == result_type).all()
    
    ideal_profile = IDEAL_SKINCARE_PROFILES.get(result_type, "")
    ranked_products = rank_products(products, ideal_profile, user_skin=result_type)
    
    return {
        "result_type": result_type,
        "products": ranked_products,
        "home_remedies": [
            {c.name: getattr(r, c.name) for c in r.__table__.columns} for r in remedies
        ]
    }

@app.post("/api/quiz/haircare")
def quiz_haircare(data: QuizAnswers, db: Session = Depends(get_db)):
    answers = data.answers
    
    # Scalp type (hq1-hq3)
    scalp_scores = {"dry": 0, "oily": 0}
    q1 = answers.get("hq1", "")
    if q1 == "A": scalp_scores["dry"] += 1
    elif q1 == "B": scalp_scores["oily"] += 1
    
    q2 = answers.get("hq2", "")
    if q2 == "A": scalp_scores["dry"] += 1
    elif q2 == "B": scalp_scores["oily"] += 1
    
    q3 = answers.get("hq3", "")
    if q3 == "A": scalp_scores["dry"] += 1
    elif q3 == "B": scalp_scores["oily"] += 1
    
    scalp_type = "oily" if scalp_scores["oily"] > scalp_scores["dry"] else "dry"
    
    # Porosity (hq4-hq7)
    por_scores = {"low": 0, "medium": 0, "high": 0}
    q4 = answers.get("hq4", "")
    if q4 == "A": por_scores["low"] += 1
    elif q4 == "B": por_scores["medium"] += 1
    elif q4 == "C": por_scores["high"] += 1
    
    q5 = answers.get("hq5", "")
    if q5 == "A": por_scores["low"] += 1
    elif q5 == "B": por_scores["medium"] += 1
    elif q5 == "C": por_scores["high"] += 1
    
    q6 = answers.get("hq6", "")
    if q6 == "A": por_scores["low"] += 1
    elif q6 == "B": por_scores["medium"] += 1
    elif q6 == "C": por_scores["high"] += 1
    
    q7 = answers.get("hq7", "")
    if q7 == "A": por_scores["low"] += 1
    elif q7 == "B": por_scores["medium"] += 1
    elif q7 == "C": por_scores["high"] += 1
    
    max_p_score = max(por_scores.values())
    tied_p_types = [k for k, v in por_scores.items() if v == max_p_score]
    hair_porosity = "medium" if "medium" in tied_p_types else tied_p_types[0]
    
    result_type = f"{scalp_type} scalp, {hair_porosity} porosity"
    
    q_resp = QuizResponse(session_id=data.session_id, category="haircare", answers=answers, result_type=result_type)
    db.add(q_resp)
    db.commit()
    
    products = db.query(Product).filter(
        Product.category == "haircare", 
        Product.scalp_type == scalp_type, 
        Product.hair_porosity == hair_porosity
    ).all()
    
    if not products:
        products = db.query(Product).filter(
            Product.category == "haircare", 
            Product.hair_porosity == hair_porosity
        ).all()
        
    remedies = db.query(HomeRemedy).filter(
        HomeRemedy.category == "haircare", 
        HomeRemedy.hair_porosity == hair_porosity
    ).all()
    
    ideal_profile = IDEAL_HAIRCARE_PROFILES.get(hair_porosity, "")
    if scalp_type == "oily":
        ideal_profile += ", salicylic acid, tea tree oil, purifying, clear shampoo"
    else:
        ideal_profile += ", aloe vera, nourishing, moisturizing, flake control"
        
    ranked_products = rank_products(products, ideal_profile, user_scalp=scalp_type, user_porosity=hair_porosity)
    
    return {
        "result_type": result_type,
        "products": ranked_products,
        "home_remedies": [
            {c.name: getattr(r, c.name) for c in r.__table__.columns} for r in remedies
        ]
    }
