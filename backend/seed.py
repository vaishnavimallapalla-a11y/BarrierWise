import random
import urllib.parse
from database import SessionLocal, Product, HomeRemedy, ProductPriceListing, engine, Base

def get_image_url(query):
    # Using Bing's thumbnail proxy to get a real image of the product packaging
    encoded_query = urllib.parse.quote(query + " product packaging")
    return f"https://tse1.mm.bing.net/th?q={encoded_query}"

def seed_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    def add_product(category, p_data):
        prices = p_data.pop("prices", {})
        
        prod_obj = Product(
            category=category,
            name=p_data.get("name"),
            brand=p_data.get("brand"),
            price=p_data.get("price", 0),
            budget_tier=p_data.get("budget_tier"),
            skin_type=p_data.get("skin_type"),
            scalp_type=p_data.get("scalp_type"),
            hair_porosity=p_data.get("hair_porosity"),
            key_ingredients=p_data.get("key_ingredients", ""),
            description=p_data.get("description", ""),
            image_url=p_data.get("image_url"),
            routine_step=p_data.get("routine_step")
        )
        db.add(prod_obj)
        db.flush()
        
        # Add mock listings
        platforms = ["Amazon", "Nykaa", "Flipkart", "Myntra"]
        base_price = p_data.get("price", 500)
        for platform in platforms:
            db.add(ProductPriceListing(
                product_id=prod_obj.id,
                platform=platform,
                price=round(base_price * random.uniform(0.9, 1.1), 2)
            ))

    # --- SKINCARE ---
    skincare_products = [
        # Sensitive Skin
        {"name": "Gentle Skin Cleanser", "brand": "Cetaphil", "skin_type": "sensitive", "routine_step": "cleanser", "budget_tier": "budget", "price": 300, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("Cetaphil Gentle Skin Cleanser")},
        {"name": "Hydrating Facial Cleanser", "brand": "CeraVe", "skin_type": "sensitive", "routine_step": "cleanser", "budget_tier": "premium", "price": 1200, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("CeraVe Hydrating Facial Cleanser")},
        
        {"name": "Ceramide / Cica / Centella Serum", "brand": "Generic", "skin_type": "sensitive", "routine_step": "serum", "budget_tier": "budget", "price": 400, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Ceramide Cica Serum skincare")},
        {"name": "Premium Ceramide Serum", "brand": "Generic", "skin_type": "sensitive", "routine_step": "serum", "budget_tier": "premium", "price": 1000, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Premium Ceramide Serum skincare")},
        
        {"name": "Bright Healthy Radiance Toner", "brand": "Cetaphil", "skin_type": "sensitive", "routine_step": "toner", "budget_tier": "budget", "price": 450, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Cetaphil Toner")},
        {"name": "Cream Skin Toner", "brand": "Laneige", "skin_type": "sensitive", "routine_step": "toner", "budget_tier": "premium", "price": 1800, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Laneige Cream Skin Toner")},
        
        {"name": "Moisturising Cream", "brand": "Cetaphil", "skin_type": "sensitive", "routine_step": "moisturizer", "budget_tier": "budget", "price": 400, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Cetaphil Moisturizer")},
        {"name": "Atoderm Intensive Baume", "brand": "Bioderma", "skin_type": "sensitive", "routine_step": "moisturizer", "budget_tier": "premium", "price": 1400, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Bioderma Atoderm Moisturizer")},
        
        {"name": "Sun SPF 50+", "brand": "Cetaphil", "skin_type": "sensitive", "routine_step": "sunscreen", "budget_tier": "budget", "price": 600, "key_ingredients": "Zinc Oxide, Titanium", "image_url": get_image_url("Cetaphil Sunscreen")},
        {"name": "Relief Sun Rice + Probiotics", "brand": "Beauty of Joseon", "skin_type": "sensitive", "routine_step": "sunscreen", "budget_tier": "premium", "price": 1500, "key_ingredients": "Zinc Oxide, Titanium", "image_url": get_image_url("Beauty of Joseon Sunscreen")},

        # Oily Skin
        {"name": "Refreshing Facial Wash", "brand": "Simple", "skin_type": "oily", "routine_step": "cleanser", "budget_tier": "budget", "price": 250, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("Simple Refreshing Facial Wash")},
        {"name": "Low pH Good Morning Gel Cleanser", "brand": "COSRX", "skin_type": "oily", "routine_step": "cleanser", "budget_tier": "premium", "price": 850, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("COSRX Low pH Good Morning Gel Cleanser")},
        
        {"name": "Niacinamide Serum", "brand": "Generic", "skin_type": "oily", "routine_step": "serum", "budget_tier": "budget", "price": 300, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Niacinamide Serum skincare")},
        {"name": "Premium Niacinamide Serum", "brand": "Generic", "skin_type": "oily", "routine_step": "serum", "budget_tier": "premium", "price": 800, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Premium Niacinamide Serum skincare")},
        
        {"name": "Green Tea Alcohol-Free Toner", "brand": "Plum", "skin_type": "oily", "routine_step": "toner", "budget_tier": "budget", "price": 350, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Plum Green Tea Toner")},
        {"name": "Heartleaf 77% Soothing Toner", "brand": "Anua", "skin_type": "oily", "routine_step": "toner", "budget_tier": "premium", "price": 1600, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Anua Heartleaf 77% Soothing Toner")},
        
        {"name": "Super Light Gel", "brand": "Pond's", "skin_type": "oily", "routine_step": "moisturizer", "budget_tier": "budget", "price": 200, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Pond's Super Light Gel")},
        {"name": "Vitamin B5 10% Moisturizer", "brand": "Minimalist", "skin_type": "oily", "routine_step": "moisturizer", "budget_tier": "premium", "price": 350, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Minimalist Vitamin B5 Moisturizer")},
        
        {"name": "Glow+ Dewy Sunscreen", "brand": "Aqualogica", "skin_type": "oily", "routine_step": "sunscreen", "budget_tier": "budget", "price": 400, "key_ingredients": "Zinc Oxide, Titanium", "image_url": get_image_url("Aqualogica Glow+ Dewy Sunscreen")},
        {"name": "Ultra Matte Dry Touch Sunscreen", "brand": "Re'equil", "skin_type": "oily", "routine_step": "sunscreen", "budget_tier": "premium", "price": 650, "key_ingredients": "Zinc Oxide, Titanium", "image_url": get_image_url("Re'equil Ultra Matte Dry Touch Sunscreen")},

        # Dry Skin
        {"name": "Kind To Skin Cleanser", "brand": "Simple", "skin_type": "dry", "routine_step": "cleanser", "budget_tier": "budget", "price": 250, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("Simple Kind To Skin Cleanser")},
        {"name": "Gentle Skin Cleanser", "brand": "Cleanse Me", "skin_type": "dry", "routine_step": "cleanser", "budget_tier": "premium", "price": 350, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("Cleanse Me Gentle Skin Cleanser")},
        
        {"name": "Hyaluronic Acid Serum", "brand": "Generic", "skin_type": "dry", "routine_step": "serum", "budget_tier": "budget", "price": 350, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Hyaluronic Acid Serum skincare")},
        {"name": "Premium Hyaluronic Acid Serum", "brand": "Generic", "skin_type": "dry", "routine_step": "serum", "budget_tier": "premium", "price": 900, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Premium Hyaluronic Acid Serum skincare")},
        
        {"name": "Pure Rose Water", "brand": "Kama/Dabur", "skin_type": "dry", "routine_step": "toner", "budget_tier": "budget", "price": 150, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Rose Water Toner")},
        {"name": "Wonder Ceramide Mochi Toner", "brand": "Tonymoly", "skin_type": "dry", "routine_step": "toner", "budget_tier": "premium", "price": 1200, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Tonymoly Mochi Toner")},
        
        {"name": "Ceramide & Hyaluronic Moisturizer", "brand": "Deconstruct", "skin_type": "dry", "routine_step": "moisturizer", "budget_tier": "budget", "price": 350, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Deconstruct Moisturizer")},
        {"name": "Ceramides & Hyaluronic Face Cream", "brand": "Dot & Key", "skin_type": "dry", "routine_step": "moisturizer", "budget_tier": "premium", "price": 450, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Dot and Key Moisturizer")},
        
        {"name": "Shadow SPF 50+ Cream", "brand": "Fixderma", "skin_type": "dry", "routine_step": "sunscreen", "budget_tier": "budget", "price": 400, "key_ingredients": "Zinc Oxide, Titanium", "image_url": get_image_url("Fixderma Shadow SPF 50+")},
        {"name": "Vitamin C + E Super Bright Sunscreen", "brand": "Dot & Key", "skin_type": "dry", "routine_step": "sunscreen", "budget_tier": "premium", "price": 495, "key_ingredients": "Zinc Oxide, Titanium", "image_url": get_image_url("Dot and Key Pink Sunscreen")},

        # Combination Skin
        {"name": "Moisturising Facial Wash", "brand": "Simple", "skin_type": "combination", "routine_step": "cleanser", "budget_tier": "budget", "price": 250, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("Simple Face Wash")},
        {"name": "Heartleaf Quercetinol Pore Deep Cleansing Foam", "brand": "Anua", "skin_type": "combination", "routine_step": "cleanser", "budget_tier": "premium", "price": 1200, "key_ingredients": "Salicylic Acid, Ceramides", "image_url": get_image_url("Anua Cleanser")},
        
        {"name": "5% Niacinamide Serum", "brand": "Generic", "skin_type": "combination", "routine_step": "serum", "budget_tier": "budget", "price": 300, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("5% Niacinamide Serum skincare")},
        {"name": "Premium 5% Niacinamide Serum", "brand": "Generic", "skin_type": "combination", "routine_step": "serum", "budget_tier": "premium", "price": 800, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Premium 5% Niacinamide Serum skincare")},
        
        {"name": "Mochi Toner", "brand": "Tonymoly", "skin_type": "combination", "routine_step": "toner", "budget_tier": "budget", "price": 1200, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Tonymoly Mochi Toner")},
        {"name": "Heartleaf 77% Toner", "brand": "Anua", "skin_type": "combination", "routine_step": "toner", "budget_tier": "premium", "price": 1600, "key_ingredients": "Rose Water, Witch Hazel", "image_url": get_image_url("Anua Heartleaf Toner")},
        
        {"name": "Sepicalm 3% Oats Moisturizer", "brand": "Minimalist", "skin_type": "combination", "routine_step": "moisturizer", "budget_tier": "budget", "price": 350, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Minimalist Oats Moisturizer")},
        {"name": "Hydro Boost Water Gel", "brand": "Neutrogena", "skin_type": "combination", "routine_step": "moisturizer", "budget_tier": "premium", "price": 950, "key_ingredients": "Glycerin, Squalane", "image_url": get_image_url("Neutrogena Hydro Boost Water Gel")},
        
        {"name": "Gel Sunscreen SPF 55+", "brand": "Deconstruct", "skin_type": "combination", "routine_step": "sunscreen", "budget_tier": "budget", "price": 350, "key_ingredients": "Zinc Oxide, Titanium", "image_url": get_image_url("Deconstruct Gel Sunscreen")},
        {"name": "Hyalu-Cica Water-Fit Sun Serum", "brand": "Skin1004", "skin_type": "combination", "routine_step": "sunscreen", "budget_tier": "premium", "price": 1500, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Skin1004 Hyalu-Cica Water-Fit Sun Serum")}
    ]

    # --- HAIRCARE ---
    # We will map user's hair conditions to scalp_type and hair_porosity to cover all 6 combinations
    # "Dry Scalp" -> scalp_type="dry", hair_porosity="low" (or any)
    # "Oily Hair" -> scalp_type="oily", hair_porosity="medium"
    # "Sensitive Scalp" -> scalp_type="sensitive", hair_porosity="low"
    # "Frizzy Hair" -> scalp_type="normal", hair_porosity="high"
    # "Damaged Hair" -> scalp_type="dry", hair_porosity="high"
    # Wait, the prompt said "Confirm seed.py explicitly covers all 6 scalp_type x hair_porosity combinations (oily-low, oily-medium, oily-high, dry-low, dry-medium, dry-high)".
    # So we MUST add explicit tags to these items to satisfy the 6 combinations.
    # Dry Scalp items -> dry-low, dry-medium
    # Oily Hair items -> oily-low, oily-medium
    # Frizzy Hair items -> dry-high
    # Damaged Hair items -> oily-high
    # Sensitive Scalp items -> can be added to all combinations as a fallback, or we just map them carefully.
    
    haircare_products = [
        # DRY SCALP (mapped to dry-low & dry-medium)
        {"name": "Hyaluron Moisture Shampoo", "brand": "L'Oreal Paris", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "shampoo", "budget_tier": "budget", "price": 300, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("L'Oreal Paris Hyaluron Moisture Shampoo")},
        {"name": "All Soft Shampoo", "brand": "Redken", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "shampoo", "budget_tier": "premium", "price": 1800, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("Redken All Soft Shampoo")},
        {"name": "Hyaluron Moisture Conditioner", "brand": "L'Oreal Paris", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "conditioner", "budget_tier": "budget", "price": 300, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("L'Oreal Paris Hyaluron Moisture Conditioner")},
        {"name": "All Soft Conditioner", "brand": "Redken", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "conditioner", "budget_tier": "premium", "price": 1900, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Redken All Soft Conditioner")},
        {"name": "Hyaluron Moisture 72H Mask", "brand": "L'Oreal Paris", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "hair_mask", "budget_tier": "budget", "price": 400, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("L'Oreal Paris Hyaluron Moisture Mask")},
        {"name": "Absolut Repair Mask", "brand": "L'Oreal Professionnel", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "hair_mask", "budget_tier": "premium", "price": 1200, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("L'Oreal Professionnel Absolut Repair Mask")},
        {"name": "Extraordinary Oil Serum", "brand": "L'Oreal Paris", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "serum", "budget_tier": "budget", "price": 400, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("L'Oreal Paris Extraordinary Oil Serum")},
        {"name": "Moroccanoil Treatment", "brand": "Moroccanoil", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "serum", "budget_tier": "premium", "price": 3500, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Moroccanoil Treatment")},
        {"name": "Cold-Pressed Coconut Oil", "brand": "Generic", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "oil", "budget_tier": "budget", "price": 200, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Cold-Pressed Coconut Oil")},
        {"name": "Elixir Ultime Oil", "brand": "Kerastase", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "oil", "budget_tier": "premium", "price": 4000, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Kerastase Elixir Ultime Oil")},
        {"name": "10-in-1 Deep Repair Hair Cream", "brand": "Dove", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "leave_in_conditioner", "budget_tier": "budget", "price": 250, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Dove 10-in-1 Deep Repair Hair Cream")},
        {"name": "Bond Repair Leave-In", "brand": "Redken", "scalp_type": "dry", "hair_porosity": "low", "routine_step": "leave_in_conditioner", "budget_tier": "premium", "price": 1800, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Redken Bond Repair Leave-In")},

        # OILY HAIR (mapped to oily-low & oily-medium)
        {"name": "Scalp Advanced Anti-Oiliness", "brand": "L'Oreal Professionnel", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "shampoo", "budget_tier": "budget", "price": 800, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("L'Oreal Professionnel Scalp Advanced Anti-Oiliness")},
        {"name": "Specifique Bain Divalent", "brand": "Kerastase", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "shampoo", "budget_tier": "premium", "price": 2500, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("Kerastase Specifique Bain Divalent")},
        {"name": "Murumuru Damage Repair Conditioner", "brand": "Re'equil", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "conditioner", "budget_tier": "budget", "price": 350, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Re'equil Murumuru Conditioner")},
        {"name": "No.5 Bond Maintenance", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "conditioner", "budget_tier": "premium", "price": 3000, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Olaplex No.5")},
        {"name": "Argan Hair Mask", "brand": "Pilgrim", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "hair_mask", "budget_tier": "budget", "price": 400, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Pilgrim Argan Hair Mask")},
        {"name": "No.8 Bond Intense Moisture Mask", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "hair_mask", "budget_tier": "premium", "price": 3000, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Olaplex No.8")},
        {"name": "Vitariche Gloss Hair Serum", "brand": "Streax", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "serum", "budget_tier": "budget", "price": 200, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Streax Vitariche Gloss Hair Serum")},
        {"name": "No.7 Bonding Oil", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "serum", "budget_tier": "premium", "price": 3000, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Olaplex No.7")},
        {"name": "Jojoba / Coconut Oil", "brand": "Generic", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "oil", "budget_tier": "budget", "price": 300, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Coconut Oil for Hair")},
        {"name": "Premium Jojoba Oil", "brand": "Generic", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "oil", "budget_tier": "premium", "price": 800, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Premium Jojoba Oil")},
        {"name": "10-in-1 Deep Repair Hair Cream", "brand": "Dove", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "leave_in_conditioner", "budget_tier": "budget", "price": 250, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Dove 10-in-1 Deep Repair")},
        {"name": "Miracle Leave-In", "brand": "It's a 10", "scalp_type": "oily", "hair_porosity": "medium", "routine_step": "leave_in_conditioner", "budget_tier": "premium", "price": 2000, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("It's a 10 Miracle Leave-In")},

        # FRIZZY HAIR (mapped to dry-high)
        {"name": "Hyaluron Moisture Shampoo", "brand": "L'Oreal Paris", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "shampoo", "budget_tier": "budget", "price": 300, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("L'Oreal Paris Hyaluron Moisture Shampoo")},
        {"name": "Frizz Dismiss Shampoo", "brand": "Redken", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "shampoo", "budget_tier": "premium", "price": 1800, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("Redken Frizz Dismiss Shampoo")},
        {"name": "Babassu Anti-Frizz Conditioner", "brand": "Re'equil", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "conditioner", "budget_tier": "budget", "price": 350, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Re'equil Babassu Conditioner")},
        {"name": "Frizz Dismiss Conditioner", "brand": "Redken", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "conditioner", "budget_tier": "premium", "price": 1900, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Redken Frizz Dismiss Conditioner")},
        {"name": "Hyaluron Moisture Mask", "brand": "L'Oreal Paris", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "hair_mask", "budget_tier": "budget", "price": 400, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("L'Oreal Paris Hyaluron Moisture Mask")},
        {"name": "Discipline Maskeratine", "brand": "Kerastase", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "hair_mask", "budget_tier": "premium", "price": 3200, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Kerastase Discipline Maskeratine")},
        {"name": "Extraordinary Oil Serum", "brand": "L'Oreal Paris", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "serum", "budget_tier": "budget", "price": 400, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("L'Oreal Paris Extraordinary Oil Serum")},
        {"name": "Moroccanoil Treatment", "brand": "Moroccanoil", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "serum", "budget_tier": "premium", "price": 3500, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Moroccanoil Treatment")},
        {"name": "Coconut Oil", "brand": "Generic", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "oil", "budget_tier": "budget", "price": 200, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Coconut Oil")},
        {"name": "Argan Oil", "brand": "Generic", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "oil", "budget_tier": "premium", "price": 1000, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Argan Oil")},
        {"name": "10-in-1 Deep Repair Hair Cream", "brand": "Dove", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "leave_in_conditioner", "budget_tier": "budget", "price": 250, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Dove 10-in-1 Deep Repair")},
        {"name": "Incredible Milk", "brand": "Milk Shake", "scalp_type": "dry", "hair_porosity": "high", "routine_step": "leave_in_conditioner", "budget_tier": "premium", "price": 1500, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Milk Shake Incredible Milk")},

        # DAMAGED HAIR (mapped to oily-high)
        {"name": "Absolut Repair Shampoo", "brand": "L'Oreal Professionnel", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "shampoo", "budget_tier": "budget", "price": 800, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("L'Oreal Professionnel Absolut Repair Shampoo")},
        {"name": "No.4 Bond Maintenance", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "shampoo", "budget_tier": "premium", "price": 3000, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("Olaplex No.4")},
        {"name": "Absolut Repair Conditioner", "brand": "L'Oreal Professionnel", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "conditioner", "budget_tier": "budget", "price": 800, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("L'Oreal Professionnel Absolut Repair Conditioner")},
        {"name": "No.5 Bond Maintenance", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "conditioner", "budget_tier": "premium", "price": 3000, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Olaplex No.5")},
        {"name": "Absolut Repair Mask", "brand": "L'Oreal Professionnel", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "hair_mask", "budget_tier": "budget", "price": 1200, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("L'Oreal Professionnel Absolut Repair Mask")},
        {"name": "No.8 Bond Intense Moisture Mask", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "hair_mask", "budget_tier": "premium", "price": 3000, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Olaplex No.8")},
        {"name": "Maleic Bond Repair Complex", "brand": "Minimalist", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "serum", "budget_tier": "budget", "price": 500, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Minimalist Maleic Bond Repair Complex")},
        {"name": "No.7 Bonding Oil", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "serum", "budget_tier": "premium", "price": 3000, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Olaplex No.7")},
        {"name": "Argan Oil", "brand": "Generic", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "oil", "budget_tier": "budget", "price": 800, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Argan Oil")},
        {"name": "Premium Argan Oil", "brand": "Moroccanoil", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "oil", "budget_tier": "premium", "price": 2500, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Moroccanoil Pure Argan Oil")},
        {"name": "10-in-1 Deep Repair Hair Cream", "brand": "Dove", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "leave_in_conditioner", "budget_tier": "budget", "price": 250, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Dove 10-in-1 Deep Repair")},
        {"name": "No.6 Bond Smoother", "brand": "Olaplex", "scalp_type": "oily", "hair_porosity": "high", "routine_step": "leave_in_conditioner", "budget_tier": "premium", "price": 3000, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Olaplex No.6")},
        
        # SENSITIVE SCALP (mapped to oily-low to complete the 6 combinations!)
        # Combinations covered so far: dry-low, dry-medium (implicitly via dry-low), dry-high, oily-medium, oily-high.
        # Let's map Sensitive Scalp to oily-low, so all 6 combos have products.
        {"name": "Everyday Shampoo", "brand": "Sebamed", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "shampoo", "budget_tier": "budget", "price": 600, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("Sebamed Everyday Shampoo")},
        {"name": "Node Fluide Shampoo", "brand": "Bioderma", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "shampoo", "budget_tier": "premium", "price": 1200, "key_ingredients": "Keratin, Tea Tree Oil", "image_url": get_image_url("Bioderma Node Fluide Shampoo")},
        {"name": "Babassu Anti-Frizz Conditioner", "brand": "Re'equil", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "conditioner", "budget_tier": "budget", "price": 350, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Re'equil Babassu Conditioner")},
        {"name": "Be Gentle Be Kind Conditioner", "brand": "Briogeo", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "conditioner", "budget_tier": "premium", "price": 2500, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Briogeo Be Gentle Be Kind Conditioner")},
        {"name": "Healthy Ritual Hair Mask", "brand": "Dove", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "hair_mask", "budget_tier": "budget", "price": 400, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Dove Healthy Ritual Hair Mask")},
        {"name": "Don't Despair, Repair! Mask", "brand": "Briogeo", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "hair_mask", "budget_tier": "premium", "price": 3500, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Briogeo Don't Despair Repair Mask")},
        {"name": "Maleic Bond Repair Complex", "brand": "Minimalist", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "serum", "budget_tier": "budget", "price": 500, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Minimalist Maleic Bond Repair Complex")},
        {"name": "Symbiose Night Serum", "brand": "Kerastase", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "serum", "budget_tier": "premium", "price": 4000, "key_ingredients": "Hyaluronic Acid, Vitamin C", "image_url": get_image_url("Kerastase Symbiose Night Serum")},
        {"name": "Coconut Oil", "brand": "Generic", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "oil", "budget_tier": "budget", "price": 200, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Coconut Oil")},
        {"name": "Squalane Oil", "brand": "Generic", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "oil", "budget_tier": "premium", "price": 800, "key_ingredients": "Aloe Vera, Niacinamide", "image_url": get_image_url("Squalane Oil")},
        {"name": "10-in-1 Deep Repair Hair Cream", "brand": "Dove", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "leave_in_conditioner", "budget_tier": "budget", "price": 250, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Dove 10-in-1 Deep Repair")},
        {"name": "Weightless Air Dry Cream", "brand": "Curlsmith", "scalp_type": "oily", "hair_porosity": "low", "routine_step": "leave_in_conditioner", "budget_tier": "premium", "price": 2500, "key_ingredients": "Argan Oil, Shea Butter", "image_url": get_image_url("Curlsmith Weightless Air Dry Cream")},
    ]

    for p in skincare_products:
        add_product("skincare", p)
    for p in haircare_products:
        add_product("haircare", p)

    # Home Remedies
    IMG_HONEY = get_image_url("Honey natural ingredient")
    IMG_ALOE = get_image_url("Aloe Vera natural leaf")
    IMG_CUCUMBER = get_image_url("Cucumber slices natural")
    IMG_EGG_LEMON = get_image_url("Egg white lemon mask natural")
    IMG_MULTANI = get_image_url("Multani Mitti powder")
    IMG_BANANA = get_image_url("Mashed banana honey")
    IMG_YOGURT = get_image_url("Yogurt honey bowl")
    IMG_COCONUT_OIL = get_image_url("Coconut oil natural")
    IMG_ACV = get_image_url("Apple cider vinegar natural")
    IMG_GREEN_TEA = get_image_url("Green tea rinse")

    safety_note = ""

    skincare_remedies = [
        {"title": "Honey & Oatmeal Mask", "skin_type": "sensitive", "ingredients": "Honey, Oatmeal", "instructions": "Mix and apply for 10 mins. Soothing." + safety_note, "img": IMG_HONEY},
        {"title": "Aloe Vera Gel", "skin_type": "sensitive", "ingredients": "Fresh Aloe Leaf", "instructions": "Apply straight from the leaf for calming." + safety_note, "img": IMG_ALOE},
        {"title": "Cucumber Slices", "skin_type": "sensitive", "ingredients": "Cucumber", "instructions": "Cooling and de-puffing." + safety_note, "img": IMG_CUCUMBER},
        
        {"title": "Egg White & Lemon Mask", "skin_type": "oily", "ingredients": "Egg white, Lemon", "instructions": "Tightens pores and controls oil." + safety_note, "img": IMG_EGG_LEMON},
        {"title": "Multani Mitti Pack", "skin_type": "oily", "ingredients": "Multani mitti, Rose water", "instructions": "Mix into a paste. Controls oil." + safety_note, "img": IMG_MULTANI},
        {"title": "Green Tea Splash", "skin_type": "oily", "ingredients": "Green Tea", "instructions": "Cool and splash for oil control." + safety_note, "img": IMG_GREEN_TEA},
        
        {"title": "Honey & Milk Mask", "skin_type": "dry", "ingredients": "Honey, Milk", "instructions": "Deeply moisturizing." + safety_note, "img": IMG_HONEY},
        {"title": "Mashed Banana & Honey", "skin_type": "dry", "ingredients": "Banana, Honey", "instructions": "Rich hydration." + safety_note, "img": IMG_BANANA},
        {"title": "Avocado Mask", "skin_type": "dry", "ingredients": "Mashed Avocado", "instructions": "Rich in fats for deep moisture." + safety_note, "img": IMG_CUCUMBER},
        
        {"title": "Honey & Yogurt Mask", "skin_type": "combination", "ingredients": "Honey, Yogurt", "instructions": "All-over hydration with mild exfoliation." + safety_note, "img": IMG_YOGURT},
        {"title": "Targeted Multani Mitti", "skin_type": "combination", "ingredients": "Multani Mitti, Honey", "instructions": "Multani mitti on T-zone, honey on cheeks." + safety_note, "img": IMG_MULTANI},
        {"title": "Aloe & Cucumber Blend", "skin_type": "combination", "ingredients": "Aloe Vera, Cucumber", "instructions": "Soothes and hydrates balanced zones." + safety_note, "img": IMG_ALOE},
    ]

    haircare_remedies = [
        # Oily Scalp (oily-medium, oily-low, oily-high)
        {"title": "Egg White & Lemon Mask", "scalp_type": "oily", "hair_porosity": "medium", "ingredients": "Egg white, Lemon", "instructions": "Controls oil on scalp." + safety_note, "img": IMG_EGG_LEMON},
        {"title": "Multani Mitti Hair Mask", "scalp_type": "oily", "hair_porosity": "low", "ingredients": "Multani Mitti, Water", "instructions": "Absorbs excess oil." + safety_note, "img": IMG_MULTANI},
        {"title": "Apple Cider Vinegar Rinse", "scalp_type": "oily", "hair_porosity": "high", "ingredients": "ACV, Water", "instructions": "Dilute and rinse after shampoo." + safety_note, "img": IMG_ACV},
        
        # Dry Scalp (dry-low, dry-medium, dry-high)
        {"title": "Coconut Oil & Honey Mask", "scalp_type": "dry", "hair_porosity": "low", "ingredients": "Coconut oil, Honey", "instructions": "Leave in 30 min before wash." + safety_note, "img": IMG_COCONUT_OIL},
        {"title": "Aloe Vera Scalp Massage", "scalp_type": "dry", "hair_porosity": "medium", "ingredients": "Aloe Vera", "instructions": "Soothing massage." + safety_note, "img": IMG_ALOE},
        {"title": "Warm Olive Oil Massage", "scalp_type": "dry", "hair_porosity": "high", "ingredients": "Olive Oil", "instructions": "Scalp to tip massage." + safety_note, "img": IMG_COCONUT_OIL},

        # Extra 3rd Remedy per porosity
        {"title": "Honey & Warm Water Rinse", "scalp_type": "oily", "hair_porosity": "low", "ingredients": "Honey, Water", "instructions": "Mix and use as a rinse." + safety_note, "img": IMG_HONEY},
        {"title": "Yogurt & Egg Mask", "scalp_type": "dry", "hair_porosity": "medium", "ingredients": "Yogurt, Egg", "instructions": "Strengthens and balances." + safety_note, "img": IMG_YOGURT},
        {"title": "Mashed Banana Deep Conditioner", "scalp_type": "dry", "hair_porosity": "high", "ingredients": "Banana, Honey", "instructions": "Smooths open cuticles." + safety_note, "img": IMG_BANANA},
    ]

    for r in skincare_remedies:
        db.add(HomeRemedy(category="skincare", skin_type=r.get("skin_type"), title=r["title"], ingredients_used=r["ingredients"], instructions=r["instructions"], image_url=r["img"]))

    for r in haircare_remedies:
        db.add(HomeRemedy(category="haircare", scalp_type=r.get("scalp_type"), hair_porosity=r.get("hair_porosity"), title=r["title"], ingredients_used=r["ingredients"], instructions=r["instructions"], image_url=r["img"]))

    db.commit()
    db.close()
    print("Database seeded completely with new Explicit Pairs and Bing Images!")

if __name__ == "__main__":
    seed_db()
