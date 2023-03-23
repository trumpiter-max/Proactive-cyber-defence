bind = '0.0.0.0:8000' 
workers = 1 
backlog = 2048
debug = True
proc_name = 'gunicorn.pid'
pidfile = '/var/log/gunicorn/debug.log'
loglevel = 'debug'
