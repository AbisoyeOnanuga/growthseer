from pymongo.mongo_client import MongoClient
import csv
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')

uri = "mongodb+srv://username:password@cluster0.yrqjzc6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client["pesticide-data"]

collection = db["PesticideUse"]
# Load CSV file 
with open('Pesticides-Use.csv') as f:
  reader = csv.DictReader(f)
  
  # Transform data
  transformed_data = []
  for row in reader:
    temperature_item = {
      "element": row["Element"],
      "item": row["Item"],
      "year": row["Year"],
      "unit": row["Unit"],
      "value": row["Value"],
      #"item": row["Item"],
      "flag": row["Flag"],
      "flag description": row["Flag Description"],
      #"area_harvested": row["Value"]
    }
    if row["Area"] not in transformed_data:
      transformed_data.append({
        "country": row["Area"], 
        "pesticide-use": [temperature_item]  
      })
    else:
      for doc in transformed_data:
        if doc["country"] == row["Area"]:
          doc["temperature-change"].appen(temperature_item)
          
  # Load transformed data into MongoDB 
  collection.insert_many(transformed_data)
