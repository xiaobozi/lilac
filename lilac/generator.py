# coding=utf8

"""this is the main processor when lilac building"""


import signals
from .models import *
from .config import config
from .parser import parser
from .renderer import renderer
from .exceptions import *
from .utils import *
from . import src_ext, out_ext, src_dir, out_dir
from .logger import logger, logging

import sys
from os import listdir as ls
from os.path import join
from os.path import exists
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
        # set logger's level to info
        logger.setLevel(logging.INFO)
        # register signals
        self.register_signals()

    def register_signals(self):
        """Register all signals in this process"""
        signals.initialized.connect(self.parse_posts)
        signals.posts_parsed.connect(self.extract_tags)
        signals.posts_parsed.connect(self.compose_pages)
        signals.posts_parsed.connect(self.render_posts)
        signals.tags_extracted.connect(self.render_tags)

    def initialize(self):
        """Initialize config, blog, author, feed and jinja2 environment"""
        logger.info(self.initialize.__doc__)
        # read config to update the default
        update_nested_dict(self.config, config.read())
        # update blog and author according to configuration
        self.blog.__dict__.update(self.config['blog'])
        self.author.__dict__.update(self.config['author'])
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
            author=self.author,
            config=self.config,
        )
        renderer.initialize(self.blog.templates, jinja_global_data)
        logger.success("Generator initialized")
        # send signal that generator was already initialized
        signals.initialized.send(self)

    def parse_posts(self, sender):
        """Parse posts and sort them by create time"""
        logger.info(self.parse_posts.__doc__)
        posts_src_dir = join(src_dir, "post")
        # get all posts' filename
        files = [fn for fn in ls(posts_src_dir) if fn.endswith(src_ext)]

        # parse each post's content and append post instance to self.posts
        for fn in files:
            filepath = join(posts_src_dir, fn)  # source file full path
            try:
                post = parser.parse_from(filepath)
            except ParseException, e:
                logger.warn(e.__doc__ + ": filepath '%s'" % filepath)
                pass  # skip the wrong post
            else:
                post.name = fn[:-3]  # set it a name attribute
                self.posts.append(post)
        # sort posts by its create time
        self.posts.sort(
            key=lambda post: post.datetime.timetuple(),  # from now to past
            reverse=True
        )
        logger.success("Posts parsed")
        signals.posts_parsed.send(self)

    def extract_tags(self, sender):
        """Extract tags from posts, and sort by their posts' amount"""
        logger.info(self.extract_tags.__doc__)
        # traversal all posts and get the minial tag to posts dict
        tags = {}

        for post in self.posts:
            for tag in post.tags:
                tags.setdefault(tag, []).append(post)

        # initialize tags
        for tag, posts in tags.iteritems():
            self.tags.append(Tag(tag, posts))

        # sort by tag's size
        self.tags.sort(key=lambda x: len(x.posts), reverse=True)
        logger.success("Tag extracted")
        signals.tags_extracted.send(self)

    def compose_pages(self, sender):
        """Compose pages from posts"""
        logger.info(self.compose_pages.__doc__)
        groups = chunks(self.posts, 7)  # 7 posts per page

        for index, group in enumerate(groups):
            self.pages.append(Page(number=index+1, posts=list(group)))

        if self.pages:  # must not empty
            self.pages[0].first = True
            self.pages[-1].last = True
        logger.success("Pages composed")

    def render_posts(self, sender):
        """Render all posts to 'post/' with template 'post.html'"""
        logger.info(self.render_posts.__doc__)
        posts_out_dir = join(out_dir, "post")

        if not exists(posts_out_dir):
            mkdir(posts_out_dir)

        for post in self.posts:
            out_path = join(posts_out_dir, post.name+out_ext)
            try:
                renderer.render_to(out_path, "post.html", post=post)
            except RenderException as e:
                logger.error(e.__doc__ + ": Template 'post.html'")
                sys.exit(1)

        logger.success("Posts rendered")

    def render_tags(self, sender):
        """Render all tags to 'tag/' with template 'tag.html'"""
        logger.info(self.render_tags.__doc__)
        tags_out_dir = join(out_dir, "tag")

        if not exists(tags_out_dir):
            mkdir(tags_out_dir)

        for tag in self.tags:
            out_path = join(tags_out_dir, tag.name + out_ext)
            # TODO: Add try except
            renderer.render_to(out_path, "tag.html", tag=tag)

        # the 'tags.html'
        out_path = join(out_dir, "tags" + out_ext)
        renderer.render_to(out_path, "tags.html", tags=self.tags)
        logger.info("Tags rendered")


generator = Generator()
