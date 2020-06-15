import flask
from flask import jsonify
from flask import request
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

@app.route('/api/apps/<app_id>/traces/', methods=['POST'])
def create_trace(app_id):
  trace_data = request.json['trace']
  trace = Trace(app_id, trace_data['span_id'], trace_data['event_name'], trace_data['event_data'])
  db.session.add(trace)
  db.session.commit()
  return jsonify({ "trace": trace.serialize() })

@app.route('/api/apps/<app_id>/traces/', methods=['GET'])
def get_traces(app_id):
  traces = Trace.query.filter_by(app_id=app_id).all()
  traces = map(lambda t: t.serialize(), traces)
  return jsonify({ "traces": traces })

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response

class Trace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Text())
    span_id = db.Column(db.Text())
    event_name = db.Column(db.Text())
    event_data = db.Column(db.Text())
    time_stamp = db.Column(db.DateTime())

    def __init__ (self, app_id, span_id, event_name, event_data):
        self.app_id = app_id
        self.span_id = span_id
        self.event_name = event_name
        self.event_data = event_data
        self.time_stamp = datetime.now()

    def serialize(self):
      return {
        "app_id": self.app_id,
        "span_id": self.span_id,
        "event_name": self.event_name,
        "event_data": self.event_data,
        "time_stamp": self.time_stamp,
      }


if __name__ == '__main__':
  app.run(port= 8004)