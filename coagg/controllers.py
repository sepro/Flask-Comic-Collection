from flask import Blueprint, render_template, make_response, request

from coagg.models import Comic

from datetime import timedelta, date

main = Blueprint('main', __name__)


@main.route('/')
def index():
    images = Comic.query.all()

    for i in images:
        cookie_url = request.cookies.get(str(i.id))
        if cookie_url != i.img_url:
            i.new = True

    resp = make_response(render_template('main.html', images=images))
    return resp


@main.route('/<cid>')
def comic(cid):
    images = Comic.query.all()
    image = Comic.query.get_or_404(cid)

    for i in images:
        cookie_url = request.cookies.get(str(i.id))
        if cookie_url != i.img_url and i.id != image.id:
            i.new = True

    resp = make_response(render_template('main.html', images=images, image=image))

    expires = date.today() + timedelta(days=7)
    resp.set_cookie(str(cid), image.img_url, expires=expires.ctime())

    return resp

