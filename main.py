from flask import Flask, render_template
import requests

# API
API_ENDPOINT = "https://api.npoint.io/0a998b24f76ffdde88d1"
response = requests.get(API_ENDPOINT)
response_data = response.json()
# You can also use simplify version
# api_data = requests.get("https://api.npoint.io/0a998b24f76ffdde88d1").json()

# Create an instance of flask class
app = Flask(__name__)

# Homepage
@app.route("/")
def home():
	return render_template("index.html", post_data=response_data)

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/post/<int:index>")
def post(index):
	filename = "{}.jpg".format(index)
	requested_post = None
	for blog in response_data:
		if blog["id"] == index:
			requested_post = blog
	return render_template("post.html", post=requested_post, filename=filename)

# Run app
if __name__ == "__main__":
	app.run(debug=True)