from flask import Flask, make_response, request
# from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mongoengine import MongoEngine

import csv
import pandas as pd
import quandl
import pandas as pd
import pymongo
from pymongo import MongoClient
from datetime import date

# Making a Connection with MongoClient
client = MongoClient("mongodb+srv://irccimmigration:adtproject@cluster0.91ztf.mongodb.net/API?retryWrites=true&w=majority")
# database
db = client["API"]
# collection
visadata= db["visadata"]


app = Flask(__name__)
CORS(app)

database_name = "API"
DB_URI = "mongodb+srv://irccimmigration:adtproject@cluster0.91ztf.mongodb.net/API?retryWrites=true&w=majority"
# //.format("newuser", "newuser", database_name)
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)


class User(db.Document):
    
    uname = db.StringField()
    password = db.StringField()

    def to_json(self):
        return {
            "uname": self.uname,
            "password": self.password
        }

@app.route("/ircc/login", methods = ["POST", "GET"])
def loginUser():
    user = request.get_json()
    # pw_hash = bcrypt.generate_password_hash(user['password'])
    # print(pw_hash)
    dbuser = User.objects(uname=user['uname'], password=user['password']).first()
    print(dbuser['uname'])
    return make_response("test", 201)
    # print("success")
    # return make_response("test", 201)



@app.route("/ircc/signup", methods = ["POST"])
def signupUser():
    user = request.get_json()
    print(user)
    data = User(uname=user['uname'], password=str(user['password']))
    data.save()
    print(user)
    return make_response("", 201)



@app.route("/ircc/cleandata", methods = ["POST"])
def cleandata():
    df=pd.read_csv('VisaData.csv')
    
    #rename the columns
    df.rename(columns={'Passport Number': 'passport_number'}, inplace=True)
    df.rename(columns={'Full Name': 'full_name'}, inplace=True)
    df.rename(columns={'Date of Birth': 'birth_date'}, inplace=True)
    df.rename(columns={'Gender': 'gender'}, inplace=True)
    df.rename(columns={'Citizenship': 'citizenship'}, inplace=True)
    df.rename(columns={'Marital Status': 'marital_status'}, inplace=True)
    df.rename(columns={'Intake Applied For': 'intake'}, inplace=True)
    df.rename(columns={'Passport Issue Date': 'passport_issue_date'}, inplace=True)
    df.rename(columns={'Phone Number': 'phone_number'}, inplace=True)
    df.rename(columns={'Email Address': 'email_address'}, inplace=True)
    df.rename(columns={'Canadian Institution Name': 'institution_name'}, inplace=True)
    df.rename(columns={'Course Name': 'course_name'}, inplace=True)
    df.rename(columns={'Date of Upfront Medical': 'medical_date'}, inplace=True)
    df.rename(columns={'Biometric Date': 'biometric_date'}, inplace=True)
    df.rename(columns={'Visa Application Date': 'application_date'}, inplace=True)
    df.rename(columns={'Medical Updated': 'medical_update_date'}, inplace=True)
    df.rename(columns={'Visa Category': 'visa_category'}, inplace=True)
    df.rename(columns={'Status': 'status'}, inplace=True)

    #generate age column
    now = pd.Timestamp('now')
    df['birthdate']= pd.to_datetime(df['birth_date']);
    df['age']= (now - df['birthdate']).astype('<m8[Y]').astype(str).apply(lambda x: x.replace('.0',''))   
    #df['age']=df['age'].astype(int)
    #print(df.shape[0])

    #drop duplicate records
    df = df.drop_duplicates()

    #remove data of those students who already got ppr
    df = df[df['status'] != 'PPR Received']

    #fill missing values
    df['visa_category'] = df['visa_category'].fillna('Study Visa',inplace=True)

    #remove unused columns
    df = df.drop('City of Birth', axis=1)
    df = df.drop('Country of Birth', axis=1)
    df = df.drop('Name of Spouse', axis=1)
    df = df.drop('status', axis=1)

    df.drop(df.tail(1).index,inplace=True)

    data_dict = df.to_dict("records")
    for rec in data_dict:
            visadata.insert_one(rec)
    
    return make_response("", 201)

if __name__ == "__main__":
    app.run()

