import pandas as pd
import pycountry_convert as pc

# Function to map country to continent
def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except:
        return "Unknown"  # For countries not found in the package

# Function to check if any keyword is in the item description
def contains_keywords(item, keywords):
    return any(keyword in item for keyword in keywords)

# Function to normalize units
def normalize_units(unit, value):
    if '1000' in unit:
        return value * 1000
    return value

# Function to categorize items based on keywords
def categorize_items(item):
    crops_primary_keywords = ["Cereals", "Citrus", "Fibre", "Fruit", "Oil", "Pulses", "Roots", "Sugar", "Treenuts", "Vegetables"]
    live_animals_keywords = ["Animals live", "Asses", "Beehives", "Buffaloes", "Camelids", "Camels", "Cattle", "Chickens", "Ducks", "Geese", "Goats", "Horses", "Mules", "Pigeons", "Pigs", "Rabbits", "Rodents", "Sheep", "Turkeys"]
    livestock_primary_keywords = ["Beeswax", "Eggs", "Hides", "Honey", "Meat", "Milk", "Offals", "Silk-worm", "Skins", "Snails", "Wool"]
    livestock_processed_keywords = ["Butter", "Cheese", "Cream", "Ghee", "Lard", "Milk products", "Silk", "Tallow", "Whey", "Yoghurt"]

    if contains_keywords(item, crops_primary_keywords):
        return "Crops Primary"
    elif contains_keywords(item, live_animals_keywords):
        return "Live Animals"
    elif contains_keywords(item, livestock_primary_keywords):
        return "Livestock Primary"
    elif contains_keywords(item, livestock_processed_keywords):
        return "Livestock Processed"
    else:
        return "Other"

# Read the dataset
df = pd.read_csv('Production_Crops_Livestock.csv', encoding='latin1', low_memory=False)

# Filter the DataFrame for the years 1992-2022
df = df[df['Year'].between(1992, 2022)]

# Categorize 'Item' column
df['Item Category'] = df['Item'].apply(categorize_items)
# Normalize 'Value' column based on 'Unit'
df['Normalized Value'] = df.apply(lambda row: normalize_units(row['Unit'], row['Value']), axis=1)
# Map 'Area' to 'Continent'
df['Continent'] = df['Area'].apply(country_to_continent)

# Group by 'Continent' and save to separate CSV files
for continent, data in df.groupby('Continent'):
    filename = f'{continent}_Production_Crops_Livestock.csv'
    data.to_csv(filename, index=False)
    print(f'Saved {filename}')
