import os
import re
import json
import mimetypes
import requests
import urllib.parse
import platform
import platformdirs
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class API:
    def __init__(self):
        open('log.txt', "w+")
        self.bearer_token = ""
        self.notification_url = ""
        self.queryIds = {}
        self.initial_notification_data = None
        self.media_endpoint_url = "https://upload.twitter.com/i/media/upload.json"
        self.graphql_endpoint_url = "https://twitter.com/i/api/graphql/"
        self.session = requests.Session()
        os_name = platform.system()
        if os_name == 'Darwin':
            self.service = Service()
            self.log("This is macOS (Mac).")
        elif os_name == 'Windows':
            self.service = Service(r"C:\chromedriver.exe")
            self.log("This is Windows.")
        else:
            self.service = Service()
            self.log("This is a different operating system.")
    
    def log(self, *msg):
        with open('log.txt', 'a') as log:
            log.write('[{:%d/%m/%Y - %H:%M:%S}]  {}\n'.format(datetime.now(), *msg))
            print('[{:%d/%m/%Y - %H:%M:%S}]  {}'.format(datetime.now(), *msg))

    def login(self, auto=True, name="temp"):
        options = Options()
        options.add_argument("--user-data-dir=" + platformdirs.user_data_dir(name))
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-notifications")
        #options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(service=self.service, options=options)
        if auto:
            self.log("Login in automatically on browser.")
            browser.get("https://twitter.com/notifications")
        else:
            browser.get("https://twitter.com")
            self.log("Login in manually on browser.")
            input("Press Enter to continue...")
            browser.get("https://twitter.com/notifications")
        sleep(10) #neccessary on some system to chill here for a bit
        logs = browser.get_log('performance')
        for log in logs:
            log_entry = json.loads(log['message'])['message']
            if 'Network.requestWillBeSent' in log_entry['method']:
                if 'params' in log_entry and 'request' in log_entry['params']:
                    request_data = log_entry['params']['request']
                    url = request_data['url']
                    if "https://abs.twimg.com/responsive-web/client-web/main" in url.lower() or "https://abs.twimg.com/responsive-web/client-web-legacy/main" in url.lower():
                        mainjs = self.session.get(url).text
                        self.bearer_token = re.findall(r'AAAAAAAAA[^"]+', mainjs)[0]
                        operations = re.findall('\{queryId:"[a-zA-Z0-9_]+[^\}]+"', mainjs)
                        for operation in operations:
                            pattern = r'queryId:"(.*?)",operationName:"(.*?)"'
                            match = re.search(pattern, operation)
                            if match:
                                query_id = match.group(1)
                                operation_name = match.group(2)
                                self.queryIds[operation_name] = query_id
                    if "https://twitter.com/i/api/2/notifications/all.json" in url.lower():
                        self.notification_url = url
                        cookies = requests.cookies.RequestsCookieJar()
                        for c in browser.get_cookies():
                            cookies.set(c["name"], c["value"])
                        self.session.headers.update(request_data['headers'])
                        self.session.cookies.update(cookies)
                        self.log("Twitter Session Snatch Success!\n")
                        browser.quit()
        assert self.session.headers is not None, "Session Acquisition Failed!"

    def getTweetID(self, url):
        tweet_id = re.findall(r'(?<=status/)\d+', url)
        assert tweet_id is not None and len(tweet_id) == 1, f'Could not parse tweet id from tweet url: {url}'
        tweet_id = tweet_id[0]
        return tweet_id
    
    def getNotifications(self, since_id):
        tweets = []
        response = self.session.get(self.notification_url)
        if response.status_code == 200:
            data = response.json()
            if "tweets" in data['globalObjects']:
                tweet_data = data['globalObjects']['tweets']
                alltweets = sorted(tweet_data.keys())
                for thing in alltweets:
                    tweet = tweet_data[thing]
                    tid = int(tweet["id_str"])
                    if since_id < tid:
                        since_id = tid
                        tweets.append(tweet)
            else:
                self.log("No new data")
            #updating endpoint url before next query
            for index, instruction in enumerate(data["timeline"]["instructions"]):
                if "addEntries" in instruction:
                    new_cursor_value = data["timeline"]["instructions"][index]["addEntries"]["entries"][0]["content"]["operation"]["cursor"]["value"]
                    parsed_url = urlparse(self.notification_url)
                    query_parameters = parse_qs(parsed_url.query)
                    query_parameters["cursor"] = [new_cursor_value]
                    if "requestContext" in query_parameters:
                        del query_parameters["requestContext"]
                    encoded_query_parameters = urlencode(query_parameters, doseq=True)
                    self.notification_url = urlunparse(parsed_url._replace(query=encoded_query_parameters))
                    break
        else:
            self.log(f"Failed to get latest notifications: {response.status_code}")
            self.log(response.text)
        return tweets, since_id

    def createTweet(self, text="", in_reply_to_tweet_id=None, media=[], attachment_url=None):
        mode = "CreateTweet"
        data = {
            "variables": {
                "tweet_text": text,
                "dark_request": False,
                "semantic_annotation_ids": []
            },
            "features": {
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": False,
                "tweet_awards_web_tipping_enabled": False,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "responsive_web_media_download_video_enabled": False,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_enhance_cards_enabled": False,
                "rweb_video_timestamps_enabled": False
            },
            "fieldToggles": {
                "withArticleRichContentState": False,
                "withAuxiliaryUserLabels": False
            },
            "queryId": self.queryIds[mode]
        }
        # if it is a reply to a tweet
        if in_reply_to_tweet_id:
            data["variables"]["reply"] = {
                "in_reply_to_tweet_id": in_reply_to_tweet_id,
                "exclude_reply_user_ids": []
            }
        # if it contains any media
        if len(media):
            ct = 0
            media_entities = []
            for medium in media:
                if ct > 3: # break loop for twitter 4 media limit
                    break
                else:
                    media_entities.append({
                        "media_id": medium,
                        "tagged_users": []
                    })
                    ct+=1
            data["variables"]["media"] = {
                "media_entities": media_entities,
                "possibly_sensitive": False
            }
        # if it is a quote tweet
        if attachment_url:
            data["variables"]["attachment_url"] = attachment_url
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def deleteTweet(self, tweetid):
        mode = "DeleteTweet"
        data = {
            "variables": {
                "tweet_id": tweetid,
                "dark_request": False,
            },
            "queryId": self.queryIds[mode]
        }
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def readTweet(self, tweet_id):
        if self.queryIds["TweetResultByRestId"] is not None:
            mode = "TweetResultByRestId"
        elif self.queryIds["TweetDetail"] is not None:
            mode = "TweetDetail"
        else:
            self.log("Tweet Reader N/A")
            return
        features = {
            "features": {
                "rweb_lists_timeline_redesign_enabled":True,
                "responsive_web_graphql_exclude_directive_enabled":True,
                "verified_phone_label_enabled":False,
                "creator_subscriptions_tweet_preview_api_enabled":True,
                "responsive_web_graphql_timeline_navigation_enabled":True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,
                "tweetypie_unmention_optimization_enabled":True,
                "responsive_web_edit_tweet_api_enabled":True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,
                "view_counts_everywhere_api_enabled":True,
                "longform_notetweets_consumption_enabled":True,
                "responsive_web_twitter_article_tweet_consumption_enabled":False,
                "tweet_awards_web_tipping_enabled":False,
                "freedom_of_speech_not_reach_fetch_enabled":True,
                "standardized_nudges_misinfo":True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":True,
                "longform_notetweets_rich_text_read_enabled":True,
                "longform_notetweets_inline_media_enabled":True,
                "responsive_web_media_download_video_enabled":False,
                "responsive_web_enhance_cards_enabled":False,
                "rweb_video_timestamps_enabled": False
            }
        }
        variables = {
            "variables":{
                "focalTweetId":tweet_id,
                "tweetId":tweet_id,
                "with_rux_injections":False,
                "includePromotedContent":True,
                "withCommunity":True,
                "withQuickPromoteEligibilityTweetFields":True,
                "withBirdwatchNotes":True,
                "withVoice":True,
                "withV2Timeline":True
            }
        }
        fieldToggles = {
            "fieldToggles": {
                "withAuxiliaryUserLabels":False,
                "withArticleRichContentState":False
            }
        }
        url = f"{self.graphql_endpoint_url}/{self.queryIds[mode]}/{mode}?variables={urllib.parse.quote(json.dumps(variables))}&features={urllib.parse.quote(json.dumps(features))}&fieldToggles={urllib.parse.quote(json.dumps(fieldToggles))}"
        tweet = self.session.get(url)
        max_retries = 5
        cur_retry = 0
        while tweet.status_code == 400 and cur_retry < max_retries:
            self.log("Retrying...")
            tweet = self.session.get(url)
            cur_retry += 1
        assert tweet.status_code == 200, f'Failed to get tweet details. Status code: {tweet.status_code}. Tweet ID: {tweet_id}'
        return tweet

    def likeTweet(self, tweetid):
        mode = "FavoriteTweet"
        data = {
            "variables": {
                "tweet_id": tweetid,
            },
            "queryId": self.queryIds[mode]
        }
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def unlikeTweet(self, tweetid):
        mode = "UnfavoriteTweet"
        data = {
            "variables": {
                "tweet_id": tweetid,
            },
            "queryId": self.queryIds[mode]
        }
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def follow(self, userid):
        mode = "Follow"
        data = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'user_id': userid
        }
        response = self.session.post("https://twitter.com/i/api/1.1/friendships/create.json", data=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def unfollow(self, userid):
        mode = "Unfollow"
        data = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'user_id': userid
        }
        response = self.session.post("https://twitter.com/i/api/1.1/friendships/destroy.json", data=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def createRetweet(self, tweetid):
        mode = "CreateRetweet"
        data = {
            "variables": {
                "tweet_id": tweetid,
                "dark_request": False,
            },
            "queryId": self.queryIds[mode]
        }
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def deleteRetweet(self, tweetid):
        mode = "DeleteRetweet"
        data = {
            "variables": {
                "tweet_id": tweetid,
                "dark_request": False,
            },
            "queryId": self.queryIds[mode]
        }
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def createBookmark(self, tweetid):
        mode = "CreateBookmark"
        data = {
            "variables": {
                "tweet_id": tweetid,
            },
            "queryId": self.queryIds[mode]
        }
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def deleteBookmark(self, tweetid):
        mode = "DeleteBookmark"
        data = {
            "variables": {
                "tweet_id": tweetid,
            },
            "queryId": self.queryIds[mode]
        }
        response = self.session.post(self.graphql_endpoint_url+self.queryIds[mode]+"/"+mode, json=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response

    def pinTweet(self, tweetid):
        mode = "PinTweet"
        data = {
            'tweet_mode': 'extended',
            'id': tweetid
        }
        response = self.session.post("https://api.twitter.com/1.1/account/pin_tweet.json", data=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def unpinTweet(self, tweetid):
        mode = "UnpinTweet"
        data = {
            'tweet_mode': 'extended',
            'id': tweetid
        }
        response = self.session.post("https://api.twitter.com/1.1/account/unpin_tweet.json", data=data)
        if response.status_code == 200:
            self.log(mode+" Success")
        else:
            self.log(mode+" Fail: "+str(response.status_code))
            self.log(mode+" Error Info: "+str(response.text))
        return response
    
    def createMedia(self, media, media_category):#media_category=tweet_image,tweet_video
        total_bytes = os.path.getsize(media)
        mimetype = mimetypes.guess_type(media)[0]
        assert mimetype, "Could not generate media mimetype:"
        #INIT
        self.log('INIT')
        init_data = {
            'command': 'INIT',
            'media_type': mimetype,
            'total_bytes': total_bytes,
            'media_category': media_category
        }
        init = self.session.post(self.media_endpoint_url, data=init_data).json()
        media_id = init['media_id_string']
        self.log('Media ID: %s' % str(media_id))
        #APPEND
        segment_id = 0
        bytes_sent = 0
        file = open(media, 'rb')
        while bytes_sent < total_bytes:
            chunk = file.read(4*1024*1024)
            self.log('APPEND')
            append_data = {
                'command': 'APPEND',
                'media_id': media_id,
                'segment_index': segment_id
            }
            files = {
                'media':chunk
            }
            append = self.session.post(self.media_endpoint_url, data=append_data, files=files)
            if append.status_code < 200 or append.status_code > 299:
                self.log(append.status_code)
            segment_id = segment_id + 1
            bytes_sent = file.tell()
            self.log('%s of %s bytes uploaded' % (str(bytes_sent), str(total_bytes)))
        self.log('Upload chunks complete')
        #FINALIZE
        self.log('FINALIZE')
        finalize_data = {
            'command': 'FINALIZE',
            'media_id': media_id
        }
        if media_category == "tweet_video":
            finalize_data["allow_async"] =  True

        finalize = self.session.post(self.media_endpoint_url, data=finalize_data).json()
        processing_info = finalize.get('processing_info', None)
        self.checkMediaStatus(media_id, processing_info)
        return media_id
            
    def checkMediaStatus(self, media_id, processing_info):
        if processing_info is None:
            return
        state = processing_info['state']
        self.log('Media processing status is %s ' % state)
        if state == u'succeeded':
            return
        if state == u'failed':
            self.log('Media processing %s ' % state)
        check_after_secs = processing_info['check_after_secs']
        self.log('Checking after %s seconds' % str(check_after_secs))
        sleep(check_after_secs)
        self.log('STATUS')
        status_params = {
            'command': 'STATUS',
            'media_id': media_id
        }
        req = self.session.get(self.media_endpoint_url, params=status_params)
        processing_info = req.json().get('processing_info', None)
        self.checkMediaStatus(media_id, processing_info)