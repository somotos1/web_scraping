from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection and create mars_app database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Get the data from the mongo database
    final_results = mongo.db.final_results.find_one()

    # Return template and data
    return render_template("index.html", final_results=final_results)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    final_results = mongo.db.final_results
    final_results_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    final_results.update({}, final_results_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
