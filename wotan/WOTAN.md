Wotan is the main Django ORM server. It's purpose is to control access to the database, and use the data to interpret queries, including authentication. It schedules tasks such as checking subscriptions and payments, as well as the main workhorse of the application, fee reporting.

It operates as a completely traditional HTTP server, with no frills, since the websockets are handled by Heimdal.
