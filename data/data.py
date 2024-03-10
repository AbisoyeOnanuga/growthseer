
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

db = client["crop_livestock_data"]

collection = db["CropLivestockYield"]

csv_files = ['Production_Crops_Livestock.csv']

for csv_file in csv_files:
    with open(csv_file) as f:

        reader = csv.DictReader(f)

        headers = reader.fieldnames

        for row in reader:

            document = {header: row[header] for header in headers}

            collection.insert_one(document)

