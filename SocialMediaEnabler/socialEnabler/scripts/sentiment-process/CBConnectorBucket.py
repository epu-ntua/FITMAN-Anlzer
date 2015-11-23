from couchbase import Couchbase

class connector:
    def __init__(self):
        if __package__ is None:
            import sys
            from os import path
            sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
            import script_settings
        else:
            from .. import script_settings
        server = script_settings.cb_server
        port = script_settings.couchbase_port
        bucket = script_settings.cb_twitter_bucket
        password = script_settings.cb_admin_password

        self.cbucket = Couchbase.connect(host=server, port=port, bucket=bucket, password=password)
