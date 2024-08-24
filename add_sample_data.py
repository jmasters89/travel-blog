from website import create_app, mongo

app = create_app()

with app.app_context():
    # Add sample cities
    cities = [
        {"name": "Paris", "country": "France"},
        {"name": "London", "country": "United Kingdom"},
        {"name": "New York", "country": "United States"},
        {"name": "Tokyo", "country": "Japan"},
        {"name": "Sydney", "country": "Australia"},
        {"name": "Rome", "country": "Italy"},
        {"name": "Barcelona", "country": "Spain"},
        {"name": "Amsterdam", "country": "Netherlands"},
        {"name": "Berlin", "country": "Germany"},
        {"name": "Prague", "country": "Czech Republic"},
    ]

    mongo.db.cities.insert_many(cities)

print("Sample data added successfully!")