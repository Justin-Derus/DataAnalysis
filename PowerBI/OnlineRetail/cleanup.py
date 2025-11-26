import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("./PowerBI/OnlineRetail/online_retail_original.csv")
df_clean = df.dropna()  # Drop rows with empty values

# Country → major cities
country_to_cities = {
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "Austria": ["Vienna", "Salzburg", "Graz", "Innsbruck", "Linz"],
    "Bahrain": ["Manama", "Riffa", "Muharraq"],
    "Belgium": ["Brussels", "Antwerp", "Ghent", "Bruges", "Charleroi"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza"],
    "Canada": ["Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa"],
    "Channel Islands": ["Jersey", "Guernsey"],
    "Cyprus": ["Nicosia", "Limassol", "Larnaca", "Paphos"],
    "Czech Republic": ["Prague", "Brno", "Ostrava", "Plzeň"],
    "Denmark": ["Copenhagen", "Aarhus", "Odense", "Aalborg"],
    "Eire": ["Dublin", "Cork", "Galway", "Limerick"],
    "European Community": ["Brussels", "Luxembourg"],
    "Finland": ["Helsinki", "Espoo", "Tampere", "Turku"],
    "France": ["Paris", "Lyon", "Marseille", "Nice", "Bordeaux"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"],
    "Greece": ["Athens", "Thessaloniki", "Patras", "Heraklion"],
    "Iceland": ["Reykjavik", "Keflavik"],
    "Israel": ["Tel Aviv", "Jerusalem", "Haifa", "Beersheba"],
    "Italy": ["Rome", "Milan", "Naples", "Turin", "Florence"],
    "Japan": ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Sapporo"],
    "Lebanon": ["Beirut", "Tripoli", "Sidon"],
    "Lithuania": ["Vilnius", "Kaunas", "Klaipeda"],
    "Malta": ["Valletta", "Birkirkara", "Sliema"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
    "Norway": ["Oslo", "Bergen", "Trondheim", "Stavanger"],
    "Poland": ["Warsaw", "Krakow", "Gdansk", "Wroclaw"],
    "Portugal": ["Lisbon", "Porto", "Braga", "Coimbra"],
    "RSA": ["Johannesburg", "Cape Town", "Durban", "Pretoria"],
    "Saudi Arabia": ["Riyadh", "Jeddah", "Mecca", "Medina"],
    "Singapore": ["Singapore"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
    "Sweden": ["Stockholm", "Gothenburg", "Malmo"],
    "Switzerland": ["Zurich", "Geneva", "Basel", "Bern"],
    "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Liverpool", "Leeds",
                       "Newcastle", "Sheffield", "Glasgow", "Edinburgh", "Bristol"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"]
}

# Country → city → region
country_to_regions = {
    "Australia": {"Sydney": "New South Wales", "Melbourne": "Victoria", "Brisbane": "Queensland", "Perth": "Western Australia", "Adelaide": "South Australia"},
    "Austria": {"Vienna": "Vienna", "Salzburg": "Salzburg", "Graz": "Styria", "Innsbruck": "Tyrol", "Linz": "Upper Austria"},
    "Bahrain": {"Manama": "Manama", "Riffa": "Southern Governorate", "Muharraq": "Muharraq Governorate"},
    "Belgium": {"Brussels": "Brussels-Capital", "Antwerp": "Flanders", "Ghent": "Flanders", "Bruges": "Flanders", "Charleroi": "Wallonia"},
    "Brazil": {"São Paulo": "São Paulo", "Rio de Janeiro": "Rio de Janeiro", "Brasília": "Federal District", "Salvador": "Bahia", "Fortaleza": "Ceará"},
    "Canada": {"Toronto": "Ontario", "Montreal": "Quebec", "Vancouver": "British Columbia", "Calgary": "Alberta", "Ottawa": "Ontario"},
    "Channel Islands": {"Jersey": "Jersey", "Guernsey": "Guernsey"},
    "Cyprus": {"Nicosia": "Nicosia District", "Limassol": "Limassol District", "Larnaca": "Larnaca District", "Paphos": "Paphos District"},
    "Czech Republic": {"Prague": "Prague", "Brno": "South Moravia", "Ostrava": "Moravian-Silesian", "Plzeň": "Plzeň Region"},
    "Denmark": {"Copenhagen": "Hovedstaden", "Aarhus": "Central Denmark", "Odense": "Southern Denmark", "Aalborg": "North Denmark"},
    "Eire": {"Dublin": "Leinster", "Cork": "Munster", "Galway": "Connacht", "Limerick": "Munster"},
    "European Community": {"Brussels": "Belgium", "Luxembourg": "Luxembourg"},
    "Finland": {"Helsinki": "Uusimaa", "Espoo": "Uusimaa", "Tampere": "Pirkanmaa", "Turku": "Southwest Finland"},
    "France": {"Paris": "Île-de-France", "Lyon": "Auvergne-Rhône-Alpes", "Marseille": "Provence-Alpes-Côte d'Azur", "Nice": "Provence-Alpes-Côte d'Azur", "Bordeaux": "Nouvelle-Aquitaine"},
    "Germany": {"Berlin": "Berlin", "Hamburg": "Hamburg", "Munich": "Bavaria", "Cologne": "North Rhine-Westphalia", "Frankfurt": "Hesse"},
    "Greece": {"Athens": "Attica", "Thessaloniki": "Central Macedonia", "Patras": "Western Greece", "Heraklion": "Crete"},
    "Iceland": {"Reykjavik": "Capital Region", "Keflavik": "Southern Peninsula"},
    "Israel": {"Tel Aviv": "Tel Aviv District", "Jerusalem": "Jerusalem District", "Haifa": "Haifa District", "Beersheba": "Southern District"},
    "Italy": {"Rome": "Lazio", "Milan": "Lombardy", "Naples": "Campania", "Turin": "Piedmont", "Florence": "Tuscany"},
    "Japan": {"Tokyo": "Tokyo", "Osaka": "Osaka", "Kyoto": "Kyoto", "Nagoya": "Aichi", "Sapporo": "Hokkaido"},
    "Lebanon": {"Beirut": "Beirut", "Tripoli": "North", "Sidon": "South"},
    "Lithuania": {"Vilnius": "Vilnius County", "Kaunas": "Kaunas County", "Klaipeda": "Klaipeda County"},
    "Malta": {"Valletta": "Valletta", "Birkirkara": "Central Region", "Sliema": "Central Region"},
    "Netherlands": {"Amsterdam": "North Holland", "Rotterdam": "South Holland", "The Hague": "South Holland", "Utrecht": "Utrecht", "Eindhoven": "North Brabant"},
    "Norway": {"Oslo": "Oslo", "Bergen": "Vestland", "Trondheim": "Trøndelag", "Stavanger": "Rogaland"},
    "Poland": {"Warsaw": "Masovian", "Krakow": "Lesser Poland", "Gdansk": "Pomeranian", "Wroclaw": "Lower Silesian"},
    "Portugal": {"Lisbon": "Lisbon", "Porto": "Northern Portugal", "Braga": "Northern Portugal", "Coimbra": "Central Portugal"},
    "RSA": {"Johannesburg": "Gauteng", "Cape Town": "Western Cape", "Durban": "KwaZulu-Natal", "Pretoria": "Gauteng"},
    "Saudi Arabia": {"Riyadh": "Riyadh Province", "Jeddah": "Makkah Province", "Mecca": "Makkah Province", "Medina": "Al Madinah Province"},
    "Singapore": {"Singapore": "Singapore"},
    "Spain": {"Madrid": "Madrid", "Barcelona": "Catalonia", "Valencia": "Valencian Community", "Seville": "Andalusia", "Bilbao": "Basque Country"},
    "Sweden": {"Stockholm": "Stockholm County", "Gothenburg": "Västra Götaland County", "Malmo": "Skåne County"},
    "Switzerland": {"Zurich": "Zurich", "Geneva": "Geneva", "Basel": "Basel-Stadt", "Bern": "Bern"},
    "United Arab Emirates": {"Dubai": "Dubai", "Abu Dhabi": "Abu Dhabi", "Sharjah": "Sharjah"},
    "United Kingdom": {"London": "South East", "Manchester": "North West", "Birmingham": "West Midlands", "Liverpool": "North West",
                       "Leeds": "Yorkshire", "Newcastle": "North East", "Sheffield": "Yorkshire", "Glasgow": "Scotland", "Edinburgh": "Scotland", "Bristol": "South West"},
    "USA": {"New York": "New York", "Los Angeles": "California", "Chicago": "Illinois", "Houston": "Texas", "San Francisco": "California"}
}

# Store assigned locations per CustomerID
customer_location_map = {}

def assign_location(row):
    customer = row["CustomerID"]
    country = row["Country"]

    # Already assigned? reuse
    if customer in customer_location_map:
        return pd.Series(customer_location_map[customer])

    # Valid country?
    if country not in country_to_cities:
        country = np.random.choice(list(country_to_cities.keys()))

    # Random city
    city = np.random.choice(country_to_cities[country])
    region = country_to_regions[country][city]

    # Save mapping
    customer_location_map[customer] = (country, city, region)
    return pd.Series((country, city, region))

# Apply assignment, preserving all original columns including InvoiceNo
df_clean[["Country", "City", "Region"]] = df_clean.apply(assign_location, axis=1)

# Save CSV
df_clean.to_csv("./PowerBI/OnlineRetail/online_retail1.csv", index=False)
print(df_clean.head())
