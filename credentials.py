import os
# This is my second key for the PyRocket buckets
access_key = os.environ.get('pyrocket_access_key')
secret_key = os.environ.get('pyrocket_secret_key')

mysql_username = os.environ.get('pyrocket_mysql_usertname')
mysql_password = os.environ.get('pyrocket_mysql_password')
mysql_database = os.environ.get('pyrocket_mysql_database')
mysql_host = os.environ.get('pyrocket_mysql_host')