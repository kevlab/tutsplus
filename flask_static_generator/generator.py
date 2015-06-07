from flask import Flask, render_template, url_for
from werkzeug import cached_property
import markdown
import os
import yaml

POSTS_FILE_EXTENSION = '.md'

app = Flask(__name__)


class Post:

    def __init__(self, path, root_dir=''):
        self.urlpath = os.path.splitext(path.strip('/'))[0]
        self.filepath = os.path.join(root_dir, path.strip('/'))
        self._initialize_metadata()

    @cached_property
    def html(self):
        with open(self.filepath, 'r') as fin:
            # skip over the metadata with split('/n/n', 1)[1]
            content = fin.read().split('\n\n', 1)[1].strip()
        return markdown.markdown(content)

    @property
    def url(self):
        return url_for('post', path=self.urlpath)

    def _initialize_metadata(self):
        content = ''
        with open(self.filepath, 'r') as fin:
            for line in fin:
                if not line.strip():  # first blank line
                    break
                content += line
        # update the class internal dict
        self.__dict__.update(yaml.load(content))


@app.template_filter('date')  # to pipe the date into the template
def format_date(value, format='%B %d, %Y'):
    return value.strftime(format)
# app.jinja_env.filters['date'] = format_date
# another way to pipe the date in the template

# a thrid way to get the date in the template
# @app.context_processor
# def inject_format_date():
#     return {'format_date': format_date}


@app.route('/')
def index():
    posts = [Post('hello.md', root_dir='posts')]
    return render_template('index.html', posts=posts)


@app.route('/blog/<path:path>')
def post(path):
    # raise  to start werkzeug debugger where we are in the code
    # import pdb; pdb.set_trace()  to start python debugger
    post = Post(path + POSTS_FILE_EXTENSION, root_dir='posts')
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
