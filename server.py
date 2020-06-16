# Standard library imports
import csv
import re

# Third party imports
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/projects/<page_name>')
def project(page_name=None):
    return render_template(f"projects/{page_name}")


@app.route('/work_experience/<page_name>')
def work_experience(page_name=None):
    return render_template(f"work_experience/{page_name}")


@app.route('/<page_name>')
def go_to_page(page_name=None):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            if is_email_address_valid(data["email"]):
                write_to_csv_file(data)
                error_message = ""
            else:
                error_message = f"The provided email address ({data['email']}) seems to be invalid. Please check it."
            return render_template("thank_you.html", firstname=data["firstname"], error=error_message)
        except Exception as e:
            return f"did not save to database : {e}"
    else:
        return "Something went wrong"


def write_to_csv_file(data):
    with open("database.csv", newline='', mode='a') as database:
        firstname = data["firstname"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        # newline unknown !!
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([firstname, email, subject, message])


def is_email_address_valid(email):
    pattern = "[\w.-]+@\w+[.][a-z]+"
    if not re.search(pattern, email):
        return False
    return True
