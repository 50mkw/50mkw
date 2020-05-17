from . import home


@home.route('/')
def index():
    return 'Hello World!'

@home.route('/test')
def test():
    return 'Hello World test!'