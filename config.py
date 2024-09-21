# config.py
import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://adm:qyVIEuWrZ89GhpAV@adm.6jacvht.mongodb.net")
