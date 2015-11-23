__author__ = 'mpetyx'


BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_IMPORTS = ('tasks', )

CELERY_RESULT_BACKEND = 'amqp'
CELERY_RESULT_PERSISTENT = True
CELERY_TASK_RESULT_EXPIRES = None

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = {
    'default': {
        'binding_key': 'task.#',
    },
    'save_on_couchbase': {
        'binding_key': 'save_on_couchbase.#',
    },
    'process_values': {
        'binding_key': 'process_values.#',
    },
}
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'
CELERY_ROUTES = {
    'tasks.save_on_couchbase': {
        'queue': 'save_on_couchbase',
        'routing_key': 'save_on_couchbase.a_result'
    },
    'tasks.process_values': {
        'queue': 'process_values',
        'routing_key': 'process_values.handle',
    },
}