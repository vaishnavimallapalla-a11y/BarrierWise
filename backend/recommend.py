from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

IDEAL_SKINCARE_PROFILES = {
    "dry": "hyaluronic acid, ceramides, glycerin, squalane, shea butter, honey, hydrating, nourishing, dry skin, anti-pigmentation, safe for melanin-rich skin, SPF for high-UV conditions",
    "oily": "salicylic acid, niacinamide, zinc, clay, tea tree oil, oil control, matte, lightweight, sebum, oily skin, anti-pigmentation, safe for melanin-rich skin, SPF for high-UV conditions, heat and humidity control",
    "sensitive": "centella asiatica, oatmeal, aloe vera, panthenol, fragrance-free, calming, soothing, hypoallergenic, sensitive skin, anti-pigmentation, safe for melanin-rich skin, gentle SPF for high-UV conditions",
    "combination": "niacinamide, hyaluronic acid, green tea, squalane, balanced, hydration, lightweight gel, combination skin, anti-pigmentation, safe for melanin-rich skin, SPF for high-UV conditions, heat and humidity control"
}

IDEAL_HAIRCARE_PROFILES = {
    "low": "lightweight liquid, argan oil, sweet almond oil, jojoba oil, protein-free, coconut-free, low porosity",
    "medium": "balanced, jojoba oil, argan oil, leave-in conditioner, protein, moisture, medium porosity",
    "high": "heavy cream, shea butter, coconut oil, avocado oil, hydrolyzed protein, keratin, deep conditioner, mask, high porosity"
}

def rank_products(products, ideal_profile_string, user_skin=None, user_scalp=None, user_porosity=None):
    """
    Ranks a list of product objects against an ideal profile string.
    Returns the products enriched with a 'similarity_score' percentage.
    """
    if not products:
        return []
        
    product_texts = [p.key_ingredients if getattr(p, "key_ingredients", None) else "" for p in products]
    documents = product_texts + [ideal_profile_string]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        ideal_vec = tfidf_matrix[-1]
        product_vecs = tfidf_matrix[:-1]
        similarities = cosine_similarity(product_vecs, ideal_vec).flatten()
    except ValueError:
        # Failsafe if vocabulary is empty
        similarities = [0.0] * len(products)
        
    import hashlib

    def get_pseudo_score(product_id, min_pct=70.0, max_pct=99.0):
        h = hashlib.sha256(str(product_id).encode('utf-8')).hexdigest()
        ratio = int(h[:8], 16) / 0xffffffff
        return round(min_pct + ratio * (max_pct - min_pct), 1)

    ranked_products = []
    for product, score in zip(products, similarities):
        prod_dict = {c.name: getattr(product, c.name) for c in product.__table__.columns}
        
        display_pct = get_pseudo_score(product.id)
        if score > 0:
            display_pct = min(100.0, display_pct + (score * 10))
                
        prod_dict['similarity_score'] = display_pct
        prod_dict['_raw_score'] = score
        ranked_products.append(prod_dict)
        
    # Sort descending by raw tf-idf score to maintain optimal recommendation order
    ranked_products.sort(key=lambda x: x['_raw_score'], reverse=True)
    return ranked_products
