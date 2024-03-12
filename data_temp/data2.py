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

# Read the dataset
df = pd.read_csv('Temperature-Change-on-Land.csv', encoding='latin1', low_memory=False)

# Filter the DataFrame for the years 1992-2022
df = df[df['Year'].between(1961, 2022)]

# Categorize 'Item' column
df['Continent'] = df['Area'].apply(country_to_continent)
# Rename 'Area' column to 'Country'
df.rename(columns={'Area': 'Country'}, inplace=True)

# Group by 'Continent' and save to separate CSV files
for continent, data in df.groupby('Continent'):
    # Drop the 'Continent' column from the data subset
    data = data.drop('Continent', axis=1)
    filename = f'{continent}_Temperature_Change_on_Land.csv'
    data.to_csv(filename, index=False)
    print(f'Saved {filename}')
