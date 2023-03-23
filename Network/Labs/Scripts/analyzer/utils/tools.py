import random
import os

def get_path(filename):
    current_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(current_path, 'utils', filename)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pcap', 'cap', 'pcapng'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_filetype(filename):
    return '.' + filename.rsplit('.', 1)[1]

def random_name():
    return ''.join(random.sample('1234567890qazxswedcvfrtgbnhyujmkiolp', 10))