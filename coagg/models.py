from coagg import cache

import requests
import re
import hashlib


def __get_comic(name, base_url, pattern):
    page = requests.get(base_url)

    match = re.search(pattern, page.content.decode('utf-8'))

    url = match.group(1) if match else None
    return {
        'id': hashlib.md5(name.encode()).hexdigest(),
        'name': name,
        'base_url': base_url,
        'url': url
    }


@cache.cached(timeout=300, key_prefix='load_urls')
def get_all_links(data, urls=None):
    print(urls)
    if urls is None:
        urls = ''

    output = [__get_comic(d['name'], d['base_url'], d['pattern']) for d in data]

    for o in output:
        o['new'] = o['url'] not in urls

    print(output)

    return output
