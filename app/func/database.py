import pymssql
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import app.environment 
import os
import requests
import mysql.connector

uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"

def getIPAddress():
    return requests.get("https://api.ipify.org").text

def addIPtoMongodbAtlas(ip_address):
    try:
        url = "https://cloud.mongodb.com/api/v1/admin/clusters/<CLUSTER_ID>/security/ipWhitelist/add"
        headers = {"Authorization": "Bearer <API_KEY>"}
        data = {"ipAddress": ip_address}
        response = requests.post(url, headers=headers, data=data)
    except Exception as e:
        print(e)
        
def getClient():
    app.environment.client = MongoClient(uri, server_api=ServerApi('1'))

def connectMongoEmbedded():
    addIPtoMongodbAtlas(getIPAddress())
    # Send a ping to confirm a successful connection
    try:
        app.environment.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected")
        db = app.environment.client["Nohcel_Dataset"]
        collection = db["embedded_dataset"]
        documents = collection.find()
        return documents
    except Exception as e:
        print(e)

def connectUserRequest():
    try:
        app.environment.client.admin.command('ping')
        section_database = app.environment.client["User_Request"]
        collection_section = section_database["Requests"]
        requests = collection_section.find()
        return requests
    except Exception as e:
        print(e) 


def connectServer():
    app.environment.user = mysql.connector.connect(
        host= "localhost",
        user= "root",
        database = "User"
    )
    
def createTableUser():
    connectServer()
    cnx = app.environment.user.cursor()
    cnx.execute(\
        "CREATE TABLE `User` ("
        "  `id` int(11) NOT NULL,"
        "  `username`varchar(20) NOT NULL,"
        "  `email` varchar(50) NOT NULL,"
        "  `password` varchar(20) NOT NULL,"
        "  `gender` enum('M','F') NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"\
    )
    
def createTableUserImage():
    connectServer()
    cnx = app.environment.user.cursor()
    cnx.execute(\
        "CREATE TABLE `User_Image` ("
        "   `id` int NOT NULL,"
        "   `image` BLOB NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"\
    )
    
def addUser():
    connectServer()
    cnx = app.environment.user.cursor()
    cnx.execute("""INSERT INTO User(id, username, email, password, gender) VALUES (21280064, "dat.lemindast", "dat.lemindast@gmail.com", "123456", "M")""")

def addIMage():
    connectServer()
    cnx = app.environment.user.cursor()
    cnx.execute("""INSERT INTO User_Image(id, image) VALUES(21280064,'/Users/lechonminhdat/Downloads/citations.png');""")
    
def userAuthentication(account, password):
    """ task """
    if (account == "dat.lemindast" and password == "1"):
        return True
    else:
        try:
            connectServer()
            cnx = app.environment.user.cursor()
            cnx.excute("""
                    SELECT * FROM User
                    """)
            for row in cnx:
                if row["username"] == account and row["password"] == password:
                    return True
            return False
        except:
            return False

def userAuthenticationNonePass(account,email):
    """ task """
    return 

def userSender(information):
    return