from coagg import db

import requests
import re
import urllib

from datetime import datetime


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Comic(db.Model):
    __tablename__ = 'comics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    base_url = db.Column(db.Text)
    img_url = db.Column(db.Text)

    new = False

    @staticmethod
    def __get_comic(name, base_url, pattern):
        page = requests.get(base_url)

        match = re.search(pattern, page.content.decode('utf-8'))

        url = match.group(1) if match else None
        return {
            'id': urllib.parse.quote(name.lower().replace(' ', '_')),
            'name': name,
            'base_url': base_url,
            'url': url
        }

    @staticmethod
    def update_all_links(data):
        new = 0

        for d in data:
            print("Getting %s ..." % d['name'])

            comic_data = Comic.__get_comic(d['name'], d['base_url'], d['pattern'])
            comic = Comic.query.filter_by(name=comic_data['name']).first()

            print("Getting %s ..." % comic_data['url'])

            if comic is None:
                comic = Comic()
                comic.name = comic_data['name']
                comic.base_url = comic_data['base_url']
                comic.img_url = comic_data['url']

                db.session.add(comic)
                new += 1
            else:
                if comic.img_url != comic_data['url']:
                    comic.img_url = comic_data['url']
                    new += 1

            db.session.commit()

        msg = Message()

        if new > 1:
            msg.message = 'Update complete: found %d new comics' % new
        elif new == 1:
            msg.message = 'Update complete: found %d new comic' % new
        else:
            msg.message = 'Update complete: no new comics found'

        db.session.add(msg)
        db.session.commit()

        return True
