# coding=utf8

"""
  Generator from source to html.

  This is the processor when lilac building: read config, initialize
all models, and then render with jinja2, write to html files.
"""

from ._ import charset

from .models import Blog
from .models import Author
from .models import Post
from .models import Tag
from .models import Page
from .models import About

from .config import config

from .parser import parser
from .parser import SeparatorNotFound
from .parser import PostTitleNotFound
from .parser import PostDateTimeNotFound
from .parser import PostDateTimeInvalid
from .parser import PostTagsTypeInvalid

from .utils import chunks
from .utils import log
from .utils import update_nested_dict

from os import listdir as ls
from os.path import join
from os.path import exists
from os import makedirs as mkdir
from datetime import datetime
from pyatom import AtomFeed
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateNotFound


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
        self.about = About()
        self.blog = Blog()
        self.author = Author()
        self.config = config.default

    def initialize(self):
        """Initialize config, blog, author and jinja2 env"""
        # read configuration to update config
        update_nested_dict(self.config, config.read())
        # update blog and author from config
        self.blog.__dict__.update(self.config['blog'])
        self.author.__dict__.update(self.config['author'])
        # initialize jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.blog.templates))
        self.env.trim_blocks = True
        # initialize feed
        self.feed = AtomFeed(
            title=self.blog.name,
            subtitle=self.blog.description,
            feed_url=self.blog.url+"/feed.atom",
            url=self.blog.url,
            author=self.author.name
        )

    def render(self, template, **data):
        """
            Render data with some template::

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

            config is indeed what in your config.toml

        """
        dct = dict(
            blog=self.blog,
            author=self.author,
            config=self.config
        )
        dct.update(data)
        try:
            re = self.env.get_template(template).render(**dct)
        except TemplateNotFound:
            log.error("Template '%s' not found in directory '%s'" % (template, self.blog.templates))
        else:
            return re

    def render_to(self, path, template, **data):
        """render data with template, write to path"""
        r = self.render(template, **data)
        return open(path, "w").write(r.encode(charset))

    def parse_posts(self):
        """parse posts and sort them by create time"""

        src_dir = join(self.src_dir, "post")  # posts source directory
        template = "post.html"  # posts template
        # get all post's filename
        files = [fn for fn in ls(src_dir) if fn.endswith(self.src_ext)]
        # parse each post's content and append post instance to self.posts
        for fn in files:
            filepath = join(src_dir, fn)  # source file full path
            content = open(filepath).read().decode(charset)
            try:
                post = parser.parse_from(filepath)
            except SeparatorNotFound:
                log.error("separator not found in post '%s'" % filepath)
            except PostTitleNotFound:
                log.error("title not found in post '%s'" % filepath)
            except PostDateTimeNotFound:
                log.error("datetime not found in post '%s'" % filepath)
            except PostDateTimeInvalid:
                log.error(
                    "datetime invalid in post '%s', e.g.'2013-04-05 10:10'" % filepath
                )
            except PostTagsTypeInvalid:
                log.error("tags should be array type in post '%s'" % filepath)
            else:
                post.name = fn[:-3]  # set it a name attribute
                self.posts.append(post)
            # sort posts by its create time: from now to before
        self.posts.sort(
            key=lambda post: post.datetime.timetuple(), reverse=True)
        log.ok("Parse posts ok.")

    def extract_tags(self):
        """extract tags from posts, and sort them by posts' number"""
        # traversal all posts and get the minial tag to posts dict
        tags = dict()
        for post in self.posts:
            for tag in post.tags:
                tags.setdefault(tag, []).append(post)
        # initialize tags
        for tag, posts in tags.iteritems():
            self.tags.append(Tag(tag, posts))
        # sort by count
        self.tags.sort(key=lambda x: len(x.posts), reverse=True)
        log.ok("Exract tags from posts ok.")

    def generate_pages(self):
        """generate pages"""
        groups = chunks(self.posts, 7)  # 7 posts per page
        for index, group in enumerate(groups):
            self.pages.append(Page(number=index + 1, posts=list(group)))
        if self.pages:  # not empty
            self.pages[0].first  = True
            self.pages[-1].last = True
        log.ok("Generate pages ok.")

    def render_posts(self):
        """render all posts with template"""
        out_dir = join(self.out_dir, "post")
        if not exists(out_dir):
            mkdir(out_dir)
        for post in self.posts:
            out_path = join(out_dir, post.name + self.out_ext)
            self.render_to(out_path, "post.html", post=post)
        log.ok("Render posts ok")

    def render_tags(self):
        """render all tags with template"""
        out_dir = join(self.out_dir, "tag")
        if not exists(out_dir):
            mkdir(out_dir)
        for tag in self.tags:
            out_path = join(out_dir, tag.name + self.out_ext)
            self.render_to(out_path, "tag.html", tag=tag)
        out_path = join(self.out_dir, 'tags' + self.out_ext)
        self.render_to(out_path, "tags.html", tags=self.tags)
        log.ok("Render tags ok.")

    def render_pages(self):
        """render all pages with template"""
        # set attribute `summary` to each post
        for post in self.posts:
            setattr(post, "summary", parser.markdown.render(post.markdown[:255]))
        # start render..
        out_dir = join(self.out_dir, "page")
        if not exists(out_dir):
            mkdir(out_dir)
        for page in self.pages:
            if page.first:
                out_path = join(self.out_dir, "index" + self.out_ext)
            else:
                out_path = join(out_dir, page.number + self.out_ext)
            self.render_to(out_path, "page.html", page=page)
        log.ok("Render pages ok.")

    def render_archives(self):
        """render archives page"""
        out_path = join(self.out_dir, "archives" + self.out_ext)
        self.render_to(out_path, "archives.html", posts=self.posts)
        log.ok("Render archives ok.")

    def render_about_page(self):
        """
          render about me page.

          attributes
            html        rendered about.md's markdown's html production

          About page has no toml header neither no separator, only markdown.

        """
        src = join(self.src_dir, "about" + self.src_ext)
        if exists(src):
            content = open(src).read().decode(charset)
            self.about.markdown = content
        else:
            self.about.markdown = ''
        self.about.html = parser.markdown.render(self.about.markdown)
        out = join(self.out_dir, "about"+self.out_ext)
        self.render_to(out, "about.html", about=self.about)
        log.ok("Render about page ok.")

    def generate_feed(self):
        """
          generate feed of first 10 posts.
        """
        for post in self.posts[:10]:
            self.feed.add(
                title=post.title,
                content=post.html,
                content_type="html",
                author=self.author.name,
                url=self.blog.url+"/post/"+post.name+self.out_ext,
                updated=post.datetime
            )
        # write to /feed.atom
        open("feed.atom", "w").write(self.feed.to_string().encode(charset))
        log.ok("Generate feed.atom ok.")

    def render_404(self):
        """4o4"""
        self.render_to(join(self.out_dir, "404"+self.out_ext), "404.html")
        log.ok("render 404.html ok")

    def generate(self):
        """Generate posts, tags, all pages."""
        self.initialize()
        self.parse_posts()
        self.extract_tags()
        self.generate_pages()
        self.render_posts()
        self.render_tags()
        self.render_pages()
        self.render_about_page()
        self.render_archives()
        self.render_404()
        self.generate_feed()

generator = Generator()
