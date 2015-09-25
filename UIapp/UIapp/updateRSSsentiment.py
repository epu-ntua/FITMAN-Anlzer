from couchbase import Couchbase
import configurations


def connectTOdb():
    server = configurations.server_ip
    port = configurations.couchbase_port
    bucket = configurations.couchbase_rss_bucket
    password = configurations.couchbase_rss_password
    cbucket = Couchbase.connect(host=server, port=port, bucket=bucket, password=password)
    return cbucket

# cb = None

def update(key, value):

    # print "tried to retrieve " + str(key)

    try:
        cb = connectTOdb()
        document = cb.get(key)

        document.value["sentiment"] = value

        cb.set(document.key, document.value)

        return 1
    except:

        return 0


def multiple_rss_update( lista ):
    print "in rss"


    for item in lista:

        update(item['key'], item['value'])

    # cb._close()


