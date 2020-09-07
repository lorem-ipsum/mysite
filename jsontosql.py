from myapp.models import Movie, Character

import json

file = open('./movieresults.json')

movies = json.load(file)['movies']

for movie in movies:
    id = int(movie['id'])
    title = movie['title']
    mainPicSrc = movie['mainPicSrc']
    star = movie['star']
    summary = movie['summary']


print(movies[0])
