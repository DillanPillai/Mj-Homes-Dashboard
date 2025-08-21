properties = [
    { "id": 1, "location": "Auckland", "price": 1000000, "interest": "High", "description": "Luxury pool villa" },
    { "id": 2, "location": "Wellington", "price": 700000, "interest": "Medium", "description": "Cozy studio" },
    { "id": 3, "location": "Christchurch", "price": 500000, "interest": "Low", "description": "Family house" },
    { "id": 4, "location": "Auckland", "price": 1200000, "interest": "Medium", "description": "Modern apartment with pool" },
]

def filter_properties(properties, location=None, max_price=None, interest=None, keyword=None):
    filtered = []
    for p in properties:
        if location and p["location"] != location:
            continue
        if max_price is not None and p["price"] > max_price:
            continue
        if interest and p["interest"] != interest:
            continue
        if keyword and keyword.lower() not in p["description"].lower():
            continue
        filtered.append(p)
    return filtered

def display_properties(filtered):
    for p in filtered:
        print(f'{p["location"]} - ${p["price"]} - Interest: {p["interest"]}')
        print(f'  {p["description"]}\n')

if __name__ == "__main__":
    # Example usage
    result = filter_properties(properties, location="Auckland", max_price=1200000, interest="Medium", keyword="pool")
    display_properties(result)
