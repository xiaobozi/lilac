# coding=utf8

"""
  Configuration manager for lilac.

  lilac's configuration is in TOML::

      [blog]
      name = "blog-name"
      description = "Make difference."
      templates = "classic"
      [author]
      name = "hit9"
      email = "me@example.com"

  each key of the configuration should be set and
valid.

"""

from ._ import charset

import os
import toml


class Config(object):
    """
      Config manager, all configuration is stored in `config.toml` in
    TOML. To manage it::

        config = Config()
        config.read()  # return dict
        config.write(dct)  # write dict to config.toml

    """

    filename = "config.toml"  # the
    path = os.path.join(".", filename)

    def read(self):
        """Read and parse config, return dict"""
        content = open(self.path).read().decode(charset)
        return toml.loads(content)

    def write(self, dct):
        """Write config to toml file from dict"""
        content = toml.dumps(dct)
        return open(self.path).write(content.encode(charset))


config = Config()  # yes, build a config instance
