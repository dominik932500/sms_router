#!flask/bin/python
from flask import Flask, jsonify
from flask import request
from flask_restful import reqparse
#!/usr/bin/python3
import time
import vodem.simple
import string
import requests

check_token = 'djVNzY5Ir1TEg4xaBkUXr4UeHuE9DgSc'

app = Flask(__name__)

@app.route('/api/v1/tasks/sms/reset', methods=['POST'])         #Accept only POST requests
def send_sms():
        header = request.headers                                #Get the header as an object
        auth_token = request.headers.get('Authorization')       #Get authorization token from the header
        content = request.get_json(silent=False)                #Get the body of sent JSON
        print(content)

        if auth_token == check_token:                           #If statement to check the auth token
                try:
                        code_to_send = content['resetCode'].strip()
                except Exception as e:
                        return jsonify({'error': 'reset code is missing'}), 400
                try:
                        username = content['username'].strip()
                except Exception as e:
                        return jsonify({'error': 'username is missing'}), 400
                try:
                        phone_number = content['phone'].strip()
                except Exception as e:
                        return jsonify({'error': 'phone number is missing'}), 400

                if phone_number[:1] != '+':     #:1 means that we check the first character
                        return jsonify({'error': 'Bad phone number format'}), 400
                if phone_number[1:].isdigit() == False: #isdigit checks if all characters are digits
                        return jsonify({'error': 'Phone number has invalid characters'}), 400
                if code_to_send.isdigit() == False:
                        return jsonify({'error': 'Reset code has invalid characters'}), 400

                message = 'Reset code for ' + username + ': ' + code_to_send    #making the SMS string to send
                try:    #Try used to check if the modem is down
                        vodem.simple.sms_send(phone_number, message)    #Sending the SMS
                        print(message)
                        print(content)
                        resp = jsonify(success=True)            #Return success code as a response
#                       resp = jsonify({'ok': 'sms disabled for testing'})
                        return resp, 200
                except:
                        return jsonify({'error': 'Modem is disconnected'}), 500
                        #If try clause catches an exception, it means that the modem doesn't work

        else:
                return jsonify({'error': 'Unauthorized'}), 401
                #If the provided token doesn't match with the auth token, 401 code is returned

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
