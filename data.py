import pandas as pd
import requests
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.svm import SVC
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn.utils import shuffle
import pylab
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import re
import seaborn
import random
pd.set_option('display.max_columns', 500)
%matplotlib inline

df1 = pd.read_csv('https://raw.githubusercontent.com/Columbia-Intro-Data-Science/python-introduction-lee-jw/master/data.csv')
slugs = df1['slug']
apikey = "INSERT API KEY"
url = "https://api.trackico.io/v1/icos/profile/"

def getInfo(slug):
    proj_url = url + slug + "/?apiKey=" + apikey
    title = requests.get(proj_url).json()["title"]
    slug = requests.get(proj_url).json()["slug"]
    ticker = requests.get(proj_url).json()["ticker"]
    ico_type = requests.get(proj_url).json()["ico_type"]
    platform = requests.get(proj_url).json()["platform"]
    accepted_currencies = requests.get(proj_url).json()["finance"]["accepted_currencies"]
    country = requests.get(proj_url).json()["country"]
    category = requests.get(proj_url).json()["category"]
    rating = requests.get(proj_url).json()["rating"]
    return(title, slug, ticker, ico_type, platform, accepted_currencies, country, category, rating)

def getMisc(slug):
    proj_url = url + slug + "/?apiKey=" + apikey    
    web_url = requests.get(proj_url).json()["url"]
    description = requests.get(proj_url).json()["description"]
    link_bitcointalk = requests.get(proj_url).json()["links"]["bitcointalk"]    
    return(web_url, description, link_bitcointalk)
    
def getDates(slug):
    proj_url = url + slug + "/?apiKey=" + apikey
    pre_ico_start = requests.get(proj_url).json()["pre_ico_start"]
    pre_ico_end = requests.get(proj_url).json()["pre_ico_end"]
    ico_start = requests.get(proj_url).json()["ico_start"]
    ico_end = requests.get(proj_url).json()["ico_end"]
    return(pre_ico_start, pre_ico_end, ico_start, ico_end)
    
def getFinances(slug):
    proj_url = url + slug + "/?apiKey=" + apikey
    token_for_sale = requests.get(proj_url).json()["finance"]["token_for_sale"]
    token_supply = requests.get(proj_url).json()["finance"]["token_supply"]
    soft_cap = requests.get(proj_url).json()["finance"]["soft_cap"]
    soft_cap_currency = requests.get(proj_url).json()["finance"]["soft_cap_currency"]
    hard_cap = requests.get(proj_url).json()["finance"]["hard_cap"]
    hard_cap_currency = requests.get(proj_url).json()["finance"]["hard_cap_currency"]
    token_price_in_usd = requests.get(proj_url).json()["finance"]["token_price_in_usd"]
    total_raised_in_usd = requests.get(proj_url).json()["finance"]["total_raised_in_usd"]
    bonus_available = requests.get(proj_url).json()["finance"]["bonus_available"]
    return(token_for_sale, token_supply, soft_cap, soft_cap_currency, hard_cap, hard_cap_currency, token_price_in_usd, total_raised_in_usd, bonus_available)

def getLegal(slug):
    proj_url = url + slug + "/?apiKey=" + apikey
    whitelist_required = requests.get(proj_url).json()["finance"]["whitelist_required"]
    kyc_required = requests.get(proj_url).json()["finance"]["kyc_required"]
    restricted_countries = requests.get(proj_url).json()["finance"]["restricted_countries"]
    return(whitelist_required, kyc_required, restricted_countries)
    
def getInterests(slug):
    proj_url = url + slug + "/?apiKey=" + apikey    
    alexa_global_rank = requests.get(proj_url).json()["interest"]["alexa_global_rank"]
    twitter_participants = requests.get(proj_url).json()["interest"]["twitter_participants"]
    telegram_members = requests.get(proj_url).json()["interest"]["telegram_members"]
    video_views = requests.get(proj_url).json()["interest"]["video_views"]
    return(alexa_global_rank, twitter_participants, telegram_members, video_views)

def getPrice(slug):
    list_url = "https://api.coinmarketcap.com/v2/listings/"
    ticker = getInfo(slug)[1]
    price_data = requests.get(list_url).json()["data"]
    for i in range(len(price_data)-1):
        if price_data[i]['symbol'] == ticker: idx = price_data[i]['id']
    proj_url = "https://api.coinmarketcap.com/v2/ticker/" + str(idx)
    price = requests.get(proj_url).json()["data"]["quotes"]["price"] # can get circ/total/max supplies if needed
    return(price)
    
df = pd.DataFrame(columns = list(['title','slug','ticker','ico_type','platform','accepted_currencies','country','category','rating','token_for_sale','token_supply','soft_cap','soft_cap_currency','hard_cap','hard_cap_currency','token_price_in_usd','total_raised_in_usd','bonus_available','whitelist_required','kyc_required','restricted_countries','alexa_global_rank','twitter_participants','telegram_members','video_views']))
df_y = pd.DataFrame(colums = list(['current_price', 'ROI'])
for slug in slugs:
    df = df.append({'title': getInfo(slug)[0], 'slug': getInfo(slug)[1], 'ticker': getInfo(slug)[2], 'ico_type': getInfo(slug)[3], 'platform': getInfo(slug)[4], 'accepted_currencies': getInfo(slug)[5], 'country': getInfo(slug)[6], 'category': getInfo(slug)[7], 'rating': getInfo(slug)[8], 'token_for_sale': getFinances(slug)[0], 'token_supply': getFinances(slug)[1], 'soft_cap': getFinances(slug)[2], 'soft_cap_currency': getFinances(slug)[3], 'hard_cap': getFinances(slug)[4], 'hard_cap_currency': getFinances(slug)[5], 'token_price_in_usd': getFinances(slug)[6], 'total_raised_in_usd': getFinances(slug)[7], 'bonus_available': getFinances(slug)[8], 'whitelist_required': getLegal(slug)[0], 'kyc_required': getLegal(slug)[1], 'restricted_countries': getLegal(slug)[2], 'alexa_global_rank': getInterests(slug)[0], 'twitter_participants': getInterests(slug)[1], 'telegram_members': getInterests(slug)[2], 'video_views': getInterests(slug)[3]}, ignore_index=True)
    df_y = df.append({'current_price': getPrice(slug), 'ROI': getPrice(slug)/getFinances(slug)[6]}, ignore_index=True)
df.head()
df_y.head()
df.to_csv('data_masterlist.csv')