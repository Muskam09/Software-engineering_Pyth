from wsgiref.simple_server import make_server
from jinja2 import Template


home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Welcome to the Home Page</h1>
    <p>Go to <a href="/info">InfoPage</a>, to learn more.</p>
</body>
</html>
"""

info_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Info</title>
</head>
<body>
    <h1>Information Page</h1>
    <p>This is a page with information. Return to <a href="/">HomePage</a>.</p>
</body>
</html>
"""


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    if path == '/':
        template = Template(home_template)
        response_body = template.render()
    elif path == '/info':
        template = Template(info_template)
        response_body = template.render()
    else:
        response_body = "<h1>404 Not Found</h1>"
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [response_body.encode('utf-8')]


if __name__ == '__main__':
    port = 8080
    print(f"The server is running on http://localhost:{port}")
    with make_server('', port, application) as httpd:
        httpd.serve_forever()
