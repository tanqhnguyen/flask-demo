import config
import json
from jinja2.filters import do_mark_safe

def static(value):
    if value.startswith('//') or value.startswith('http://') or value.startswith('https://'):
        return value
    return "%s/%s/%s" % (config.STATIC_PATH, str(config.STATIC_VERSION), value)

def to_json(value):
    return do_mark_safe(json.dumps(value))  