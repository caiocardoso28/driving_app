import requests
import json
from flask import Flask, request, render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_point = db.Column(db.String(60))
    end_point = db.Column(db.String(60))
    waypoints = db.Column(db.String(750))


@app.route('/')
def home():
    return render_template('testing.html')


@app.route('/markers', methods=['POST'])
def add_marker():
    data = request.get_json()  # Get the JSON data sent from the JavaScript
    lat = data['lat']
    lng = data['lng']
    print(f"{lat}, {lng}")
    # Do something with the lat and lng

    return "Success", 200


@app.route('/create_route', methods=['POST'])
def create_route():
    waypoints = [f"{coord['lat']}, {coord['lng']}" for coord in request.get_json()['coordinates']]
    print(waypoints)
    api_key = ''
    start_point = waypoints[0]
    end_point = waypoints[-1]
    waypoints_str = "|".join(waypoints[1:len(waypoints)-1])  # Prepare waypoints string
    with app.app_context():
        route = Route(start_point=start_point, end_point=end_point, waypoints=waypoints_str)
        db.session.add(route)
        db.session.commit()

    # Build URL
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start_point}&destination={end_point}"
        f"&waypoints=optimize:true|{waypoints_str}&key={api_key}"
    )

    # Send GET request
    response = requests.get(url)

    # Fetch response data
    data = response.json()
    overview_polyline = None
    for item in data['routes']:
        for key in item:
            if item.get('overview_polyline'):
                overview_polyline = item.get('overview_polyline')['points']
                break

    return jsonify({"polyline": overview_polyline})


@app.route('/get_route/<id>', methods=['GET'])
def get_route(id):
    api_key = ''
    with app.app_context():
        route = Route.query.filter_by(id=id).first()
        start_point = route.start_point
        end_point = route.end_point
        waypoints_str = route.waypoints

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start_point}&destination={end_point}"
        f"&waypoints=optimize:true|{waypoints_str}&key={api_key}"
    )

    # Send GET request
    response = requests.get(url)

    # Fetch response data
    data = response.json()
    overview_polyline = None
    for item in data['routes']:
        for key in item:
            if item.get('overview_polyline'):
                overview_polyline = item.get('overview_polyline')['points']
                break

    return jsonify({"polyline": overview_polyline,
                    "waypoints": waypoints_str.split('|'),
                    "start": start_point,
                    "end": end_point})
# start_point = "40.7128,-74.0060"
# end_point = "38.9072,-77.0369"
# waypoints = ["39.9526,-75.1652", "39.2904,-76.6122"]
# response_complete = create_route(start_point, end_point, waypoints)

# def test_it(response):
    # for key in response_complete['routes']:
        # for inner_key in key:
            # print(f"{inner_key}: {key[inner_key]}")

    # print(response_complete['status'])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="192.168.86.104")

