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



def healthcheck_message(status, dbconnection):
    message = {"status": status, "dbconnection": dbconnection}
    return json.dumps(message)


@views.route('/')
def home():
    return render_template('home.html')


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
@views.route('/admin/start_questionnaire_upd')
def start_questionnaire_upd():
    return render_template('admin.html')


# POST request method to upload selected JSON file with data of a new questionnaire
@views.route('/admin/upl_questionnaire_upd', methods=['GET', 'POST'])
def upl_questionnaire_upd():
    if request.method == 'POST':
        if 'jsonfile' not in request.files:
            flash('No file part')
            return '1' #redirect(request.url)
        jsonfile = request.files['jsonfile']
        if jsonfile.filename == '':
            flash('No selected file')
            return '2' #redirect(request.url)
        if request.files:
            print(jsonfile)
            #newq_string = StringIO(jsonfile.stream.read().decode("UTF8"), newline=None)
            #print(newq_string)
            filedata = jsonfile.read()
            print(filedata)
            print(type(filedata))
            newq_dict = json.loads(filedata.decode('utf-8'))
            print(newq_dict)
            print(type(newq_dict))
            connection = mysql.connector.connect(**config)
            cur = connection.cursor()
            questionnaireID = newq_dict['questionnaireID']
            questionnaireTitle = newq_dict['questionnaireTitle']
            keywords = newq_dict['keywords']
            cur.execute("INSERT INTO questionnaires(questionnaireID, questionnaireTitle, keywords) VALUES (%s, %s, %s)",
                        (questionnaireID, questionnaireTitle, keywords[0]))
            connection.commit()
            connection.close()
            return redirect(request.url)
        '''
        if file:
            connection = mysql.connector.connect(**config)
            cur = connection.cursor()
            for data in file:
                questionnaireID = data.get('questionnaireID')
                questionnairTitle = data.get('questionnairTitle')
                keywords = data.get('keywords')
                cur.execute("INSERT INTO questionnaire(questionnaireID, questionnairTitle, keywords) value (%i, %s, %s)",
                            questionnaireID, questionnairTitle, keywords)

            connection.commit()
            connection.close()
            return '200'
            
        else:
                return 'fail1'
        '''
    return render_template('home.html')



# pass input of uploaded file into database
@views.route('/admin/questionnaire_upd')
def questionnaire_upd():
    return 'what?'
