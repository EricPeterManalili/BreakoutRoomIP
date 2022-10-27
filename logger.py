from datetime import date
import json

def reqLog(path, method):
   today = str(date.today())
   logItem = f'{today}\t{method}\t{path}'

   
   with open ('./logs/logRequest.log', 'a') as writeLog:
      writeLog.write(logItem+"\n")
   
def backLogs(data,path,method):
   with open ('./logs/backlog.json', 'r') as jsonLog:
      backlog = json.loads(jsonLog.readline())
   
      today = str(date.today())
      
      metadata = {
         "timestamp": today,
         "path": path,
         "method": method, 
      }
      
      newBackLog = {
         "meta": metadata,
         "body": data
      }
      
      backlog.append(newBackLog)
      
      with open ('./logs/backlog.json', 'w') as writeBackLog:
         writeBackLog.write(json.dumps(backlog))
      