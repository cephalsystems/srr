import flask
app = flask.Flask(__name__)

mission_planner = None


@app.route("/environment.kml")
def environment_route():
    """
    Flask route that dynamically generates a KML of the current environment
    as specified in the mission YAML.
    """
    return "Hello World!"


@app.route("/mission.kml")
def mission_route():
    """
    Flask route that dynamically generates a KML of the current mission
    as specified in the mission YAML.
    """
    return "Hello World!"


@app.route("/perception.kml")
def perception_route():
    """
    Flask route that dynamically generates a KML of the current perception
    outputs from the perception module.
    """
    return "Hello World!"


@app.route("/navigation.kml")
def navigation_route():
    """
    Flask route that dynamically generates a KML of the current navigation
    outputs from the navigation module.
    """
    return "Hello World!"


def run():
    """
    Blocking function that runs Flask webserver instance.
    """
    app.run()