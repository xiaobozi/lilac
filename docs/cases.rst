.. _cases:

Use Cases
=========

Github Pages
-------------

Thank GitHub, we have a great place to host static blogs.

If you want to learn about Github Pages, head over to `GitHub Pages <http://pages.github.com/>`_.

If you create a repository named `username.github.com` (now it's `username.github.io`), its master
branch will be served on GitHub Pages.

If you create a branch named `gh-pages` on any repository, this branch will be served on GitHub Pages.

GitHub Pages is a static files HTTP server, free to use and no bandwidth limit.

Here's a short tutorial to use lilac on github pages.

`Create a repo <https://github.com/new>`_ for blog on GitHub, and then open a shell::

    $ mkdir you.github.com && cd you.github.com
    $ git init
    $ git remote add origin git@github.com:you/you.github.com.git

It's a good habit to ignore trash files::

    $ vim .gitignore

we should add this to `.gitignore`::

    .*.swp
    .*.swo
    venv/

Now make the first commit::

    $ git add .gitignore
    $ git commit -m 'init commit'
    $ git push origin master

It's time to deploy lilac::

    $ lilac deploy

I recommend you to add theme as git submodule(need to remove the auto generated theme directory)::

    $ rm classic -rf
    $ git submodule add git://github.com/hit9/lilac-theme-classic.git classic

You may take a look at :ref:`Quick Start <quickstart>` for customization.

And start writing::

    $ make serve

Let's deploy the site to GitHub's Pages::

    $ git add .
    $ git commit -m 'deploy my blog'
    $ git push origin master

GitHub will send you an email once your blog is ready.

You can set up a custom domain with github pages, just define a file `CNAME` for your site,
and write your domain in it(see here: `CNAME <https://github.com/hit9/lilac/blob/gh-pages/CNAME>`_),
after this, create a CNAME record pointing to `your-github-username.github.io.` on the domain panel, more
information is on `github pages help <https://help.github.com/articles/setting-up-a-custom-domain-with-pages>`_.

Host Blog in Sub Directory
--------------------------

If your blog must run from a sub-directory, the main scenario being if your blog will be hosted
on a GitHub Project Page, take a look at this configuration: :ref:`root_path <root_path>`.
