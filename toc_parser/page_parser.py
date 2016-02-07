from html.parser import HTMLParser
from lxml import html

class TocPageParser(HTMLParser):
    movie_title_style = 'font-family: Helvetica; font-size: 20px;'
    in_movie_span = False
    movies = list()

    def __init__(self):
        super().__init__()
        self.movies = list()

    def is_movie_span(self, tag, attrs):
        if tag == 'span':
            for name, value in attrs:
                if name == 'style' and value == self.movie_title_style:
                    return True
        return False

    def handle_starttag(self, tag, attrs):

        if self.is_movie_span(tag, attrs):
            self.in_movie_span = True

    def handle_data(self, data):
        if self.in_movie_span:
            self.movies.append(data)

    def handle_endtag(self, tag):
        if tag == 'span':
            self.in_movie_span = False

    def get_movies(self):
        return self.movies
