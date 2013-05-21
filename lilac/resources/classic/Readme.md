classic 
-------

templates for [golb](https://github.com/hit9/golb)

Demo
----

http://hit9.org

Usage
-----

`cd` to your blog's directory and clone this repo as a submodule:

```
git submodule add git://github.com/hit9/golb-templates-classic.git classic
```

set `tempaltes="classic"` in conf.toml

On these plugins in conf.toml:

```
plugins = ["feed","post_summary","gravatar"]
```

Developers
----------

1. requirements: `sass`:

    gem install sass

2. to build it, have to open a shell session and watch the sass:

    make
