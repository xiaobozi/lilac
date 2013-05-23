# coding=utf8

"""models in lilac: Blog, Author, Post, Tag, Page"""

from hashlib import md5


class Blog(object):
    """
    The blog itself.
    attributes
      name        unicode     blog's name
      description unicode     blog's description
      url         str         blog's site url
      templates   str         which set of templates to use
    """

    def __init__(self, name=None, description=None, url=None, templates=None):
        self.name = name
        self.description = description
        self.url = url
        self.templates = templates


class Author(object):
    """
    The blog's author, only one.
    attributs
      name          unicode     author's name
      email         unicode     author's email
      gravatar_id   str         gravatar_id generated from email
    the gravatar_id is a property decorated method.
    """

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    @property
    def gravatar_id(self):
        """it's md5(author.email), author's gravatar_id"""
        return md5(self.email).hexdigest()


class Post(object):
    """
    The blog's post(s).
    attributes
      name      str      post's filename without extension
      title     unicode  post's title
      datetime  datetime post's create time, e.g. "2012-10-10 13:20"
      tags      list     post's tags
      markdown  unicode  post's markdown source(its body)
      html      unicode  post's html(parrsed from markdown)
    the `html` is a property decorated method
    """

    def __init__(
        self,
        name=None, tags=None, title=None, datetime=None, markdown=None
    ):
        self.name = name
        self.title = title
        self.datetime = datetime
        self.markdown = markdown

        if tags is None:
            self.tags = []
        else:
            self.tags = tags

    @property
    def html(self):
        """Return the post's content's rendered markdown"""
        # the parser should be import in method, else will cause annoying loop
        # import issue
        from .parser import parser
        return parser.markdown.render(self.markdown)


class Tag(object):
    """
    Each posts may have tags, each tag has some posts.
    attributes
      name      unicode     tag's name
      posts     list        posts in this tag
    """

    def __init__(self, name=None, posts=None):
        self.name = name

        if posts is None:
            self.posts = []
        else:
            self.posts = posts


class Page(object):
    """
    The pages, 1st, 2nd, 3rd page..
    attributes
      number    int   the order of this page
      posts     list  the posts in this page
      first     bool  is this page the first page?
      last      bool  is this page the last page
    """

    def __init__(self, number=1, posts=None, first=False, last=False):
        self.number = number
        self.first = first
        self.last = last

        if posts is None:
            self.posts = []
        else:
            self.posts = posts


class About(object):
    """
    The blog's about page, only one.
    attributes
      markdown  its content
      html      its markdown's html
    about has no header, only body in markdown.
    the `html` is a property decorated method.
    """

    def __init__(self, markdown=None):
        self.markdown = markdown

    @property
    def html(self):
        """Render its markdown to html"""
        from .parser import parser
        return parser.markdown.render(self.markdown)
