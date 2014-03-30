##
# Gunicorn config at 
# Managed by Chef - Local Changes will be Nuked from Orbit (just to be sure)
##

# What ports/sockets to listen on, and what options for them.
bind = "0.0.0.0:3000"

# The maximum number of pending connections
backlog = 2048

# What the timeout for killing busy workers is, in seconds
timeout = 60

# How long to wait for requests on a Keep-Alive connection, in seconds
keepalive = 2

# The maxium number of requests a worker will process before restarting
max_requests = 0

# Whether the app should be pre-loaded
preload_app = False

# How many worker processes
workers = 4

# Type of worker to use
worker_class = "gevent"

