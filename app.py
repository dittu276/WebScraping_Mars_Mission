# import necessary libraries
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from  scrape_mars import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_info = mongo.db.collection.find().limit(3).sort([('_id', 1)])
    # return template and data
    return render_template("index2.html", mars_info=mars_info)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars_mission = scrape_mars()

    # Store results into a dictionary
    mars_info = {
        "News_Title": mars_mission["News_Title"],
        "News_Paragraph": mars_mission["News_Paragraph"],
        "Featured_Image": mars_mission["Featured_Image"],
        "Mars_Weather": mars_mission["Mars_Weather"],
        "Mars_Facts":mars_mission["Mars_Facts"],
        "Hemisphere_Images":mars_mission["Hemisphere_Images"]
    }

    # Insert forecast into database
    mongo.db.collection.insert_one(mars_info)

    # Redirect back to home page
    return redirect(url_for('home'), code=302)


if __name__ == "__main__":
    app.run(debug=True)
