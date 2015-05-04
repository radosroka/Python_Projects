#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import codecs
import urllib2
import sys
import os.path
import cPickle as pickle
from tweet import Tweet

consumer_key = "L2XvpFvzu9WSzyRNHt6K5Cjs3"
consumer_secret = "mhxiJhjjOCdSVxdW3PqPQMUmD4gdKRqosyUPH91bypN6X7mgNt"

access_token = "338698488-lOPYlMxpWi7DGrYlHqejBXFLOXiBuFWG6xNIpbNP"
access_token_secret = "qFQuuLjxtIdDUK2nLZxInYNcGBFGg0HRLUIATyXaW0DlV"

MAX_COUNT = 50

def init_mode():

	global MAX_COUNT
	global consumer_key
	global consumer_secret
	global access_token
	global access_token_secret

	if not os.path.exists("./urls"):
		os.system("mkdir urls")	

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	tiff = []
	tiff = api.user_timeline(screen_name = "TiffanyAlvord", count = MAX_COUNT)

	tweets = []

	for t in tiff:
		urls = {}
		index = 0
		for x in t.entities["urls"]:
			html = urllib2.urlopen(x["expanded_url"])
			urls[index] = [x["url"], x["expanded_url"]]
			page = open("urls/" + str(t.id) + "-" + str(index) + ".html", "w")
			page.write(html.read())
			page.close()
			index += 1

		text = t.text
		text = text.replace('\n', '\\n')

		tweet = Tweet(t.id, t.user.name, t.user.id, text, t.created_at, urls)
		tweets.append(tweet)
	records = codecs.open("tweets", "w", encoding="utf-8")

	for t in tweets:
		t.write_to_file(records)
	records.close()



def update_mode():

	global MAX_COUNT
	global consumer_key
	global consumer_secret
	global access_token
	global access_token_secret

	if not os.path.exists("./tweets") or not os.path.exists("./urls"):
		sys.stderr.write("First must call init\n")
		exit(1)

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	records = codecs.open("tweets", "r", encoding="utf-8")

	tweets = []

	for line in records:
		tweet = Tweet.fill_from_line(line)
		if not tweet:
			sys.stderr.write("bad tweets file\n")
			print line
			exit(1)
		tweets.append(tweet)

	records.close()

	tiff = []
	tiff = api.user_timeline(screen_name = "TiffanyAlvord", since_id = int(tweets[0].id))

	for t in tiff:
		urls = {}
		index = 0
		for x in t.entities["urls"]:
			html = urllib2.urlopen(x["expanded_url"])
			urls[index] = [x["url"], x["expanded_url"]]
			page = open("urls/" + str(t.id) + "-" + str(index) + ".html", "w")
			page.write(html.read())
			page.close()
			index += 1

		text = t.text
		text = text.replace('\n', '\\n')

		tweet = Tweet(t.id, t.user.name, t.user.id, text, t.created_at, urls)
		tweets.append(tweet)

	tweets = sorted(tweets, reverse = True, key = lambda Tweet: Tweet.id)

	old_tweets = tweets[MAX_COUNT:]
	
	for t in old_tweets:
		if len(t.urls) > 0:
			os.system("rm ./urls/" + str(t.id) + "*")
		tweets.remove(t)	

	records = codecs.open("tweets", "w", encoding="utf-8")
	for t in tweets:
		t.write_to_file(records)
	records.close()

def clean():
	os.system("rm -rf ./urls")
	os.system("rm tweets")

def main():

	global MAX_COUNT

	if len(sys.argv) is 1:
		sys.stderr.write("Bad parameters\n")
		exit(1)

	elif len(sys.argv) in [2, 3]:
		if len(sys.argv) is 2 and sys.argv[1] == "clean":
			clean()
			exit(0)

		if len(sys.argv) is 3:
			MAX_COUNT = int(sys.argv[2])

		if sys.argv[1] == "init":
			init_mode()
			exit(0)

		if sys.argv[1] == "update":
			update_mode()
			exit(0)
		else:
			sys.stderr.write("Bad parameters\n")
			exit(1)
	else:
		sys.stderr.write("Bad parameters\n")
		exit(1)


main()