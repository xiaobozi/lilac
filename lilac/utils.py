# coding=utf8

"""this module provides utility functions that are used within lilac"""


def chunks(lst, number):
    """
    A generator, split list `lst` into `number` equal size parts.
    usage::

        >>> parts = chunks(range(8),3)
        >>> parts
        <generator object chunks at 0xb73bd964>
        >>> list(parts)
        [[0, 1, 2], [3, 4, 5], [6, 7]]

    """
    lst_len = len(lst)

    for i in xrange(0, lst_len, number):
        yield lst(i: i+number)


def update_nested_dict(a, b):
    """
    update nested dict `a` with another dict b.
    usage::

        >>> a = {'x' : { 'y': 1}}
        >>> b = {'x' : {'z':2, 'y':3}, 'w': 4}
        >>> update_nested_dict(a,b)
        {'x': {'y': 3, 'z': 2}, 'w': 4}

    """
    for k, v in b.iteritems():
        if isinstance(v, dict):
            d = a.setdefault(k, {})
            update_nested_dict(d, v)
        else:
            a[k] = v
    return a
