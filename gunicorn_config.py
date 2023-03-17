bind = "0.0.0.0:8000"
workers = 1
threads = 4
worker_class = 'eventlet'
module = "app"
callable = "app"