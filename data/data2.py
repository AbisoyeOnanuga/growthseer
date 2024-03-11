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
    crops_primary_keywords = ["Cereals", "Citrus", "Fibre", "Fruit", "Linseed", "Pulses", "Roots", "Sugar", "Treenuts", "Vegetables", "Apricots", "Almonds", "Nuts", "Watermelons", "Tomatoes", "vegetables", "nuts", "beans", "Persimmons", "in shell", "Pears", "Apples", "Millet", "Hazelnuts", "Garlic", "Grapes", "Currants", "Cucumbers", "Cranberries", "Peppers", "Cherries", "Carrots", "Chestnuts", "Melons", "Cabbages", "Barley", "Asparagus", "Cauliflowers", "Mushrooms", "Nutmeg", "Onions", "Oranges", "Pepper", "Plantain", "Pumpkins", "Rape or colza", "Raspberries", "seed", "Sorghum", "Strawberries", "Tangerines", "Tea", "Vanilla, raw", "Wheat", "Oilcrops", "Cassava", "Eggplants", "Buckwheat", "berries", "raw"]
    crops_processed_keywords = ["Beer of barley", "Cotton lint", "Cottonseed", "Margarine", "short", "Molasses", "Oil, palm", "Oil, palm kernel", "Oil, rapeseed", "Oil, safflower", "Oil, sesame", "Oil, soybean", "Oil, sunflower", "Palm kernels", "sugar (centrifugal only)", "Wine", "Rice", "wool"]
    live_animals_keywords = ["Animals live", "Asses", "Beehives", "Bees", "Buffaloes", "Buffalo", "Camelids", "Camels", "Cattle", "Chickens", "Ducks", "Geese", "Goats", "Horses", "Mules", "Pigeons", "Pigs", "Rabbits", "Rodents", "Sheep", "Turkeys", "Birds"]
    livestock_primary_keywords = ["Beeswax", "beeswax", "Eggs", "eggs", "Hides", "hides", "Honey", "honey", "Meat", "meat", "Milk", "milk", "Offals", "offal", "Silk-worm", "Skins", "Snails"]
    livestock_processed_keywords = ["Butter", "Cheese", "Cream", "Ghee", "ghee", "Lard", "Milk products", "milk products", "Silk", "silk", "Tallow", "tallow", "Whey", "whey", "Yoghurt", "yoghurt", "Beeswax", "fat"]

    if any(keyword.lower() in item.lower() for keyword in crops_primary_keywords):
        return "Crops Primary"
    elif any(keyword.lower() in item.lower() for keyword in crops_processed_keywords):
        return "Crops Processed"
    elif any(keyword.lower() in item.lower() for keyword in livestock_processed_keywords):
        return "Livestock Processed"
    elif any(keyword.lower() in item.lower() for keyword in live_animals_keywords):
        return "Live Animals"
    elif any(keyword.lower() in item.lower() for keyword in livestock_primary_keywords):
        return "Livestock Primary"
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
# Rename 'Area' column to 'Country'
df.rename(columns={'Area': 'Country'}, inplace=True)

# Group by 'Continent' and save to separate CSV files
for continent, data in df.groupby('Continent'):
    # Drop the 'Continent' column from the data subset
    data = data.drop('Continent', axis=1)
    filename = f'{continent}_Production_Crops_Livestock.csv'
    data.to_csv(filename, index=False)
    print(f'Saved {filename}')
