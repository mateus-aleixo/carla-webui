from flask import Blueprint, redirect, render_template, request, url_for
from jinja2 import TemplateNotFound
from launch import args

views = Blueprint("views", __name__)


def get_segment(request):
    try:
        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"
    except:
        segment = None

    return segment


@views.route("/", methods=["GET"])
def route_default():
    return index()


@views.route("/index", methods=["GET"])
def index():
    return render_template("home/index.html", segment="index", theme=f"{args.theme}")


@views.route("/<template>")
def route_template(template):
    try:
        if not template.endswith(".html"):
            template += ".html"

        segment = get_segment(request)

        page = render_template(template, segment=segment)
        status = 200
    except TemplateNotFound:
        page = render_template("error/page-404.html")
        status = 404
    except:
        page = render_template("error/page-500.html")
        status = 500

    return page, status


@views.route("/shutdown", methods=["GET"])
def shutdown():
    return render_template("error/page-500.html")


@views.route("/load_map", methods=["GET"])
def load_map():
    return render_template("views/map.html", theme=f"{args.theme}")


@views.route("/add_npc", methods=["GET"])
def add_npc():
    return render_template("views/npc.html", theme=f"{args.theme}")


@views.route("/add_sensor", methods=["GET"])
def add_sensor():
    return render_template("views/sensor.html", theme=f"{args.theme}")


@views.route("/ego_vehicle", methods=["GET"])
def lego_vehicle():
    return render_template("views/ego.html", theme=f"{args.theme}")


@views.route("/change_weather", methods=["POST"])
def change_weather():
    from src.api import change_weather

    try:
        chosen_number = request.form["chosen_number"]
        print("chosen_number: ", chosen_number)
        change_weather(chosen_number)
    except Exception as e:
        print("Error: ", e)
        return redirect(url_for("views.shutdown"))

    return route_default()
