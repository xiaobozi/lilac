title = "lilac- a static blog generator that sucks less"

datetime = "2013-05-25 16:15"

tags = ["lilac"]

----------

lilac
=====

It is - **a static blog generator**

Demo
----

demo site is on branch [gh-pages](https://github.com/hit9/lilac/tree/gh-pages)

- http://lilac.hit9.org

Featrues
--------

- [Toml](https://github.com/mojombo/toml) & Markdown([GFM](http://github.github.com/github-flavored-markdown/)) based

- 100% in Python

- tags & feed & templates & Code highlighting support

- jinja2 templating language

- minimal blog

Quick Start
-----------

1. install `lilac`:

   ```
mkdir MyBlog && cd MyBlog
virtualenv venv
. venv/bin/activate
pip install git+git://github.com/hit9/lilac.git
   ```

2. deploy your blog:

   ```
   lilac deploy
   ```

   `lilac` generate you a `Makefile` to manage blog.

3. edit `config.toml` to meet your needs.

4. build blog:

   ```
   make build
   ```

5. see your blog in action:

   ```
   make server
   ```

   preview htmls at http://0.0.0.0:8000


Write a Post
------------

To write a post, just follow the 3 simple steps:

1. new a file in directory `src/post` , for example: `src/post/hello-world.md`

2. edit that file, write header in [Toml](https://github.com/mojombo/toml) and
write body in markdown, header and body are separated with a line `----`

3. run `make build` , and then preview under the ''cute' server in your browser

OS Plat
--------

Only works on \*nix.

> windows doesn't count.


FAQ?
-----

- Don't forget to activate virtualenv environment - `. venv/bin/activate` before building

About the Name
--------------
 
`lilac` is `紫丁香` in chinese, they are everywhere in my university HIT.

TODOs
-----

- Need plugins support?
- docs for templates developers

License
-------

MIT
