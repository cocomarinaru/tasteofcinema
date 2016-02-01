import codecs
import urllib.request
import urllib.response
import json

from model.FilmList import FilmList


def read_film_list(page_index):
    website = 'http://www.tasteofcinema.com/category/lists/film-lists/page/' + str(page_index) + '/'
    html = get_url_content(website)

    print("Parsing: ", website)
    from toc_parser.page_parser import TocPageParser
    parser = TocPageParser()
    parser.feed(html.decode('utf-8'))
    parser.close()
    return parser.get_film_list()


def get_url_content(website):
    headers = {'Accept-Charset': 'utf-8'}
    request = urllib.request.Request(website, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    response.close()
    return html


def write_lists_to_json(film_list):
    with codecs.open("output/film_list.json", "w", 'utf-8') as output_file:
        json.dump(film_list, output_file, ensure_ascii=False, indent=4)


def read_lists_from_json():
    with codecs.open("output/film_list.json", "r", 'utf-8') as input_file:
        json_load = json.load(input_file)
    return json_load

def get_movies(list_url):
    html = get_url_content(list_url)
