from flask import Flask, render_template, request, redirect, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from base64 import b64encode
import base64

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# mongo = PyMongo(app)


# def get_category_names():
#     categories = []
#     for category in mongo.db.collection_names():
#         if not category.startswith("system."):
#             categories.append(category)
#     return categories    


@app.route("/")
def get_tasks():
    # categories = get_category_names()
    # return render_template("tasks.html", categories=categories, category='Task List')
    return render_template("base.html")




if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)