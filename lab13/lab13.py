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
    <form method="post" action="/info">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br>
        <button type="submit">Submit</button>
    </form>
    {% if data %}
    <h2>Submitted Data:</h2>
    <table border="1">
        <tr>
            <th>Name</th>
            <th>Email</th>
        </tr>
        <tr>
            <td>{{ data.name }}</td>
            <td>{{ data.email }}</td>
        </tr>
    </table>
    {% endif %}
    <p>Return to <a href="/">HomePage</a>.</p>
</body>
</html>
"""

error_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>Invalid Data</h1>
    <p>Please provide valid name and email.</p>
    <p>Return to <a href="/info">InfoPage</a>.</p>
</body>
</html>
"""

from urllib.parse import parse_qs

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')

    if path == '/':
        template = Template(home_template)
        response_body = template.render()
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    elif path == '/info':
        if method == 'POST':
            try:
                content_length = int(environ.get('CONTENT_LENGTH', 0))
                post_data = environ['wsgi.input'].read(content_length)
                post_params = parse_qs(post_data.decode('utf-8'))

                name = post_params.get('name', [''])[0].strip()
                email = post_params.get('email', [''])[0].strip()

                if name and email:
                    template = Template(info_template)
                    response_body = template.render(data={"name": name, "email": email})
                    start_response('200 OK', [('Content-Type', 'text/html')])
                    return [response_body.encode('utf-8')]
                else:
                    raise ValueError("Invalid input")

            except Exception as e:
                template = Template(error_template)
                response_body = template.render()
                start_response('400 Bad Request', [('Content-Type', 'text/html')])
                return [response_body.encode('utf-8')]

        else:
            template = Template(info_template)
            response_body = template.render(data=None)
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [response_body.encode('utf-8')]

    else:
        response_body = "<h1>404 Not Found</h1>"
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]


if __name__ == '__main__':
    port = 8080
    print(f"The server is running on http://localhost:{port}")
    with make_server('', port, application) as httpd:
        httpd.serve_forever()
