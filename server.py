import os
from py_dotenv import read_dotenv
from flask import Flask, make_response, jsonify, request
import requests
from logger import reqLog, backLogs
import json

# .env
DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(DOTENV_PATH)

# PORT for the server to listen. Use env PORT if available else 5500
PORT = os.getenv("PORT") or 5500

# Items to get
filterItems = [
   "ip",
   "network",
   "version",
   "asn",
   "postal",
   "latitude",
   "longitude",
   "country_code",
]

# Instantiate Flask app
app = Flask(__name__)

# Get Current IP Information Route
@app.route('/ip/info', methods=["GET"])
def getMyIP():
   reqLog(request.path, request.method)
   # Fetch data from ipapi.co REST API
   data = requests.get('https://ipapi.co/json/')
   myInfo = data.json()
   
   if(data.status_code >= 400):
      res = make_response(myInfo, data.status_code)
      return res

   # Filter fetched data using filterItems
   filteredIpInfo = {}
   for key in myInfo:
      if(key in filterItems):
         filteredIpInfo.update({key: myInfo[key]})

   # Response
   backLogs(filteredIpInfo, request.path, request.method)
   res = make_response(filteredIpInfo, 200)
   
   return res  

# Get Specific IP Information Route
@app.route('/ip/info/<ip>', methods=["GET"])
def getIP(ip):
   reqLog(request.path, request.method)
   # Fetch data from ipapi.co REST API
   data = requests.get(f'https://ipapi.co/{ip}/json/')
   myInfo = data.json()
   
   if(data.status_code >= 400):
      res = make_response(myInfo, data.status_code)
      return res

   # Filter fetched data using filterItems
   filteredIpInfo = {}
   for key in myInfo:
      if(key in filterItems):
         filteredIpInfo.update({key: myInfo[key]})
   
   # Response
   backLogs(filteredIpInfo, request.path, request.method)
   res = make_response(filteredIpInfo, 200)
   
   return res

# Get Backlog Items Route
@app.route('/ip/backlog', methods=["GET"])
def printBackLog():
   reqLog(request.path, request.method)
   # Update Backlog
   with open ('./logs/backlog.json', 'r') as jsonLog:
      backlog = json.loads(jsonLog.readline())
   
   for i,log in enumerate(backlog):
      print(f'LOG ITEM {i}')
      for key in log:
         print(f'{key}: {log[key]}')
      print('\n')   
   
   # Response
   return make_response(jsonify(backlog), 200)


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=PORT)