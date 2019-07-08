from flask import request, url_for, jsonify, render_template
from flask_api import FlaskAPI, status, exceptions
from flask_restful import reqparse

# import json

import requests
import json


response = requests.get("https://api.weather.gov/alerts/active")
data = response.json()
print(data)


# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='rate cannot be converted')
# parser.add_argument('coordinates')
# args = parser.parse_args()
# import response

# app = FlaskAPI(__name__, template_folder = "templates" )

# url = "/https://api.weather.gov"

# @app.route('/')
# def index():
#    return render_template('index.html')

# @app.route('/alerts', methods=['GET'])
# def warnings():
#     location = request.get("coordinates")
#     effective = request.get("effective")
#     expires = request.get("expires")
#     status = request.get("status")
#     severity = request.get("severity")
#     urgency = request.get("urgency")
#     event = request.get("event")
#     senderName = request.get("senderName")
#     headline = request.get("headline")
#     response = request.get("response")
#     return print (jsonify(warnings))


# @app.route('/json',methods=['GET','POST'])
# def json():
#   j = [{"id":1, "username":"john"},{"id":2,"username":"doe"}]
#   return jsonify(j=j)

# url = "https://api.weather.gov"
# params = {
#     "location": "coordinates",
#     "effective": "effective",
#     "expires": "expires",
#     "status": "status",
#     "severity": "severity",
#     "urgency": "urgency",
#     "event": "event",
#     "senderName": "senderName",
#     "headline": "headline",
#     "response": "respose",
# }

# @app.route("/alerts/active", methods=['GET'])



# def warnings():
  # location = request.arg.get('coordinates')
  # effective = request.arg.get('effective')
  # expires = request.arg.get('expires')
  # status = request.arg.get('status')
  # severity = request.arg.get('severity')
  # urgency = request.arg.get('urgency')
  # event = request.arg.get('event')
  # senderName = request.arg.get('senderName')
  # headline = request.arg.get('headline')
  # response = request.arg.get('response')

  # return '''<h1>The location of affected areas: {location}</h1>
  #             <h1>The effective date is: {effective}</h1>
  #             <h1>The expiration of effect notice is: {expires}</h1>
  #             <h1>The status of notice is: {status}</h1>
  #             <h1>The severity of this notice is: {severity}</h1>
  #             <h1>The urgency of methond for safety is: {urgency}</h1>
  #             <h1>The event of disaster is: {event}</h1>
  #             <h1>The sender of notice is: {senderName}</h1>
  #             <h1>Description of event: {headline}</h1>
  #             <h1>The response of approaching event: {response}</h1>'''.format(language, framework, website)




# @app.route("/", methods=['GET'])
# def notes_list():
#     if request.method == 'POST':
#         note = str(request.data.get('text', ''))
#         idx = max(params.keys()) + 1
#         params[idx] = note
#         return weather(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    # return [weather(idx) for idx in sorted(params.keys())]


# if __name__ == "__main__":
#     app.run(debug=True)