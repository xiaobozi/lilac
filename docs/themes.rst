.. _themes:

Themes
======

There isn't a process called "installation" for lilac's themes, 
just tell lilac where the target theme is by editing item `theme` in `config.toml`::

    [blog]
    theme = "the-theme-path"

Generally, the themes are under the root of your blog's directory.


Use Theme
---------

You really should manage your theme in a standalone git repository,
and use it as a submodule of your blog's submodule if your blog is under
git versioning too.

For instance, add theme `classic` a submodule of your blog's repo::

    $ git submodule add git://github.com/hit9/lilac-theme-classic.git classic

If you want to modify a theme created by someone else(i.e. classic), just fork his(or her) repo,
and then modify it.

But it's 100% ok to use themes not in the submodule way.

.. _theme_list:

Theme List
-----------

Here I maintain a lilac's themes list:

- `classic <https://github.com/hit9/lilac-theme-classic>`_ - the default theme for lilac. by `hit9 <https://github.com/hit9>`_

- `less <https://github.com/hit9/lilac-theme-less>`_ - a clean theme for lilac. by `hit9 <https://github.com/hit9>`_

The built in theme is classic, also the demo site's theme.

Have you made one? Please send a pull request on `lilac's Repo <https://github.com/hit9/lilac>`_, append yours to this list.
