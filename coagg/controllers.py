from flask import Blueprint, render_template, make_response, request

from coagg.models import Comic, Message

from datetime import timedelta, date

main = Blueprint('main', __name__)


@main.route('/')
def index():

    resp = make_response(render_template('main.html'))
    return resp


@main.route('/<cid>')
def comic(cid):
    image = Comic.query.get_or_404(cid)

    resp = make_response(render_template('main.html', image=image))

    expires = date.today() + timedelta(days=7)
    resp.set_cookie(str(cid), image.img_url, expires=expires.ctime())

    return resp

