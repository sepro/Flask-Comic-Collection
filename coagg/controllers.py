from flask import Blueprint, render_template, current_app, request, make_response

from coagg.models import get_all_links

main = Blueprint('main', __name__)


@main.route('/')
def index():
    urls = request.cookies.get('urls')

    images = get_all_links(current_app.config['DATA'], urls=urls)

    resp = make_response(render_template('main.html', images=images))

    new_urls = [i['url'] for i in images]
    resp.set_cookie('urls', ', '.join(new_urls))
    return resp


@main.route('/<cid>')
def comic(cid):
    urls = request.cookies.get('urls')

    images = get_all_links(current_app.config['DATA'], urls=urls)

    resp = make_response(render_template('main.html', images=images, id=cid))

    new_urls = [i['url'] for i in images]
    resp.set_cookie('urls', ', '.join(new_urls))
    return resp

