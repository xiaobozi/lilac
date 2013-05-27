title = "lilac theme how-to"

datetime = "2013-05-27 19:27"

tags = ["themes"]

---------------

Getting Start
==============

Nice to see that you want to create one theme or to modify your theme.

You can check out theme [classic](https://github.com/hit9/lilac/tree/master/lilac/resources/classic).

We use the excellent templating engine [jinja2](https://github.com/mitsuhiko/jinja2) to render templates, you may need to take 15 mins to 
learn [how to write jinja2 templates](http://jinja.pocoo.org/docs/templates/).

Theme structure
===============

lilac only knows where to find jinja2 templates, but it doesn't care where the images are or where the stylesheets are.

Just put all templates right under the root of your theme directory.

The minimal required templates should be:

- post.html
- tag.html
- page.html
- tags.html
- archives.html
- about.html
- 404.html

Variables in templates
======================

We need to know variables in each template.

Checking out the [models definition](https://github.com/hit9/lilac/blob/master/lilac/models.py) may help a lot.

1. Global variables
-------------------

3 variables can be acccessed in every template, they are:

- blog   --- attributes: name, url, decription, theme
- author --- attributes: name, email, gravatar_id
- config --- attributes: all vars in config.toml

For any var defined in `config.toml`, for instance:

```
[mysettings]
myvar = 12345
```

we can get it in any template like this:

```
{{ config.mysettings.myvar }}
```

But using `{{ blog.name }}` is better than `{{ config.blog.name }}`

2. post.html
------------

It's the post's content page. (i.e. `/post/sample-post.html`)

variable: `post`

attributes:

```
name        str        post's filename without extension
title       str        post's title
datetime    datetime   post's create time, e.g. "2012-10-10 13:20"
tags        list       post's tags
markdown    str        post's markdown source(its body)
html        str        post's html(markdown rendered)
summary     str        post's summary
```

As a sample: we want to display a single post

```html
<h1 class="title">{{post.title}}</h1>
<p><span class="date">{{post.datetime.strftime("%b  %d, %y")}}</span></p>  {# created at #}
<div class="post-html">{{post.html}}</div>
<div class="tags">
  {%for tag in post.tags%}
  <a href="/tag/{{tag}}.html">{{tag}}</a>
  {%endfor%}
</div>
```

And, for any variables defined in post's header, can get it this way: `{{post.myvar}}`

3. tag.html
-----------

It's the tag's content page. (i.e. `/tag/sample-tag.html`)

variable: `tag`

attributes:

```
name      str         tag's name
posts     list        posts in this tag
```

Sample: we want to display a single tag's page

```html
<h1 class="name">Tag: {{tag.name}}</h1>
{%for post in tag.posts%}
<p class="post">
  <a href="/post/{{post.name}}.html" class="title">{{post.title}}</a>
  <a class="date">{{post.datetime.strftime("%Y-%m-%d")}}</a>
</p>
{%endfor%}
```

4. page.html
------------

It's the page's content page. (`/index.html, /page/2.html, ..`)

variable: `page`

attributes:

```
number    int   the order of this page
posts     list  the posts in this page
first     bool  is this page the first page?
last      bool  is this page the last page
```

Sample to list posts in some page:

```html
{%for post in page.posts%}
<div class="post">
  <p class="title"><a href="/post/{{post.name}}.html">{{post.title}}</a></p>
  <p><span class="date">{{post.datetime.strftime("%b  %d, %y")}}</span></p>
  <div class="post-html">
    {{post.summary}}
  </div>
  <div class="tags">
    {%for tag in post.tags%}
    <a href="/tag/{{tag}}.html">{{tag}}</a>
    {%endfor%}
  </div>
  <p class="readmore"><a href="/post/{{post.name}}.html">Read more  >> </a></p>
</div>
{%endfor%}
```

5. tags.html
------------

variable: `tags`, it's a list of tag objects.

To list all tags:

```html
 {% for tag in tags %}
    <a href="/tag/{{tag.name}}.html">{{tag.name}}</a>x{{tag.posts|count }}
  {% endfor %}
```

6. archives.html
----------------

variable: `posts`, it's a list of post objects.

To list all posts:

```html
 {%for post in posts%}
  <p class="post">
    <a href="/post/{{post.name}}.html" class="title">{{post.title}}</a>
    <a class="date">{{post.datetime.strftime("%Y-%m-%d")}}</a>
  </p>
  {%endfor%}
```

7. about.html
-------------

variables: about

attributes:

```
markdown  its content
html      its markdown's html
```

8. 404.html
-----------

No variables here(except global variables).

Share your theme
------------------

Have you created a great theme? share it via pulling request to [lilac's readme](https://github.com/hit9/lilac/blob/master/README.md)

Questions?
----------

Send email to me(nz2324[AT]126.com) or new an issue on github.
