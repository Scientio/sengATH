import requests
from flask import Blueprint, render_template, request, flash, jsonify, redirect, Flask, url_for
import mysql.connector
from mysql.connector import errorcode
import json
from io import StringIO
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

config = {'host': 'localhost',
          'database': 'survey',
          'user': 'root',
          'password': 'Fierlefran7'}


@views.route('/')
def home():
    return render_template('home.html')


def healthcheck_message(status, dbconnection):
    message = {"status": status, "dbconnection": dbconnection}
    return json.dumps(message)


@views.route('/admin/healthcheck')
def healthcheck():
    try:
        connection = mysql.connector.connect(**config)
        connection.close()
        return healthcheck_message("OK", config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return healthcheck_message("failed", config)


# page to input json data (questionnaire)
@views.route('/admin')
def admin():
    return render_template('admin.html')


# POST request method to upload selected JSON file with data of a new questionnaire
@views.route('/admin/questionnaire_upd', methods=['GET', 'POST'])
def questionnaire_upd():
    if request.method == 'POST':
        if 'jsonfile' not in request.files:
            flash('No file part')
            return '1'  # redirect(request.url)
        jsonfile = request.files['jsonfile']
        if jsonfile.filename == '':
            flash('No selected file', 'error')
            return '2'  # redirect(request.url)
        if request.files:
            filedata = jsonfile.read()
            newq_dict = json.loads(filedata.decode('utf-8'))
            # get dict content
            questionnaireID = newq_dict['questionnaireID']
            questionnaireTitle = newq_dict['questionnaireTitle']
            keywords = newq_dict['keywords']
            questions = newq_dict['questions']
            # implement in mysql
            connection = mysql.connector.connect(**config)
            cur = connection.cursor()
            #check if allready existent
            #cur.execute("SELECT questionnaireID FROM questionnaires")
            #print(cur.fetchone())
            #print(type(cur.fetchone()))
            #if questionnaireID == cur.fetchone():
            #    flash("ID allready exists!")
            #    return redirect(request.url)

            cur.execute("CREATE TABLE IF NOT EXISTS questionnaires (\
                        questionnaireID VARCHAR(5) PRIMARY KEY NOT NULL, \
                        questionnaireTitle VARCHAR(100)\
                        )")
            cur.execute("CREATE TABLE IF NOT EXISTS questions (\
                        qID VARCHAR(3) PRIMARY KEY NOT NULL, \
                        qtxt VARCHAR(100), \
                        req VARCHAR(6),\
                        qtype VARCHAR(50),\
                        questionnaireID VARCHAR(5)\
                        )")
            cur.execute("CREATE TABLE IF NOT EXISTS keywords (\
                        kwtxt VARCHAR(30) PRIMARY KEY NOT NULL,\
                        questionnaireID VARCHAR(5)\
                        )")
            cur.execute("CREATE TABLE IF NOT EXISTS opttable (\
                        optID VARCHAR(6) PRIMARY KEY NOT NULL, \
                        opttxt VARCHAR(20), \
                        nextqID VARCHAR(3),\
                        qID VARCHAR(3)\
                        )")

            # insert values into tables
            cur.execute("INSERT INTO questionnaires(questionnaireID, questionnaireTitle) VALUES (%s, %s)",
                        (questionnaireID, questionnaireTitle))
            for entry in keywords:
                cur.execute("INSERT INTO keywords(kwtxt, questionnaireID) VALUES (%s, %s)",
                            (entry, questionnaireID))
            print(questions)
            for question in questions:
                cur.execute("INSERT INTO questions(qID, qtxt, qtype, req, questionnaireID) VALUES (%s, %s,%s, %s, %s)",
                            (question["qID "], question["qtext"], question["type"], question["required"], questionnaireID))
                for entry in question["options"]:
                    cur.execute("INSERT INTO opttable(optID, opttxt, nextqID, qID) VALUES (%s, %s,%s, %s)",
                                (entry["optID"], entry["opttxt"], entry["nextqID"], question["qID "]))
            connection.commit()
            connection.close()
            flash("Database Successfully Uploaded", 'message')
        return redirect(request.url)
    return render_template('admin.html')


@views.route('/admin/resetall', methods=['GET', 'POST'])
def resetall():
    if request.method == 'POST':
        connection = mysql.connector.connect(**config)
        cur = connection.cursor()
        cur.execute("DROP TABLE IF EXISTS keywords")
        cur.execute("DROP TABLE IF EXISTS opttable")
        cur.execute("DROP TABLE IF EXISTS questionnaires")
        cur.execute("DROP TABLE IF EXISTS questions")
        connection.commit()
        connection.close()
        flash("Database Successfully Reseted", 'message')
        return redirect(request.url)
    return render_template('admin.html')


@views.route('/admin/resetq/:questionnaireID', methods=['GET', 'POST'])
def reset_quans():
    if request.method == 'POST':
        pass
    return render_template('admin.html')


@views.route('/analyze')
def analyze():
    return render_template('analyze.html')


@views.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        #questionnaireID = request.form.get('questionnaireID')
        questionnaireID = request.form
        questionnaireID = questionnaireID["questionnaireID"]
        questionareDetails = get_questionnaire_details(questionnaireID)
        print(questionareDetails)
        print("exit")
    return render_template('analyze.html')


def get_questionnaire_details(questionnaireID: str):
    connection = mysql.connector.connect(**config)
    cur = connection.cursor()

    cur.execute("SELECT questionnaireTitle FROM questionnaires WHERE questionnaireID = 'QQ000'")
    questionnaireTitle = cur.fetchone()[0]

    cur.execute(f"SELECT kwtxt FROM keywords WHERE questionnaireID = '{questionnaireID}'")
    keywords = cur.fetchall()
    keywords = [k[0] for k in keywords]

    cur.execute(f"SELECT qtxt FROM questions WHERE questionnaireID = '{questionnaireID}'")
    questions = cur.fetchall()
    questions = [k[0] for k in questions]

    connection.close()

    return questionnaireTitle, keywords, questions
