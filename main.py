import requests
import tweetSearch
from flask import Flask, request
import logging
import logging.config
import constants

api_url = ""
port = 5100
app = Flask(__name__)

def create_headers(bearer_token):
    search_term = 'Djokovic'
    query_params = {'query': search_term, 'space.fields': 'title,created_at', 'expansions': 'creator_id'}
    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
        "User-Agent": "v2SpacesSearchPython"
    }
    return headers

def connect_to_endpoint(url, headers, params):
    search_url='ss'
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def search(search_string: str) -> list:
    """
      Entry point
      :return:
      """
    if search_string is None:
        search_string = "Andric"

    credentials = tweetSearch.TweetCredentials(constants.TwitterAPIAccess.BEARER_TOKEN,
                                               constants.TwitterAPIAccess.ACCESS_TOKEN,
                                               constants.TwitterAPIAccess.ACCESS_TOKEN_SECRET)
    searchtweets = tweetSearch.Search()
    credentials.bearer_token = constants.TwitterAPIAccess.BEARER_TOKEN
    credentials.access_token = constants.TwitterAPIAccess.ACCESS_TOKEN
    credentials.access_token_secret = constants.TwitterAPIAccess.ACCESS_TOKEN_SECRET
    rezultati = []
    rezultati = searchtweets.search_tweets(credentials, search_string, constants.TwitterAPIAccess.MAX_RESULTS)
    return rezultati

@app.get("/tweet_id")
def get_tweet_id():
    #return jsonify(countries)
    html_text = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><title>Some Title</title></head><body>" \
                "<form>Please enter search string:</br><input name=\"input_string\" maxlength=\"50\"></input>" \
                "</br><button type=\"submit\">click</button></form>$$1</body></html>"
    res = []
    search_text = request.args.get("input_string")
    if search_text is None:
        search_text = ""
    else:
        res = search(search_text)
    text2 = html_text.replace("$$1", search_text) + "duzina: " + str(len(res))
    for text in res:
        text2=text2 + "</br>" + text2

    text2+= "/<br>"

    return text2

if __name__ == '__main__':
    rezultati = search("Sanader")



