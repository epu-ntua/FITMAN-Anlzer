from couchbase import Couchbase
import script_settings


class connector:
    def __init__(self):
        server = script_settings.cb_server
        port = script_settings.couchbase_port
        bucket = script_settings.cb_twitter_bucket
        password = script_settings.cb_admin_password

        self.cbucket = Couchbase.connect(host=server, port=port, bucket=bucket, password=password)
