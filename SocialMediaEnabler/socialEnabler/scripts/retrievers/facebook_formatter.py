import datetime

def parse_comment_en(page_name, comment, clean_text):
    json_to_keep = fix_json_format_en("FB_CMT " + clean_text, comment['created_time'],
                                   page_name + ":" + comment['from']['name'], comment['id'])
    return json_to_keep

def parse_comment_es(page_name, comment, clean_text):
    json_to_keep = fix_json_format_es("FB_CMT " + clean_text, comment['created_time'],
                                   page_name + ":" + comment['from']['name'], comment['id'])
    return json_to_keep


def parse_post_en(page_name, message, clean_text):
    json_to_keep = fix_json_format_en(clean_text, message['created_time'],
                                   page_name + ":" + message['from']['name'], message['id'])
    if 'full_picture' in message:
        json_to_keep["entities"] = {"media": [{"media_url_https": message['full_picture']}]}
    return json_to_keep

def parse_post_es(page_name, message, clean_text):
    json_to_keep = fix_json_format_es(clean_text, message['created_time'],
                                   page_name + ":" + message['from']['name'], message['id'])
    if 'full_picture' in message:
        json_to_keep["entities"] = {"media": [{"media_url_https": message['full_picture']}]}
    return json_to_keep


def fix_json_format_en(text, date, username, pid):
    username = "facebook:" + username
    json_to_keep = {'text_no_url': text, 'fbid': pid,
                    'created_at': datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+0000').strftime(
                        '%a %b %d %H:%M:%S +0000 %Y'), 'text': text, 'user_screen_name': username,
                    'senti_tag': "neutral", 'social_source': 'facebook'}
    return json_to_keep

def fix_json_format_es(text, date, username, pid):
    username = "facebook:" + username
    json_to_keep = {'text_no_url_es': text, 'fbid': pid,
                    'created_at': datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+0000').strftime(
                        '%a %b %d %H:%M:%S +0000 %Y'), 'text': text, 'user_screen_name': username,
                    'senti_tag': "neutral", 'social_source': 'facebook'}
    return json_to_keep