# coding=utf8

"""
  models in lilac.
"""


class Blog(object):
    """
      Blog should have only one instance.

      attributes
        name            unicode     this blog's name
        description     unicode     this blog's description
        url             str         the url of your blog
        templates       str         which set of templates to use

      Note: `url` should be a remote url, you needn't to change url back
    to `localhost` to preview pages locally, this url is only used in feed
    generation so far.

    """

    def __init__(self, name=None, description=None, url=None, templates=None):
        self.name = name
        self.description = description
        self.url = url
        self.templates = templates


class Author(object):
    """
      The author of this blog.

      attributes
        name        unicode         your(the author) name
        email       unicode(or str) your(the author) email
      And the gravatar comes from this email.

    """

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email


class Post(object):
    """
      Post object.

      attributes
        markdown    unicode     post's markdown source
        html        unicode     post's body's html
        title       unicode     post's title
        datetime    datetime    post's create time
        tags        list        post's tags
        src         unicode     post's source file's path
        ..          these attributes are from key-to-value dict
      from head(which is in toml)

      A post is made up of header and body, they are separated by a separator
    '----'. The header is in toml, and the body is in markdown, the separator
    should be a single line all of character '-'(at least 3)::

          title = 'This-is-post-title'
          datetime = '2013-04-05 12:00'
          tags = ['tag1', 'tag2']
          ...
          -------
          markdown here

      And `title` and `datetime` is required in a post, the tags are optional,
    all keys in header will be attributes of this post, for instance::

        [mysettings]
        setting = 1
        -----------
        markdown here

    we can touch `setting` in this way::

        post.mysettings["setting"]

    and touch it in jinja2 templates in this way(as jinja2 enable
    to get an item of some dict like the way getting attributes)::

        {{post.mysettings.setting}}

    """

    def __init__(self, title, datetime, markdown, html, tags=None, src=None):
        self.title = title
        self.datetime = datetime
        self.markdown = markdown
        self.html = html
        self.src = src
        if tags is None:
            self.tags = []
        else:
            self.tags = tags


class Tag(object):
    """
      Tag object.

      Each post may belong to some tags, each tag has some posts.

      attributes
        name        unicode     tag's name
        posts       list        posts in this tag
    """

    def __init__(self, name, posts=None):
        self.name = name
        if posts is None:
            self.posts = []
        else:
            self.posts = posts


class Page(object):
    """
      Page object.

      attributes
        number      int     the 1st, 2nd or 3rd page?
        posts       list    the posts in this page
        frist       bool    is this page the first page?
        last        bool    is this page the last page?
    """

    def __init__(self, number, posts=None, first=False, last=False):
        self.number = number
        if posts is None:
            self.posts = []
        else:
            self.posts = posts
        self.first = first
        self.last = last
