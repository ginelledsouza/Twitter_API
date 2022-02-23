import tweepy
import pandas as pd

#TWITTER CREDENTIAL
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

Users = ["Twitter","YouTube","Meta","Snapchat"]

name = []
username = []
description = []
status = []
following = []
followers = []

for i in Users:
    print(i)

    item = api.get_user(i)
    
    name.append(item.name)
    username.append(item.screen_name)
    description.append(item.description)
    status.append(int(item.statuses_count))
    following.append(int(item.friends_count))
    followers.append(int(item.followers_count))
    

Users = pd.DataFrame({"Name":name,"Twitter Handle":username,"Bio":description,
                      "Tweets":status,"Following":following,"Followers":followers})