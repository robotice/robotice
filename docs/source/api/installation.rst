
..code-block: python

	[pipeline:api]
	pipeline = request_id faultwrap ssl versionnegotiation authurl authtoken context apiv1app


	[app:robotice.api]
	paste.app_factory = robotice.api.wsgi:app_factory
	robotice.app_factory = robotice.api.v1:API

