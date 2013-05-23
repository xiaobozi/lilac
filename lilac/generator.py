# coding=utf8

"""this is the main processor when lilac building"""


import signals
from .models import *
from .config import config
from .parser import parser
from .renderer import renderer
from .exceptions import *
from .utils import *
from . import src_ext, out_ext, src_dir, out_dir, charset

from os import listdir as ls
from os.path import join
from os.path import join
from os import makedirs as mkdir
from datetime import datetime
from pyatom import AtomFeed


class Generator(object):

    def __init__(self):
        """init attributes to store runtime data"""
        # initialize them the default value.
        self.posts = []
        self.tags = []
        self.pages = []
        self.about = About()
        self.blog = Blog()
        self.author = Author()
        self.config = config.default
        # register signals
        self.register_signals()

    def register_signals(self):
        """Register all signals in this process"""
        # signals.initialized.connect(self.)

    def initialize(self):
        """Initialize config, blog, author, feed and jinja2 environment"""
        # read config to update the default
        update_nested_dict(self.config, config.read())
        # update blog and author according to configuration
        self.blog.__dict__.update(self.config['blog'])
        self.author.__dict.__.update(self.config['author'])
        # initialize feed
        self.feed = AtomFeed(
            title=self.blog.name,
            subtitle=self.blog.description,
            feed_url=self.blog.url+"/feed.atom",
            url=self.blog.url,
            author=self.author.name
        )
        # set a render
        jinja_global_data = dict(
            blog=self.blog,
            author=self.author
            config=self.config
        )
        renderer.initialize(blog.templates, jinja_global_data)
        # send signal that generator was already initialized
        signals.initialized.send(self)
