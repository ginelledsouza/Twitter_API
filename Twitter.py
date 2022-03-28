import tweepy
import pandas as pd
from datetime import datetime

#TWITTER CREDENTIAL
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

Users = ["Twitter","YouTube","Meta","Snapchat","WhatsApp","Instagram","TikTok",
         "Reddit","Pinterest","LinkedIn","Flickr","Quora","Vimeo","Medium","Viber","Spotify",
         "TRILLER","Houseparty","Caffeine","Tinder","GitHub"]

UsersData = pd.DataFrame()

def get_all_tweets(screen_name):

    alltweets = []  
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    alltweets.extend(new_tweets)
    
    usertweets = [tweet.text for tweet in alltweets]
    usertweetscreated = [tweet.created_at for tweet in alltweets]

    target=screen_name
    item = api.get_user(target)
    
    name=item.name
    username=item.screen_name
    description=item.description
    tweets=int(item.statuses_count)
    following=int(item.friends_count)
    followers=int(item.followers_count)
    
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    
    account_age=int(account_age_days)
    
    avg_tweets=0
    if account_age_days > 0:
        avg_tweets="%.2f"%(float(tweets)/float(account_age_days))
    
    Data = pd.DataFrame({"User Name":[name],"User Handle":[username],"Bio":[description],"Created At":[account_created_date],"Followers":[followers],"Following":[following],
                         "Account Age":[account_age],"Average Tweets":[avg_tweets],"Tweets":[usertweets],"Tweets Created":[usertweetscreated]})

    return Data

for i in Users:
    print(i)
    Data = get_all_tweets(i)
    UsersData = UsersData.append(Data,ignore_index=True)
    
for i in range(len(UsersData)):
    if len(UsersData["Tweets"][i]) != 200:
        
        additional = 200 - len(UsersData["Tweets"][i])
        
        additionaltweet = UsersData["Tweets"][i] + ([""]*additional)
        additionaltime = UsersData["Tweets Created"][i] + ([""]*additional)
        
        UsersData["Tweets"].loc[i] = additionaltweet
        UsersData["Tweets Created"].loc[i] = additionaltime
        
Tweets = pd.DataFrame()

for i in range(len(UsersData)):
    Message = UsersData["Tweets"][i]
    Timestamp = UsersData["Tweets Created"][i]
    
    Tweets.insert(Tweets.shape[1],UsersData["User Name"][i],Message) 
    Tweets.insert(Tweets.shape[1],str(UsersData["User Name"][i])+str(" Tweet Timestamp"),Timestamp)
    
with pd.ExcelWriter("Output/Twitter.xlsx") as writer:
    UsersData.to_excel(writer, sheet_name='Users Data', index=False)
    Tweets.to_excel(writer, sheet_name='Tweets', index=False) 
    
############# Twitter User Data using User Access Token [BONUS CONTENT] #############    
    
from requests_oauthlib import OAuth1Session
import json

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

fields = "id,created_at,name,username,verified,description,location,protected,profile_image_url,public_metrics"
params = {"user.fields": fields}

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

response = oauth.get("https://api.twitter.com/2/users/me", params=params)

if response.status_code != 200:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

json_response = response.json()

print(json.dumps(json_response, indent=4, sort_keys=True))

tid = [json_response["data"]["id"]]
created_at = [json_response["data"]["created_at"]]
name = [json_response["data"]["name"]]
username = [json_response["data"]["username"]]
verified = [json_response["data"]["verified"]]
description = [json_response["data"]["description"]]
protected = [json_response["data"]["protected"]]
profile_image_url = [json_response["data"]["profile_image_url"]]
followers = [json_response["data"]["public_metrics"]["followers_count"]]
following_count = [json_response["data"]["public_metrics"]["following_count"]]
tweet_count = [json_response["data"]["public_metrics"]["tweet_count"]]

Twitter_Personal = pd.DataFrame({"Twitter ID":tid,"Created At":created_at,"Name":name,
                                "Username":username,"Verified":verified,"Description":description,
                                "Protected":protected,"Profile Image":profile_image_url,
                                "Followers":followers,"Following":following_count,
                                "Tweet":tweet_count})