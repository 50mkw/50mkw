from . import home


@home.route('/')
def index():
    return 'Hello World!'
