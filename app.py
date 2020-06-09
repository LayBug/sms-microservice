import os
import flask
from flask import Response
import requests
import json
from flask import request, jsonify
from twilio.rest import Client


#Avoid putting your credentials here, use environment instead!!

account_sid = "ACadd0dabcbecf336727762e6675d6410f"
auth_token = "f532b89c16a4a759dd0c99c660d54cd3"
sender = "+16312914028"


client = Client(account_sid, auth_token)
balanceEndPointURI = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Balance.json"



app = flask.Flask(__name__)
app.config["DEBUG"] = True



#Task 1 *Check sms balance 

@app.route("/api/v1/sms/balance", methods=["GET"])
def checkBalance():
    response = requests.get(balanceEndPointURI, auth = (account_sid, auth_token))
    data = response.json()
    del data["account_sid"]
    return jsonify(data)



#Task 2 *Send sms

@app.route("/api/v1/sms/send", methods=["POST"])
def sendSms():
    try:
        if request.method == "POST":
            to = request.form["to"]
            message = request.form["message"]
            message = client.messages.create(
                    to = to,
                    from_ = sender,
                    body = message
                    )
            return f"Message sent successfully to {to} with message id {message.sid}"
    except KeyError:
        return Response("Invalid credentials", status=403)




app.run()

