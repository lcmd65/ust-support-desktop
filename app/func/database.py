import pymssql
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"


def connectMongoEmbedded():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db = client["Nohcel_Dataset"]
        collection = db["embedded_dataset"]
        documents = collection.find()
        return documents
    except Exception as e:
        print(e)


def connectServer():
    """ task """
    return

def userAuthentication(account, password):
    """ task """
    if (account == "dat.lemindast" and password == "1"):
        return True
    else:
        try:
            conn = pymssql.connect("localhost", "Nohcel_user", "sa", "123456")
            cur = conn.cursor()
            conn.commit()
            cur.excute("""
                    SELECT * FROM User
                    """)
            for row in cur:
                if row["Username"] == account and row["Password"] == password:
                    return True
            return False
        except:
            return False

def userAuthenticationNonePass(account,email):
    """ task """
    return 

def userSender(information):
    return
    