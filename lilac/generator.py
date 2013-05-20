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
        # initialize posts, tags container
        self.posts = []
        self.tags = []
        self.pages = []
        # read configuration
        self.config = conf = config.read()
        # initialize blog, author from conf
        self.blog = Blog(**conf["blog"])
        self.blog = Author(**conf["author"])
        # initialize jinja2 environment
        self.env = Environment(loader=FileSystemLoader(conf["blog"]["templates"]))
        self.env.trim_blocks = True
