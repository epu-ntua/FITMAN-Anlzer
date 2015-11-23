__author__ = 'mpetyx'


from tasks import save_on_couchbase, process_values

# save_on_couchbase.delay( "yolo")
result = process_values.delay("yo")
print result
