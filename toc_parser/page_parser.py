from html.parser import HTMLParser


class TocPageParser(HTMLParser):
    href = ''
    label = ''
    in_div_title = False
    in_anchor = False;

    def __init__(self):
        super().__init__()
        self.film_list = dict()

    def error(self, message):
        super(TocPageParser).error(message)

    def is_title_div(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'title':
                    return True
        return False

    def handle_starttag(self, tag, attrs):

        if self.is_title_div(tag, attrs):
            self.in_div_title = True

        if self.in_div_title and tag == 'a':
            self.in_anchor = True
            for name, value in attrs:
                if name == 'href':
                    self.href = value

    def handle_data(self, data):
        if self.in_div_title and self.in_anchor:
            self.label = data

    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_div_title = False
        if tag == 'a':
            self.in_anchor = False
            if len(self.href) > 0 and len(self.label) > 0:
                self.film_list[self.label] = self.href
            self.href = ''
            self.label = ''

    def get_film_list(self):
        return self.film_list
