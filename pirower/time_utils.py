import datetime

def timedelta_milliseconds(td):
    return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

def convert_ms_to_elapsed(ms):
    d = datetime.timedelta(milliseconds=ms)
    s = str(d)
    return s[:-5]
