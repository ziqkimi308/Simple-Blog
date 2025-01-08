from flask import Flask, render_template, request
import requests
import smtplib

# Constant
# --- CHANGE EMAIL DETAILS HERE ---
MY_EMAIL = ""
MY_PASSWORD = "" # Gmail App password
TARGET_EMAIL = ""

# Npoint API to store json data of all post
# --- CHANGE YOUR NPOINT API HERE ---
API_ENDPOINT = "" # Make your own using npoint
response = requests.get(API_ENDPOINT)
response_data = response.json()
# You can also use simplify version
# api_data = requests.get("https://api.npoint.io/0a998b24f76ffdde88d1").json()

# Create an instance of flask class
app = Flask(__name__)

# Send feedback message via email
def send_email(name, email, number, message):
	email_message = f"Subject:Blog Feedback\n\nName: {name}\nEmail: {email}\nPhone Number: {number}\nMessage: {message}"
	with smtplib.SMTP("smtp.gmail.com", 587) as connection:
		connection.starttls()
		connection.login(MY_EMAIL, MY_PASSWORD)
		connection.sendmail(MY_EMAIL, TARGET_EMAIL, email_message)

# Homepage
@app.route("/")
def home():
	return render_template("index.html", post_data=response_data)

# Contact page
@app.route("/contact")
def contact():
	return render_template("contact.html")

# About page
@app.route("/about")
def about():
	return render_template("about.html")

# Post page
@app.route("/post/<int:index>")
def post(index):
	filename = "{}.jpg".format(index)
	requested_post = None
	for blog in response_data:
		if blog["id"] == index:
			requested_post = blog
	return render_template("post.html", post=requested_post, filename=filename)

# Contact page after sent feedback form
@app.route("/contact", methods=["POST"])
def receive_form():
	if request.method == 'GET':
		return render_template("contact.html", msg_sent=False)
	else:
		data = request.form
		send_email(data["username"], data["email"], data["number"], data["message"])
		return render_template("contact.html", msg_sent=True)

# Run app
if __name__ == "__main__":
	app.run(debug=True)