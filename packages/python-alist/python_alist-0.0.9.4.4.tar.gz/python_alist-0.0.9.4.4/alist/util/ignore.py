#!/usr/bin/env python3
# encoding: utf-8


__author__  = "ChenyangGao <https://chenyanggao.github.io>"
__all__ = ["escape", "translate", "parse", "parse_from_file", "ignore"]

from glob import escape
from os import PathLike
from re import compile as re_compile, IGNORECASE
from typing import Callable, Iterable, TextIO

from .text import posix_glob_translate_iter


def translate(pattern: str, /) -> str:
    s = "".join(t[0] for t in posix_glob_translate_iter(pattern))
    use_basename = "/" not in pattern[:-1]
    s = (("(?:^|/)" if use_basename else "^/?")) + s
    if pattern.endswith("/"):
        return s + ("/" if use_basename else "/$")
    elif use_basename:
        return s + "(?:/|$)"
    else:
        return s + "/?$"


def parse(
    patterns: Iterable[str], 
    /, 
    ignore_case: bool = False, 
) -> Callable[[str], bool]:
    shows: list[str] = []
    ignores: list[str] = []
    for pattern in patterns:
        if not pattern:
            continue
        if pattern.startswith("\\"):
            ignores.append(pattern[1:])
        elif pattern.startswith("!"):
            shows.append(pattern[1:])
        else:
            ignores.append(pattern)
    flags = IGNORECASE if ignore_case else 0
    if shows:
        show = re_compile("|".join(map(translate, shows)), flags).search
    if ignores:
        ignore = re_compile("|".join(map(translate, ignores)), flags).search
    if shows:
        if ignores:
            return lambda p: show(p) is None and ignore(p) is not None
        else:
            return lambda p: show(p) is None
    elif ignores:
        return lambda p: ignore(p) is not None
    else:
        return lambda p: False


def parse_from_file(
    file: bytes | str | PathLike | TextIO, 
    /, 
    ignore_case: bool = False, 
) -> Callable[[str], bool]:
    if isinstance(file, (bytes, str, PathLike)):
        file = open(file, encoding="utf-8")
    return parse(l.removesuffix("\n") for l in file if not l.startswith("#"))


def ignore(
    pats: str | Iterable[str], 
    path: str, 
    ignore_case: bool = False, 
) -> bool:
    """
    Description:
        See: https://git-scm.com/docs/gitignore#_pattern_format

    Examples::
        # test str cases
        >>> ignore("hello.*", "hello.py")
        True
        >>> ignore("hello.*", "foo/hello.py")
        True
        >>> ignore("/hello.*", "hello.py")
        True
        >>> ignore("!/hello.*", "foo/hello.py")
        True
        >>> ignore("!foo/", "foo")
        True
        >>> ignore("foo/", "foo/")
        True
        >>> ignore("foo/", "bar/foo/")
        True
        >>> ignore("!foo/", "bar/foo")
        True
        >>> ignore("foo/", "bar/foo/baz")
        True
        >>> ignore("/foo/", "foo/")
        True
        >>> ignore("!/foo/", "bar/foo/")
        True
        >>> ignore("foo/*", "foo/hello.py")
        True
        >>> ignore("!foo/*", "bar/foo/hello.py")
        True
        >>> ignore("foo/**/bar/hello.py", "foo/bar/hello.py")
        True
        >>> ignore("foo/**/bar/hello.py", "foo/fop/foq/bar/hello.py")
        True
        >>> ignore("h?llo.py", "hello.py")
        True
        >>> ignore("h[a-g]llo.py", "hello.py")
        True
        >>> not ignore("h[!a-g]llo.py", "hello.py")
        True
        >>> ignore("!h[!a-g]llo.py", "hello.py")
        True
        >>> not ignore("!hello.py", "hello.py")
        True
    """
    if isinstance(pats, str):
        pats = pats,
    return parse(pats, ignore_case=ignore_case)(path)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

