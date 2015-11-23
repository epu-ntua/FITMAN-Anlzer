def fix_json_en(json_tweet, text_no_url):
    json_to_keep = fix_json_all_languages(json_tweet)
    json_to_keep["text_no_url"] = text_no_url
    return json_to_keep


def fix_json_es(json_tweet, text_no_url):
    json_to_keep = fix_json_all_languages(json_tweet)
    json_to_keep["text_no_url_es"] = text_no_url
    return json_to_keep


def fix_json_all_languages(json_tweet):
    fields_wanted = {"created_at", "text", "lang", "retweet_count", "id", "retweeted", "entities"}
    json_to_keep = {}
    for k in fields_wanted:
        if json_tweet[k]:
            json_to_keep[k] = json_tweet[k]
    user_name = json_tweet["user"]["name"]
    user_name = 'twitter:' + user_name
    json_to_keep["user_name"] = user_name
    user_screen_name = json_tweet["user"]["screen_name"]
    user_screen_name = 'twitter:' + user_screen_name
    json_to_keep["user_screen_name"] = user_screen_name
    json_to_keep["senti_tag"] = "neutral"
    return json_to_keep