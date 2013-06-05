.. _post:

Post Syntax
===========

Overview
--------

A post is made up of two parts: header and body.

The header is in `TOML <https://github.com/mojombo/toml>`_ and body is in `Github Flavored Markdown <http://github.github.com/github-flavored-markdown/>`_, 
the two parts are separated with a '---' like separator.

A sample post is::

    title = "Hello World"
    datetime = "2013-06-05 19:38"
    tags = ["sample", "some-tag"]
    ----------
    
    # Here is markdown content

Post's Header
-------------

The post's header is in TOML.

The header part contains post's information: title, tags, created time, etc.

The required items are `title` and `datetime`, others like `tags`, `summary`
are optional.

- the `datetime` is a `"%Y-%m-%d %H:%M"` formatted string, it's the post's
  created time.

- the `tags` is an array of tags.

- the `summary` is your post's summary(default: the post's first certain count characters).

Other variables in header can be got in template::

    {{post.myvar}}

Post's Body
-----------

The body is in Markdown. I recommend your this link to learn markdown: https://github.com/site/markdown_cheatsheet

The separator
-------------

Post's header and body are separated with a separator::

    ----

Or longer::

    ------------

It's at least 3 '-' long.
