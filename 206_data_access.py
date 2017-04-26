# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # same deal as always...
import itertools

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

CACHE_FNAME = "SI206_final_project_cache.json"
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

		return twitter_search_results

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


	

class Tweet(object):
	"""docstring for Tweet"""
	def __init__(self, some_dictionary):
		# The user who poseted the tweet
		self.list_of_neighbors = some_dictionary["statuses"]
		self.query_search = some_dictionary["search_metadata"]

##############
# Twitter User
##############
class TwitterUser(object):
	"""docstring for TwitterUser"""
	def __init__(self, arg, query_search):
			# Tweets Data
		self.tweet_text = arg["text"]
		self.tweet_id = arg["id"]
			# This data would be found int the twitter stuff 
		self.twitter_user = arg["user"]["id"]
			# This data would be provided by search term
		self.query_item = query_search["query"]
			# Number of favorites
		self.favorites = arg["favorite_count"]

			# Number of retweets 
		self.retweets = arg["retweet_count"]

		#Tweets User table

			#Twitter User ID 
		self.user_id = arg["user"]["id"]
			# User Screen name
		self.user_screen_name = arg["user"]["screen_name"]
			# Number of favoirtes
		self.num_of_favorites = arg["user"]["favourites_count"]

			# Number of friends
		self.num_friends = arg["user"]["friends_count"]



	def return_tuple_for_twitter_user(self):

		return (self.user_id, self.user_screen_name, self.num_of_favorites, self.num_friends)





movies_list = ["toy story 3", "The Pursuit of Happyness", "The Notebook"]

# This will return a list of dictonaries 
lst_of_movie_dictionaries = search_movie(movies_list)

# This will return a list of instances of each Movie Class

lst_instances_movie_class = [Movie(x) for x in lst_of_movie_dictionaries]

# Create a list of directors to search in twitter

lst_of_directors = [x.director for x in lst_instances_movie_class]


#This case would return a list of dictionaries of data that could be held in


lst_of_tweets = [searh_twitter(x) for x in lst_of_directors]


# We will create a list of instances of each tweet

def create_lst_of_instances(lst_tweet):
	temp_lst = []

	for item in lst_tweet:

		temp_lst.append(Tweet(item))
		

	return temp_lst




# This will create a class that holds all the users into groups based on the meta data searched 
lst_instances_tweet = create_lst_of_instances(lst_of_tweets)


#This function will return a list with each thing you need and twitter user instances in the list

def instances_of_twitter(lst_again):
	temp_lst = []

	query_holder = lst_again.query_search
		
	for item in lst_again.list_of_neighbors:
			temp_lst.append(TwitterUser(item, query_holder))

	return temp_lst

# This variable will contain all the instances of the Twiiter User

lst_of_twitteruser = [instances_of_twitter(x) for x in lst_instances_tweet]










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


# table Users, with columns:
# - User_ID
# - screen_name (containing the text of the title)
# - number_of_favorites (A number containg how many languages there are)
# - number_of_friends

# Creating a function that allows us to just only have one data

lst_of_twitter_user_tuples = set()

for elem in lst_of_twitteruser:
	for x in elem:
		temp_val = x.return_tuple_for_twitter_user()
		lst_of_twitter_user_tuples.add(temp_val)

statement = 'INSERT INTO Users VALUES (?,?,?,?)'



cur.execute('DROP TABLE IF EXISTS Users')
table_spec = 'CREATE TABLE IF NOT EXISTS Users(User_ID TEXT PRIMARY KEY, screen_name TEXT, number_of_favorites INTEGER, number_of_friends INTEGER)'
cur.execute(table_spec)

# This will create the table and add all the twitter users
for elem in lst_of_twitter_user_tuples:
	cur.execute(statement, elem)



# table Tweets, with columns:
# - Tweet text
# - Tweet ID (primary key)
# - The user who posted the tweet (represented by a reference to the users table)
# - The movie search this tweet came from (represented by a reference to the movies table)
# - Number favorites
# - Number retweets



cur.execute('DROP TABLE IF EXISTS Tweets')
table_spec = """CREATE TABLE IF NOT EXISTS Tweets(tweet_text TEXT,tweet_id Text PRIMARY KEY ,user TEXT, search TEXT, number_of_favoirted INTEGER, number_of_retweets INTEGER)"""
cur.execute(table_spec)

statement = 'INSERT INTO Tweets VALUES (?,?,?,?,?,?)'


for elem in lst_of_twitteruser:
	for item in elem:

		
		user_poster = str(item.user_screen_name)
		user_search = str(item.query_item)

		ok = user_search.replace("+", " ")


		some_tuple = (item.tweet_text, item.tweet_id, user_poster, ok, item.favorites, item.retweets)

		cur.execute(statement, some_tuple)






