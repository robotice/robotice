CELERY_RESULT_EXCHANGE = 'results'
CELERY_RESULT_EXCHANGE_TYPE = 'fanout'
#CELERY_TASK_RESULT_EXPIRES = 120

CELERY_ACCEPT_CONTENT = [
    'json', 'msgpack', 'yaml', 'application/x-python-serialize', ]

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_TIMEZONE = 'UTC'

CELERY_ROUTES = {
    'monitor.get_real_data': {
        'queue': 'monitor',
    },
    'planner.get_model_data': {
        'queue': 'planner',
    },
    'reasoner.compare_data': {
        'queue': 'reasoner',
    },
    'reasoner.process_real_data': {
        'queue': 'reasoner',
    },
    'reactor.commit_action': {
        'queue': 'reactor',
    }
}

CELERY_REDIRECT_STDOUTS_LEVEL = "DEBUG"
