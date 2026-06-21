import requests
import json

base_url = "http://localhost:8000"

print("--- 1. Health Check ---")
res = requests.get(f"{base_url}/api/health")
print("Status Code:", res.status_code)
print("Response:", res.json())

print("\n--- 2. Skincare Quiz (Dry Skin) ---")
# Answering "A" to most gives 'dry'
data_skin = {
    "session_id": "test_skin",
    "answers": {
        "q1": "A",
        "q2": "A",
        "q3": "A",
        "q4": "A",
        "q5": "A"
    }
}
res_skin = requests.post(f"{base_url}/api/quiz/skincare", json=data_skin)
skin_json = res_skin.json()
print("Result Type:", skin_json.get("result_type"))
print("Total Products returned:", len(skin_json.get("products", [])))
for p in skin_json.get("products", [])[:2]:
    print(f" - {p.get('name')} (Brand: {p.get('brand')}, Match: {p.get('similarity_score')}%)")

print("\n--- 3. Haircare Quiz (Oily Scalp + High Porosity) ---")
# Answering B for hq1-3 gives oily scalp, C for hq4-7 gives high porosity
data_hair = {
    "session_id": "test_hair",
    "answers": {
        "hq1": "B",
        "hq2": "B",
        "hq3": "B",
        "hq4": "C",
        "hq5": "C",
        "hq6": "C",
        "hq7": "C"
    }
}
res_hair = requests.post(f"{base_url}/api/quiz/haircare", json=data_hair)
hair_json = res_hair.json()
print("Result Type:", hair_json.get("result_type"))
print("Total Products returned:", len(hair_json.get("products", [])))
for p in hair_json.get("products", [])[:2]:
    print(f" - {p.get('name')} (Brand: {p.get('brand')}, Match: {p.get('similarity_score')}%)")
