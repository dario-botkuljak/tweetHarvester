from twarc.client2 import Twarc2
import constants

class TweetCredentials():
    def __init__(self, bearer_token='', access_token='', access_token_secret=''):
        """
        Class that holds Twitter credentials for search
        :param bearer_token:
        :param access_token:
        :param access_token_secret:
        """
        self.bearer_token = bearer_token
        self.access_token = access_token
        self.access_token_secret = access_token_secret

class TweetSummary():
    def __init__(self):
        pass

class SearchResult():
    def __init__(self):
        self.result_data = []
        self.result_tweets = []
        self.result_users = []
        self.tweet_summary = TweetSummary()

        self.author_id = ''  # Tweet Account ID, numeric field
        self.username = ''  # Tweet Account name, string field
        self.name = ''  # Tweed Account full name, string field
        self.id = ''  # Tweed ID, numeric field
        self.text = ''  # Tweet text, string field
        self.location = ''  # Tweet Account location name, string
        self.created_at = ''  # Tweet date, string format YYYY-MM-DDT24HH:MIN:SEC.000Z

    def __str__(self):
        """overloads built-in str function"""
        retval = 'ID: ' + self.id + ' username: ' + self.username + ' created at: ' + self.created_at \
            + ' text: ' + self.text
        return retval

    def getCreatedAtDate(self):
        if len(len(self.created_at) > 0):
            return 'found'
        else:
            return None


class Search():

    def __init__(self, author='', conversation_id='',
                 created_at_str='',
                 tweet_id='',
                 tweet_text='',
                 includes_user_id='',
                 includes_username='',
                 includes_profile_id='',
                 includes_created_at=''):

        #self.tweet_dict = {}
        self.author = author
        self.conversation_id = conversation_id
        self.created_at_str = created_at_str
        self.tweet_id = tweet_id
        self.tweet_text = tweet_text

        self.includes_user_id = includes_user_id
        self.includes_username = includes_username
        self.includes_profile_id = includes_profile_id
        self.includes_created_at = includes_created_at
        self.credentials = TweetCredentials()
        self.created_at = ''
        # self.start_time = datetime.datetime(2022, 6, 21, 0, 0, 0, 0, datetime.timezone.utc)
        # self.end_time = datetime.datetime(2022, 6, 25, 0, 0, 0, 0, datetime.timezone.utc)
        # self.created_at = datetime.strptime(self.created_at_str, '')

    def search_tweets(self, credentials: TweetCredentials, search_term: str,
                      result_limit=constants.TwitterAPIAccess.MAX_RESULTS) -> list:
        """performs actual search
        :param credentials: object containing credentials to access Twitter api
        :param search_term: text that is being searched
        :param result_limit: limited for this credentials
        """
        retval = []
        try:
            self.credentials = credentials
            if search_term is None:
                return

            self.twarc = Twarc2(bearer_token=self.credentials.bearer_token,
                                consumer_key=self.credentials.access_token,
                                consumer_secret=self.credentials.access_token_secret, metadata=True)
            search_results = self.twarc.search_recent(query=search_term, max_results=10)
            passed = False
            for iteration in search_results:
                if passed == False:
                    result_data = iteration['data']
                    # pprint(self.data)
                    self.includes = iteration['includes']

                    #pprint(self.includes)

                    count = 0
                    for xx in result_data:
                        temp_result = SearchResult()
                        temp_result.author_id = xx['author_id']
                        temp_result.id = xx['id']
                        temp_result.text = xx['text']
                        temp_result.username = self.includes['users'][count]['username']
                        try:
                            temp_result.location = self.includes['users'][count]['location']
                        except:
                            pass
                        print(temp_result)
                        retval.append(temp_result)
                        count += 1
                    self.author = self.data[0]['author_id']
                    self.conversation_id = self.data[0]['conversation_id']
                    self.created_at = self.data[0]['created_at']
                    #print(type(self.created_at))
                    #self.twit_id = self.data[0]['id']
                    #self.tweet_text = self.data[0]['text']
                    #self.includes_user_id = self.includes['users'][0]['name']
                    #self.includes_profile_id = self.includes['users'][0]['id']
                    #self.includes_username = self.includes['users'][0]['username']
                    #self.includes_created_at = self.includes['users'][0]['created_at']
                    passed = True
        except BaseException as err:
            retval.append(f"Unexpected {err=}, {type(err)=}")
            print(f"Unexpected {err=}, {type(err)=}")
        return retval