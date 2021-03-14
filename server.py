from flask import Flask, render_template, request, redirect
import csv
import json
import logging

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app import app

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)

@app.route('/<string:page_name>')
def htmlPage(page_name):
    return render_template(page_name, page_title=page_name)

@app.route('/')
def pageHome():
    return render_template('./index.html')

# #Writing to Text File
# def write_to_file(data):
#     with open('database.txt',mode='a') as database:
#         email = data["email"]
#         subject = data["subject"]
#         message = data["message"]
#         textfile = database.write(f"\n{email},{subject},{message}")

#Writing Contact Form Data to CSV

def write_to_csv(data):
    with open('database2.csv', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

@app.route('/send-message', methods=['POST','GET'])
def sendMessage():
    form_entry = False
    if request.method =='POST':
        try:
            #Getting data into a dictionary
            data = request.form.to_dict()
            write_to_csv(data)
            return render_template("about.html", form_entry=True, message='Thank you for your message. I will get back to you shortly.')
        except:
            return render_template("about.html", form_entry=True, message="Something went wrong. Try again by refreshing the page.")
    else:
        return render_template("about.html", form_entry=True, message="Something went wrong. Try again by refreshing the page.")

#Writing Color Check Form to Data
@app.route('/color', methods=['POST','GET'])
def get_color_code():
    results='waiting'
    load_colorlib = open("data/colorlist.json")
    colorlib = json.load(load_colorlib)
    input_color = request.form.get("input_color")
    input_color = input_color.lower()

    if input_color in colorlib.keys():
        input_color_hex = colorlib[input_color]
        return render_template("color.html", result="found", color_name=input_color, hexcode=input_color_hex)
    else: 
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning('is when the incorrect color name was logged.')
        return render_template("color.html", result="not found", color_name=input_color, hexcode='not found')