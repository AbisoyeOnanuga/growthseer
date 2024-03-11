import pandas as pd
import pycountry_convert as pc

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
df = pd.read_csv('Production_Crops_Livestock.csv', encoding='latin1')

# Filter the DataFrame for the years 1992-2022
df = df[df['Year'].between(1992, 2022)]

# Categorize 'Item' column
df['Item Category'] = df['Item'].apply(categorize_items)
# Normalize 'Value' column based on 'Unit'
df['Normalized Value'] = df.apply(lambda row: normalize_units(row['Unit'], row['Value']), axis=1)
# Drop the 'Continent' column as it's redundant
df.drop('Continent', axis=1, inplace=True)

# Save the processed DataFrame to a CSV file
df.to_csv('Processed_Production_Crops_Livestock.csv', index=False)
print('Saved Processed_Production_Crops_Livestock.csv')
