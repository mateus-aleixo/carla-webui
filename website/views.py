from flask import Blueprint, redirect, render_template, url_for, request
from jinja2 import TemplateNotFound

views = Blueprint("views", __name__)


def get_segment(request):
    try:
        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"
    except:
        segment = None

    return segment


@views.route("/")
def route_default():
    return redirect(url_for("views.index"))


@views.route("/index")
def index():
    return render_template("home/index.html", segment="index")


@views.route("/<template>")
def route_template(template):
    try:
        if not template.endswith(".html"):
            template += ".html"

        segment = get_segment(request)

        page = render_template("home/" + template, segment=segment)
        status = 200
    except TemplateNotFound:
        page = render_template("home/page-404.html")
        status = 404
    except:
        page = render_template("home/page-500.html")
        status = 500

    return page, status
