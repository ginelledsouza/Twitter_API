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

Users = ["Twitter","YouTube","Meta","Snapchat"]

UsersData = pd.DataFrame()

def get_all_tweets(screen_name):

    alltweets = []  
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    alltweets.extend(new_tweets)
    
    usertweets = [tweet.text for tweet in alltweets]

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
    
    Data = pd.DataFrame({"User Name":[name],"User Handle":[username],"Bio":[description],"Followers":[followers],"Following":[following],
                         "Account Age":[account_age],"Average Tweets":[avg_tweets],"Tweets":[usertweets]})

    return Data

for i in Users:
    print(i)
    Data = get_all_tweets(i)
    UsersData = UsersData.append(Data,ignore_index=True)
    
Tweets = pd.DataFrame()

for i in range(len(UsersData)):
    Message = UsersData["Tweets"][i]
    Tweets.insert(Tweets.shape[1],UsersData["User Name"][i],Message) 
    
with pd.ExcelWriter("Output/Twitter.xlsx") as writer:
    UsersData.to_excel(writer, sheet_name='Users Data', index=False)
    Tweets.to_excel(writer, sheet_name='Tweets', index=False) 