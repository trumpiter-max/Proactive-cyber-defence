import random

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pcap', 'cap'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_filetype(filename):
    return '.' + filename.rsplit('.', 1)[1]

def random_name():
    return ''.join(random.sample('1234567890qazxswedcvfrtgbnhyujmkiolp', 10))