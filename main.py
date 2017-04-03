#!/usr/bin/python
from twython import Twython
import random
import markovify
from ConfigParser import SafeConfigParser

class User():
	def __init__(self, app_key, app_secret, oauth_token, oauth_secret):
		"""Initializes the app usage: User(app_key, app_secret, oauth_token, oauth_secret)"""
		self.app_key = app_key
		self.app_secret = app_secret
		self.oauth_token = oauth_token
		self.oauth_secret = oauth_secret
		self.twitter = self.Authenticate()
		self.followers = len(self.twitter.get_friends_ids(screen_name="HPNovels")['ids'])
	def Authenticate(self):
		"""Logs into Twitter using app_key, app_secret and oauth tokens"""
		#Login to Twitter
		t = Twython(self.app_key, self.app_secret, self.oauth_token, self.oauth_secret)
		return t

	def followPeople(self):
		"""Follows random people from one of these accounts"""
		people = ["realDonaldTrump", "itsHarryPotter", "ArryPottah","PotterWorldUK","celinedion","ProgrammerWorld"]
		myFollowers = self.twitter.get_followers_list(screen_name=random.choice(people),count=40)
		allFollowers = []
		for user in myFollowers['users']:
			allFollowers.append(user['screen_name'])


		randChoice = random.choice(allFollowers)
		userFollowers = self.twitter.get_followers_list(screen_name=randChoice, count=25)
		for user in userFollowers['users']:
			try:
				self.twitter.create_friendship(screen_name=user['screen_name'])
#				print (user['screen_name'])
			except:
				print ("Failure")
				continue

	def createSentence(self):
		"""Uses markovify library to create a tweet (140 characters) from the first four Harry Potter books"""
		corpus = ['Harry1','Harry2', 'Harry3', 'Harry4']
		models = []
		for source in corpus:
			with open("/home/tom/MarkovChain/" + source + ".doc") as f:
				text = f.read()

			text_model = markovify.Text(text, state_size=3)
			models.append(text_model)

		model_combo = markovify.combine(models)

		return (model_combo.make_short_sentence(140))

	def sendTweet(self):
		"""Uses the Twython Library to tweet from user's account"""
		tweet = self.createSentence()
		self.twitter.update_status(status=tweet)

	def unfollow(self):
		"""Unfollows users using Twython"""
		x = 0
		for id in self.twitter.get_friends_ids(screen_name="HPNovels")['ids']:
#			print id
			try:
				self.twitter.destroy_friendship(user_id=id)
				if x >= 50:
					return
				x += 1
			except:
				continue


if __name__ == '__main__':
	parser = SafeConfigParser()
	parser.read("config.ini")
	consumer_key = parser.get("twitter", "CONSUMER_KEY")
	consumer_token = parser.get("twitter", "CONSUMER_TOKEN")
	access_key = parser.get("twitter", "ACCESS_KEY")
	access_token = parser.get("twitter", "ACCESS_TOKEN")

	Tom = User(consumer_key, consumer_token, access_key, access_token) #Authenticates my account
	if Tom.followers >= 200:
		Tom.unfollow() #If my account is following over 200 people, start unfollowing users
	else:
		Tom.followPeople() #If my account is not following over 200 people, start following users
	Tom.sendTweet() #Tweets sentence
