from crypt import methods
import json
import os
from bson import ObjectId
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from mongoengine import *
from algo import Algorithm

import csv
import pandas as pd
import pymongo
from pymongo import MongoClient
from datetime import date

from algo import Algorithm

# Making a Connection with MongoClient
client = MongoClient(
    "mongodb+srv://irccimmigration:adtproject@cluster0.91ztf.mongodb.net/API?retryWrites=true&w=majority")
# database
db = client["API"]
# collection
visadata = db["visadata"]

app = Flask(__name__)
CORS(app)

database_name = "API"
DB_URI = "mongodb+srv://irccimmigration:adtproject@cluster0.91ztf.mongodb.net/API?retryWrites=true&w=majority"
# //.format("newuser", "newuser", database_name)
app.config["MONGODB_HOST"] = DB_URI
database = MongoEngine()
database.init_app(app)


class User(database.Document):

    uname = database.StringField()
    password = database.StringField()

    def to_json(self):
        return {
            "uname": self.uname,
            "password": self.password
        }

class Visadata(DynamicDocument):
    _id = ObjectIdField(default=ObjectId, primary_key=True)
    passport_number = StringField()
    full_name = StringField()
    # birth_date = DateTimeField()
    gender = StringField()
    citizenship = StringField()
    marital_status = StringField()
    intake = StringField()
    passport_issue_date = StringField()
    phone_number = IntField()
    email_address = StringField()
    institution_name = StringField()
    course_name = StringField()
    medical_date = StringField()
    biometric_date = StringField()
    application_date = StringField()
    medical_update_date = StringField()
    visa_categor = StringField()
    status = StringField()
    file_submit_priority = IntField()
    biometric_days_priority = IntField()
    medical_updated_priority = IntField()
    visa_applied_days = IntField()
    biometric_days = IntField()
    medical_days = IntField()
    file_submit_days = IntField()


@app.route("/ircc/login", methods=["POST", "GET"])
def loginUser():
    try:
        user = request.get_json()
        # pw_hash = bcrypt.generate_password_hash(user['password'])
        # print(pw_hash)
        dbuser = User.objects(uname=user['uname'],
                          password=user['password']).first()
        print(dbuser['uname'])
        return make_response("", 201)
        # print("success")
        # return make_response("test", 201)
    except:
        return make_response("Invalid Credentials", 500)


@app.route("/ircc/signup", methods=["POST"])
def signupUser():
    user = request.get_json()
    print(user)
    data = User(uname=user['uname'], password=str(user['password']))
    data.save()
    print(user)
    return make_response("", 201)


@app.route("/ircc/cleandata", methods=["POST"])
def cleandata():
    df = pd.read_csv('VisaData.csv')

    # rename the columns
    df.rename(columns={'Passport Number': 'passport_number'}, inplace=True)
    df.rename(columns={'Full Name': 'full_name'}, inplace=True)
    df.rename(columns={'Date of Birth': 'birth_date'}, inplace=True)
    df.rename(columns={'Gender': 'gender'}, inplace=True)
    df.rename(columns={'Citizenship': 'citizenship'}, inplace=True)
    df.rename(columns={'Marital Status': 'marital_status'}, inplace=True)
    df.rename(columns={'Intake Applied For': 'intake'}, inplace=True)
    df.rename(
        columns={'Passport Issue Date': 'passport_issue_date'}, inplace=True)
    df.rename(columns={'Phone Number': 'phone_number'}, inplace=True)
    df.rename(columns={'Email Address': 'email_address'}, inplace=True)
    df.rename(
        columns={'Canadian Institution Name': 'institution_name'}, inplace=True)
    df.rename(columns={'Course Name': 'course_name'}, inplace=True)
    df.rename(
        columns={'Date of Upfront Medical': 'medical_date'}, inplace=True)
    df.rename(columns={'Biometric Date': 'biometric_date'}, inplace=True)
    df.rename(
        columns={'Visa Application Date': 'application_date'}, inplace=True)
    df.rename(columns={'Medical Updated': 'medical_update_date'}, inplace=True)
    df.rename(columns={'Visa Category': 'visa_category'}, inplace=True)
    df.rename(columns={'Status': 'status'}, inplace=True)

    df.drop(df.tail(1).index,inplace=True)

    #generate age column
    now = pd.Timestamp('now')
    temp_date=pd.to_datetime(df['birth_date'])
    # df['birth_date']= pd.to_datetime(df['birth_date']);
    df['age']= (now - temp_date).astype('<m8[Y]').astype(str).apply(lambda x: x.replace('.0',''))   
    df['age']=df['age'].astype(int)
    #print(df.shape[0])

    #convert date columns from string to date format
    # df['passport_issue_date']= pd.to_datetime(df['passport_issue_date'], format="%Y/%m/%d");
    # df['medical_date']= pd.to_datetime(df['medical_date'], format="%Y/%m/%d");
    # df['biometric_date']= pd.to_datetime(df['biometric_date'], format="%Y/%m/%d");
    # df['application_date']= pd.to_datetime(df['application_date'], format="%Y/%m/%d");
    # df['medical_update_date']= pd.to_datetime(df['medical_update_date'], format="%Y/%m/%d");

    #df['passport_issue_date']= df['passport_issue_date'].dt.date;
    
    #drop duplicate records
    df = df.drop_duplicates()

    # remove data of those students who already got ppr
    df = df[df['status'] != 'PPR Received']

    #fill missing values
    df['visa_category'].fillna('Study Visa',inplace=True)

    # remove unused columns
    df = df.drop('City of Birth', axis=1)
    df = df.drop('Country of Birth', axis=1)
    df = df.drop('Name of Spouse', axis=1)
    df = df.drop('status', axis=1)
    df = df.drop('birth_date', axis=1)

    data_dict = df.to_dict("records")
    for rec in data_dict:
        visadata.replace_one({'passport_number': rec['passport_number']}, rec, upsert=True)
    
    return make_response("", 201)

def getCandidateDetails():
    data = Visadata.objects()
    return data

@app.route("/ircc/alldata", methods = ["GET"])
def getAllCandidates():
    data = getCandidateDetails()
    for d in data:
        print(d["medical_date"])
    return make_response(jsonify(data), 201)

@app.route("/ircc/uploadcsv", methods=['GET','POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
    # set the file path
        uploaded_file.save("VisaData.csv")
        cleandata()
    # save the file
    return make_response("", 201)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ircc/runalgorithm", methods=['POST'])
def tagProfiles():
    data= Algorithm().algo()
    result=json.loads(data)
    i=0
    print("came before")
    for update_data in result:
        i=i+1
        update_data['_id']=update_data['_id']['$oid']
        # print(update_data['_id'])
        # print(update_data['birth_date'])
        insert_data=Visadata.objects(_id=update_data['_id']).first()
        # print(insert_data)
        insert_data.update(**update_data)
    print(i)
    return make_response("",201)

if __name__ == "__main__":
    app.run()
