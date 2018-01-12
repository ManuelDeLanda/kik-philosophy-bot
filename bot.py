from flask import Flask, request, Response

import sqlite3
import unicodecsv
import random

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

app = Flask(__name__)
kik = KikApi('user', 'key')

kik.set_configuration(Configuration(webhook='web_hook'))

def processMessage(sMessage):
   con = sqlite3.connect('philosopherz.db')
   cur = con.cursor()
   with con:
      cur.execute("SELECT quote FROM philosopherz WHERE philosopher LIKE '%" + sMessage + "%'")
      # print(cur.fetchall())
   try:
      returnString = random.choice(cur.fetchall())[0]
   except:
      returnString = "Sorry no philosopher by that name found.  Please enter partial or full name of philosopher or try again later..."
      with open("logfile.txt", "a") as myfile:
        myfile.write("\n" + sMessage)
   return returnString.encode('utf-8')


@app.route('/', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, TextMessage):
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=processMessage(message.body)
                    # body="hello"
                )
            ])
    return Response(status=200)

if __name__ == "__main__":
    app.run(port=8080, debug=True)

