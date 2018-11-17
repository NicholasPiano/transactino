Heimdal is a websocket proxy for the main Django ORM web server. It's purpose is to maintain connections to external clients and convert their messages into requests sent to the Django ORM server, Wotan. Heimdal also maintains a small http server to receive requests from Wotan. These will be converted into outgoing messages to the appropriate clients. In this way, all of the requirements of the application will be satisfied:

1. A client is able to maintain a connection to a websocket for real-time communication.
2. Asynchronous tasks can be scheduled with the task server, triggered on the ORM server, and relayed to the correct clients via Heimdal.
