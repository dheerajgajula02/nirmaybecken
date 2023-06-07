import pyrebase
from flask import Flask, json, jsonify, request
from csv import writer
import pandas as pd


configuration={
    
    "apiKey": "AIzaSyDz9uMvSRsada7wYB0LUDh9YSoFZq2KX8w",
    "authDomain": "smsstore-561fb.firebaseapp.com",
    "projectId": "smsstore-561fb",
    "storageBucket": "smsstore-561fb.appspot.com",
    "messagingSenderId": "261313261268",
    "appId": "1:261313261268:web:b9288c472a3520d7b1d541",
    "measurementId": "G-RCP2ZZ525P",
    "databaseURL":"gs://smsstore-561fb.appspot.com"

}

firebase = pyrebase.initialize_app(configuration)

storage = firebase.storage()

app = Flask(__name__)
field_names = ['SENDER', 'MESSAGE', 'TIME', 'LOCATION']

# with open("asserts\\user_messages.csv", "a") as f_object:
#     writer_object = writer(f_object)
#     writer_object.writerow(field_names)
#     f_object.close()

@app.route("/initilize", methods=['DELETE'])
def initialize():
    with open("asserts\\user_messages.csv", "a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(field_names)
        f_object.close()
    return({
        "message":"csv_initialized"
    })

@app.route("/upload",methods=['POST'])
def upload():
    file_name = "asserts\\user_messages.csv"
    f= open("asserts\\user_no.txt", "r")
    line = f.readline()
    k = int(line)
    user_name= "user_"+str(k)+".csv"
    print(user_name)
    k+=1
    f= open("asserts\\user_no.txt", "w")
    f.write(str(k))
    f.close()
    cloud_name= user_name
    print(cloud_name)

    storage.child(cloud_name).put(file_name)
    f= open(file_name, "w+")
    f.close()

    with open(file_name,'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(field_names)
        f_object.close()



    return jsonify({
        "message": "uploaded_successfully "
    })


@app.route("/extract", methods=['POST'])
def extract():
    body = request.get_json(force=True)
    sender_name = body['sender']
    message= body['message']
    time = body['time']
    location = body['location']
    list_values = [sender_name, message, time, location]
    with open("asserts\\user_messages.csv", 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_values)
        f_object.close()
    return jsonify({
        "message" : "written to csv"
    })



if __name__=="__main__":
    app.run()
    with open("asserts\\user_messages.csv", "a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(field_names)
        f_object.close()







