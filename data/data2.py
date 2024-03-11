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

# Load the dataset
df = pd.read_csv('Production_Crops_Livestock.csv', encoding='latin1')

# Filter the DataFrame for the years 2013-2022
df = df[df['Year'].between(2013, 2022)]

# Map 'Area' to 'Continent'
df['Continent'] = df['Area'].apply(country_to_continent)

# Group by 'Continent' and save to separate CSV files
for continent, data in df.groupby('Continent'):
    filename = f'{continent}_Production_Crops_Livestock.csv'
    data.to_csv(filename, index=False)
    print(f'Saved {filename}')
