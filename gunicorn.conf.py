backlog = 2048
bind = "127.0.0.1:8003"
pidfile = "/tmp/gunicorn-tolwod.pid"
daemon = True
debug = False
workers = 1
logfile = "/var/www/Tolwod/logs/gunicorn.log"
loglevel = "info"