# I wanted to know that if the users had more favoirted tweets than there tweets favoirted
statement = "SELECT Tweets.user , Tweets.number_of_favoirted , Users.number_of_favorites From Users INNER Join Tweets on Tweets.user = Users.screen_name Where Users.number_of_favorites > Tweets.number_of_favoirted"

lst_of_tweet_favorited_users = set((x[0], x[1], x[2]) for x in cur.execute(statement).fetchall())


# The Director tweet with the highest tweet retweets 

statement = "SELECT Tweets.tweet_text , Tweets.number_of_retweets , Tweets.search  From Tweets INNER Join Users on Tweets.user = Users.screen_name"
highest_director_retweeted = max(set((x[0], x[1], x[2]) for x in cur.execute(statement).fetchall()), key = lambda x:x[1])


#I want to get all the tweets and group them by each person 

statement = "SELECT Tweets.tweet_text , Tweets.search , Tweets.number_of_retweets  From Movie INNER Join Tweets on Tweets.search = Movie.Director"

lst_temp_default = set((y[0], y[1], y[2]) for y in cur.execute(statement).fetchall())


lst_of_tweets_based_on_directors = set(map(lambda x: x[1] , lst_temp_default))


grouping_lst_tweets = [[(y[0], y[1], y[2]) for y in lst_temp_default if y[1]==x] for x in lst_of_tweets_based_on_directors]


# Sort by highest number of followers in his account

statement = "SELECT * From Users"

lst_of_highest_users = set(sorted(cur.execute(statement), key = lambda x: x[-1] , reverse= True))


########################3
output_file = open("data_access_final_project.txt", "w")

output_file.write("Summary Stats \n")

output_file.write("The Three Movies Title are listed below \n")

for elem in movies_list:
	output_file.write(elem + "\n")

output_file.write("\n")

output_file.write("Users Having more favorites than there tweet being favorited \n")
##########################
output_file.write("(User, Number of favorited, Number of favorites \n")
for elem in lst_of_tweet_favorited_users:
	output_file.write(str(elem) + "\n")

output_file.write("\n")
###########################
output_file.write("The director that had more tweets \n")

output_file.write("Retweets: " + str(highest_director_retweeted[1]) + " Director: " + str(highest_director_retweeted[2]) + "\n")
output_file.write("\n")

###########################


output_file.write("In this table its data based on Twitter users tweeting about the directors of the movies \n")

for elem in grouping_lst_tweets:
	temp_val = elem[0][1]
	output_file.write("Director: " + str(temp_val) +"\n")

	for item in elem:
		output_file.write("Tweet Text: " + str(item[0]) + " Retweets: " + str(item[2]) + "\n")

	output_file.write("======================\n")

output_file.write("\n \n")

#########################

output_file.write("The Twitter Users with highest to lowest followers \n")


for elem in lst_of_highest_users:
	output_file.write("User: " + str(elem[1]) + " Followers: "+str(elem[2])  + "\n")

output_file.close()

conn.commit()
conn.close()

print("*** OUTPUT OF TESTS BELOW THIS LINE ***")
# Testing Twitters Class Methods and Instances
class PartOne(unittest.TestCase):
	# Testing whether the class Twitter.search exists
	def test1(self):

		twitter_class = Twitter()

		class ClassName(object):
			def __init__(self):
				self = 0
		
		self.assertTrue(type(twitter_class) , type(ClassName))

	# Testing if the search method in Twitter Class returns a list
	def test2(self):
		twitter_class = Twitter()

		self.assertTrue(twitter_class.search("Get Out"), type([]))

# Testing Movie Class

class PartTwo(unittest.TestCase):
	# Testing whether the class movie exsits 
	def test1(self):
		movie_class = Movie()

		class ClassName(object):
			def __init__(self):
				self = 0
		
		self.assertTrue(type(movie_class) , type(ClassName))

	# Testing for the movie seach and returns a dictorany contian items
	def test2(self):
		movie_class = Movie()

		self.assertTrue(movie_class.search("Get Out"), type({}))

	# Testing whether the first item is a string type

		movie_class = Movie()

		item = movie_class.search("Get Out")

		self.assertTrue(type(item[1]), type(""))	

	# Making sure that our function in movie returns the string type of it.
	def test3(self):
		movie_class = Movie()

		self.assertTrue(movie_class.__str__(), type(""))

	# Test case is making sure that the data we get is the actual the users
	def test4(self):
		twitter_class = Twitter()

		self.assertEqual(type(twitter_class.get_twitter_users("Get Out is Good Moview")),type({'movierevier', 'search'}))

class PartThree(unittest.TestCase):
		# A function that returns a list of users testing for that
		def test1(self):

			twitter_class = Twitter()

			self.assertTrue(type(twitter_class.return_user()), type([]))
		
		# Returns a list of each movies we searched for and making sure that the data is correct
		def test2(self):
			twitter_class = Twitter()

			self.assertTrue(type(twitter_class.return_user()[1]), type([]))








	






if __name__ == "__main__":
	unittest.main(verbosity=2)
