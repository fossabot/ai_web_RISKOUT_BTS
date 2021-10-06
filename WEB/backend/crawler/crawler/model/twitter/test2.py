import twitter

twitter_consumer_key = ""
twitter_consumer_secret = ""
twitter_access_token = ""
twitter_access_secret = ""
BEARER_TOKEN = ''

twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret, 
                          access_token_key=twitter_access_token, 
                          access_token_secret=twitter_access_secret)

query = "코로나"
statuses = twitter_api.GetSearch(term=query, count=100, until="2021_10_01", since="2021_10_05")
for status in statuses:
    print(status.text)
