import taipy as tp
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
import os
username = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')

uri = "mongodb+srv://{username}:{password}@cluster0.yrqjzc6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client["CropLivestockYield"]

yields = tp.from_mongo(db["yields"])

chart = (
    yields.plot.line(x='year', y='yield', by='country', legend=True)
)

tp.show(chart)
