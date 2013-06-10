.. _config:

Configuration
=============

Overview
--------

There are only a few items to configure. A minimal configuration is::

    root_path = ""
    
    [blog]
    name = "Make Difference"
    description = "Here goes your blog's description"
    url = "http://your-blog.org"
    theme = "classic"
    
    [author]
    name = "me"
    email = "me@some.com"
    
    [disqus]
    shortname = "your-disqus-short-name"

.. _root_path:

Root Path
---------

If you are deploying your blog right under the server's root, you needn't
to set this item, leave it blank::

    root_path = ""

Else, if you are deploying your blog to some sub_directory under the server,
you need to configure this item. For instance, your blog are deployed here:

    http://my-server.com/myblog/

you should set `root_path` to `"/myblog"`::

    root_path = "/myblog"


But note that: when in localhost, your site will run regardless of `root_path`,
so you must run `lilac build` before deploying this site to remote server.

Blog & Author
-------------

It's easy enough to configure these by yourself.

Notes you need to know:

- the item `url` in section `blog` is only used in feed generation.
- better to set `author` 's `email` to your Gravatar's email.

Disqus
-------

Lilac uses `Disqus <http://disqus.com/>`_ to manage blog's comments.

Follow this link to `register your blog to disqus.com <https://disqus.com/admin/signup/>`_
, and then set item `shortname` in the section `disqus`::

    [disqus]
    shortname = "your-short-name-from-disqus.com"

Theme Vars
----------

This section configure your theme. We configure theme's variables in config.toml instead of
`your_theme/theme.toml` so that we can use theme as a standalone repo(or submodule).

What to configure depends on your theme.
