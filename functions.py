import codecs
import urllib.request
import urllib.response
import json


def read_film_list(page_index):
    website = 'http://www.tasteofcinema.com/category/lists/film-lists/page/' + str(page_index) + '/'
    headers = {'Accept-Charset': 'utf-8'}

    request = urllib.request.Request(website, headers=headers)

    response = urllib.request.urlopen(request)
    html = response.read()
    response.close()

    print("Parsing: ", website)
    from toc_parser.page_parser import TocPageParser
    parser = TocPageParser()
    parser.feed(html.decode('utf-8'))
    parser.close()
    return parser.get_film_list()


def write_lists_to_json(film_list):
    with codecs.open("output/film_list.json", "w", 'utf-8') as output_file:
        json.dump(film_list, output_file, ensure_ascii=False, indent=4)
