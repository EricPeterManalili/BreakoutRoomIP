import os
from py_dotenv import read_dotenv
from flask import Flask, make_response, jsonify, request
import requests
from logger import reqLog, backLogs
import json

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

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

PORT = os.getenv("PORT") or 5500

app = Flask(__name__)

@app.route('/ip/info', methods=["GET"])
def getMyIP():
   # headers = f'{request.headers}'
   data = requests.get('https://ipapi.co/json/')
   myInfo = data.json()

   filteredIpInfo = {}
   for key in myInfo:
      if(key in filterItems):
         filteredIpInfo.update({key: myInfo[key]})
   
   reqLog(request.path, request.method)
   backLogs(filteredIpInfo, request.path, request.method)
   res = make_response(filteredIpInfo, 200)
   
   return res

@app.route('/ip/info/<ip>', methods=["GET"])
def getIP(ip):

   data = requests.get(f'https://ipapi.co/{ip}/json/')
   myInfo = data.json()

   filteredIpInfo = {}
   for key in myInfo:
      if(key in filterItems):
         filteredIpInfo.update({key: myInfo[key]})
   
   reqLog(request.path, request.method)
   backLogs(filteredIpInfo, request.path, request.method)
   res = make_response(filteredIpInfo, 200)
   
   return res

@app.route('/ip/backlog', methods=["GET"])
def printBackLog():
   with open ('./logs/backlog.json', 'r') as jsonLog:
      backlog = json.loads(jsonLog.readline())
   
   return jsonify(backlog)


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=PORT, debug=True)