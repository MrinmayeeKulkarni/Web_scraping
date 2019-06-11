from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

@app.route("/")
def home():
    data = mongo.db.collection.find_one()
    return render_template("index.html", mars_page=data)

@app.route("/scrape")
def scrape_data():
    mars=scrape_mars.scrape()
    mongo.db.collection.update({},mars, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
   



