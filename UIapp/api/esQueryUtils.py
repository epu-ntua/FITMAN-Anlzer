def get_main_facet(topic,account,from_timestamp,until_timestamp):
    main_facet = "\"%s-%s\": { \"date_histogram\": { " \
                 "\"field\": \"doc.created_at\", \"interval\": \"day\" }," \
                 " \"global\": true, " \
                 "\"facet_filter\": { \"fquery\": { \"query\": { \"filtered\": " \
                 "{ \"query\": " \
                 "{ \"query_string\": { \"query\": \"doc.entities.hashtags.text:%s\" } }, " \
                 "\"filter\": " \
                 "{ \"bool\": { \"must\": [ " \
                 "{ \"range\": { \"doc.created_at\": { \"from\": %s, \"to\": %s } } }, " \
                 "{ \"terms\": { \"_type\": [ \"couchbaseDocument\" ] } }, " \
                 "{ \"terms\": { \"doc.user_screen_name\": [ \"%s\" ] } } ] } } } } } } },"
    main_facet = main_facet %(topic,account,topic,from_timestamp,until_timestamp,account)
    return main_facet

def get_topic_facet(topic,from_timestamp,until_timestamp):
    main_facet = "\"%s\": { \"date_histogram\": { " \
                 "\"field\": \"doc.created_at\", \"interval\": \"day\" }," \
                 " \"global\": true, " \
                 "\"facet_filter\": { \"fquery\": { \"query\": { \"filtered\": " \
                 "{ \"query\": " \
                 "{ \"query_string\": { \"query\": \"doc.entities.hashtags.text:%s\" } }, " \
                 "\"filter\": " \
                 "{ \"bool\": { \"must\": [ " \
                 "{ \"range\": { \"doc.created_at\": { \"from\": %s, \"to\": %s } } }, " \
                 "{ \"terms\": { \"_type\": [ \"couchbaseDocument\" ] } } " \
                 " ] } } } } } } },"
    main_facet = main_facet %(topic,topic,from_timestamp,until_timestamp)
    return main_facet


def build_facet_query(topics,accounts,from_timestamp,until_timestamp):
    query_start = "{\"facets\": {"
    query_end = " },\"size\": 0}"
    query=query_start
    for topic in topics:
        query+=get_topic_facet(topic,topic,from_timestamp,until_timestamp)
        for account in accounts:
            query+=get_main_facet(topic,account,from_timestamp,until_timestamp)
    query = query[:-1] #just remove last comma
    query+=query_end
    return  query

