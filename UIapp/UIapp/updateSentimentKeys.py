from couchbase import Couchbase
import configurations

def connectTOdb():
    server = configurations.server_ip
    port = configurations.couchbase_port
    bucket = configurations.couchbase_bucket
    password = configurations.couchbase_password
    cbucket = Couchbase.connect(host=server, port=port, bucket=bucket, password=password)
    return cbucket

# cb = None

def update(key, value):

    # print "tried to retrieve " + str(key)

    try:
        #print "entered update"
        cb = connectTOdb()
        document = cb.get(key)

        document.value["senti_tag"] = value

        cb.set(document.key, document.value)

        return 1
    except Exception:
        print Exception.message
        print "error connecting to database"
        return 0


def multiple_values_update( lista ):
    print "entered multiple values update"
    for item in lista:
        update(item['key'], item['value'])

    # cb._close()