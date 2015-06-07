from flask import Flask, render_template
from werkzeug import cached_property
import markdown
import os
import yaml

POSTS_FILE_EXTENSION = '.md'

app = Flask(__name__)


class Post:

    def __init__(self, path):
        self.path = path
        self._initialize_metadata()

    @cached_property
    def html(self):
        with open(self.path, 'r') as fin:
            # skip over the metadata with split('/n/n', 1)[1]
            content = fin.read().split('\n\n', 1)[1].strip()
        return markdown.markdown(content)

    def _initialize_metadata(self):
        content = ''
        with open(self.path, 'r') as fin:
            for line in fin:
                if not line.strip():  # first blank line
                    break
                content += line
        # update the class internal dict
        self.__dict__.update(yaml.load(content))


def format_date(value, format='%B %d, %Y'):
    return value.strftime(format)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/blog/<path:path>')
def post(path):
    # raise  to start werkzeug debugger where we are in the code
    # import pdb; pdb.set_trace()  to start python debugger
    path = os.path.join('posts', path + POSTS_FILE_EXTENSION)
    post = Post(path)
    return render_template('post.html', post=post, format_date=format_date)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
