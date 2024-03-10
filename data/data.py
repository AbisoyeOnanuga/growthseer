
from pymongo.mongo_client import MongoClient
import csv
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')

uri = "mongodb+srv://{username}:{password}@cluster0.yrqjzc6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client["crop-livestock-data"]

collection = db["CropLivestockYield"]
# Load CSV file 
with open('Production_Crops_Livestock.csv') as f:
  reader = csv.DictReader(f)
  
  # Transform data
  transformed_data = []
  for row in reader:
    crop_item = {
      "year": row["Year"],
      "item": row["Item"],
      "element": row["Element"],
      "unit": row["Unit"],
      "value": row["Value"],
      "note": row["Note"],
      #"area_harvested": row["Value"]  
    }
    if row["Area"] not in transformed_data:
      transformed_data.append({
        "country": row["Area"], 
        "crop-livestock": [crop_item]  
      })
    else:
      for doc in transformed_data:
        if doc["country"] == row["Area"]:
          doc["crops-livestock"].append(crop_item)
          
  # Load transformed data into MongoDB 
  collection.insert_many(transformed_data)
