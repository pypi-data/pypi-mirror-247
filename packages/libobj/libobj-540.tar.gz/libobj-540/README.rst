NAME

::

   LIBOBJ - object library


DESCRIPTION

::

   LIBOBJ provides an obj namespace that allows for easy json save//load
   to/from disk of objects. It provides an "clean namespace" Object class
   that only has dunder methods, so the namespace is not cluttered with
   method names. This makes storing and reading to/from json possible.


SYNOPSIS

::

   >>> from obj import Object
   >>> o = Object()
   >>> o.a = "b"
   >>> write(o, "test")
   >>> oo = Object()
   >>> read(oo, "test")
   >>> oo
   {"a": "b"}  


INSTALL

::

   $ pip install libobj


AUTHOR

::

   libbot <libbotx@gmail.com>


COPYRIGHT

::

   LIBOBJ is Public Domain.
