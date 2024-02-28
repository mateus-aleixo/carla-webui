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


@views.route("/maps", methods=["GET"])
def maps():
    return render_template("views/maps.html", theme=f"{args.theme}")


@views.route("/npc", methods=["GET"])
def npc():
    return render_template("views/npc.html", theme=f"{args.theme}")


@views.route("/sensor", methods=["GET"])
def sensor():
    return render_template("views/sensor.html", theme=f"{args.theme}")


@views.route("/ego", methods=["GET"])
def ego():
    return render_template("views/ego.html", theme=f"{args.theme}")


@views.route("/load_map", methods=["POST"])
def load_map():
    from src.api import load_map

    try:
        map_number = int(request.form["map_number"])
        load_map(map_number)
    except Exception as e:
        print("Error: ", e)
        return redirect(url_for("views.shutdown"))

    return maps()


@views.route("/load_default_map", methods=["POST"])
def load_default_map():
    from src.api import load_default_map

    try:
        load_default_map()
    except Exception as e:
        print("Error: ", e)
        return redirect(url_for("views.shutdown"))

    return maps()
