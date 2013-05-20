# coding=utf8

"""
  Generator from source to html.

  This is the processor when lilac building: read config, initialize
all models, and then render with jinja2, write to html files.
"""

# import all models we need
from .models import Blog
from .models import Author
from .models import Post
from .models import Tag
from .models import Page

from .config import config

from .utils import chunks
from .utils import log

from jinja2 import Environment
from jinja2 import FileSystemLoader


class Generator(object):
    """
      Generator for lilac.
    """

    src_ext = ".md"  # source filename extention
    out_ext = ".html"  # output filename extention
    src_dir = "src"  # source directory, './src'
    out_dir = "."    # output directory, './'

    def __init__(self):
        # init attributes with default value
        self.posts = []
        self.tags = []
        self.pages = []
        self.blog = Blog()
        self.author = Author()
        self.config = config.default_conf


    def initialize(self):
        """Initialize config, blog, author and jinja2 env"""
        # read configuration to update config
        conf = config.read()
        self.config.update(conf)
        # update blog and author from config
        # pop blog and author from config
        self.blog.__dict__.update(self.config['blog'])
        self.author.__dict__.update(self.config['author'])
        # initialize jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.blog.templates))
        self.env.trim_blocks = True

    def render(self, template, data):
        """
            Render data with some template::

                generator.render(template, data)

            parameters
              template  str  the filename of some template in templates folder
              data      dict data dict to render

            Configuration in config.toml will be append to the data.

            Any key in config.toml can be touched in templates::

                [mysetting]
                setting = 'xxx'

            in the template side::

                {{config.mysetting.setting}}

            but you can touch `blog` or `author` more quick::

                {{blog.name}}
                {{author, email}}
                ... # etc
            than this way::

                {{config.blog.name}}
                {{config.author.email}}

        """
        dct = dict(
            blog=self.blog,
            author=self.author,
            config=self.config
        )
        dct.update(data)
        return self.env.get_template(template).render(**dct)


generator = Generator()
