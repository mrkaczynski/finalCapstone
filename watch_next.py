# get spacy ready to use
import spacy
nlp = spacy.load('en_core_web_md')

# base film
planet_hulk = "Will he save their world or destroy it? When the Hulk becomes too dangerous for the Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the Hulk can live in peace. Unfortunately, Hulk land on the planet Sakaar where he is sold into slavery and trained as a gladiator"
nlp_planet_hulk = nlp(planet_hulk)

# list to hold movies
movies = []

# read data
with open('movies.txt', 'r') as f:
    for line in f:
        movies.append(line[9::])
        
        #alt
        '''line = line.split()
        line[2] = line[2].strip(':')
        movies.append(line[2::])'''

#function
def watch_next(x):
    # list to hold spacy similarities
    ratings = []

    #iterate through movies
    for movie in movies:
        similarity = nlp(movie).similarity(nlp_planet_hulk)
        ratings.append(similarity)

    #work out the index of the most similar movie
    most_similar_movies = max(ratings)
    index = ratings.index(most_similar_movies)

    return print(f"based on what you've watched, we suggest movie {index + 1}. Here's the description: {movies[index]}")

#run function
watch_next(nlp_planet_hulk)