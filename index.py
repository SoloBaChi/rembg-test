from email import contentmanager
import pymongo
from flask import Flask
from flask import request,jsonify
from flask_cors import CORS

myclient =  pymongo.MongoClient("mongodb+srv://txeafrica:txeafrica2023@txe-africa.bn2btt0.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycul = mydb['customers']

# create an app
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# route
# Default Route
@app.route("/")
def index():
    return "Hello, World! This is the default route."

@app.route("/Push", methods = ["POST"])
def Push():
    content = request.get_json()
    mycul.insert_one(content)
    return jsonify({"message": "Data inserted successfully"}), 200

@app.route("/Update", methods = ["POST"])
def Update():
    content = request.get_json()
    myval = {"$set": {"Score": content["Score"]}}
    mycul.update_one({"Name": content["Name"]}, myval)
    return jsonify({"message": "Data updated successfully"}), 200

@app.route("/Deleting", methods = ["POST"])
def Delete():
    content = request.get_json()
    mycul.delete_one({"Name": content["Name"]})
    return jsonify({"message": "Data deleted successfully"}), 200


@app.route("/Pulling", methods = ["Post","GET"])
def Pull():
    content = request.get_json()
    ViewQuery = []
    pullData = mycul.find({"Name":content["Name"]})
    for i in pullData:
        ViewQuery.append({"Name":i["Name"], "Score":i["Score"]})
    return jsonify(ViewQuery)

# Not Found (404) Route
@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, This page does not exist.", 404

# run the app
if __name__ == "__main__":
    app.run()