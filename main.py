from flask import Flask, render_template, request
import requests
import smtplib

# Constant
MY_EMAIL = "sweetsugarpastry@gmail.com"
MY_PASSWORD = "rqaarmydmibkgzdl" # Gmail App password
TARGET_EMAIL = "haziqhakimiyes@gmail.com"

# API
API_ENDPOINT = "https://api.npoint.io/0a998b24f76ffdde88d1"
response = requests.get(API_ENDPOINT)
response_data = response.json()
# You can also use simplify version
# api_data = requests.get("https://api.npoint.io/0a998b24f76ffdde88d1").json()

# Create an instance of flask class
app = Flask(__name__)

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

@app.route("/contact", methods=["POST"])
def receive_form():
	if request.method == 'GET':
		return render_template("contact.html", msg_sent=False)
	else:
		# name = request.form["username"]
		# email = request.form["email"]
		# number = request.form["number"]
		# message = request.form["message"]
		# print(f"Name: {name}\nEmail: {email}\nPhone Number: {number}\nMessage: {message}")
		data = request.form
		send_email(data["username"], data["email"], data["number"], data["message"])
		return render_template("contact.html", msg_sent=True)

# Run app
if __name__ == "__main__":
	app.run(debug=True)