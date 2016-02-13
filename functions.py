import codecs
import json
import urllib.request
import urllib.response
import urllib.parse

from lxml import html

output_dir = 'output'


def read_film_list(page_index):
    website = 'http://www.tasteofcinema.com/category/lists/film-lists/page/' + str(page_index) + '/'
    html = get_url_content(website)

    print("Parsing: ", website)
    from toc_parser.list_parser import TocListParser
    parser = TocListParser()
    parser.feed(html.decode('utf-8'))
    parser.close()
    return parser.get_film_list()


def get_url_content(website):
    headers = {'Accept-Charset': 'utf-8',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'}
    request = urllib.request.Request(website, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    response.close()
    return html


def write_lists_to_json(film_list, file_name):
    file_path = output_dir + '/' + file_name
    with codecs.open(file_path, "w", 'utf-8') as output_file:
        json.dump(film_list, output_file, ensure_ascii=False, indent=4)


def read_lists_from_json(file_name):
    file_path = output_dir + '/' + file_name
    with codecs.open(file_path, "r", 'utf-8') as input_file:
        json_load = json.load(input_file)
    return json_load


def remove_bad_results(movies):
    index = movies.index("Subscribe via ")
    return movies[:index]


def get_movies(list_url):
    content = get_url_content(list_url)
    tree = html.fromstring(content)
    movies = tree.xpath('//span[@style="font-family: Helvetica; font-size: 20px;"]/text()')
    movies = remove_bad_results(movies)
    print("Parsing... " + list_url)
    other_pages = tree.xpath('//p[@class="pages"]/span/a/@href')
    return movies, other_pages


# def get_imdb_link_google(movie):
#     imdb_prefix = 'http://www.imdb'
#     google_search_page = 'http://www.google.ro/search?q='
#     url_encoded_movie = urllib.parse.quote_plus(movie + " imdb")
#     url = google_search_page + url_encoded_movie
#     content = get_url_content(url)
#     tree = html.fromstring(content)
#     text = tree.xpath('.//ol[@id="rso"]/div[1]/div[1]//cite/text()')
#     imdb_link = imdb_prefix + text[1]
#     print("Search for:", movie, "  link:", imdb_link)
#     return imdb_link


def get_imdb_link_fom_omdb(movie, imdb_movies, notfound):
    title = movie['title']
    if not title:
        return

    for year in movie['years']:
        if year == 'N/A':
            year = ''
        json_load = get_movie_json(title, year)

        if json_load['Response'] == 'True':
            id = json_load['imdbID']
            imdb_movies[id] = json_load
        else:
            if not year:
                notfound.append(title + "; " + year)
            else:
                json_load = get_movie_json(title, '')
                if json_load['Response'] == 'True':
                    id = json_load['imdbID']
                    imdb_movies[id] = json_load
                else:
                    notfound.append(title + "; " + year)


def get_movie_json(title, year):
    url = "http://www.omdbapi.com/?" + "t=" + urllib.parse.quote_plus(title) + "&y=" + year + "&r=json"
    content = get_url_content(url)
    json_load = json.loads(content.decode())
    print(url, json_load['Response'])
    return json_load
