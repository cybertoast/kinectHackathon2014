# OSC Bridge as Flask application with Websockets

The objective is to provide a Flask proxy that handles OSC messages from a back-end service,
and forwards that data to a front-end application through web sockets

## Quick Start

	mkvirtualenv oscbridge
	pip install -r deploy/requirements.txt
	cp oscbridge/config/config.yml.sample oscbridge/config/config.yml
	python wsgi.py

## References

* https://github.com/memo/TornadoOSCWSStream
* http://www.brettdangerfield.com/post/realtime_data_tag_cloud/
* http://stackoverflow.com/questions/23232399/server-sent-events-with-flask-and-tornado
* https://www.npmjs.org/package/osc
* http://stackoverflow.com/questions/23484491/flask-streaming-data-by-writing-to-client