Installation
============

OS Support
----------

Lilac supports only \*nix: Mac OS X, Linux, BSD (Only linux tested).

It doesn't support Windows.

Virtualenv
----------

If you are a pythoner, you should install lilac via virtualenv_.

.. _virtualenv: http://www.virtualenv.org/

If virtualenv is not installed on your OS, install it::

    sudo pip install virtualenv

Once you have virtualenv installed, open a shell and create a new environment for your blog::

    $ mkdir MyBlog
    $ cd MyBlog
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools............done.
    Installing pip...............done.

Now, whenever you want to write blog, you have to activate the corresponding environment::

    $ . venv/bin/activate


