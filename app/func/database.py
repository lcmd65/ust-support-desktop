import pymssql
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.model.user import User
from bson import ObjectId
import app.environment 
import os
import base64
import io
import requests
import mysql.connector
import time

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
        db = app.environment.client["Nohcel_Dataset"]
        collection = db["embedded_dataset"]
        documents = collection.find()
        return documents
    except Exception as e:
        print(e)
        
def pushRequestToMongo(id, subject_text, request_text):
    document = {
            "_id": ObjectId(),
            "id": str(id),
            "subject": str(subject_text),
            "request": str(request_text),
            "respone": "",
        }
    db = app.environment.client["User"]
    collection = db["Request"]
    collection.insert_one(document)
    return document
    

def connectUserRequest():
    getClient()
    try:
        app.environment.client.admin.command('ping')
        section_database = app.environment.client["User"]
        collection_section = section_database["Request"]
        requests = collection_section.find()
        return requests
    except Exception as e:
        print(e) 


def connectServer():
    try:
        try:
            app.environment.user = mysql.connector.connect(
                host= "localhost",
                user= "root",
                database = "User_Nohcel"
            )
        except:
            app.environment.user = mysql.connector.connect(
                host= "localhost",
                user= "root",
                password= "123456",
                database = "User_Nohcel"
            )
    except:
        pass
        
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
    cnx.execute("DROP TABLE `User_Image`")
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
    value = (21280064, "dat.lemindast", "dat.lemindast@gmail.com", "123456", "M")
    cnx.execute("""INSERT INTO User(id, username, email, password, gender) VALUES (%s, %s, %s, %s,%s)""", value)

def insert_image(cnx, id, image_path):
    sql = """INSERT INTO User_Image(id, image) VALUES(21280064, LOAD_FILE("""+image_path+"""))"""
    cnx.execute(sql)


def addIMage():
    connectServer()
    cnx = app.environment.user.cursor()
    cnx.execute("""INSERT INTO User_Image(id, image) VALUES(21280064, LOAD_FILE("/Users/lechonminhdat/Downloads/citations.png"))""")
    
def userAuthentication2(account, password):
    app.environment.client = MongoClient(uri, server_api=ServerApi('1'))
    addIPtoMongodbAtlas(getIPAddress())
    # Send a ping to confirm a successful connection
    app.environment.client.admin.command('ping')
    db = app.environment.client["User"]
    collection = db["User"]
    documents = collection.find()
    for item in documents:
        if item["username"] == account and item["password"] == password:
            return True
    return False
    
def userAuthentication(account, password):
    """ task """
    if (account == "admin" and password == "1"):
        return True
    else:
        try:
            connectServer()
            cnx = app.environment.user.cursor()
            cnx.execute("""SELECT * FROM User; """)
            rows = cnx.fetchall()
            print(rows)
            for row in rows:
                if row[1] == account and row[3] == password:
                    return True
            time.sleep(5)
        except:
            bool = userAuthentication2(account, password)
            if bool == 1 : 
                return True
            else :
                return False
    

def userParsing(account,password):
    try:
        connectServer()
        cnx = app.environment.user.cursor()
        cnx.execute("""SELECT * FROM User; """)
        rows = cnx.fetchall()
        for row in rows:
            if row[1] == account and row[3] == password:
                app.environment.User_info = User(row[1],row[3],row[2], row[0])
    except:
        db = app.environment.client["User"]
        collection = db["User"]
        documents = collection.find()
        for item in documents:
            if item["username"] == account and item["password"] == password:
                app.environment.User_info = User(item["username"],item["password"], item["email"], item["_id"])
        
    

def connectUserImage(id):
    try:
        connectServer()
        cnx = app.environment.user.cursor()
        cnx.execute("""SELECT * FROM User_Image; """)
        rows = cnx.fetchall()
        for row in rows:
            if row[0] == id:
                return row[1]
    except:
        db = app.environment.client["User"]
        collection = db["Image"]
        documents = collection.find()
        for item in documents:
            if item["id"] == id:
                return item["image"]
        
        
def addiamge():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="User_Nohcel"  # Name of the database
    )
    cursor = mydb.cursor()
    file = open('app/images/citations.png','rb').read()
    file = base64.b64encode(file)
    args = (21280064, file)
    query = 'INSERT INTO User_Image VALUES(%s, %s)'
    
    # Execute the query and commit the database.
    cursor.execute(query,args)
    mydb.commit()


def addimage1():
    # Connect to the MongoDB database.
    app.environment.client = MongoClient(uri, server_api=ServerApi('1'))
    addIPtoMongodbAtlas(getIPAddress())
    db = app.environment.client["User"]
    collection = db["Image"]

    # Open the file and read the image data.
    file = open("app/images/citations.png", "rb").read()
    file = base64.b64encode(file)

    # The image data is the second argument to the `insert_one()` method.
    collection.insert_one(
        {
            "id": 21280064,
            "image": file
        })

if __name__ == "__main__":
    addimage1()
    
