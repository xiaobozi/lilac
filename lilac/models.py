# coding=utf8

"""
  models in lilac.
"""


class Post(object):
    """
      Post object.

      attributes
        markdown    unicode     post's markdown source
        html        unicode     post's body's html
        title       unicode     post's title
        datetime    datetime    post's create time
        tags        list        post's tags
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

    and touch it in jinja2 templates in this way(as jinja2 enable to get an item
    of some dict like the way getting attributes)::

        post.mysettings.setting

    """

    def  __init__(self, title, datetime, markdown, html, tags=None):
        self.title = title
        self.datetime = datetime
        self.markdown = markdown
        self.html = html
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
