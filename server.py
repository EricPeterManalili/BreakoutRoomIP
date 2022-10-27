import os
from py_dotenv import read_dotenv
from flask import Flask
import requests

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

PORT = os.getenv("PORT") or 5500

app = Flask(__name__)

@app.route('/', methods=["GET"])
def getMyIP():
   # ipInfo = requests.get('/')
   return "<h1>Hello World!</h1>"


if __name__ == "__main__":
   print(f'Listening on port {PORT}')
   app.run(host="0.0.0.0", port=PORT, debug=True)