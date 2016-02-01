import functions
from model.FilmList import FilmList

all_lists = list()
for index in range(1, 77):
    film_list = functions.read_film_list(index)
    for key in film_list:
        filmList = FilmList(key, film_list[key])
        all_lists.append(filmList.__dict__)

functions.write_lists_to_json(all_lists)