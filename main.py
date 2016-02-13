import functions
import re

lists_file = 'film_list.json'
titles_file = "film_list_with_movies.json"
# all_lists = list()
# for index in range(1, 77):
#     film_list = functions.read_film_list(index)
#     for key in film_list:
#         filmList = FilmList(key, film_list[key])
#         all_lists.append(filmList.__dict__)

# functions.write_lists_to_json(all_lists)
# LISTS_FROM_JSON = functions.read_lists_from_json(lists_file)
#
# print("Parsing ", len(LISTS_FROM_JSON))
# for movie_list in LISTS_FROM_JSON:
#     movies, pages = functions.get_movies(movie_list.get('link'))
#     for page in pages:
#         next_movies, next_pages = functions.get_movies(page)
#         movies.extend(next_movies)
#     movie_list['movies'] = movies
#
# functions.write_lists_to_json(LISTS_FROM_JSON, titles_file)

movie_lists = functions.read_lists_from_json(titles_file)

failed_parsing = list()
all_movies = list()
for movie_list in movie_lists:
    if len(movie_list['movies']) == 0:
        failed_parsing.append(movie_list['link'])
    else:
        all_movies.extend(movie_list['movies'])

process_movies = set()

for movie in all_movies:
    if movie[len(movie) - 1] == '(':
        movie = movie[:len(movie) - 2]
    movie = movie.strip().lower()
    matched = re.findall(r'^\d+?[.|)](.*)', movie)
    if len(matched) == 0:
        process_movies.add(movie)
    else:
        process_movies.add(matched[0].strip())

sorted_movies = list()
sorted_movies.extend(process_movies)
sorted_movies.sort()

print("Parsing failed for :", len(failed_parsing), " lists")

movie_obj_list = list()
for movie in sorted_movies:
    movie_info = re.findall(r'(.*?)\(.*(\d{4}).*\)', movie)

    movie_obj = None
    if len(movie_info) == 0:
        movie_obj = {'title': movie, 'year': 'N/A'}
    else:
        movie_obj = {'title': movie_info[0][0].strip(), 'year': movie_info[0][1]}

    movie_obj_list.append(movie_obj)

print("Movies to search for :", len(movie_obj_list))

movie_obj_list_no_duplicates = list()

previous_movie = {'title': 'test', 'year': 'test'}
for movie_obj in movie_obj_list:
    equal = False
    year = previous_movie['year']
    if previous_movie['title'] == movie_obj['title']:
        if previous_movie['year'] == movie_obj['year']:
            equal = True
            year = previous_movie['year']
        elif previous_movie['year'] == 'N/A':
            equal = True
            year = movie_obj['year']
        elif movie_obj['year'] == 'N/A':
            equal = True
            year = previous_movie['year']
        else:
            equal = False
    else:
        equal = False

    if equal:
        index = len(movie_obj_list_no_duplicates) - 1
        movie_obj_list_no_duplicates[index]['year'] = year
    else:
        movie_obj_list_no_duplicates.append(movie_obj)
        previous_movie = movie_obj

print("Movies to search for: ", len(movie_obj_list_no_duplicates))

for movie_obj in movie_obj_list_no_duplicates:
    title = movie_obj['title']
    # print(title)

    movie_info = re.findall(r'\“(.*?)\”', title)
    if len(movie_info) != 0:
        movie_obj['title'] = movie_info[0]
        title = movie_obj['title']

    movie_info = re.findall(r'^(.*?) directed', title)
    if len(movie_info) != 0:
        movie_obj['title'] = movie_info[0]
        title = movie_obj['title']

    movie_info = re.findall(r'^(.*?) dir\.', title)
    if len(movie_info) != 0:
        movie_obj['title'] = movie_info[0]
        title = movie_obj['title']
        # print(title)

    n = len(title)
    if n > 0 and title[n - 1] == '–':
        movie_obj['title'] = title[:n - 1]
        title = movie_obj['title']

for movie in movie_obj_list_no_duplicates:
    movie['title'] = movie['title'].strip()
    if not movie['title']:
        movie_obj_list_no_duplicates.remove(movie)

movie_obj_list_no_duplicates.sort(key=lambda movie: movie['title'])

final_movies = list()
previous_movie = {'title': 'test', 'year': 'test'}
i = -1
for movie_obj in movie_obj_list_no_duplicates:

    title_ = movie_obj['title']
    year_ = movie_obj['year']

    if previous_movie['title'] != title_:
        final_movie = dict()
        final_movie['title'] = title_
        final_movie['years'] = list()
        final_movie['years'].append(year_)
        final_movies.append(final_movie)
        i += 1
    else:
        if year_ not in final_movies[i]['years']:
            final_movies[i]['years'].append(year_)
    previous_movie = movie_obj

i = 0
movies_imdb = dict()
notfound = list()
for movie_obj in final_movies:
    # print(i, movie_obj)
    i += 1
    functions.get_imdb_link_fom_omdb(movie_obj, movies_imdb, notfound)
# #   movie_obj['imdb_link'] = imdblink

functions.write_lists_to_json(movies_imdb, "imdb.json")
for title in notfound:
    print("Not found! " + title)
print("Total not found:", len(notfound))
print("Total found:", len(movies_imdb))
functions.write_lists_to_json(notfound, "not_found.json")
