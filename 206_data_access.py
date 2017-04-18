# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # same deal as always...
# import twitter_info # still need this in the same directory, filled out

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_FNAME = "SI206_project3_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}






def search_movie(some_list):
	lst_of_movies = []

	base_url = "http://www.omdbapi.com/?t="
	
	for item in some_list:
		movie_results = {}
		movie_search = base_url + str(item)
		movie_title = "movie_{}".format(item)

		if movie_title in CACHE_DICTION:
			print(('using cached data for', movie_title))
			
			movie_results = CACHE_DICTION[movie_title]

			lst_of_movies.append(movie_results)

		else:

			response = requests.get(movie_search)
			json_response = json.loads(response.text)

			CACHE_DICTION[movie_title] = json_response

			f = open(CACHE_FNAME, 'w')
			f.write(json.dumps(CACHE_DICTION))

			f.close()

			lst_of_movies.append(json_response)

	return lst_of_movies





# List of Movies that are going to be search

def searh_twitter(search_item):
	twitter_key = "twitter_{}".format(search_item)

	if twitter_key in CACHE_DICTION:
		print(('using cached data for', twitter_key))

		twitter_search_results = CACHE_DICTION[twitter_key]

	else:
		twitter_search_results = api.search(search_item)

		CACHE_DICTION[twitter_key] = twitter_search_results

		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

		return twitter_search_results



class Movie():
	"""docstring for Movie"""
	def __init__(self, some_dictionary):
		self.title = some_dictionary["Title"]
		self.director = some_dictionary["Director"]
		self.IMDB_rating = some_dictionary["imdbRating"]
		self.actors = [x for x in some_dictionary["Actors"].split(",")]
		self.number_of_languages = len([x for x in some_dictionary["Language"].split(",")])
		self.imdbID = some_dictionary["imdbID"]

	def __str__(self):
		return str(self.number_of_languages)

	# Returns the first actor that is paid
	def return_first_actor(self):
		return self.actors[0]

	# Returns a Directors

	def return_direcor(self):
		return self.director


	






movies_list = ["toy story 3", "The Pursuit of Happyness", "The Notebook"]

# This will return a list of dictonaries 
lst_of_movie_dictionaries = search_movie(movies_list)

# This will return a list of instances of each Movie Class

lst_instances_movie_class = [Movie(x) for x in lst_of_movie_dictionaries]

# Create a list of directors to search in twitter

lst_of_directors = [x.director for x in lst_instances_movie_class]


#This case would return a list of dictionaries of data that could be held in

lst_of_tweets = [searh_twitter(x) for x in lst_of_directors]




class Tweet(object):
	"""docstring for Tweet"""
	def __init__(self, some_dictionary):
		# The user who poseted the tweet
		self.user_post_tweet 
		pass

		




conn = sqlite3.connect('final_project_option_2.db')

cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Movie')
table_spec = 'CREATE TABLE IF NOT EXISTS Movie(ID TEXT PRIMARY KEY, Title TEXT, Director TEXT ,number_of_languages INTEGER, IMDB_Rating INTEGER, top_billed TEXT)'
cur.execute(table_spec)



## Task 2 - Creating database and loading data into database
# table Movies, with columns:
# - ID (containing the string id belonging to the OMBD id number) -- this column should be the PRIMARY KEY of this table
# - Title (containing the text of the title)
# - Director (an text of the director )
# - Number of Language (A number containg how many languages there are)
# - Raitnging 
# - The top billed (first in the list) actor in the movie
# - File wneeds to be added

database_information_movie = set()

statement = 'INSERT INTO Movie VALUES (?, ?, ?, ? , ?, ?)'

for items in lst_instances_movie_class:

	actor = items.return_first_actor()
	some_tuple = (items.imdbID, items.title, items.director, items.number_of_languages, items.IMDB_rating, actor)

	database_information_movie.add(some_tuple)
	cur.execute(statement,some_tuple)






conn.commit()

conn.close()
print("*** OUTPUT OF TESTS BELOW THIS LINE ***")
# Testing Twitters Class Methods and Instances
# class PartOne(unittest.TestCase):
# 	# Testing whether the class Twitter.search exists
# 	def test1(self):
# 		twitter_class = Twitter()

# 		class ClassName(object):
# 			def __init__(self):
# 				self = 0
		
# 		self.assertTrue(type(twitter_class) , type(ClassName))

# 	# Testing if the search method in Twitter Class returns a list
# 	def test2(self):
# 		twitter_class = Twitter()

# 		self.assertTrue(twitter_class.search("Get Out"), type([]))

# # Testing Movie Class

# class PartTwo(unittest.TestCase):
# 	# Testing whether the class movie exsits 
# 	def test1(self):
# 		movie_class = Movie()

# 		class ClassName(object):
# 			def __init__(self):
# 				self = 0
		
# 		self.assertTrue(type(movie_class) , type(ClassName))

# 	# Testing for the movie seach and returns a dictorany contian items
# 	def test2(self):
# 		movie_class = Movie()

# 		self.assertTrue(movie_class.search("Get Out"), type({}))

# 	# Testing whether the first item is a string type

# 		movie_class = Movie()

# 		item = movie_class.search("Get Out")

# 		self.assertTrue(type(item[1]), type(""))	

# 	# Making sure that our function in movie returns the string type of it.
# 	def test3(self):
# 		movie_class = Movie()

# 		self.assertTrue(movie_class.__str__(), type(""))

# 	# Test case is making sure that the data we get is the actual the users
# 	def test4(self):
# 		twitter_class = Twitter()

# 		self.assertEqual(type(twitter_class.get_twitter_users("Get Out is Good Moview")),type({'movierevier', 'search'}))

# class PartThree(unittest.TestCase):
# 		# A function that returns a list of users testing for that
# 		def test1(self):

# 			twitter_class = Twitter()

# 			self.assertTrue(type(twitter_class.return_user()), type([]))
		
# 		# Returns a list of each movies we searched for and making sure that the data is correct
# 		def test2(self):
# 			twitter_class = Twitter()

# 			self.assertTrue(type(twitter_class.return_user()[1]), type([]))








	






if __name__ == "__main__":
	unittest.main(verbosity=2)
