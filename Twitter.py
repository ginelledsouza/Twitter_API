import tweepy
import requests
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
    twitterid=item.id
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
    
    Data = pd.DataFrame({"User Name":[name],"Twitter ID":[twitterid],"User Handle":[username],"Bio":[description],"Created At":[account_created_date],"Followers":[followers],"Following":[following],
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
    
############# Twitter API v2 [BONUS CONTENT] #############    
    
consumer_key = ""
consumer_secret = ""
bearer_token = ""
access_token = ""
access_token_secret = ""

def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)

    if response.status_code != 200:
        print(response.status_code)
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def user_info(user_id):
    
    fields = "id,created_at,name,username,verified,description,location,protected,profile_image_url,public_metrics"
    params = {"user.fields": fields}

    url =  "https://api.twitter.com/2/users/{}".format(user_id)
    
    json_response = connect_to_endpoint(url, params)

    public_metrics = json_response['data'].pop("public_metrics")
    user_data = json_response['data']

    detailed = {}

    detailed.update(user_data)
    detailed.update(public_metrics)

    detailed = pd.DataFrame(detailed, index=[0])

    return detailed

Data = pd.DataFrame()

for i in UsersData['Twitter ID'].tolist():
    print(UsersData['Twitter ID'].tolist().index(i) + 1)
    Data = Data.append(user_info(i),ignore_index=True)