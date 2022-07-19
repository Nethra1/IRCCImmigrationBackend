from flask import Flask, make_response, request
# from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mongoengine import MongoEngine
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
    # pw_hash = bcrypt.generate_password_hash(user['password'])
    data = User(uname=user['uname'], password=str(user['password']))
    data.save()
    print(user)
    return make_response("", 201)

if __name__ == "__main__":
    app.run()

