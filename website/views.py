from flask import Blueprint, Response, redirect, render_template, url_for, request
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


def gen_frames():
    while True:
        from src.api import capture_frame

        frame = capture_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


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


@views.route("/load_map", methods=["POST"])
def load_map():
    from src.api import load_map

    try:
        map_number = int(request.form["map_number"])
        load_map(map_number)
    except Exception as e:
        print("Error: ", e)
        return redirect(url_for("views.shutdown"))

    return route_default()


@views.route("/load_default_map", methods=["POST"])
def load_default_map():
    from src.api import load_default_map

    try:
        load_default_map()
    except Exception as e:
        print("Error: ", e)
        return redirect(url_for("views.shutdown"))

    return route_default()


@views.route("/video_feed", methods=["GET"])
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
