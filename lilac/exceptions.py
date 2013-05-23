# coding=utf8

"""all possible exceptions"""

class LilacException(Exception):
    """There was an ambiguous exception that occurred while
    handling lilac process"""
    pass


class ParseException(LilacException):
    """There was an exception occurred while parsing the source."""
    pass


class SeparatorNotFound(ParseException):
    """Raised when no separator found in a post"""
    pass


class PostDateTimeNotFound(ParseException):
    """Raised when no datetime found in a post"""
    pass


class PostTitleNotFound(ParseException):
    """Raised when no title found in a post"""
    pass


class PostDateTimeInvalid(ParseException):
    """Invalid datetime format, should like '2012-04-05 10:10' """
    pass


class PostTagsTypeInvalid(ParseException):
    """Invalid tags datatype, should be a array"""
    pass


class PostHeaderSyntaxError(ParseException):
    """TomlSyntaxError occurred in post's header"""
    pass


class ConfigSyntaxError(LilacException):
    """TomlSyntaxError occurred in config.toml"""
    pass
