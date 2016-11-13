from flask import Blueprint, render_template, make_response

from coagg.models import Comic

main = Blueprint('main', __name__)


@main.route('/')
def index():
    images = Comic.query.all()

    resp = make_response(render_template('main.html', images=images))
    return resp


@main.route('/<cid>')
def comic(cid):
    images = Comic.query.all()
    image = Comic.query.get_or_404(cid)

    resp = make_response(render_template('main.html', images=images, image=image))
    return resp

