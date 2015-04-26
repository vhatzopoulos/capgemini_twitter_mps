import pandas as pd
import twitter
import csv
"""
get tweets with the twitter API
"""

################# set up the API #################

filename = 'twitter_credentials.csv'
f = open(filename,'r')
reader = csv.reader(f)

application_credentials = {}
for line in reader:
  application_credentials[line[0]] = line[1]
  

api = twitter.Api(consumer_key=application_credentials['consumer_key'],\
  consumer_secret=application_credentials['consumer_secret'], \
  access_token_key=application_credentials['access_token_key'],\
   access_token_secret=application_credentials['access_token_secret'])

################# read the conservative and labour mp details #################
conservative_details = pd.read_csv('conservative_mp_twitter_ids.csv')
labour_details = pd.read_csv('labour_mp_twitter_ids.csv')


#test
authorised = 0
non_authorised = 0

for twitter_id in conservative_details['twitter_id']:
  
  try:
    print [s.text for s in api.GetUserTimeline(screen_name=twitter_id)]
    authorised += 1
  except:
    print "not authorised"
    non_authorised += 1