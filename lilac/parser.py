# coding=utf8

"""
  A parser parses post's source to html.

  exceptions
    SeparatorNotFound       no separator in a post's source.
    PostTitleNotFound       a post require title.
    PostDateTimeNotFound    a post require its create datetime
    PostDateTimeInvalid     invalid datetime format
    PostTagsTypeInvalid     invalid tags datatype, should be a list
"""

from ._ import charset
from .models import Post

from datetime import datetime

import toml
import misaka
import houdini
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class ColorRender(HtmlRenderer, SmartyPants):
    """misaka render to color codes"""

    def block_code(self, text, lang):

        if not lang:
            text = text.encode(charset).strip()
            return (
                """\n<div class="highlight">
                <pre><code>%s</code></pre>
                </div>\n""" % houdini.escape_html(text)
            )

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()

        return highlight(text, lexer, formatter)


class SeparatorNotFound(Exception):
    """Raised when no separator found in a post"""
    pass


class PostDateTimeNotFound(Exception):
    """Raised when a post initialized without a datetime"""
    pass


class PostTitleNotFound(Exception):
    """Raised when a post initialized without a title"""
    pass


class PostDateTimeInvalid(Exception):
    """Invalid datetime format"""
    pass


class PostTagsTypeInvalid(Exception):
    """Invalid tags datatype"""
    pass


class Parser(object):
    """
      Parser from post's source to post object::

          parser = Parser()
          parser.parse(str)  # return post instance
          parser.parse_from(filepath)  # parse from filepath
    """

    separator = '---'  # separator between toml head and markdown body.

    def __init__(self):
        """
          Initialize the parser, set attribute `markdown` to parser::

              parser.markdown.render(markdown_str)  # return a post object
        """
        render = ColorRender()  # initialize this render
        extensions = misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_AUTOLINK
        # initialize markdown
        # `markdown.render(str)` to render `markdown` to `html`
        self.markdown = misaka.Markdown(render, extensions=extensions)

    def parse(self, post_source):
        """
          Parse unicode post source to post object.
        """
        lines = post_source.splitlines()
        l = None  # flag: separator's index

        for line_no, line in enumerate(lines):
            if self.separator in line:
                l = line_no
                break

        if not l:
            raise SeparatorNotFound
        # separate header and body
        header, body = "\n".join(lines[:l]), "\n".join(lines[l+1:])

        dct = toml.loads(header)  # parse header to dict

        # check header
        # title, datetime are required
        # datetime must be in this format 'year-month-day hour:minutes'
        # tags must be a list
        if 'title' not in dct:
            raise PostTitleNotFound
        else:
            title = dct.pop('title')

        if 'datetime' not in dct:
            raise PostDateTimeNotFound
        else:
            datetime_str = dct.pop('datetime')
            try:
                date_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            except ValueError:  # invalid format
                raise PostDateTimeInvalid

        tags = dct.get('tags', [])

        if not isinstance(tags, list):
            raise PostTagsTypeInvalid

        markdown = body
        html = self.markdown.render(body)

        post = Post(title, date_time, markdown, html, tags=tags)
        # append k, v to post's attributes
        post.__dict__.update(**dct)
        return post

    def parse_from(self, filepath):
        """
          Parse from filepath, and add an attribute `src` to parsed post
        """
        post = self.parse(open(filepath).read().decode(charset))
        post.src = filepath
        return post


parser = Parser()
