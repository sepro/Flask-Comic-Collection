from coagg import db

import requests
import re
import urllib
import sys

from datetime import datetime

from .functions import fetch_all


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

    @staticmethod
    def update_all_links(data):
        def parse_pages(base_urls, patterns):
            pages = fetch_all(base_urls)

            results = []

            for base_url, pattern, page in zip(base_urls, patterns, pages):
                match = re.search(pattern, page)
                try:
                    results.append(match.group(1))
                except Exception as _:
                    print("Problem found parsing {} with pattern \"{}\"".format(base_url, pattern))
                    results.append(None)

            return results

        new = 0

        urls = parse_pages([d['base_url'] for d in data], [d['pattern'] for d in data])

        for d, url in zip(data, urls):
            print("Getting %s ..." % d['name'])

            comic = Comic.query.filter_by(name=d['name']).first()

            if url is not None:
                print("Found %s ..." % url)
                if comic is None:
                    comic = Comic()
                    comic.name = d['name']
                    comic.base_url = d['base_url']
                    comic.img_url = url

                    db.session.add(comic)
                    new += 1
                else:
                    if comic.img_url != url:
                        comic.img_url = url
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
