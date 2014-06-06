from lxml import etree
from pykml.factory import KML_ElementMaker as KML

import flask
app = flask.Flask(__name__)

import srr.util

mission_planner = None


def point_placemark(origin, name, x, y):
    point = srr.util.local_to_global(origin, x, y, 0.0)

    return KML.Placemark(
        KML.name(name),
        KML.Point(
            KML.coordinates("{lon},{lat},{alt}".format(
                lon=point[0], lat=point[1], alt=0)),
            )
        )


def frame_placemark(origin, name, x, y, theta=0.0):
    frame = srr.util.local_to_global(origin, x, y, theta)

    return KML.Placemark(
        KML.name(name),
        KML.Point(
            KML.coordinates("{lon},{lat},{alt}".format(
                lon=frame[0], lat=frame[1], alt=0)),
            ),
        KML.Style(
            KML.IconStyle(
                KML.scale(5.0),
                KML.heading(frame[2]),
                KML.Icon(
                    KML.href(flask.url_for('static',
                                           filename='axes.png',
                                           _external=True)),
                    ),
                KML.hotSpot(x="0.5", y="0.5",
                            xunits="fraction",
                            yunits="fraction")
                ),
            )
        )


def bounds_placemark(origin, name, bounds_polygon):
    bounds_list = []
    for coord in list(bounds_polygon.exterior.coords):
        (lon, lat, heading) = srr.util.local_to_global(origin, coord[0],
                                                       coord[1], 0)
        bounds_list.append("{lon},{lat},{alt}".format(lon=lon, lat=lat, alt=0))
        bounds = " ".join(bounds_list)

    return KML.Placemark(
        KML.name(name),
        KML.LineString(
            KML.extrude(1.2),
            KML.coordinates(bounds)
        )
    )


@app.route("/environment.kml")
def environment_route():
    """
    Flask route that dynamically generates a KML of the current environment
    as specified in the mission YAML.
    """
    # Compute origin and start location.
    origin = mission_planner.environment.origin
    start = mission_planner.environment.start
    bounds = mission_planner.environment.bounds

    # Create a KML document with this environment represented.
    doc = KML.kml(
        KML.Document(
            KML.name("SRR Environment"),
            frame_placemark(origin, "Origin",
                            0, 0, 0),
            frame_placemark(origin, "Start",
                            start[0], start[1], start[2]),
            bounds_placemark(origin, "Bounds", bounds)
        )
    )
    return etree.tostring(doc)


@app.route("/mission.kml")
def mission_route():
    """
    Flask route that dynamically generates a KML of the current mission
    as specified in the mission YAML.
    """
    # Retrieve origin and create a list of KML attributes
    origin = mission_planner.environment.origin
    kml_list = [KML.name("SRR Mission")]

    # Add placemarks for each mission waypoint.
    for task in mission_planner.mission:
        kml_list.append(point_placemark(origin, task.name,
                                        task.location.x, task.location.y))
        if not task.is_point:
            kml_list.append(
                bounds_placemark(origin, task.name + " bounds", task.bounds))

    # Create a KML document with this environment represented.
    doc = KML.kml(
        KML.Document(
            *kml_list
        )
    )
    return etree.tostring(doc)


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