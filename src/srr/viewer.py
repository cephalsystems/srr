from lxml import etree
from pykml.factory import KML_ElementMaker as KML

import flask
app = flask.Flask(__name__)

import srr.util

mission_planner = None


def frame_placemark(name, lon, lat, heading):
    return KML.Placemark(
        KML.name(name),
        KML.Point(
            KML.coordinates("{lon},{lat},{alt}".format(
                lon=lon, lat=lat, alt=0)),
            ),
        KML.Style(
            KML.IconStyle(
                KML.scale(5.0),
                KML.heading(heading),
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


@app.route("/environment.kml")
def environment_route():
    """
    Flask route that dynamically generates a KML of the current environment
    as specified in the mission YAML.
    """
    # Compute origin and start location.
    origin = mission_planner.environment.origin
    local_start = mission_planner.environment.start
    start = srr.util.local_to_global(origin,
                                     local_start[0],
                                     local_start[1],
                                     local_start[2])

    # Compute bounds of environment.
    bounds_list = []
    for coord in list(mission_planner.environment.bounds.exterior.coords):
        (lon, lat, heading) = srr.util.local_to_global(origin, coord[0],
                                                       coord[1], 0)
        bounds_list.append("{lon},{lat},{alt}".format(lon=lon, lat=lat, alt=0))
        bounds = " ".join(bounds_list)

    # Create a KML document with this environment represented.
    doc = KML.kml(
        KML.Document(
            KML.name("SRR Environment"),
            frame_placemark("Origin", origin[0], origin[1], origin[2]),
            frame_placemark("Start", start[0], start[1], start[2]),
            KML.Placemark(
                KML.name("Bounds"),
                KML.LineString(
                    KML.extrude(1.2),
                    KML.coordinates(bounds)
                )
            )
        )
    )
    return etree.tostring(doc, pretty_print=True)


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